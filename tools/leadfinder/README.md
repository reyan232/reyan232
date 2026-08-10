# Leadfinder

Findet lokale Betriebe in München, für die **keine Webseite** hinterlegt ist,
und schreibt Name, Adresse und Telefonnummer als CSV.

Zwei Datenquellen zur Wahl:

| Provider | Kosten | Abdeckung | Haken |
|---|---|---|---|
| `overpass` (Standard) | gratis, ohne Key | lückenhaft, viele ohne Telefon | in vielen Netzen gesperrt |
| `google` | kostenpflichtig, Key nötig | deutlich vollständiger | Speicherbeschränkung laut ToS |

## Schnellstart

```bash
cd tools/leadfinder

python3 -m leadfinder.cli --self-check                    # geht das Netz?
python3 -m leadfinder.cli --list-categories               # welche Branchen?
python3 -m leadfinder.cli --dry-run --categories friseur  # Abfrage ansehen

# OSM (gratis)
python3 -m leadfinder.cli --categories friseur,baeckerei --limit 100 -o leads.csv

# Google (kostenpflichtig)
export GOOGLE_MAPS_API_KEY="…"
python3 -m leadfinder.cli --provider google --self-check
python3 -m leadfinder.cli --provider google --dry-run --categories friseur
python3 -m leadfinder.cli --provider google --categories friseur \
    --grid 3 --max-requests-month 50 -o leads.csv
```

Einzige Abhängigkeit: `requests`. Getestet mit Python 3.11.

## Was am Ergebnis stimmt — und was nicht

Der wichtigste Vorbehalt zuerst: **ein fehlender `website`-Tag beweist nicht,
dass der Betrieb keine Webseite hat.** OSM wird ehrenamtlich gepflegt; oft ist
die Webseite schlicht nicht erfasst. Die Liste ist eine *Vorauswahl* für die
eigene Prüfung, keine belegte Menge.

Deshalb gibt jeder Lauf Kennzahlen aus, statt nur Zeilen zu zählen:

```
  Treffer gesamt             10
  ohne Namen (übersprungen)  1
  ohne Telefonnummer         1
  Telefon nicht normierbar   1
  Adresse unvollständig      1
  Duplikate entfernt         1
  brauchbare Leads           6  (60% der Treffer)
```

Die Quote „ohne Telefonnummer" entscheidet, ob sich OSM für deine Branche
lohnt. Ist sie hoch, liefert die kostenpflichtige Google Places API deutlich
mehr — mit Key, Abrechnung und ToS-Einschränkungen beim Speichern.

## Optionen

Für beide Provider:

| Option | Wirkung |
|---|---|
| `--provider` | `overpass` (Standard) oder `google` |
| `--categories a,b` | Branchen (Standard: friseur,baeckerei,kosmetik) |
| `--limit N` | höchstens N Leads in der CSV |
| `-o DATEI` | Zieldatei (Standard: leads.csv) |
| `--no-require-phone` | auch Betriebe ohne Telefonnummer aufnehmen |
| `--delimiter` | CSV-Trenner (Standard: `;` für deutsches Excel) |
| `--dry-run` | zeigen, was passieren würde, nichts senden |
| `--self-check` | Erreichbarkeit prüfen |

Nur `overpass`:

| Option | Wirkung |
|---|---|
| `--area` | Gebiet (Standard: München) |
| `--from-file` | gespeicherte Antwort auswerten (Overpass-JSON **oder** GeoJSON); mehrfach angebbar |
| `--turbo-link` | anklickbare overpass-turbo-Links ausgeben |
| `--split N` | Branchen je Link/Abfrage (Standard: 4) |
| `--area-id` | Gebiet auf eine OSM-Relation pinnen statt über den Namen zu suchen |
| `--mirror`, `--timeout`, `--user-agent` | Spiegel und HTTP-Verhalten |

Nur `google`:

| Option | Wirkung |
|---|---|
| `--grid N` | Stadtgebiet in N×N Kacheln (Standard: 3) — **quadratischer Kostenhebel** |
| `--max-pages` | Seiten je Kachel, max. 3 (Standard: 1) |
| `--max-requests-month` | harte Monatsgrenze (Standard: 50) |
| `--budget-file` | Datei für den Abfragezähler |
| `--api-key-env` | Name der Key-Variablen (Standard: `GOOGLE_MAPS_API_KEY`) |

Exit-Codes: `0` Erfolg, `1` Fehler (Bedienung, Key, Daten), `2` Netz blockiert.

### Wenn Overpass gesperrt ist — der Browser-Umweg

In abgeschotteten Containern und hinter Firmen-Proxys ist Overpass regelmäßig
blockiert; `--self-check` sagt das mit Exit-Code 2 klar an. Der Umweg braucht
nur einen Browser:

```bash
python3 -m leadfinder.cli --turbo-link --categories friseur,baeckerei,metzger,optiker
```

1. Jeden ausgegebenen Link öffnen — overpass-turbo startet die Abfrage selbst.
2. **Export → Daten → GeoJSON** (oder „raw data directly from Overpass API").
3. Alle Downloads auf einmal einspielen:

```bash
python3 -m leadfinder.cli --from-file a.json --from-file b.json -o leads.csv
```

Beide Exportwege funktionieren: `--from-file` erkennt sowohl die
Overpass-eigene Antwort (`elements`) als auch GeoJSON (`features`). Passt das
Format zu keinem von beidem, gibt es eine Fehlermeldung statt einer stillen
Null-Ausgabe. Mehrfach angegebene Dateien werden zusammengeführt und über die
OSM-ID dedupliziert.

**Warum mehrere Links?** Alle 15 Branchen in einer Abfrage ergäben eine URL
von über 4000 Zeichen und würden bei Overpass absehbar in den Timeout laufen.
`--split N` (Standard: 4) teilt die Auswahl; die Aufteilung gilt auch für den
direkten Abruf, weil viele kleine Abfragen gegenüber einem Spendendienst das
anständigere Verhalten sind.

### Wenn Orte aus dem Umland auftauchen

Das Gebiet wird über `area["name"="München"]["admin_level"="6"]` bestimmt.
Trägt eine zweite Fläche derselben Verwaltungsstufe denselben Namen — etwa ein
gleichnamiger Landkreis —, vereinigt Overpass beide, und in der Liste stehen
Betriebe aus dem Umland. **Ohne jede Fehlermeldung.**

Erkennen lässt es sich an der Spalte `ort`: steht dort etwas anderes als
„München", ist genau das passiert. Gegenmittel ist das Pinnen auf eine
bestimmte OSM-Relation:

```bash
python3 -m leadfinder.cli --area-id 62428 --categories friseur -o leads.csv
```

Die passende Relations-ID findest du auf openstreetmap.org, wenn du die
Stadtgrenze anklickst. Hier ist bewusst keine ID fest eingebaut: sie ließ sich
in der Entwicklungsumgebung nicht verifizieren, und eine falsch geratene ID
wäre schlimmer als der Namensweg.

### Social-Media-Leads

Ein Betrieb mit Facebook-Seite, aber ohne Webseite, ist der stärkste Lead im
Datensatz: Sichtbarkeit ist ihm offensichtlich wichtig, eine eigene Seite hat
er trotzdem nicht. Das Tool liest `contact:facebook`, `contact:instagram`
(auch ohne Präfix), füllt damit die Spalte `social` und **sortiert diese Leads
nach oben**.

Der Vorbehalt bleibt: Das Signal macht den Lead *wahrscheinlicher* echt — wer
sein Facebook einträgt, hätte die Webseite vermutlich auch eingetragen — aber
es beweist nichts.

## Google Places einrichten

1. In der [Google Cloud Console](https://console.cloud.google.com/) ein Projekt
   anlegen und **Abrechnung aktivieren** — ohne geht gar nichts.
2. Unter „APIs & Dienste" die **Places API (New)** aktivieren. Achtung: die
   alte „Places API" ist etwas anderes und reicht hier nicht.
3. Einen API-Key erstellen und **einschränken**: nur Places API (New), und
   wenn möglich auf deine IP. Ein unbeschränkter Key ist bei einem Leak eine
   offene Rechnung.
4. Key setzen und prüfen:

```bash
export GOOGLE_MAPS_API_KEY="…"
python3 -m leadfinder.cli --provider google --self-check
```

Der Key wird **nur** aus der Umgebungsvariablen gelesen, nie als Argument
entgegengenommen — Kommandozeilen sind über `ps` für andere Nutzer sichtbar.
Er landet nicht in Logs, nicht in Fehlermeldungen und nicht in der CSV; ein
Test prüft das.

### Kosten im Griff behalten

Google rechnet pro Abfrage ab. Die Abfragezahl ist `Branchen × Kacheln ×
Seiten` und wächst mit `--grid` **quadratisch** — von `--grid 3` auf `--grid 6`
sind es viermal so viele Abfragen, nicht doppelt so viele.

```bash
python3 -m leadfinder.cli --provider google --dry-run --categories friseur --grid 3
# -> Mindestens 9 Abfragen
```

`--max-requests-month` ist eine harte Bremse: das Tool zählt jede Abfrage in
`~/.leadfinder/budget.json` mit und bricht an der Grenze ab — die bis dahin
gefundenen Leads werden trotzdem geschrieben. Der Zähler überlebt Abstürze,
damit nichts doppelt bezahlt wird.

**Was das Tool nicht tut:** Googles Freikontingent auswerten. Diese Regeln
ändern sich, und eine geratene Grenze wäre schlechter als keine. Der Zähler
zählt Abfragen; welche davon frei sind, steht in deiner Cloud-Konsole.

### Abdeckung

`searchText` liefert höchstens 20 Treffer je Seite und 60 je Abfrage. Ganz
München in einem Aufruf gibt es deshalb nicht — das Stadtgebiet wird in
`--grid N` × N Kacheln zerlegt und je Kachel gesucht, dedupliziert über die
`place_id`. Ein feineres Raster findet mehr, kostet aber quadratisch mehr.

### Branchen erweitern

`leadfinder/categories.py` bildet die 15 Branchen auf OSM-Tag-Paare ab
(`shop=hairdresser`, `craft=electrician`, …). Neue Branche = neuer Eintrag.

Tag-Werte vorher im [OSM-Wiki](https://wiki.openstreetmap.org/wiki/Map_features)
prüfen: ein falscher Wert wirft keinen Fehler, er liefert nur nichts. Deshalb
weist jeder Lauf Branchen ohne einen einzigen Treffer eigens aus — das ist das
Signal für einen Tippfehler im Tag.

## Overpass fair benutzen

Overpass ist ein Spendendienst von Freiwilligen, keine kommerzielle API. Das
Tool hält sich daran: ein Request zur Zeit, wachsendes Backoff bei Überlast,
Spiegelwechsel erst nach Fehlschlag.

Bitte trage im `--user-agent` eine echte Kontaktadresse ein. Für regelmäßige
Vollabzüge gehört statt der API ein Extrakt von
[Geofabrik](https://download.geofabrik.de/europe/germany/bayern.html) benutzt
und lokal mit `osmium` gefiltert — das schont den öffentlichen Dienst.

## Tests

```bash
python3 -m pytest tests -q     # 156 Tests, kein Netz nötig
```

Der Netzwerkzugriff steckt vollständig in `fetch.py` (Overpass) und
`google.py` und ist in den Tests gestubbt. Geprüft werden unter anderem
Telefon-Normalisierung, Adressbau bei fehlenden Feldern, Webseiten-Filter,
Deduplizierung, CSV-Format, Backoff und Spiegelwechsel, Kachel-Mathematik,
Budgetgrenze — und dass der API-Key in keiner Ausgabe auftaucht.

Eigener Regressionsschutz für den Browser-Umweg: dieselben Daten einmal als
Overpass-JSON und einmal als GeoJSON müssen dieselben Leads ergeben. Eine
frühere Fassung lieferte hier 6 gegen 0, ohne Fehlermeldung.

Nicht abgedeckt und ehrlich benannt: der echte Lauf gegen Overpass bzw. mit
gültigem Google-Key. Beides braucht Netz und Zugang, die eine Testumgebung
nicht hat.

## Rechtliches

**OpenStreetMap.** Steht unter der
[ODbL](https://opendatacommons.org/licenses/odbl/). Bei Weitergabe oder
Veröffentlichung ist „© OpenStreetMap-Mitwirkende" anzugeben. Das Tool schreibt
die Angabe in jede CSV-Zeile (Spalte `quelle`) und legt eine
`ATTRIBUTION.txt` daneben.

**Google Places.** Die Google-Maps-Platform-Bedingungen beschränken das
Zwischenspeichern von Places-Inhalten (Richtwert 30 Tage) und untersagen den
Aufbau dauerhafter eigener Datenbanken; dauerhaft gespeichert werden darf die
`place_id`. Eine Lead-CSV ist genau so ein Zwischenspeicher — sie ist zum
Abarbeiten gedacht, nicht zum Sammeln. Nach der Kampagne löschen und bei
Bedarf neu ziehen.

**Verwendung der Liste.** Das betrifft nicht die Recherche, sondern den
Erstkontakt:

- **UWG § 7** — Telefonwerbung gegenüber Unternehmen ist nur bei mutmaßlicher
  Einwilligung zulässig; Kalt-E-Mail an Unternehmen ohne vorherige
  Einwilligung ist grundsätzlich unzulässig.
- **DSGVO** — bei Einzelunternehmen sind Anschrift und Telefonnummer zugleich
  personenbezogene Daten. Art. 14 verlangt, die Betroffenen binnen eines
  Monats über die Speicherung zu informieren, wenn die Daten nicht bei ihnen
  erhoben wurden.

Keine Rechtsberatung. Im Zweifel vor der ersten Kampagne anwaltlich klären.
