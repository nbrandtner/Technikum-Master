# QuestQueue – MVP-Scope

Stand: 05.11.2026 · Version 0.3 · Reviewentwurf

## 1. Ziel und vereinbarter technischer Rahmen

Der vollständige Kernablauf lautet: **Steam-Anmeldung → eigener Datenimport → API-Metadaten mit Cache → Spielübersicht → Präferenzprofil → Current Taste oder All-Time Taste → begründeter Spielvorschlag**. „What should I play?“ wählt einen Titel aus derselben Rangfolge wie die Empfehlungsansicht.

Der Nutzer hat Webapp, lokale Entwicklung, Steam Sign-In, Python/FastAPI, Vue/TypeScript, PostgreSQL und API plus Metadaten-Cache gewählt. Im ersten Stand laufen Frontend, Backend und Datenbank lokal. Steam-Anmeldung und frische externe Daten benötigen weiterhin eine Internetverbindung.

Lokale Entwicklung legt weder einen späteren Hostinganbieter noch eine pauschale Ein-Nutzer-Grenze fest. Daten verschiedener verifizierter Steam-Konten müssen getrennt bleiben. Zielgröße für gleichzeitige Nutzung, öffentlicher Betrieb und Hostingbudget sind noch offen.

Die vollständige Liste mit 13 Features bleibt in der Produktspezifikation. Prioritäten und genaue Produktgrenzen sind weiterhin ein Vorschlag für die Semesterplanung.

## 2. Enthaltene Must-Funktionen

| Umfang | Anforderungen |
| --- | --- |
| Letzte Aktivität mit Zeitpunkten oder ehrlich beschriftetem Aktivitäts-Fallback | US-01 / F-01 |
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

N-01 bis N-07 gelten zusätzlich. Abmelden und persönliche Daten löschen sind verschiedene Vorgänge: Nach Abmeldung bleiben die gespeicherten Daten erhalten; die Sitzung darf sie aber nicht mehr lesen. Ein anderes Konto erhält seinen eigenen Bestand. Der allgemeine Metadaten-Cache kann kontenübergreifend genutzt werden, darf aber keine privaten Profilantworten enthalten.

Der frühere Live-Katalog mit einer Mindestgröße von 30 manuell gepflegten Spielen ist kein Produktziel mehr. Für Offline-Demo und Tests bleibt ein fester Beispieldatensatz sinnvoll. Im Live-Produkt kommen Merkmale aus der ausgewählten API und ihrem Cache; Abdeckung und Datenalter werden angezeigt.

## 3. Noch offene Entscheidungen

| Entscheidung | Status | Vorschlag für den nächsten Review |
| --- | --- | --- |
| Empfehlungsmethode und Profilgewichtung | Offen | Erklärbare inhaltsbasierte Baseline; Embeddings später mit festem Testbestand vergleichen |
| Refresh-Auslöser und Intervalle | Offen | Manueller Refresh plus Aktualisierung veralteter Daten bei Anmeldung; Automatik separat abwägen |
| Metadatenanbieter und erlaubte Speicherung | Noch zu prüfen | IGDB im Spike auf Merkmale, Steam-Zuordnung, Zugangsbedingungen und Cache-Nutzung prüfen |
| Cache-Gültigkeit und Abfrageabstände | Offen | Allgemeine Metadaten getrennt von persönlichen Spielzeiten behandeln |
| Spätere Veröffentlichung und Mehrbenutzer-Zielgröße | Offen | Zunächst lokale Demo; Kontotrennung bereits umsetzen |

Die Vorschläge sind keine neuen Nutzerentscheidungen. Es ist weder eine feste Scoreformel noch ein täglicher Refresh oder eine konkrete Cache-TTL freigegeben. Methodenwahl und Aktualisierungsregeln müssen vor Implementierung des betreffenden Verhaltens dokumentiert werden.

Die Anforderungen an belegbare Gründe, getrennte Profile, Kandidatenausschlüsse und identische Rangfolge zwischen Liste und Button bleiben unabhängig von der Methodenwahl bestehen. Current Taste soll zunächst verfügbare 14-Tage-Minuten verwenden; dieses Datenfenster ist ein weiter bestehender Reviewvorschlag und keine verdeckte Festlegung des Algorithmus.

## 4. Priorisierte Erweiterungen

| Funktion aus der Featureliste | Priorität | Abhängigkeiten und erste Grenze |
| --- | --- | --- |
| Persönliche Tags | Should · US-11 | Vier Tags mit Vorrang für Ausschlüsse; genaue positive Gewichtung mit Methode vereinbaren |
| Genre-Ausschlussfilter | Should · US-12 | Gemeinsame Kandidatenfilter für Listen und Button; keine Änderung an gespeicherten Vorlieben |
| Dashboard | Should · US-04 | Metadaten und Profilbasis; tatsächliche Minuten von Präferenzwerten unterscheiden |
| Spielzeit im Zeitverlauf | Should · US-08 | Snapshots bei erfolgreichen Imports; Auslöser unabhängig von der Speicherung vereinbaren |
| Frühere Favoriten wiederentdecken | Should · US-10 | Gespielte Titel mit belegter Pause und explizitem oder kenntlich gemachtem Interessenssignal |
| Externe Empfehlungen | Should · US-06 | Bestätigte zusätzliche API-/Cache-Kandidaten mit Steam-AppID; Besitzabgrenzung kennzeichnen |
| Like/Dislike für externe Empfehlungen | Should · US-07 | Erst nach US-06; reversibel, Ausschluss oder positive Bevorzugung |
| Zeitgesteuerte Erfassung | Could · US-18 | Erst nach US-08 und separater Refresh-Entscheidung; nur mit laufendem Backend/Scheduler |

Ein laufender lokaler Backendprozess kann auch bei geschlossenem Browser Aufgaben ausführen. Bei ausgeschaltetem Rechner entsteht keine Beobachtungshistorie. Es werden keine nachträglichen täglichen Messpunkte aus langen Importintervallen erfunden.

Die Reihenfolge ist ein Vorschlag nach Abhängigkeiten. Sollen externe Empfehlungen einschließlich Feedback früher zum Semesterziel gehören, ist dafür Zeit einzuplanen oder ein anderer Ausbau zurückzustellen.

### Außerhalb des derzeit zugesagten Umfangs

Öffentlicher Betrieb mit festem Verfügbarkeitsziel, zusätzliche QuestQueue-Passwortkonten, weitere Spieleplattformen, Social Features, Preise, Rabattalarme, Checkout, Spielinstallation, automatischer Spielstart, Cloud-Synchronisierung und ein vollständig erfasster Steam-Katalog sind nicht zugesagt.

Ein trainiertes Modell oder laufende LLM-Aufrufe sind keine Voraussetzung. Feinere Merkmalsfilter benötigen zuerst verlässliche Metadaten. Ein eigener persistenter Merkzettel ist durch die Featureliste nicht verlangt und kein zusätzliches Must.

## 5. Vollständiger Demonstrationsfall

1. Die Person öffnet die lokale Webapp und lädt den gekennzeichneten Offline-Demomodus. Der Beispieldatensatz enthält gespielte Referenzen, ungespielte Kandidaten, unterschiedliche aktuelle und langfristige Schwerpunkte sowie fehlende Daten.
2. Sie prüft Last played und Most played. Fehlende Spielzeit, Zeitpunkte und Metadaten werden nicht erfunden.
3. Sie öffnet die Profilübersicht und prüft All-Time Taste samt Datenstand und verwendeter Metadatenabdeckung.
4. Die Liste zeigt bis zu fünf geeignete eigene ungespielte Titel mit belegbaren Gründen.
5. Der Wechsel auf Current Taste erzeugt im dafür vorgesehenen Testbestand ein anderes Profil und eine andere Spitzenempfehlung.
6. „What should I play?“ liefert denselben Spitzenkandidaten wie die Liste des gewählten Profils.
7. Getrennt vom Offline-Fall meldet sich die Person tatsächlich bei Steam an. Verifizierte Identität und Zugriff auf sichtbare Spielinformationen werden separat nachgewiesen.
8. Der Live-Fall weist API-Metadatenabruf, eindeutige Steam-AppID-Zuordnung und anschließende Cache-Wiederverwendung nach. Eine API-Störung überschreibt keinen vorherigen gültigen Stand.
9. Nach Abmeldung sind persönliche Daten nicht mehr zugänglich. Nach erneuter Anmeldung desselben Kontos und einem Backendneustart sind sie wieder vorhanden.
10. Die Person löscht die eigenen Profildaten. Ein zweites Testkonto sowie der allgemeine Metadaten-Cache bleiben unverändert; die gelöschten Daten kehren nach Neustart nicht zurück.

Ein erfolgreicher Offline-Test ersetzt weder Steam-Anmeldung noch Live-Import oder Metadatenintegration. Feste Daten für reproduzierbare Rankings werden nach der Methodenwahl mit erwarteten Ergebnissen dokumentiert.

## 6. Umsetzungsetappen

| Etappe | Ergebnis | Abnahmepunkt |
| --- | --- | --- |
| 1 · Integrations-Spike | Lokaler Steam-Callback, Bibliothek, aktuelle Minuten, Zeitpunkte und Metadaten-API prüfen | Identität, Datenzugriff und eindeutige Zuordnung nachgewiesen |
| 2 · Offene Entscheidungen schließen | Rankingoptionen vergleichen, Refresh-/Cache-Regeln auswählen | Getroffene und offene Entscheidungen ausdrücklich dokumentiert |
| 3 · Datenbasis und Übersicht | Kontobezogene PostgreSQL-Daten, Cache, Last/Most played und Fehlerzustände | US-01, US-02, US-14, US-15 und US-19 erfüllt |
| 4 · Profile und Auswahl | Zwei Profile nach gewählter Methode, eigene Empfehlungen und Button | US-03, US-05, US-09 und US-13 mit festen Erwartungen erfüllt |
| 5 · Vollständiger MVP | Löschung, getrennte Demo, Startanleitung und Qualitätschecks | US-16, US-17 und N-01 bis N-07 erfüllt |
| 6 · Gezielter Ausbau | Einzelne Should-Funktionen nach Zeitbudget | Kriterien der jeweils aufgenommenen Story erfüllt |
| Puffer | Fehlerkorrekturen, freiwilliges Nutzwertfeedback und Dokumentation | Befunde geschlossen oder transparent dokumentiert |

Teamgröße, Semestertermine und Stundenbudget sind noch unbekannt. Ein belastbarer Kalenderplan folgt nach deren Klärung. Ein gescheiterter Integrations-Spike führt zu einer ausdrücklichen Scope-Entscheidung; kein stillschweigender Ersatz durch ausschließlich Demo-Daten.

## 7. MVP Definition of Done

- Die gewählte Technik ist eingesetzt; alle elf Must-Stories und N-01 bis N-07 erfüllen ihre Kriterien.
- Alle 13 gewünschten Features bleiben im Backlog enthalten. Sieben Should-Stories und eine Could-Story sind klar als Erweiterungen markiert.
- Methode, Profilgewichtung, Score-/Gleichstandsregeln und Erklärungskonzept sind vor Ranking-Abnahme ausgewählt, dokumentiert und mit festen erwarteten Ergebnissen geprüft.
- Refresh-Auslöser, Cache-Gültigkeit, Abfrageabstände und Löschverhalten bei aktiven Jobs sind vor Abnahme des betreffenden Verhaltens festgelegt.
- Steam-Anmeldung, eigene Datenzuordnung und Zugriffstrennung sind mit mindestens zwei Konten beziehungsweise eindeutig getrennten Testsitzungen geprüft.
- Profile, Listen und Button liefern konsistente Ergebnisse; ein fester Testbestand demonstriert unterschiedliche Current-/All-Time-Schwerpunkte.
- API-Metadatenintegration, Cache-Treffer und Fehlerfälle sind nachgewiesen. Fehlende Zuordnungen und veraltete Stände bleiben sichtbar.
- Live-Ablauf und vollständige Offline-Demo sind getrennt geprüft. Persistenz, Abmeldung, Löschung und Neustart funktionieren.
- Startanleitung, Konfiguration, Quellen und bekannte Grenzen sind dokumentiert; Zugangsdaten stehen nicht im Repository oder Browser.

Dies sind zukünftige Abnahmekriterien. Phase 1 bleibt bis zum Review der offenen Methoden-, Refresh- und Scope-Fragen ein Entwurf; die Software ist noch nicht implementiert.
