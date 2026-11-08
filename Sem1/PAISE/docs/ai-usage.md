# QuestQueue – AI-Einsatz im Requirements Engineering

Projektphase: Phase 1 – Produktspezifikation
Stand: 05.11.2026 · Version 1.0
Eingesetztes Werkzeug: ChatGPT / Codex

## 1. Zielsetzung

AI unterstützte die Strukturierung der Projektidee, die Ableitung überprüfbarer Anforderungen, die MVP-Abgrenzung und die Konsistenzprüfung. Ein weiterer Einsatzbereich war der Vergleich technischer Optionen und externer Datenquellen.

Die Dokumentation gliedert den AI-Einsatz nach Zielsetzung, Prompt, Ergebnis und kritischer Bewertung. Sie zeigt die Beiträge zur Anforderungsanalyse, Priorisierung, Qualitätsprüfung und Bewertung technischer Optionen.

## 2. Anwendung A: Anforderungen aus der Produktidee ableiten

### Ziel

Die Produktidee und die vorhandene Featureliste in eine nachvollziehbare, überprüfbare Anforderungsstruktur überführen.

### Prompt

> Übernimm die Rolle eines Requirements Engineers für das Semesterprojekt QuestQueue. Die Anwendung soll Steam-Spieler:innen bei der Entscheidung unterstützen, welches Spiel sie als Nächstes spielen möchten. Als Grundlage dienen das bisherige Spielverhalten, aktuelle Interessen und persönliche Rückmeldungen.
>
> Berücksichtige folgende Produktfunktionen: zuletzt und meistgespielte Spiele, ein Präferenzprofil, ein Genre-Dashboard, Empfehlungen innerhalb und außerhalb der Bibliothek, Like/Dislike für externe Empfehlungen, Spielzeitverlauf, Current Taste und All-Time Taste, Wiederentdeckung früherer Favoriten, persönliche Tags wie Finished oder Loved It, Ausschlussfilter und einen „What should I play?“-Button.
>
> Formuliere Problemstellung, Zielgruppe und Projektziel. Leite mindestens zehn konkrete User Stories sowie funktionale und nichtfunktionale Anforderungen ab. Ordne jedes Feature einer Story zu und vergib eindeutige IDs. Formuliere überprüfbare Akzeptanzkriterien für alle Must-have-Stories. Kennzeichne Annahmen und offene Fragen ausdrücklich, statt fehlende Informationen als bereits entschieden darzustellen.

### Ergebnis und Bewertung

Die Produktspezifikation enthält 19 User Stories, 19 zugeordnete funktionale Anforderungen und sieben nichtfunktionale Anforderungen. Alle 13 Produktfeatures sind im README ihren Stories zugeordnet. Ergänzt wurden notwendige Anforderungen für Anmeldung, Datenimport, Fehlerbehandlung, Löschung, Demonstration und Metadaten-Caching.

Die Struktur erleichtert die Nachverfolgbarkeit. Die Anzahl der Anforderungen allein sagt jedoch nichts über deren Qualität aus. Entscheidend sind ein klarer Nutzen, eindeutige Begriffe und Kriterien, die später tatsächlich geprüft werden können.

## 3. Anwendung B: Priorisierung und MVP-Abgrenzung

### Ziel

Aus der vollständigen Produktvision einen im Semester realistisch umsetzbaren Kernumfang ableiten.

### Prompt

> Prüfe den Anforderungsentwurf von QuestQueue hinsichtlich seines Umfangs. Priorisiere die Anforderungen als Must, Should oder Could und begründe die Einordnung anhand des Nutzens für den ersten vollständigen Anwendungsfall und der technischen Abhängigkeiten.
>
> Der Kernablauf soll von der Anmeldung und Datenübernahme über das Präferenzprofil bis zu einem nachvollziehbaren Spielvorschlag führen. Current Taste und All-Time Taste sollen dabei berücksichtigt werden. Definiere enthaltene und ausgeschlossene Funktionen, einen reproduzierbaren Demonstrationsfall und eine überprüfbare Definition of Done.
>
> Behalte sämtliche Features in der Produktvision, auch wenn sie nicht zum ersten MVP gehören. Vermeide zusätzliche Pflichtfunktionen ohne Bezug zur Featureliste.

### Ergebnis und Bewertung

Die Spezifikation unterscheidet elf Must-, sieben Should- und eine Could-Story. Der MVP umfasst Spielübersichten, Präferenzprofile, beide Taste-Varianten, eigene Empfehlungen und den Auswahlbutton sowie Datenversorgung, Anmeldung, Fehlerbehandlung, Löschung und Demonstration.

Dashboard, externe Empfehlungen, Feedback, Verlauf, Wiederentdeckung, Tags und Filter wurden als Should-Funktionen vom MVP getrennt. Zeitgesteuerte Aktualisierung wurde als Could eingestuft. Zusätzliche Funktionen ohne Beitrag zum Hauptanwendungsfall wurden nicht in den Pflichtumfang übernommen.

Die kritische Prüfung zeigte, dass die Anzahl der Must-Stories allein den Aufwand nicht angemessen beschreibt: Mehrere Stories sichern denselben Kernablauf ab, während zusätzliche Empfehlungsbereiche eigenständige Erweiterungen bilden. Für zwei Personen und die Implementierungsabgabe am 09.12.2026 wurden daher ein früher Integrationsnachweis und der Vorrang des MVP vor Erweiterungen festgehalten. Die Aufwandseinschätzung wird anhand dieses Nachweises überprüft.

## 4. Anwendung C: Konsistenz- und Qualitätsprüfung

### Ziel

Widersprüche, fehlende Datenannahmen und nicht überprüfbare Aussagen vor der Implementierung erkennen.

### Prompt

> Führe einen kritischen Review der QuestQueue-Spezifikation durch. Prüfe die Übereinstimmung zwischen Projektüberblick, User Stories, funktionalen Anforderungen und MVP. Untersuche insbesondere:
>
> - Sind alle gewünschten Features nachvollziehbar abgedeckt?
> - Werden fehlende Spielzeitwerte von explizit null Minuten unterschieden?
> - Ist Spielzeit als Interessenssignal gekennzeichnet, ohne daraus Zufriedenheit oder einen Spielabschluss abzuleiten?
> - Werden kürzlich gespielte Titel, genaue letzte Spielzeitpunkte und selbst erfasste Verlaufsdaten sauber unterschieden?
> - Sind die Wirkungen von Tags, Feedback und Filtern miteinander vereinbar?
> - Bleiben Abmeldung, Kontowechsel und Datenlöschung getrennte Vorgänge?
> - Sind personenbezogene Daten von allgemeinen Metadaten getrennt?
> - Welche technischen Aussagen benötigen noch einen Integrationsnachweis?
>
> Stelle die Befunde als Tabelle mit Problem, Auswirkung und Korrekturvorschlag dar. Behaupte keine API-Fähigkeiten, Testergebnisse oder Nutzererkenntnisse, die nicht nachgewiesen wurden.

### Ergebnisse und übernommene Präzisierungen

| Prüfpunkt                  | Übernommene Präzisierung                                      |
| -------------------------- | ------------------------------------------------------------ |
| Unbekannte Spielzeit       | Fehlende Werte gelten nicht als ungespielt; dafür sind explizite 0 Minuten erforderlich. |
| Aussagekraft von Spielzeit | Minuten werden als implizites Interessenssignal behandelt, nicht als sichere positive Bewertung. |
| Letzte Aktivität           | Eine Liste kürzlich aktiver Spiele belegt ohne Zeitpunkte keine genaue zeitliche Reihenfolge. |
| Zeitverlauf                | Snapshots liefern beobachtete Intervalländerungen seit Erfassungsbeginn, keine rückwirkende Sitzungshistorie. |
| Tags und Empfehlungen      | Ausschlüsse haben Vorrang vor positiven Signalen; Loved It verstärkt zulässige Referenzen, Like entscheidet Gleichstände im externen Bereich. |
| Kontodaten                 | Abmeldung beendet den Zugriff, während bestätigte Löschung persönliche Daten entfernt. Ein Kontowechsel darf keine fremden Daten offenlegen oder löschen. |
| Cache                      | Allgemeine Spielmerkmale werden von persönlichen Bibliotheken, Bewertungen und Snapshots getrennt. |
| Technische Machbarkeit     | Sichtbarkeit, Antwortfelder, Anmeldung und Metadatenzuordnung werden in einem frühen Spike geprüft. |

Die Prüfung verbessert die innere Konsistenz. Sie ersetzt weder einen unabhängigen Review noch Tests der späteren Anwendung. Weil dieselbe AI an Entwurf und Prüfung beteiligt ist, können Annahmen trotz Selbstprüfung bestehen bleiben.

## 5. Anwendung D: Technische Optionen bewerten

### Ziel

Technische Möglichkeiten anhand der Anforderungen vergleichen, einen geeigneten Integrationsansatz bestimmen und verbleibende Risiken erfassen.

### Prompt

> Bewerte die technische Umsetzbarkeit von QuestQueue mit folgendem gewählten Rahmen: Webanwendung, lokale Entwicklung, Steam Sign-In, Python mit FastAPI, Vue mit TypeScript, PostgreSQL sowie eine externe Metadaten-API mit lokalem Cache.
>
> Erläutere Abhängigkeiten und prüfe relevante Aussagen anhand offizieller Dokumentation. Unterscheide die Anmeldung über Steam von der Authentifizierung gegenüber einem möglichen Metadatenanbieter. Leite aus lokaler Entwicklung weder einen späteren Hostinganbieter noch eine pauschale Ein-Nutzer-Beschränkung ab.
>
> Vergleiche für Empfehlungen eine inhaltsbasierte Baseline, semantische Embeddings und kollaborative Verfahren. Bewerte außerdem manuelle Aktualisierung, Aktualisierung veralteter Daten bei Anmeldung und periodische Erfassung bei laufendem Backend. Trenne die Aktualisierung persönlicher Spielzeiten von der Gültigkeit allgemeiner Metadaten.
>
> Gib eine begründete Empfehlung ab, kennzeichne sie als Vorschlag und halte konkrete Formeln, Gewichtungen, Intervalle und Anbieter offen, solange dazu keine ausdrückliche Entscheidung vorliegt.

### Ergebnis und Bewertung

Der technische Rahmen verbindet Steam OpenID für die Identitätsprüfung, die Steam Web API für persönliche Spieldaten und IGDB für allgemeine Metadaten mit PostgreSQL-Cache. Die Sichtbarkeit der Steam-Daten bleibt eine separate Voraussetzung. Die dokumentierte Unterstützung für externe Spielkennungen und lokales Caching begründet die Auswahl von IGDB; der tatsächliche Zugriff und die Abdeckung werden im Phase-2-Integrationsnachweis geprüft.

Als Empfehlungsmethode wurde eine erklärbare genre- und minutenbasierte Baseline gewählt. Sie benötigt keine Trainingsdaten und besitzt feste Akzeptanzbeispiele für Profilgewichte und Rangfolgen. Manueller Refresh und anmeldebezogene Aktualisierung ab 24 Stunden Datenalter wurden kombiniert; Mindestabstand und Cache-Gültigkeit sind als Produktregeln definiert. Embeddings, kollaborative Verfahren und periodische Erfassung wurden wegen des zusätzlichen Aufwands nicht in den MVP aufgenommen.

Die kritische Bewertung trennte dokumentierte Schnittstellenfähigkeiten von Annahmen über reale Datenabdeckung. Ein plausibler Technologievergleich genügt nicht als Integrationsnachweis. Deshalb enthält die Spezifikation eine Bibliotheksstichprobe, eindeutige Zuordnungsregeln und einen Prüfplan für Cache- und Fehlerverhalten. Die Relevanz des Rankings bleibt zusätzlich qualitativ zu bewerten.

## 6. Quellen, Grenzen und Verantwortlichkeit

Die technische Bewertung stützt sich auf die in [requirements.md, Abschnitt 10](requirements.md#10-quellen) aufgeführten Quellen. Anbieterinformationen wurden für Zugangsbedingungen und Schnittstellen verwendet; Berechnungsregeln und Produktgrenzen wurden projektspezifisch festgelegt.

Es wurden in dieser Phase keine Nutzerinterviews, Laufzeitmessungen oder authentifizierten Live-API-Tests durchgeführt. Dokumentstruktur, Dateiverweise und Anforderungszuordnungen wurden geprüft. Vertrauliche Zugangsdaten wurden nicht in die AI-Eingaben aufgenommen.

AI war besonders hilfreich bei der Strukturierung der Featureliste, der Formulierung von Grenzfällen und dem Vergleich von Alternativen. Grenzen zeigten sich bei ergänzten Annahmen, vorzeitigen technischen Festlegungen und scheinbar plausiblen Aussagen über verfügbare Daten. Die Ergebnisse müssen deshalb fachlich geprüft und durch spätere Integrations- und Akzeptanztests abgesichert werden.

Die Verantwortung für Anforderungen, Prioritäten, technische Entscheidungen und Abgabeinhalte liegt bei den Studierenden. Die festgelegten Regeln dienen als Grundlage für Architektur und Implementierung. Integrationsnachweise, Akzeptanztests und freiwilliges Nutzwertfeedback überprüfen sie in den folgenden Projektphasen.
