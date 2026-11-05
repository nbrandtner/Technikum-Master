# QuestQueue – MVP-Scope

Stand: 05.11.2026 · Version 1.0 · Phase 1 – Project Definition & Requirements

## 1. Ziel und technischer Rahmen

Der MVP unterstützt einen vollständigen Anwendungsfall: **Steam-Anmeldung → eigener Datenimport → Metadatenanreicherung → Spielübersicht → Profilwahl → begründeter Vorschlag für ein eigenes ungespieltes Spiel**. Der Button „What should I play?“ liefert den bestgereihten Titel derselben Empfehlungsansicht.

Frontend, Backend und PostgreSQL laufen lokal. Die Anwendung verwendet Vue/TypeScript, Python/FastAPI, Steam OpenID, die Steam Web API und IGDB. Persönliche Daten verschiedener Steam-Konten bleiben getrennt; allgemeine Metadaten werden kontenübergreifend gecacht. Steam-Anmeldung und externe Datenabrufe benötigen Internetzugang.

## 2. Enthaltene Must-Funktionen

| Umfang | Anforderungen |
| --- | --- |
| Letzte Aktivität mit Zeitpunkten oder gekennzeichneten kürzlichen Aktivitäten ohne genaue Reihenfolge | US-01 / F-01 |
| Meistgespielte Titel, Bibliothek und Ungespielt-Filter | US-02 / F-02 |
| Präferenzprofil und verständliche Zusammenfassung | US-03 / F-03 |
| Höchstens fünf begründete Empfehlungen eigener ungespielter Titel | US-05 / F-05 |
| Wechsel zwischen Current Taste und All-Time Taste | US-09 / F-09 |
| „What should I play?“ mit dem bestgereihten geeigneten eigenen Titel | US-13 / F-13 |
| Verifizierte Steam-Anmeldung, eigener Import und lokale Persistenz | US-14 / F-14 |
| Fehler- und Leerzustände ohne Verlust gültiger Daten | US-15 / F-15 |
| Vollständige Löschung der persönlichen Daten des angemeldeten Kontos | US-16 / F-16 |
| Getrennter offline nutzbarer Demomodus ohne Kontodatenzugriff | US-17 / F-17 |
| Zusätzliche API-Metadaten mit eindeutiger AppID-Zuordnung und PostgreSQL-Cache | US-19 / F-19 |

Zusätzlich gelten N-01 bis N-07. Die Oberfläche beschränkt sich auf Spielübersichten, eine einfache Profilzusammenfassung und die begründete Auswahl. Das grafische Dashboard ist kein Bestandteil des MVP.

## 3. Produktentscheidungen und Umfangsbegründung

| Bereich | Festlegung | Begründung |
| --- | --- | --- |
| Empfehlung | Genrebasierte inhaltsbasierte Baseline v1; Regeln und Akzeptanzbeispiel in requirements.md, Abschnitt 5 | Nachvollziehbare Ergebnisse ohne Trainingsdaten oder laufende Modellkosten |
| Persönliche Daten | Bewusst gestarteter Erstimport; anschließend manueller Refresh und Aktualisierung bei Anmeldung ab 24 Stunden Datenalter | Kontrollierte Datenübernahme und aktueller Stand beim Einstieg |
| Abfragebegrenzung | Mindestens 60 Sekunden zwischen Importstarts je Konto; höchstens ein laufender Import je Konto | Vermeidung mehrfacher gleichzeitiger Abrufe |
| Metadaten | IGDB mit PostgreSQL-Cache; sieben Tage Frische; ältere Daten gekennzeichnet weiterverwenden | Geringere Abhängigkeit von einzelnen Anbieterabrufen |
| Betrieb | Lokale Demonstration; 0 Euro Budget für zusätzliche laufende Dienste | Begrenzung des Betriebsaufwands innerhalb des Semesterprojekts |

Die elf Must-Stories decken sechs sichtbare Produktfunktionen, die erforderliche Metadatenversorgung und vier unterstützende Funktionen für Anmeldung/Import, Fehlerbehandlung, Datenkontrolle und Demonstration ab. Jede davon trägt zum vollständigen Kernablauf oder seiner überprüfbaren Zuverlässigkeit bei.

Die größten Aufwandstreiber sind Steam-Anmeldung, Metadatenzuordnung und Kontotrennung. Sie werden in Phase 2 zuerst geprüft. Der API-Prüfplan umfasst etwa 50 reale Bibliotheksspiele und steht in requirements.md, Abschnitt 7. Bei relevanten IGDB-Lücken wird SteamSpy als Alternative bewertet. Ergebnisse und notwendige Umfangsänderungen werden vor der Implementierung dokumentiert.

## 4. Priorisierte Erweiterungen und Ausschlüsse

| Erweiterung | Priorität | Abhängigkeiten und erste Grenze |
| --- | --- | --- |
| Persönliche Tags | Should · US-11 | Vier Tags mit Ausschlussvorrang; Loved It verdoppelt den Referenzbeitrag nach Baseline v1 |
| Genre-Ausschlussfilter | Should · US-12 | Gemeinsame Kandidatenfilter für Listen und Button; keine Änderung an gespeicherten Vorlieben |
| Dashboard | Should · US-04 | Metadaten und Profilbasis; tatsächliche Minuten von Präferenzwerten unterscheiden |
| Spielzeit im Zeitverlauf | Should · US-08 | Snapshots bei erfolgreichen manuellen oder anmeldebezogenen Imports |
| Frühere Favoriten wiederentdecken | Should · US-10 | Gespielte Titel mit belegter Pause und explizitem oder kenntlich gemachtem Interessenssignal |
| Externe Empfehlungen | Should · US-06 | Bestätigte zusätzliche API-/Cache-Kandidaten mit Steam-AppID; Besitzabgrenzung kennzeichnen |
| Like/Dislike für externe Empfehlungen | Should · US-07 | Erst nach US-06; reversibel, Ausschluss oder positive Bevorzugung |
| Zeitgesteuerte Erfassung | Could · US-18 | Erst nach US-08; explizit aktivierte Zeitsteuerung bei laufendem Backend |

Should- und Could-Funktionen sind nicht für die MVP-Abnahme erforderlich. Ihre Umsetzung setzt einen vollständig geprüften Kern und verbleibende Kapazität voraus.

Außerhalb des MVP liegen öffentlicher Hostingbetrieb, weitere Spieleplattformen, Social Features, Preise und Rabattalarme, Kaufabwicklung, Spielinstallation und automatischer Spielstart, Cloud-Synchronisierung sowie eine vollständige Erfassung des Steam-Katalogs. Trainierte Mehrnutzer-Modelle und LLM-Aufrufe zur Laufzeit sind ebenfalls nicht vorgesehen.

## 5. Vollständiger Demonstrationsfall

### Live-Anwendungsfall

1. Die Person öffnet QuestQueue und meldet sich über Steam an. Das Backend verifiziert ihre Identität.
2. Nach Bestätigung des Datenhinweises startet sie den Import. Bibliothek, bekannte Spielzeiten und verfügbare aktuelle Aktivitätsdaten werden dem eigenen Konto zugeordnet.
3. Das Backend ergänzt zuordenbare Spiele um IGDB-Genres. Die Oberfläche zeigt Importstand, Metadatenabdeckung und etwaige Lücken an.
4. Die Person prüft zuletzt und meistgespielte Titel und öffnet All-Time Taste mit dessen Genregewichten.
5. Die Empfehlungsansicht zeigt bis zu fünf passende eigene ungespielte Titel. Jeder Vorschlag nennt Profil, gemeinsames Genre und Referenzspiel.
6. Bei geeigneten aktuellen Daten wechselt die Person auf Current Taste; Profil, Rangliste und Begründungen folgen dem aktuellen Zeitfenster. Ohne aktuelle Grundlage erscheint der definierte Leerzustand.
7. „What should I play?“ liefert den Spitzenkandidaten des gewählten Profils.
8. Ein erneuter Abruf mit gültigem Cache verwendet gespeicherte Metadaten. Bei simuliertem API-Ausfall bleibt der letzte gültige Datenstand erhalten und entsprechend gekennzeichnet.
9. Abmeldung beendet den Zugriff. Nach erneuter Anmeldung und Backendneustart sind die eigenen Daten weiterhin verfügbar; andere Konten bleiben getrennt.
10. Bestätigte Profillöschung entfernt die eigenen Daten und beendet die zugehörigen Sitzungen. Nach Neustart bleiben sie gelöscht; ein zweites Testkonto und allgemeine Metadaten bleiben erhalten.

### Reproduzierbare Offline-Demo

Der getrennte Demomodus enthält den festen Akzeptanzbestand aus requirements.md, Abschnitt 5 und die für US-17 erforderlichen Aktivitätszeitpunkte. Er zeigt Spielübersichten, beide Profile, unterschiedliche Spitzenempfehlungen und konsistente Button-Ergebnisse ohne Netzwerkanfrage. „Demodaten“ bleibt sichtbar; persönliche Kontodaten sind nicht zugänglich. Der Live-Anwendungsfall wird separat geprüft.

## 6. Umsetzungsetappen

Das Projektteam besteht aus **zwei Personen**. Die Bearbeitung erfolgt im **Wintersemester 2026/27**. Alle Abgabezeiten beziehen sich auf **Europe/Vienna (Wien)**. Die Arbeitsfenster strukturieren die Bearbeitung zwischen den Abgabeterminen.

| Phase | Abgabetermin | Arbeitsfenster | Projektmeilenstein |
| --- | --- | --- | --- |
| Phase 1 · Project Definition & Requirements | Montag, 09.11.2026, 17:00 | Bis 09.11.2026 | Vier geforderte Dokumente prüfen und abgeben; Problem, MVP, Anforderungen und AI-Reflexion nachvollziehbar festhalten |
| Phase 2 · Architecture & Design | Montag, 23.11.2026, 17:00 | 10.–23.11.2026 | Steam-/IGDB-Spike früh durchführen; Architektur, Datenmodell, API-Schnittstellen, Kontotrennung, Cache und UI-Ablauf aus den Anforderungen ableiten |
| Phase 3 · AI-assisted/driven Implementation | Mittwoch, 09.12.2026, 17:00 | 24.11.–09.12.2026 | Vollständigen MVP implementieren: Anmeldung → Import → Metadaten/Cache → Übersicht → beide Profile → begründete Auswahl; Persistenz, Fehlerzustände, Löschung und Demo einschließen |
| Phase 4 · Quality Assurance & Testing | Montag, 21.12.2026, 17:00 | 10.–21.12.2026 | Must-Stories und N-01 bis N-07 systematisch prüfen; Integrations-, Zugriffs-, Fehler- und Grenzfälle testen, Befunde beheben und verbleibende Grenzen dokumentieren |
| Phase 5 · Evaluation & Reflection | Dienstag, 22.12.2026, 23:59 | Evaluation begleitend, Abschluss am 22.12.2026 | Nutzen, Zielerreichung und AI-Unterstützung anhand gesammelter Nachweise bewerten; Reflexion und abschließende Abgabe fertigstellen |

### Arbeitsteilung und Terminabsicherung

Die Arbeit gliedert sich in zwei Bereiche: Backend/Datenimport/Cache und Frontend/Profilansicht/Demo. Schnittstellen, Empfehlungsregeln, Reviews und Abnahme bearbeitet das Team gemeinsam.

- **Phase 2:** Externe Zugänge und Zuordnung zuerst prüfen; anschließend Datenmodell, Schnittstellen und UI-Ablauf festlegen. Den Integrationsaufwand vor Beginn der MVP-Implementierung mit der Teamkapazität abgleichen.
- **Phase 3:** Zuerst den vollständigen Kernablauf herstellen und anschließend die übrigen Must-Kriterien erfüllen. Internes Fertigstellungsziel ist der 07.12.2026; der 08.–09.12. ist für Integration, Korrekturen und Abgabevorbereitung reserviert.
- **Phase 4:** Die bereits während der Implementierung begonnenen Tests systematisch vervollständigen, Fehler beheben und Abnahmenachweise dokumentieren. Funktionserweiterungen haben keinen Vorrang vor Qualitätssicherung.
- **Phase 5:** Fortlaufend gesammelte Entscheidungen, Testergebnisse und Nutzwertbeobachtungen auswerten und die Reflexion bis zur Abschlussabgabe fertigstellen.

## 7. MVP Definition of Done

Der MVP ist abnahmefähig, wenn folgende Kriterien erfüllt sind:

- Alle elf Must-Stories und N-01 bis N-07 erfüllen ihre dokumentierten Kriterien.
- Baseline v1 liefert die erwarteten Profile, Scores, Rangfolgen und Begründungen des festen Akzeptanzbeispiels.
- Profilwechsel, Empfehlungslisten und Button verwenden konsistente Daten und Auswahlregeln.
- Steam-Anmeldung, eigener Datenimport und Zugriffstrennung sind mit getrennten Konten beziehungsweise Testsitzungen nachgewiesen.
- IGDB-Abruf, eindeutige AppID-Zuordnung, Cache-Wiederverwendung und sichtbare Behandlung fehlender Metadaten sind geprüft.
- Aktualisierungs-, Cooldown- und Cache-Grenzen sowie API-Fehlerfälle bestehen die vorgesehenen Tests.
- Persistenz, Abmeldung, Datenlöschung und Neustart funktionieren; verspätete persönliche Importergebnisse umgehen keine Abmeldung oder Löschung.
- Der Live-Anwendungsfall und die getrennte Offline-Demo sind vollständig demonstrierbar.
- Startanleitung, Konfiguration, externe Quellen und bekannte Einschränkungen sind dokumentiert; Zugangsdaten stehen nicht im Repository oder Browser.
