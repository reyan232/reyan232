# Suchstrings für den ersten eigenen Datenbankdurchgang (Phase 1)

> Herkunft: KI-generiert (source-researcher, methodology-advisor; zusammengestellt vom Orchestrator, 2026-11-09) – Arbeitshilfe, nicht zur Abgabe. Die Strings sind Vorschläge: in der jeweiligen Datenbank testen, bei Bedarf anpassen und **jede tatsächlich ausgeführte Fassung exakt** in `02_search/search_log.csv` eintragen.

**Wichtig:** Diese Suche führst du selbst über den Hochschulzugang aus (WISO, EBSCO). Sie ist die erste echte, protokollierte Datenbanksuche. Die vorherige KI-Sondierung war nur Vorrecherche und gehört nicht in die Suchdokumentation der Arbeit.

## 1. WISO (Filter: 2023–2026, Deutsch/Englisch)

**Stufe 1** (Dokumenttyp: wissenschaftliche Zeitschriften, Bücher, Hochschulschriften/Dissertationen)

```
("KI-Agent*" OR "KI Agent*" OR "agentische KI" OR "Agentic AI" OR "AI Agent*" OR "autonome Agent*" OR Multiagent* OR "LLM-Agent*") AND (Controlling OR Rechnungswesen OR Buchhaltung OR Jahresabschluss OR Finanzbereich OR Finanzfunktion OR CFO OR Treasury OR Finanzmanagement)
```

```
("KI-Agent*" OR "agentische KI" OR "Agentic AI") AND (Erfolgsfaktor* OR Einführung OR Implementierung OR Governance OR Voraussetzung* OR Datenqualität OR Akzeptanz)
```

**Stufe 2** (in der erweiterten Suche das Feld „Quelle/Zeitschrift“ auf Titel aus Anhang 4 der Professorenvorgaben beschränken: Controller Magazin, Controlling & Management Review, CFO aktuell, Controlling (ZfC), Corporate Finance, Der Betrieb, Betriebs-Berater, BFuP, Zeitschrift für Bilanzierung, Rechnungswesen und Controlling, Risk Compliance & Audit)

```
("KI-Agent*" OR "Agentic AI" OR "agentische KI" OR "AI Agent*" OR Copilot*) AND (Controlling OR Controller OR Finanzbereich OR CFO OR Rechnungswesen OR Treasury OR Abschluss OR Planung)
```

`Copilot*` fängt unscharfe Verwendungen bewusst mit ein. Beim Screening prüfst du, ob tatsächlich ein Agent gemeint ist (Ausschlusscode E3).

**Konkreter Stufe-2-Hinweis aus den Seminarfolien:** Folie 23 zitiert Baier, L./Tischler, R. (2026): „AI im Controlling: zwischen Hype und Realität“, Controller Magazin, Heft 3/2026, S. 14–18. Gezielt in WISO suchen und prüfen. Die Folie selbst ist kein Beleg.

## 2. EBSCO Business Source (Filter: „Peer Reviewed“, 2023–2026, EN/DE)

**Use Cases**
```
(TI ("agentic AI" OR "AI agent*" OR "LLM-based agent*" OR "LLM agent*" OR "autonomous agent*" OR "multi-agent") OR AB ("agentic AI" OR "AI agent*" OR "LLM-based agent*" OR "autonomous agent*")) AND ("finance function" OR CFO OR "management accounting" OR controlling OR accounting OR "financial reporting" OR "financial close" OR treasury OR "cash management" OR "financial planning")
```

**Erfolgsfaktoren**
```
("agentic AI" OR "AI agent*" OR "autonomous agent*" OR "LLM-based agent*") AND (adoption OR implementation OR "success factor*" OR governance OR readiness OR "human oversight" OR accountability) AND (organi?ation* OR enterprise* OR firm* OR "finance function")
```

**Treasury** (Bank- und Zentralbankkontexte manuell aussortieren, Code E2)
```
("agentic AI" OR "AI agent*" OR "generative AI" OR "large language model*") AND ("corporate treasury" OR "treasury management" OR "cash management" OR "liquidity management" OR "cash flow forecast*")
```

## 3. Zusatzbegriffe je Option (methodology-advisor)

- **Option A** (Autonomie-/Delegationsrahmen): an die Use-Case-Strings anhängen
  `AND ("human-in-the-loop" OR "human oversight" OR "levels of automation" OR delegation OR Freigabe*)`
- **Option B** (Rechnungswesen): `AND (GoBD OR "internes Kontrollsystem" OR "internal control" OR "audit trail" OR Prüfpfad OR Kreditoren OR Abschluss)`. Für GoBD/IKS zusätzlich NWB und beck-online, falls lizenziert.
- **Option C** (Controlling): `AND (Berichtswesen OR Reporting OR Abweichungsanalyse OR Kommentierung OR FP&A OR Forecast*)`

## 4. Freie Portale (optional)

- AIS eLibrary (aisel.aisnet.org): `"agentic AI" AND (accounting OR finance OR controlling)`, Konferenzen ICIS/ECIS/WI 2025–2026
- Journal of Emerging Technologies in Accounting: Hefte 2026/27 auf die angekündigte Sonderrubrik „Agentic AI in Auditing and Accounting“ prüfen
- EconBiz (econbiz.de): die Stufe-1-Strings in vereinfachter Form

## 5. Protokollierung (Pflicht)

Pro ausgeführtem String eine Zeile in `02_search/search_log.csv` anlegen; die IDs ab S102 sind frei.

```
S102,2026-11-XX,Student,WISO,WISO-Erweiterte Suche,"<exakter String>","2023–2026; DE/EN; Dokumenttyp …",<Trefferzahl>,DATENBANK_GESAMT,02_search/exports/S102_wiso.ris,<Notiz>
```

- Trefferzahlen nur so eintragen, wie die Datenbank sie anzeigt, nie schätzen.
- Exporte (RIS/CSV) nach `02_search/exports/` legen; sie werden nicht ins öffentliche Repository übernommen.
- Relevante Treffer kannst du mir als Liste geben. Ich übernehme sie dann als Kandidaten und prüfe die Metadaten per Crossref.
