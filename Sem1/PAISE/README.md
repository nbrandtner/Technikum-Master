# QuestQueue

**Your next adventure awaits.**

QuestQueue hilft Steam-Spieler:innen bei der Frage **„Was soll ich als Nächstes spielen?“** Die Anwendung macht Spielverhalten sichtbar, erstellt ein persönliches Präferenzprofil und empfiehlt passende Spiele aus der eigenen Bibliothek sowie – als Erweiterung – außerhalb des eigenen Bestands. Dabei werden **Current Taste** und **All-Time Taste** unterschieden.

## Problem und Motivation

Große Spielebibliotheken erschweren die Auswahl: Ungespielte Titel gehen unter, frühere Lieblingsspiele werden vergessen und aktuelle Interessen verändern sich. Eine einfache Liste nach Gesamtspielzeit zeigt weder, was gerade interessant ist, noch welche noch unentdeckten Spiele dazu passen.

QuestQueue verbindet deshalb Spielübersichten, nachvollziehbare Vorlieben und konkrete Vorschläge. Eigene Tags, Bewertungsfeedback und Ausschlussfilter sollen die Empfehlungen später gezielt anpassbar machen. Die Problemhypothese stammt aus der Projektidee; sie ist noch nicht durch Nutzerinterviews bestätigt. Spielzeit ist ein Interessenssignal und kein sicherer Nachweis für Freude, Qualität oder einen Spielabschluss.

## Zielgruppe und Projektziel

Primäre Zielgruppe sind PC-Spieler:innen mit einer Steam-Bibliothek, mehreren ungespielten Titeln und dem Wunsch, ihren Bestand bewusster zu nutzen. Auch Personen, die neue Spiele entdecken oder frühere Favoriten wiederfinden möchten, gehören zur Zielgruppe.

Im Semester entsteht eine Webanwendung, die zunächst lokal entwickelt und demonstriert wird. Der vollständige MVP-Ablauf lautet: über Steam anmelden, den Datenimport starten, zuletzt und meistgespielte Titel ansehen, ein Präferenzprofil aufbauen, Current Taste oder All-Time Taste wählen und über „What should I play?“ einen begründeten Vorschlag aus der eigenen Bibliothek erhalten. Persönliche Daten werden je verifizierter SteamID getrennt gespeichert. Lokale Entwicklung legt weder den späteren Hostinganbieter noch den Umfang eines öffentlichen Mehrbenutzerbetriebs fest.

## Funktionsübersicht

Alle 13 Punkte der wiedergefundenen Featureliste sind in der Produktspezifikation enthalten. Die Prioritäten sind ein Vorschlag für einen realistischen Semesterumfang; sie sind keine bereits bestätigte Aufwandsschätzung.

| Gewünschtes Feature | User Story | Priorität / Umfang |
| --- | --- | --- |
| Last played games anzeigen | US-01 | Must / MVP |
| Most played games anzeigen | US-02 | Must / MVP |
| Preference Profile aufbauen | US-03 | Must / MVP |
| Dashboard, z. B. meistgespielte Genres | US-04 | Should / nach dem Kernablauf |
| Empfehlungen für eigene Spiele | US-05 | Must / MVP, zunächst ungespielte Titel |
| Empfehlungen für Spiele außerhalb der Bibliothek | US-06 | Should / Entdeckungsbereich |
| Like/Dislike für externe Empfehlungen | US-07 | Should / abhängig von US-06 |
| Spielzeit über die Zeit verfolgen | US-08 | Should / ab Beginn eigener Erfassung |
| Current Taste und All-Time Taste | US-09 | Must / MVP |
| Früher gern gespielte Titel wiederentdecken | US-10 | Should / eigener Empfehlungsbereich |
| Eigene Tags: Finished, Dropped, Loved It, Not Interested | US-11 | Should / beeinflussen Auswahl und Profil |
| Genres und andere Empfehlungseigenschaften ausschließen | US-12 | Should / zunächst Genre-Ausschluss |
| „What should I play?“ | US-13 | Must / MVP, konkrete Auswahl statt Zufall |

Steam-Anmeldung und Import, Datenqualität, Löschung, API-Metadaten mit Cache und ein getrennter Demomodus sind zusätzliche unterstützende Anforderungen. Eine zeitgesteuerte Aktualisierung ist eine mögliche Erweiterung. Refresh-Auslöser, Intervalle und Cache-Gültigkeit sind noch nicht beschlossen; manuell auslösbarer Import bleibt als überprüfbare Grundfunktion vorgesehen.

## MVP und Erweiterungen

Der MVP zeigt eine einfache Profilübersicht mit Genregewichten; ein grafisches Analyse-Dashboard ist eine Erweiterung. Current Taste verwendet verfügbare Spielzeit der letzten 14 Tage am Importzeitpunkt, All-Time Taste die verfügbare Gesamtspielzeit. Fehlen aktuelle Daten, wird dies erklärt und nicht stillschweigend durch Gesamtspielzeit ersetzt.

Spielmerkmale sollen über eine zusätzliche API bezogen und lokal in PostgreSQL gecacht werden. Anbieter und Steam-AppID-Zuordnung werden in einem frühen Spike geprüft; IGDB ist ein Kandidat. Ein kleiner fester Datensatz dient nur Offline-Demo und Tests, nicht als Begrenzung des Live-Produkts auf 30 Spiele. Metadatenabdeckung und Datenalter bleiben sichtbar. Die Empfehlungsmethode ist noch offen; erklärbares inhaltsbasiertes Ranking ist ein Vorschlag, kein freigegebener Algorithmus.

## Vereinbarte Technik und offene Entscheidungen

| Bereich | Stand |
| --- | --- |
| Plattform | Webapp – vom Nutzer gewählt |
| Entwicklung | Lokal; spätere Veröffentlichung und Hosting noch offen |
| Anmeldung | Steam Sign-In über Steam OpenID |
| Backend | Python + FastAPI |
| Frontend | Vue + TypeScript |
| Datenhaltung | PostgreSQL für persönliche Daten und Metadaten-Cache |
| Metadaten | API plus Cache gewählt; Anbieter noch im Machbarkeitstest |
| Empfehlungen | Offen; inhaltsbasierte Baseline und Embeddings werden verglichen |
| Aktualisierung | Offen; manuell, bei Anmeldung oder zeitgesteuert werden bewertet |

**Lokale Entwicklung bedeutet:** Browser, FastAPI und PostgreSQL laufen auf dem Entwicklungsrechner. Für Steam-Anmeldung und frische externe Daten wird weiterhin eine Internetverbindung benötigt. Die konkrete Entwicklungsumgebung, Bibliotheken und spätere Bereitstellung werden separat festgelegt.

**Vorschlag zur Diskussion:** Mit erklärbarem inhaltsbasiertem Ranking beginnen; bei Anmeldung nur veraltete Daten aktualisieren und zusätzlich einen manuellen Refresh anbieten. Regelmäßige Snapshots wären später bei laufendem Backend möglich. Weder dieser Ablauf noch konkrete Zeitintervalle sind beschlossen.

## Name und Branding

QuestQueue verbindet die nächste spielerische „Quest“ mit einer geordneten Auswahl möglicher nächster Spiele. Positionierung: **Deine Bibliothek. Dein nächstes Abenteuer.** Der englische Claim ist ein Branding-Vorschlag für den Review. Die Ansprache ist freundlich, direkt und ohne Kaufdruck.

Gestaltungsvorschlag: Marineblau #142033, Türkis #2DD4BF und helles Neutralgrau #F3F4F6; Textkontraste sind separat zu prüfen. Eine Kartenreihe mit hervorgehobenem Spiel kann die nächste Auswahl darstellen. Ein fertiges Logo ist nicht Bestandteil dieser Phase. QuestQueue ist ein unabhängiges Studienprojekt ohne behauptete Verbindung zu Valve.

## Dokumentation und Stand

| Datei | Inhalt |
| --- | --- |
| [docs/requirements.md](docs/requirements.md) | Featurezuordnung, User Stories, Prioritäten, Akzeptanzkriterien und Datenregeln |
| [docs/mvp.md](docs/mvp.md) | MVP, Erweiterungen, Abhängigkeiten, Demo und Umsetzungsetappen |
| [docs/ai-usage.md](docs/ai-usage.md) | AI-Einsatz, kritische Prüfung und Korrektur anhand der Featureliste |

Stand: 05.11.2026 · Version 0.3 · Phase 1 · Reviewentwurf. Es gibt noch keine implementierte Anwendung. Der technische Rahmen wurde vom Nutzer gewählt; die externe Integration wird durch einen frühen Machbarkeitstest abgesichert.

Gewünschter späterer Projektpfad: F:\Technikum-Master\Sem1\PAISE. README und docs können direkt dort liegen; Anwendungscode folgt in späteren Phasen.

Featureliste und technische Auswahl sind ausdrückliche Nutzerentscheidungen. Prioritäten, genaue Produktregeln, Empfehlungsmethode, Refresh-Verhalten und spätere Hosting-/Mehrbenutzergrenzen bleiben als Reviewvorschläge beziehungsweise offene Entscheidungen gekennzeichnet.
