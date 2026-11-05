# QuestQueue – AI-Einsatz im Requirements Engineering

Projektphase: Phase 1 – Produktspezifikation
Stand: 05.11.2026
Eingesetztes Werkzeug: ChatGPT / Codex

## 1. Zielsetzung

AI wurde eingesetzt, um die Projektidee von QuestQueue zu strukturieren, Anforderungen abzuleiten, einen realistischen MVP vorzuschlagen und den Entwurf auf Widersprüche und Unklarheiten zu prüfen. Zusätzlich unterstützte AI den Vergleich technischer Optionen und die Dokumentation offener Entscheidungen.

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
> Behalte sämtliche Features in der Produktvision, auch wenn sie nicht zum ersten MVP gehören. Vermeide zusätzliche Pflichtfunktionen ohne Bezug zur Featureliste. Gib keine festen Kalendertermine oder belastbaren Aufwandsschätzungen vor, solange Teamgröße und Zeitbudget unbekannt sind.

### Ergebnis und Bewertung

Der Entwurf unterscheidet elf Must-, sieben Should- und eine Could-Story. Der vorgeschlagene Kern umfasst Spielübersichten, Präferenzprofile, beide Taste-Varianten, eigene Empfehlungen und den Auswahlbutton sowie die dafür erforderliche Datenbasis und unterstützende Funktionen.

Dashboard, externe Empfehlungen, Feedback, Verlauf, Wiederentdeckung, Tags und Filter bleiben als priorisierte Erweiterungen enthalten. Zeitgesteuerte Aktualisierung ist als optionale Erweiterung geführt. Ein zusätzlicher persistenter Merkzettel wurde nicht als Pflichtfunktion übernommen, weil er aus der Featureliste nicht hervorgeht.

Die Priorisierung ist weiterhin ein Reviewvorschlag. Ihre Umsetzbarkeit muss mit dem tatsächlichen Semesterbudget abgeglichen werden. Auch Should-Funktionen gehören zur Produktvision; ihre Einstufung bedeutet keine ersatzlose Streichung.

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

| Prüfpunkt                  | Präzisierung im Entwurf                                      |
| -------------------------- | ------------------------------------------------------------ |
| Unbekannte Spielzeit       | Fehlende Werte gelten nicht als ungespielt; dafür sind explizite 0 Minuten erforderlich. |
| Aussagekraft von Spielzeit | Minuten werden als implizites Interessenssignal behandelt, nicht als sichere positive Bewertung. |
| Letzte Aktivität           | Eine Liste kürzlich aktiver Spiele belegt ohne Zeitpunkte keine genaue zeitliche Reihenfolge. |
| Zeitverlauf                | Snapshots liefern beobachtete Intervalländerungen seit Erfassungsbeginn, keine rückwirkende Sitzungshistorie. |
| Tags und Empfehlungen      | Ausschlüsse haben Vorrang vor positiven Signalen; genaue Verstärkungen benötigen eine dokumentierte Regel. |
| Kontodaten                 | Abmeldung beendet den Zugriff, während bestätigte Löschung persönliche Daten entfernt. Ein Kontowechsel darf keine fremden Daten offenlegen oder löschen. |
| Cache                      | Allgemeine Spielmerkmale werden von persönlichen Bibliotheken, Bewertungen und Snapshots getrennt. |
| Technische Machbarkeit     | Sichtbarkeit, Antwortfelder, Anmeldung und Metadatenzuordnung werden in einem frühen Spike geprüft. |

Die Prüfung verbessert die innere Konsistenz. Sie ersetzt weder einen unabhängigen Review noch Tests der späteren Anwendung. Weil dieselbe AI an Entwurf und Prüfung beteiligt ist, können Annahmen trotz Selbstprüfung bestehen bleiben.

## 5. Anwendung D: Technische Optionen und offene Entscheidungen bewerten

### Ziel

Technische Möglichkeiten anhand der Anforderungen vergleichen und ausgewählte Rahmenbedingungen von noch offenen Detailentscheidungen trennen.

### Prompt

> Bewerte die technische Umsetzbarkeit von QuestQueue mit folgendem gewählten Rahmen: Webanwendung, lokale Entwicklung, Steam Sign-In, Python mit FastAPI, Vue mit TypeScript, PostgreSQL sowie eine externe Metadaten-API mit lokalem Cache.
>
> Erläutere Abhängigkeiten und prüfe relevante Aussagen anhand offizieller Dokumentation. Unterscheide die Anmeldung über Steam von der Authentifizierung gegenüber einem möglichen Metadatenanbieter. Leite aus lokaler Entwicklung weder einen späteren Hostinganbieter noch eine pauschale Ein-Nutzer-Beschränkung ab.
>
> Vergleiche für Empfehlungen eine inhaltsbasierte Baseline, semantische Embeddings und kollaborative Verfahren. Bewerte außerdem manuelle Aktualisierung, Aktualisierung veralteter Daten bei Anmeldung und periodische Erfassung bei laufendem Backend. Trenne die Aktualisierung persönlicher Spielzeiten von der Gültigkeit allgemeiner Metadaten.
>
> Gib eine begründete Empfehlung ab, kennzeichne sie als Vorschlag und halte konkrete Formeln, Gewichtungen, Intervalle und Anbieter offen, solange dazu keine ausdrückliche Entscheidung vorliegt.

### Ergebnis und Bewertung

Der gewählte technische Rahmen wurde in die Dokumentation übernommen. Steam OpenID ist für die Identitätsprüfung vorgesehen; die Sichtbarkeit von Spieldaten bleibt eine separate Voraussetzung. Metadaten sollen über eine zusätzliche API bezogen und in PostgreSQL wiederverwendet werden. IGDB ist ein zu prüfender Kandidat.

Als erste Empfehlungsrichtung wurde ein erklärbares inhaltsbasiertes Verfahren vorgeschlagen. Für die Aktualisierung wurde ein manueller Refresh in Kombination mit einer Aktualisierung veralteter Daten bei Anmeldung beschrieben. Regelmäßige Erfassung bleibt eine mögliche Ergänzung. Konkrete Gewichtungen, Schwellenwerte, Cache-Gültigkeit und Anbieter sind noch nicht verbindlich festgelegt.

Diese Trennung verhindert, dass plausible AI-Vorschläge unbemerkt zu freigegebenen Anforderungen werden. Die Eignung einer Datenquelle ist erst nach einem praktischen Zugriffstest und einer Prüfung ihrer Nutzungsbedingungen ausreichend abgesichert.

## 6. Quellen, Grenzen und Verantwortlichkeit

Für technische Abhängigkeiten wurden offizielle Unterlagen von Valve, IGDB und FastAPI herangezogen. Die Links stehen in [requirements.md, Abschnitt 10](requirements.md#10-quellen). Die Recherche ist kein Nachweis eines erfolgreichen Live-Imports oder einer bereits funktionierenden Integration.

Es wurden in dieser Phase keine Nutzerinterviews, Laufzeitmessungen oder authentifizierten Live-API-Tests durchgeführt. Dokumentstruktur, Dateiverweise und Anforderungszuordnungen wurden geprüft. Vertrauliche Zugangsdaten wurden nicht in die AI-Eingaben aufgenommen.

AI war besonders hilfreich bei der Strukturierung der Featureliste, der Formulierung von Grenzfällen und dem Vergleich von Alternativen. Grenzen zeigten sich bei ergänzten Annahmen, vorzeitigen technischen Festlegungen und scheinbar plausiblen Aussagen über verfügbare Daten. Die Ergebnisse müssen deshalb fachlich geprüft und durch spätere Integrations- und Akzeptanztests abgesichert werden.

Die endgültige Verantwortung für Prioritäten, Scope, technische Entscheidungen und Abgabeinhalte liegt bei den Studierenden. Vor der Freigabe bleiben insbesondere die Empfehlungsregeln, Aktualisierungspolitik, Metadatenquelle und realistische Semesterplanung zu konkretisieren.
