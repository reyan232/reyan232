# Leadfinder

Findet lokale Betriebe in München, für die in OpenStreetMap **keine Webseite**
eingetragen ist, und schreibt Name, Adresse und Telefonnummer als CSV.

Datenquelle ist die Overpass API — kostenlos, ohne API-Key, ohne Abrechnung.

## Schnellstart

```bash
cd tools/leadfinder

python3 -m leadfinder.cli --self-check                    # geht das Netz?
python3 -m leadfinder.cli --list-categories               # welche Branchen?
python3 -m leadfinder.cli --dry-run --categories friseur  # Abfrage ansehen

python3 -m leadfinder.cli --categories friseur,baeckerei --limit 100 -o leads.csv
```

Einzige Abhängigkeit: `requests`. Getestet mit Python 3.11.

## Was am Ergebnis stimmt — und was nicht

Der wichtigste Vorbehalt zuerst: **ein fehlender `website`-Tag beweist nicht,
dass der Betrieb keine Webseite hat.** OSM wird ehrenamtlich gepflegt; oft ist
die Webseite schlicht nicht erfasst. Die Liste ist eine *Vorauswahl* für die
eigene Prüfung, keine belegte Menge.

Deshalb gibt jeder Lauf Kennzahlen aus, statt nur Zeilen zu zählen:

```
  OSM-Elemente gesamt        10
  ohne Namen (übersprungen)  1
  ohne Telefonnummer         1
  Telefon nicht normierbar   1
  Adresse unvollständig      1
  Duplikate entfernt         1
  brauchbare Leads           6  (60% der Elemente)
```

Die Quote „ohne Telefonnummer" entscheidet, ob sich OSM für deine Branche
lohnt. Ist sie hoch, liefert die kostenpflichtige Google Places API deutlich
mehr — mit Key, Abrechnung und ToS-Einschränkungen beim Speichern.

## Optionen

| Option | Wirkung |
|---|---|
| `--categories a,b` | Branchen (Standard: friseur,baeckerei,kosmetik) |
| `--area` | Gebiet (Standard: München) |
| `--limit N` | höchstens N Leads in der CSV |
| `-o DATEI` | Zieldatei (Standard: leads.csv) |
| `--no-require-phone` | auch Betriebe ohne Telefonnummer aufnehmen |
| `--delimiter` | CSV-Trenner (Standard: `;` für deutsches Excel) |
| `--from-file` | gespeicherte Overpass-Antwort auswerten, ohne Netz |
| `--dry-run` | Abfrage zeigen, nichts senden |
| `--self-check` | Erreichbarkeit der Spiegel prüfen |

Exit-Codes: `0` Erfolg, `1` Fehler, `2` Netz blockiert.

### Wenn Overpass gesperrt ist

In abgeschotteten Containern und hinter Firmen-Proxys ist Overpass regelmäßig
blockiert — `--self-check` sagt das mit Exit-Code 2 klar an. Umweg ohne
eigenen Netzzugang:

1. `--dry-run` liefert die Abfrage.
2. Auf <https://overpass-turbo.eu> einfügen, ausführen, als GeoJSON/JSON
   exportieren.
3. `--from-file antwort.json -o leads.csv` wertet sie lokal aus.

### Branchen erweitern

`leadfinder/categories.py` bildet Branchen auf OSM-Tag-Paare ab
(`shop=hairdresser`, `craft=electrician`, …). Neue Branche = neuer Eintrag.
Tag-Werte vorher im [OSM-Wiki](https://wiki.openstreetmap.org/wiki/Map_features)
prüfen: ein falscher Wert wirft keinen Fehler, er liefert nur nichts.

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
python3 -m pytest tests -q     # 70 Tests, kein Netz nötig
```

Der Netzwerkzugriff steckt vollständig in `fetch.py` und ist in den Tests
gestubbt. Geprüft werden Telefon-Normalisierung, Adressbau bei fehlenden Tags,
Webseiten-Filter, Deduplizierung, CSV-Format sowie Backoff- und
Spiegelwechsel-Verhalten.

## Rechtliches

**Lizenz der Daten.** OpenStreetMap steht unter der
[ODbL](https://opendatacommons.org/licenses/odbl/). Bei Weitergabe oder
Veröffentlichung ist „© OpenStreetMap-Mitwirkende" anzugeben. Das Tool schreibt
die Angabe in jede CSV-Zeile (Spalte `quelle`) und legt eine
`ATTRIBUTION.txt` daneben.

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
