# QuestQueue – Anforderungen

Stand: 05.11.2026 · Version 0.3 · Reviewentwurf

## 1. Grundlage und Begriffe

Diese Version übernimmt alle 13 Punkte der vom Nutzer wiedergefundenen Featureliste. Die Produktvision umfasst Spielübersichten, Präferenzprofile, Empfehlungen innerhalb und außerhalb der Bibliothek, Feedback, Zeitverlauf, Wiederentdeckung, Tags, Filter und einen „What should I play?“-Button. Anforderungen und Story-IDs wurden gegenüber Version 0.1 neu geordnet; die Funktionsübersicht im README ordnet jeden Listenpunkt einer Story zu.

| Begriff | Festlegung |
| --- | --- |
| Bibliothek | Vom letzten erfolgreichen Steam-Bibliotheksimport zurückgegebene Spiele; kein garantierter vollständiger Lizenzbestand. |
| Ungespielt | Explizit gemeldete Gesamtspielzeit von 0 Minuten. Fehlende Spielzeit bedeutet unbekannt. |
| Gespielt | Bekannte Gesamtspielzeit größer 0 Minuten; daraus folgt kein Abschlussstatus. |
| All-Time Taste | Genreprofil aus der verfügbaren Gesamtspielzeit zum letzten erfolgreichen Import. |
| Current Taste | Genreprofil aus verfügbaren Spielminuten der letzten 14 Tage zum Importzeitpunkt; keine Echtzeitbeobachtung. |
| Last played | Letzter Spielzeitpunkt, wenn die Datenquelle ihn liefert. Eine Liste kürzlich aktiver Spiele allein belegt keine exakte Reihenfolge. |
| Persönliche Tags | In QuestQueue gesetzte Angaben wie Finished; getrennt von Genre-Metadaten oder Steam-Community-Tags. |
| Snapshot | Gespeicherter kumulierter Spielzeitstand mit Erfassungszeitpunkt; keine einzelne Spielsitzung. |

Der Nutzer hat eine Webapp mit lokaler Entwicklung, Steam Sign-In, Python/FastAPI, Vue/TypeScript, PostgreSQL und API-Metadaten mit Cache gewählt. Steam OpenID bestätigt die Identität; private Spieldaten werden dadurch nicht automatisch zugänglich. QuestQueue erhebt keine Steam-Passwörter.

Persönliche Daten sind an die verifizierte SteamID gebunden. Kontowechsel darf keine Daten anderer Konten offenlegen oder löschen. Ein gemeinsam nutzbarer allgemeiner Metadaten-Cache enthält keine privaten Profilantworten. Die lokale Entwicklungsumgebung ist vereinbart; öffentlicher Betrieb, Hostinganbieter, Zahl gleichzeitig unterstützter Nutzer:innen und Betriebsbudget sind noch offen.

### Entscheidungsstand

| Bereich | Status und Grenze |
| --- | --- |
| Webapp; lokal entwickeln | Vom Nutzer gewählt; spätere Bereitstellung nicht festgelegt |
| Steam Sign-In | Vom Nutzer gewählt; OpenID-Integration und Callback lokal testen |
| Python + FastAPI; Vue + TypeScript; PostgreSQL | Vom Nutzer gewählt |
| API plus Metadaten-Cache | Vom Nutzer gewählt; konkreter Anbieter noch offen |
| Empfehlungsmethode einschließlich Profilgewichtung | Offen; Abschnitt 5 vergleicht Kandidaten |
| Refresh-Auslöser, Intervalle und Cache-Gültigkeit | Offen; Abschnitt 7 beschreibt Optionen |
| MVP-Prioritäten und numerische Produktgrenzen | Weiterhin Reviewvorschlag, keine zusätzliche Nutzerfreigabe |

Die folgende Spezifikation bleibt ein Reviewentwurf. Die Auswahl des Algorithmus und der Aktualisierungsregeln ist vor Implementierung des jeweiligen Verhaltens zu schließen; offene Punkte werden nicht durch versteckte Standardwerte ersetzt.

## 2. Prioritäten und Abdeckung

**Must:** unverzichtbar für den ersten vollständigen Anwendungsfall oder dessen verlässlichen Betrieb. **Should:** Bestandteil der Produktvision und nächste Ausbaustufe, aber nicht für die MVP-Abnahme erforderlich. **Could:** optionale Komfortfunktion. Eine Should-Einstufung bedeutet keine Streichung aus der Produktspezifikation.

Die 19 User Stories umfassen elf Must-, sieben Should- und eine Could-Story. Sieben Must-Stories beschreiben Produkt- und Datenfunktionen einschließlich API-Metadaten; vier sichern Anmeldung/Import, Fehlerbehandlung, Datenkontrolle und Demonstration. Alle sieben nichtfunktionalen Anforderungen gelten im MVP.

Die Zuordnung aller 13 gewünschten Features steht im [README](../README.md). Der MVP und die Erweiterungsreihenfolge stehen in [mvp.md](mvp.md).

## 3. User Stories mit Akzeptanzkriterien

### US-01 · Last played games · Must

Als Steam-Spieler:in möchte ich zuletzt gespielte Spiele sehen, damit ich meine jüngsten Aktivitäten wiederfinde.

- Die Ansicht zeigt bis zu zehn Spiele mit bekanntem letztem Spielzeitpunkt absteigend nach diesem Zeitpunkt; Gleichstände löst die numerische AppID aufsteigend auf.
- Der Zeitpunkt und der Datenstand werden angezeigt. Fehlende oder ungültige Zeitpunkte werden als unbekannt behandelt, nicht als „nie gespielt“.
- Falls nur eine Quelle für kürzlich aktive Spiele, aber keine exakten Zeitpunkte verfügbar ist, heißt die Ansicht „Kürzlich gespielt – genaue Reihenfolge unbekannt“. Sie verwendet eine stabile AppID-Reihenfolge und behauptet keine zeitliche Sortierung.
- Gibt es weder bekannte Zeitpunkte noch zugängliche aktuelle Aktivitätsdaten, erscheint ein erklärter Leerzustand. Gesamtspielzeit wird nicht als Ersatz für Aktualität verwendet.

### US-02 · Most played games · Must

Als Nutzer:in möchte ich meine meistgespielten Titel sehen, damit ich meine langfristigen Spielschwerpunkte erkenne.

- Es erscheinen bis zu zehn importierte Spiele mit bekannter Gesamtspielzeit größer 0, absteigend nach Minuten; Gleichstände löst die AppID aufsteigend auf.
- Spielzeit wird in Stunden und Minuten dargestellt; intern bleiben Minuten erhalten. Fehlende Werte werden nicht als 0 einsortiert.
- Die Bibliotheksansicht zeigt auch ungespielte Titel und kennzeichnet unbekannte Werte. Ein Filter „Ungespielt“ enthält ausschließlich explizite 0-Minuten-Einträge.

### US-03 · Preference Profile aufbauen · Must

Als Nutzer:in möchte ich ein aus meinem Spielverhalten abgeleitetes Präferenzprofil erhalten, damit Empfehlungen auf nachvollziehbaren Vorlieben beruhen.

- Nach erfolgreichem Import und verfügbarer Metadatenanreicherung werden die verfügbaren Profile nach einer ausdrücklich gewählten und versionierten Regel berechnet. Die endgültige Methode ist noch offen; Abschnitt 5 dokumentiert die Optionen.
- Eine einfache Profilübersicht zeigt Profilname, Zeitfenster, berücksichtigte Spiele, Datenstand und eine verständliche Genre-Zusammenfassung mit Prozentwerten. Wie diese Darstellung aus der gewählten Methode abgeleitet wird, ist zusammen mit ihr zu dokumentieren.
- Die Gewichte über alle berücksichtigten Genres summieren sich vor Anzeigerundung zu 100 Prozent. Fehlende Metadaten werden nicht erfunden.
- Die Abdeckung wird als „X von Y importierten Spielen mit Genre-Metadaten“ sowie die Zahl tatsächlich verwendeter Referenzspiele angezeigt.
- Ohne passende positive Spielzeitwerte wird kein Profil erfunden. Die Oberfläche erklärt die fehlende Grundlage.

### US-04 · Analyse-Dashboard · Should

Als Nutzer:in möchte ich meine meistgespielten Genres und Spielschwerpunkte in einem Dashboard sehen, damit ich mein Verhalten leichter verstehe.

- Das Dashboard zeigt mindestens Genreanteile nach Spielminuten, die meistgespielten Titel und das ausgewählte Zeitfenster.
- Bei Spielen mit mehreren Genres werden Minuten gleichmäßig auf die Genres verteilt, damit die Summe nicht mehrfach gezählt wird. Die Grafik benennt die berücksichtigte Teilmenge.
- Tatsächliche Spielminuten und aus US-03 abgeleitete Präferenzwerte werden unterschiedlich beschriftet; es wird keine noch nicht gewählte Gewichtungsformel vorausgesetzt.
- Der Wechsel zwischen Current Taste und All-Time Taste aktualisiert alle betroffenen Kennzahlen. Unbekannte Daten bleiben erkennbar.

### US-05 · Empfehlungen aus der Bibliothek · Must

Als Nutzer:in möchte ich zu meinem Präferenzprofil passende eigene Spiele entdecken, damit ich meine vorhandene Bibliothek besser nutze.

- Die erste Empfehlungsart berücksichtigt ausschließlich importierte ungespielte Spiele mit Genre-Metadaten und positivem Score nach Abschnitt 5.
- Die Ergebnisliste enthält höchstens fünf unterschiedliche Spiele, absteigend nach Score; Gleichstände löst die AppID aufsteigend auf.
- Jeder Vorschlag nennt das verwendete Profil, mindestens ein belegtes passendes Merkmal, etwa Genre oder Thema, und ein gespieltes Referenzspiel als nachvollziehbaren Bezug. Ein Modell darf keine Merkmale erfinden.
- Bei unveränderten Daten, Profilen und Regeln bleibt die Reihenfolge identisch. Es werden keine unpassenden Platzhalter zum Auffüllen ausgegeben.
- Bei fehlendem Profil oder fehlenden Kandidaten erscheint ein verständlicher Leerzustand. Die Bibliothek bleibt zugänglich.

### US-06 · Empfehlungen außerhalb der Bibliothek · Should

Als Nutzer:in möchte ich passende neue Spiele außerhalb meiner Bibliothek entdecken, damit ich zusätzliche Spielmöglichkeiten finde.

- Ein getrennter Bereich verwendet denselben gewählten Profiltyp, aber Kandidaten aus einem bestätigten Metadatenkatalog, deren AppIDs nicht in der importierten Bibliothek stehen.
- Ergebnisse werden als „Nicht in deiner importierten Bibliothek“ gekennzeichnet; der Importzeitpunkt und mögliche Unvollständigkeit bleiben sichtbar.
- Höchstens fünf Ergebnisse werden mit Profilbezug und Begründung angezeigt. Importierte AppIDs dürfen nicht erscheinen.
- Ohne geeignete zusätzliche Katalogeinträge erscheint ein Leerzustand. Es gibt kein Versprechen, den vollständigen Steam-Store abzudecken.
- Preise, Verfügbarkeit und sichere Nichtbesitzaussagen werden ohne entsprechende geprüfte Datenquelle nicht behauptet.

### US-07 · Like/Dislike für externe Empfehlungen · Should

Als Nutzer:in möchte ich Empfehlungen außerhalb meiner Bibliothek liken oder disliken, damit ich deren Auswahl beeinflussen kann.

- Pro AppID ist genau eine Bewertung aus Like, Dislike oder neutral gespeichert; sie lässt sich ändern und zurücksetzen.
- Dislike entfernt den Titel aus zukünftigen externen Vorschlägen. Like soll bei ansonsten gleicher Relevanz einen Titel bevorzugen; die konkrete Verrechnung mit der noch offenen Empfehlungsmethode wird vor Umsetzung festgelegt und anhand fester Beispiele geprüft.
- Feedback bleibt nach Neustart erhalten und ist in einer Übersicht reversibel. Es wird nach einem Neuimport nicht automatisch gelöscht, nur weil die AppID nun in der Bibliothek erscheint.
- Feedback beeinflusst zunächst nur den externen Empfehlungsbereich; seine Wirkung wird erklärt. Ein weitergehendes Lernen genrebezogener Vorlieben ist keine implizite Zusage.
- Bei aktiven Tags oder Filtern haben deren Ausschlüsse Vorrang vor Like.

### US-08 · Playtime over Time · Should

Als Nutzer:in möchte ich die Entwicklung meiner Spielzeit verfolgen, damit Veränderungen meiner Interessen erkennbar werden und zusätzliche Daten für mein Präferenzprofil vorliegen.

- Jeder erfolgreich ausgeführte Import speichert nach Einführung dieser Funktion einen Snapshot mit Erfassungszeitpunkt, AppID und bekannter kumulierter Spielzeit, unabhängig vom später gewählten Refresh-Auslöser. Fehlgeschlagene Imports erzeugen keinen Messpunkt.
- Nach mindestens zwei Messpunkten wird pro Spiel die Differenz zweier aufeinanderfolgender bekannter Stände mit dem tatsächlichen Intervall angezeigt. 120 auf 180 Minuten ergibt 60 beobachtete zusätzliche Minuten.
- Beim ersten Messpunkt gibt es nur eine Basislinie. Fehlende Werte, neu auftauchende Titel oder sinkende Zähler erzeugen keine erfundene oder negative Nutzungsdauer; ein sinkender Stand beginnt ein markiertes neues Vergleichssegment.
- Beobachtungsdaten beginnen mit QuestQueue. Lange Intervalle werden nicht gleichmäßig auf Tage verteilt und nicht als einzelne Sitzungen interpretiert.
- Die Profilansicht kann Referenzspiele um beobachtete Spielzeitzuwächse und Erfassungsabdeckung ergänzen. Ein 14-Tage-Signal aus Steam ist die vorgeschlagene erste Grundlage für Current Taste; ob und wie zusätzliche Verlaufsdaten gewichtet werden, gehört zur offenen Methodenentscheidung.
- Verlauf und Snapshots sind nach Neustart vorhanden und werden bei Profil-Löschung mit entfernt.

### US-09 · Current Taste und All-Time Taste · Must

Als Nutzer:in möchte ich zwischen aktuellen und langfristigen Vorlieben wechseln, damit die Auswahl zu meiner jetzigen Stimmung oder meinen dauerhaften Interessen passt.

- Zwei klar benannte Profile verwenden dieselbe Berechnung, aber unterschiedliche Eingangsminuten: verfügbare 14-Tage-Spielzeit beziehungsweise Gesamtspielzeit.
- Ein Profilwechsel aktualisiert Profilübersicht, Empfehlungsrangfolge und Begründungen ohne erneuten Import.
- Fehlen positive, geeignete aktuelle Werte, zeigt Current Taste „Keine ausreichenden aktuellen Daten“. All-Time Taste wird nicht stillschweigend als Current Taste ausgegeben.
- Der Zustand Current Taste unterscheidet, soweit vom Adapter nachweisbar, „keine aktuelle Aktivität“ von „Daten nicht verfügbar“. Mehrdeutige Antworten werden nicht sicher diagnostiziert.
- Ein fester Testdatensatz mit langfristigem Rollenspielschwerpunkt und aktuellem Strategieschwerpunkt führt zu entsprechend unterschiedlichen Genregewichten und unterschiedlichen Spitzenempfehlungen.
- Im MVP ist All-Time Taste die vorbelegte Auswahl. Für später implementierte Empfehlungsbereiche gilt derselbe Profilwechsel.

### US-10 · Frühere Favoriten wiederentdecken · Should

Als Nutzer:in möchte ich früher gern gespielte, länger nicht genutzte Spiele wiederfinden, damit ich passende Titel erneut aufgreifen kann.

- Der getrennte Bereich „Wiederentdecken“ berücksichtigt eigene gespielte Titel mit bekanntem letztem Spielzeitpunkt, der mindestens 90 Tage vor dem Importzeitpunkt liegt, sowie positivem Profilscore.
- Ein Kandidat benötigt zusätzlich entweder „Loved It“ aus US-11 oder mindestens 120 Minuten Gesamtspielzeit als ausdrücklich gekennzeichneten Näherungswert für früheres Interesse.
- Ohne Loved It wird nicht behauptet, die Person habe den Titel sicher geliebt. Unbekannte letzte Spielzeitpunkte genügen nicht für den Nachweis einer langen Pause.
- Die Begründung nennt Profilbezug und Pausenlänge. Aktive Tags und Ausschlussfilter werden berücksichtigt.
- Die Liste ungespielter eigener Titel aus US-05 bleibt getrennt; keine Doppelzuordnung oder Vermischung.

### US-11 · Persönliche Tags · Should

Als Nutzer:in möchte ich Spiele mit Finished, Dropped, Loved It und Not Interested markieren, damit meine Angaben die Empfehlungen gezielt beeinflussen.

- Tags lassen sich in der Bibliothek und auf vorhandenen Spielkarten setzen und entfernen; sie bleiben nach Import und Neustart erhalten.
- Finished und Dropped sind gegenseitig ausschließende Statuswerte. Loved It und Not Interested sind zusätzliche, unabhängig umschaltbare Angaben; Konflikte werden nach Abschnitt 6 aufgelöst.
- Finished, Dropped und Not Interested schließen einen Titel als Empfehlung aus. Loved It soll als explizites positives Signal in das Profil eingehen; die genaue Gewichtung gehört zur noch offenen Methodenentscheidung.
- Dropped und Not Interested schließen das Spiel auch als positive Profilreferenz aus. Finished allein entfernt nicht dessen positiven Beitrag zum Präferenzprofil.
- Nach einer Änderung werden die verfügbaren Profile und Vorschläge neu berechnet. Ohne positive Spielzeit macht Loved It allein ein Spiel nicht zur Referenz.
- Tags sind lokale Nutzereingaben und werden weder aus Steam-Spielzeit abgeleitet noch in Steam zurückgeschrieben.

### US-12 · Empfehlungen filtern · Should

Als Nutzer:in möchte ich bestimmte Genres und andere Eigenschaften ausschließen, damit die Vorschläge zu meinen aktuellen Einschränkungen passen.

- Die erste Ausbaustufe erlaubt den Ausschluss eines oder mehrerer Kataloggenres; ein Kandidat mit mindestens einem ausgeschlossenen Genre wird entfernt.
- Filter gelten für alle implementierten Empfehlungsbereiche sowie für „What should I play?“. Aktive Filter und eine Rücksetzfunktion sind sichtbar.
- Filter beeinflussen die Kandidaten, nicht das gespeicherte Präferenzprofil. Bei keinem verbleibenden Ergebnis wird kein Filter automatisch aufgehoben.
- Weitere Merkmale wie Einzelspieler/Mehrspieler sind Could und dürfen erst angeboten werden, wenn verlässliche Metadaten und klare Ausschlussregeln existieren.

### US-13 · What should I play? · Must

Als Nutzer:in möchte ich mit einem Button einen konkreten Spielvorschlag erhalten, damit ich ohne langes Vergleichen eine Entscheidungshilfe bekomme.

- Nach Profilwahl liefert ein Klick den höchstgereihten geeigneten Titel aus US-05 samt Begründung; der Button startet oder installiert kein Spiel.
- Gleiche Eingaben ergeben denselben Vorschlag. Wiederholtes Klicken verspricht keine zufällige Abwechslung.
- Ohne verwendbares Profil oder geeigneten Kandidaten erscheint ein Hinweis statt eines beliebigen Titels. Der Klick löst keinen versteckten Steam-Import aus.
- Nach Einführung von US-11/US-12 gelten dieselben Tags und Filter wie in der Empfehlungsansicht.
- Spätere Bereiche für neue Spiele oder Wiederentdeckung sind nur nach ausdrücklicher Bereichswahl einbezogen. Der Standard bleibt „Eigene ungespielte Spiele“.

### US-14 · Steam-Anmeldung und Datenimport · Must

Als Steam-Spieler:in möchte ich mich über Steam anmelden und meine Daten importieren, damit mein Profil zuverlässig meiner Identität zugeordnet ist.

- Die Anwendung leitet zur Steam-Anmeldung weiter. Nur eine auf dem Backend erfolgreich verifizierte OpenID-Antwort darf eine Sitzung für die zurückgemeldete SteamID erstellen; eine frei eingegebene SteamID oder URL genügt nicht.
- Ein ungültiger, manipulierter oder abgebrochener Anmeldevorgang erstellt keine angemeldete Sitzung und keinen fremden Datenimport. QuestQueue fragt kein Steam-Passwort ab.
- Ein Datenhinweis erklärt vor dem Erstimport Datenarten, Verarbeitung im lokalen Backend, Zweck und Löschung. Eine Anmeldung allein gilt nicht als Zustimmung zu laufenden Hintergrundabfragen.
- Der Import gehört zur angemeldeten Identität, dedupliziert Spiele nach AppID und speichert bekannte Gesamtspielzeit sowie verfügbare aktuelle Minuten und letzte Spielzeitpunkte. Fehlende Werte bleiben unbekannt.
- Erfolgreiche Datenstände und spätere Nutzereingaben bleiben in PostgreSQL nach Neustart erhalten. Abmelden beendet die eigene Sitzung, löscht aber keine gespeicherten Profildaten. Erneutes Anmelden desselben Kontos zeigt dessen Bestand wieder.
- Ein anderes Steam-Konto erhält einen getrennten Datenbestand. Demo-Daten sind separat und überschreiben keine Kontodaten.
- Der erste Spike prüft Steam-Anmeldung mit lokalem Callback und Live-Datenimport getrennt. Die konkrete OpenID-Bibliothek und Sitzungsumsetzung werden erst nach dem Integrationsnachweis gewählt.

### US-15 · Fehler und Datenlücken verstehen · Must

Als Nutzer:in möchte ich klare Fehler- und Leerzustände erhalten, damit ich die Zuverlässigkeit der Vorschläge beurteilen kann.

- Testantworten für Timeout, HTTP 429 und unlesbare Antworten führen zu verständlichen Hinweisen und manuell auslösbarer Wiederholung.
- Ein fehlgeschlagener Bibliotheksimport ersetzt keinen vorherigen erfolgreichen Datenstand. Dieser bleibt sichtbar als letzter erfolgreicher Stand.
- Mehrdeutige leere Antworten heißen „Keine zugänglichen Spieldaten“ mit möglichen Ursachen; die Anwendung behauptet nicht sicher, das Profil sei privat.
- Fehlende Genres, Spielzeiten oder Zeitpunkte werden nicht erfunden. Ohne Profil oder Kandidaten werden keine persönlichen Empfehlungen behauptet.
- Ein Fehler nur beim aktuellen Aktivitätsabruf darf vorhandene Gesamtspielzeit nicht als aktuelle Aktivität ausgeben.

### US-16 · Lokale Profildaten löschen · Must

Als Nutzer:in möchte ich meine gespeicherten Daten löschen, damit ich die Speicherung selbst kontrollieren kann.

- Nach Bestätigung werden die gespeicherte SteamID-Zuordnung, Bibliothek, aktuelle Daten, abgeleitete Profile und Auswahlzustände des angemeldeten Kontos gelöscht; fremde Konten bleiben unverändert. Die zugehörigen Sitzungen werden beendet.
- Sobald Erweiterungen implementiert sind, umfasst derselbe Vorgang auch alle Snapshots, Tags, Bewertungen und Filtereinstellungen.
- Die Löschung benötigt keine Verbindung zu Steam oder dem Metadatenanbieter, aber Zugriff auf das lokale Backend und PostgreSQL. Nach Neustart bleibt der gelöschte Zustand bestehen; es gibt keinen automatischen Neuimport. Die Identität wird dabei über die vorhandene verifizierte Sitzung geprüft.
- Der Anwendungsschlüssel und der allgemeine Metadatenkatalog sind keine persönlichen Profildaten und bleiben getrennt konfiguriert.

### US-17 · Reproduzierbar demonstrieren · Must

Als präsentierende Person möchte ich einen gekennzeichneten Beispieldatensatz laden, damit ich den Kernablauf unabhängig von Steam zeigen kann.

- Der Datensatz enthält mindestens drei gespielte und sechs ungespielte Titel, unterschiedliche aktuelle und langfristige Schwerpunkte, letzte Spielzeitpunkte, einen unbekannten Spielzeitwert und einen Titel ohne Metadaten.
- Profilaufbau, Listen, beide Geschmacksprofile, Empfehlungen und der Button funktionieren ohne Netzwerkanfrage; „Demodaten“ bleibt sichtbar.
- Demo und Live werden nicht vermischt. Eine separate Demo-Identität darf weder persönliche Daten lesen noch Live-Imports auslösen und benötigt keinen Steam-Login. Für implementierte Erweiterungen werden passende Zusatzfälle bereitgestellt, etwa Snapshots oder alte Lieblingsspiele.
- Der Demomodus ersetzt nicht den gesonderten Nachweis eines funktionierenden Live-Imports.

### US-18 · Automatisch aktualisieren · Could

Als Nutzer:in möchte ich bei laufender Anwendung optional regelmäßig aktualisieren, damit eine dichtere Beobachtungshistorie ohne jeden manuellen Import entsteht.

- Voraussetzung ist US-08. Die Automatik ist standardmäßig ausgeschaltet, wird bewusst aktiviert und ist jederzeit deaktivierbar.
- Das Intervall ist noch offen und wird vor Umsetzung mit Rate-Limits und gewünschter Messauflösung abgestimmt. Automatische lokale Aktualisierung ist nur möglich, solange Backend und gegebenenfalls Scheduler laufen; ein geschlossener Browser allein muss sie nicht stoppen. Bei ausgeschaltetem Rechner entstehen keine Beobachtungen.
- Fehler erzeugen keine Messpunkte und keine unbegrenzten Wiederholungen. Datenlöschung deaktiviert kontobezogene Jobs. Ob eine verifizierte Einwilligung zur Aktualisierung auch nach Abmeldung gelten soll, ist Teil der noch offenen Refresh-Entscheidung.

### US-19 · API-Metadaten mit Cache · Must

Als Nutzer:in möchte ich automatisch bezogene Spielmerkmale auch nach dem ersten Abruf schnell wieder nutzen können, damit Profile und Empfehlungen nicht von einem manuell gepflegten Minikatalog abhängen.

- Das Backend ordnet Steam-AppIDs bestätigten Einträgen des ausgewählten Metadatenanbieters zu und speichert normalisierte Merkmale, Provider-ID, Herkunft und Abrufzeitpunkt in PostgreSQL.
- Eine fehlende oder mehrdeutige Zuordnung wird angezeigt und nicht allein durch ähnliche Spielnamen als sicher erklärt. Das Spiel bleibt in der Bibliothek sichtbar.
- Bereits vorhandene, nach der noch zu vereinbarenden Cache-Regel gültige Metadaten werden wiederverwendet. Ein Test mit unverändertem gültigem Cache erzeugt keinen erneuten Anbieterabruf für dieselben Daten.
- Scheitert ein Abruf, bleiben frühere Daten erhalten. Ein vorhandener abgelaufener Stand darf nur mit sichtbarer Kennzeichnung verwendet werden; ohne Daten werden keine Merkmale erfunden.
- Der Cache enthält allgemeine Spielmetadaten, keine privaten Steam-Profilantworten. Kontolöschung entfernt persönliche Daten, ohne den allgemeinen Cache für andere Konten zu löschen.
- Nach Aufnahme dieser Funktion weist ein Live-Test den API-Abruf, die eindeutige AppID-Zuordnung und die Wiederverwendung nach Neustart nach. Ein kleiner Beispieldatensatz bleibt ausschließlich Test-/Demoquelle.
- Anbieter, erlaubte Speicherung, Cache-Gültigkeit und Refresh-Regeln werden im Spike geprüft beziehungsweise noch entschieden; IGDB ist ein Kandidat, keine bereits beschlossene Integration.

## 4. Funktionale Anforderungen und Nachverfolgbarkeit

| ID | Anforderung | Priorität | Story |
| --- | --- | --- | --- |
| F-01 | Letzte Aktivität mit ehrlicher Behandlung fehlender Zeitpunkte anzeigen | Must | US-01 |
| F-02 | Meistgespielte Titel und Bibliothek mit Minutenwerten anzeigen | Must | US-02 |
| F-03 | Präferenzprofil berechnen und Genregewichte transparent darstellen | Must | US-03 |
| F-04 | Dashboard mit Genre-Spielzeitanteilen und Zeitfenstern anzeigen | Should | US-04 |
| F-05 | Bis zu fünf eigene ungespielte Spiele mit Gründen empfehlen | Must | US-05 |
| F-06 | Getrennte Empfehlungen außerhalb der importierten Bibliothek | Should | US-06 |
| F-07 | Persistentes, reversibles Like/Dislike für externe Vorschläge | Should | US-07 |
| F-08 | Spielzeit-Snapshots und nachvollziehbare Intervallzuwächse speichern | Should | US-08 |
| F-09 | Current Taste und All-Time Taste getrennt berechnen und wechseln | Must | US-09 |
| F-10 | Frühere Favoriten mit belegter längerer Pause empfehlen | Should | US-10 |
| F-11 | Persönliche Tags speichern und im Ranking berücksichtigen | Should | US-11 |
| F-12 | Genres ausschließen und Filter auf Kandidaten anwenden | Should | US-12 |
| F-13 | Konkrete Auswahl über „What should I play?“ treffen | Must | US-13 |
| F-14 | Steam-Anmeldung verifizieren, Kontositzung führen und eigenen Import bereitstellen | Must | US-14 |
| F-15 | Fehlerbehandlung ohne Verlust gültiger Daten gewährleisten | Must | US-15 |
| F-16 | Alle persönlichen Profildaten lokal löschen können | Must | US-16 |
| F-17 | Getrennten offline nutzbaren Demomodus bereitstellen | Must | US-17 |
| F-18 | Optionale zeitgesteuerte Aktualisierung bei laufendem Backend | Could | US-18 |
| F-19 | Externe Metadaten eindeutig zuordnen und in PostgreSQL wiederverwenden | Must | US-19 |

## 5. Empfehlungsmethode: offene Entscheidung

Der Nutzer hat die Empfehlungsmethode ausdrücklich noch nicht ausgewählt. Die früher vorgeschriebene Quadratwurzel-Gewichtung, genaue Scoreformel und festen Like-/Loved-It-Faktoren gelten deshalb nicht als freigegebene Anforderungen.

| Option | Vorteile | Nachteile / Voraussetzung |
| --- | --- | --- |
| Inhaltsbasiertes Ranking aus Genres, Themen und weiteren verlässlichen Merkmalen | Verständliche Gründe; funktioniert ohne große Nutzerbasis; explizite Tags leicht einbeziehbar | Qualität hängt von Metadaten und einer sinnvollen Gewichtung ab; feine Ähnlichkeit kann fehlen |
| Embeddings aus Spielmerkmalen und Beschreibungen | Kann semantische Nähe über identische Genres hinaus abbilden | Zusätzliche Vorberechnung, Modellwahl und Evaluation; Gründe müssen weiter aus belegten Daten kommen |
| Kollaborative Empfehlungen | Kann Muster ähnlicher Spieler:innen nutzen | Benötigt eine geeignete Mehrnutzer-Datengrundlage; nicht allein aus einem neuen Konto ableitbar |
| LLM als primäre Empfehlungsquelle | Flexible sprachliche Begründungen | Zusätzliche Kosten-/Betriebsfragen und schwerere Reproduzierbarkeit; Fakten und Kandidaten müssen geprüft werden |

**Vorschlag zur Diskussion:** Mit einer erklärbaren inhaltsbasierten Baseline beginnen und später Embeddings auf demselben festen Testbestand vergleichen. Ein trainiertes Mehrnutzer-Modell oder laufende LLM-Aufrufe sind keine beschlossene Voraussetzung.

Unabhängig von der späteren Auswahl gelten folgende Produktverträge:

1. Current Taste und All-Time Taste bleiben getrennt. Gesamtspielzeit darf fehlende aktuelle Daten nicht stillschweigend ersetzen.
2. Der Algorithmus verwendet nur tatsächlich vorhandene Merkmale und zulässige Kandidaten. Bibliotheks-, Entdeckungs- und Wiederentdeckungsbereich bleiben getrennt.
3. Gleiche Eingaben, Metadaten und Modell-/Regelversionen ergeben dieselbe Rangfolge. Score-Skala, Schwelle und Gleichstandsregeln werden bei der Methodenwahl festgelegt; ein optionaler LLM darf diesen Vertrag nicht unbemerkt aufheben.
4. Jede Empfehlung hat eine belegbare Begründung mit Profilbezug. Tags, negatives Feedback und aktive Filter dürfen nicht durch eine positive Gewichtung übergangen werden.
5. „What should I play?“ verwendet dieselbe Rangfolge wie die zugehörige Liste.
6. Profilzusammenfassung und tatsächlich gemessene Spielminuten werden unterschieden. Es wird keine Zufriedenheit aus Minuten behauptet.

**Entscheidungsnachweis vor Implementierung:** Eingangsmerkmale, Gewichtung aktueller/gesamter Minuten, persönliche Signale, Scoreberechnung, Gleichstände und Erklärungsmethode werden dokumentiert. Ein fester Beispieldatensatz erhält erwartete Profile, Reihenfolgen und Grenzfälle. Für die Auswahl wird außerdem ein kleiner qualitativer Vergleich der Relevanz und Erklärungen geplant. Diese Evaluation ist noch nicht durchgeführt.

Bis zur Auswahl bleibt dieser Teil der Phase-1-Spezifikation ausdrücklich offen. Die technologischen Nutzerentscheidungen werden dadurch nicht infrage gestellt.

## 6. Regeln für Tags, Feedback und Filter

Diese Regeln gelten erst mit der jeweiligen Should-Funktion, sind aber jetzt festgelegt, damit spätere Erweiterungen nicht widersprüchlich werden.

| Angabe | Als Empfehlung zulässig? | Als positive Profilreferenz zulässig? |
| --- | --- | --- |
| Finished | Nein, auch nicht in Wiederentdecken | Ja, wenn positive Minuten und Genres vorhanden |
| Dropped | Nein | Nein |
| Loved It | Ja, wenn der jeweilige Kandidatenbereich passt | Explizites positives Signal; genaue Verrechnung noch offen |
| Not Interested | Nein, in allen Bereichen | Nein |
| Externes Dislike | Nein, im externen Bereich | Keine Änderung am Profil |
| Externes Like | Bevorzugung im externen Bereich; genaue Verrechnung noch offen | Keine beschlossene genreweite Profiländerung |
| Ausgeschlossenes Genre | Nein, wenn mindestens ein Kandidatengenre ausgeschlossen ist | Keine Änderung am Profil |

Ausschlüsse haben stets Vorrang vor Verstärkung. Beispielsweise wird ein Spiel mit Loved It und Not Interested weder vorgeschlagen noch als Referenz verwendet. Finished und Dropped können nicht gleichzeitig gesetzt sein. Loved It darf mit Finished kombiniert werden: Das Spiel wird dann nicht empfohlen, kann aber weiterhin die Vorlieben verstärken.

Genres und persönliche Tags sind getrennte Datenarten. Tags werden nicht aus Spielzeit erraten. Explizite Präferenzen sind wichtiger als die implizite Annahme „lange gespielt bedeutet gemocht“.

## 7. Daten, externe Abhängigkeiten und Kosten

### Import und Datenqualität

Die offizielle Steam-Dokumentation beschreibt Methoden für Bibliotheksdaten und zuletzt gespielte Titel; die Sichtbarkeit begrenzt den Bibliothekszugriff [S1]. Der öffentliche API-Host ist in [S3] beschrieben. Der frühe Spike prüft die konkreten Rückgabefelder und Berechtigungen für Gesamtspielzeit, 14-Tage-Spielzeit und letzte Spielzeitpunkte. Letztere werden nicht allein aus dem Namen einer API-Methode als garantiert verfügbar angenommen.

Ein erfolgreicher Bibliotheksimport ersetzt den Bibliotheksstand vollständig und erhält bei gleicher SteamID vorhandene Nutzereingaben. Ist die aktuelle Aktivitätsquelle erfolgreich, werden deren nachgewiesene Daten demselben Import zugeordnet. Fällt nur diese Quelle aus und fehlen aktuelle Werte auch in der Bibliotheksantwort, bleibt der neue All-Time-Stand nutzbar; Current Taste wird als nicht verfügbar markiert. Alte aktuelle Minuten werden nicht mit neuem Importdatum versehen. Die vorige Bibliothek bleibt erhalten, wenn der Bibliotheksabruf selbst scheitert.

Negative Minuten, unplausible zukünftige letzte Spielzeitpunkte und ungültige AppIDs werden nicht für Profile oder Rangfolgen verwendet. Verworfene Datensätze und Datenlücken werden als Anzahl gemeldet. Leere, unlesbare oder mehrdeutige Bibliotheksantworten überschreiben keinen gültigen Bestand; nur eine im Adapter nachweisbar gültige leere Bibliothek darf einen leeren Stand ersetzen.

### API-Metadaten, Cache und Kandidatenbestand

API plus Cache ist vom Nutzer gewählt. Der konkrete Metadatenanbieter ist noch offen. IGDB bietet Spielmerkmale und externe Kennungen und ist ein Kandidat für den Machbarkeitstest [S5]. Vor Auswahl werden zuverlässige Steam-AppID-Zuordnung, relevante Genres/Themen, Nutzbarkeit der Speicherung, Zugang, Request-Limits und Kosten geprüft. Entwickler-Zugangsdaten bleiben im Backend; eine mögliche separate Anbieter-Authentifizierung ist nicht der Steam-Login der Nutzer:innen.

Allgemeine Metadaten werden mit Provider-ID, Steam-AppID, Herkunft, Schema-/Normalisierungsversion und Abrufzeitpunkt in PostgreSQL gespeichert. Cache-Gültigkeit und Ablaufstrategie sind noch zu entscheiden. Fehlende Einträge dürfen nachgeladen werden; ein ungültiger Cache oder Rate-Limit-Fehler löst keine unkontrollierte Wiederholung aus. Veraltete vorhandene Daten werden kenntlich gemacht. Nicht zuordenbare Titel bleiben in der Bibliothek sichtbar, können aber nicht mit erfundenen Merkmalen personalisiert werden.

Die frühere Grenze von 30 manuell kuratierten Spielen entfällt für das Live-Produkt. Ein fester kleiner Demo-/Testbestand bleibt für reproduzierbare Prüfungen erhalten. Der Live-Test benötigt mindestens zwei tatsächlich zugeordnete gespielte und zwei ungespielte Bibliothekstitel. Sichtbare Abdeckung bleibt erforderlich; vollständige Steam-Abdeckung wird nicht garantiert.

US-06 verwendet zusätzliche bestätigte API-/Cache-Einträge mit Steam-AppID außerhalb des importierten Bestands. Für den reproduzierbaren Test dieser Erweiterung enthält der feste Testbestand mindestens zehn zusätzliche externe Kandidaten; daraus folgt keine Mindestgröße oder Vollerfassung des Live-Katalogs.

Die Metadatenanreicherung kann schrittweise nach dem Steam-Import erfolgen. Fortschritt und fehlende Abdeckung werden angezeigt; ein einzelner Metadatenfehler verwirft weder den erfolgreichen Bibliotheksimport noch vorhandene Profildaten.

### Speicherung und Zeitbezug

Der MVP speichert die verifizierte SteamID als Kontozuordnung, Sitzungsinformationen, AppIDs, Namen, bekannte Minutenwerte, verfügbare letzte Spielzeitpunkte, Importstatus, Zeitstempel und Metadaten-/Regelversionen in PostgreSQL. Erweiterungen ergänzen Snapshots, persönliche Tags, Bewertungen und Filtereinstellungen. Ein erneuter Import entfernt Tags oder Feedback nicht stillschweigend, auch wenn ein Spiel zeitweise nicht mehr zurückgegeben wird.

Zeitpunkte werden intern in UTC gespeichert und bei Anzeige mit erkennbarer Zeitzone dargestellt. Die 90-Tage-Grenze verwendet volle 24-Stunden-Intervalle bis zum Importzeitpunkt. Playtime over Time erfasst nur beobachtete Änderungen seit Beginn der eigenen Aufzeichnung. Ohne Messpunkte wird keine frühere Historie rekonstruiert.

Der Verlauf liefert zusätzliche Belege für veränderte Interessen und kann spätere Profilverbesserungen ermöglichen. Eine zusätzliche zeitbasierte Rankingregel wird nicht ohne Methodenentscheidung zugesagt und ist getrennt gegen die dann gewählte Baseline zu bewerten.

### Aktualisierung: offene Entscheidung

Refresh-Auslöser und konkrete Intervalle sind noch nicht gewählt. Drei unterschiedliche Datenarten sind zu trennen: persönliche Steam-Bestände/Spielzeiten, allgemeine Metadaten und abgeleitete Empfehlungen. Ein Profilwechsel, Tag oder Filter benötigt keine neue Steam-Abfrage, wenn die benötigten Daten bereits vorliegen.

| Option für persönliche Daten | Vorteil | Nachteil |
| --- | --- | --- |
| Nur manuell | Wenig API-Aufrufe, klar kontrollierbar | Lückenhafter Verlauf bei seltener Nutzung |
| Bei Anmeldung, nur wenn Daten zu alt sind | Frischer Stand beim Einstieg, weniger manuelle Schritte | Benötigt ein vereinbartes Mindestalter; keine Beobachtung zwischen Besuchen |
| Zusätzlich periodisch bei laufendem Backend | Regelmäßigere Snapshots | Scheduler, Einwilligung und Limits beachten; keine Erfassung bei ausgeschaltetem Rechner |

**Vorschlag, nicht beschlossen:** Manuellen Refresh bereitstellen und bei Anmeldung nur einen nach vereinbartem Alter veralteten persönlichen Datenstand aktualisieren. Eine tägliche automatische Aufzeichnung wäre später eine Option für US-18. Es sind noch keine 24-Stunden-Grenze, Abfragehäufigkeit oder Cache-TTL verbindlich festgelegt.

Ein manueller Grundablauf bleibt prüfbar. Automatische Refresh-Auslöser benötigen dieselbe verifizierte Kontozuordnung, Fehlerbehandlung und transparente Datenverarbeitung. Allgemeine Metadaten dürfen eine andere Gültigkeitsdauer als persönliche Spielzeiten haben. Abgeleitete Profile werden aus dem vorhandenen Datenstand neu berechnet.

Vor Umsetzung festzulegen: Auslöser, Mindestabstand/Cooldown, Behandlung abgelaufener Daten, beobachtete Zeitauflösung, Einwilligung bei Abmeldung und Cache-Gültigkeit. Lokale Automatik kann ohne laufenden Backend-/Schedulerprozess keine Daten sammeln. FastAPI-Aufgaben nach einer HTTP-Antwort sind nicht allein eine Festlegung eines periodischen Schedulers [S6].

### Zugriff, Betrieb und Kosten

Steam Sign-In verwendet Steam OpenID [S4]. Steam- und Metadaten-Zugangsdaten bleiben im FastAPI-Backend; Nutzer:innen sollen weder ihr Steam-Passwort in QuestQueue noch einen eigenen API-Schlüssel eingeben. Laut API-Bedingungen ist die Nutzung kostenlos, hat eine Aufrufgrenze und kann sich ändern [S2]. Bis zur Entscheidung über automatische Auslöser ist ein bewusst gestarteter Import die überprüfbare Grundfunktion. Steam-Anmeldung ist keine pauschale Zustimmung zu fortlaufender Erfassung.

Kostenpflichtiges Hosting und kostenpflichtige AI-Aufrufe sind nicht vorgesehen; bestehender Entwicklungsrechner und Internetzugang werden vorausgesetzt. Öffentlicher Betrieb und zusätzlich entstehende Anbietergebühren erfordern eine eigene Betriebs- und Kostenentscheidung. Die gewählte Authentifizierung wird bereits lokal umgesetzt; sie ist nicht bis zur Veröffentlichung aufgeschoben.

## 8. Nichtfunktionale Anforderungen

| ID | Überprüfbare Anforderung | Nachweis |
| --- | --- | --- |
| N-01 | Profilberechnung und Ranking benötigen für 1.000 Bibliotheksspiele und bis zu 1.000 Katalogeinträge auf dem dokumentierten Entwicklungsrechner in 20 aufeinanderfolgenden Läufen jeweils höchstens 2 Sekunden. | Zeitmessung für beide Profiltypen nach Laden der Daten; keine externen API-Zeiten einrechnen. |
| N-02 | Ein Steam-Datenimport endet innerhalb von 30 Sekunden mit Erfolg, nutzbarem Teilergebnis nach Abschnitt 7 oder erklärtem Abbruch. Separate Metadatenanreicherung zeigt Fortschritt; einzelne Anbieteranfragen enden nach spätestens 30 Sekunden mit Erfolg oder Fehler. | Simulation wartender Quellen sowie 429-/Fehlerantworten; kein unbegrenzter Retry. |
| N-03 | Der API-Schlüssel erscheint weder im Browser noch im Repository oder in Logs; externe API-Anfragen verwenden HTTPS. | Konfigurations-, Netzwerk- und Logprüfung mit Testschlüssel. |
| N-04 | Personenbezogene Daten bleiben im lokalen aktiven Datenspeicher; keine Telemetrie. Logs enthalten keine SteamID oder rohen Antworten. US-16 entfernt sämtliche aktiven Profildaten einschließlich späterer Verlaufs- und Feedbackdaten. | Speicherprüfung vor/nach Löschung und Neustart; keine durch den MVP erstellten externen Backups. |
| N-05 | Der vollständige Kernablauf ist per Tastatur nutzbar; alle Bedienelemente besitzen verständliche Namen und sichtbaren Fokus. Fehler und Status sind auch textlich erkennbar. | Manueller Ablauf ohne Maus; Profilwahl und Button einschließen. |
| N-06 | Profile, Ranking, Gleichstände und Fehlerbehandlung sind ohne Live-Zugriff überprüfbar; Datenadapter und Profil-/Empfehlungslogik sind getrennt austauschbar. | Nach Methodenwahl Tests mit festen erwarteten Ergebnissen und simulierten Importantworten. |
| N-07 | Persönliche Bibliothek, Profile, Tags, Feedback und Snapshots sind nur mit einer verifizierten Sitzung des zugehörigen Kontos zugänglich. Abmelden beendet den Zugriff; eine fremde SteamID im Request reicht nicht. | Tests mit zwei getrennten Konten/Sitzungen, manipulierten Kontoparametern und abgemeldeter Sitzung; allgemeiner Metadaten-Cache enthält keine persönlichen Daten. |

## 9. Widerspruchs-, Lücken- und Abhängigkeitsprüfung

| Thema | Risiko oder Unklarheit | Entscheidung im Entwurf |
| --- | --- | --- |
| Featureliste gegenüber erstem Entwurf | Wesentliche Produktfunktionen fehlten oder waren als beiläufige Ideen behandelt. | Alle 13 Features explizit zuordnen; beide Taste-Profile sind Must. |
| „Bereits in Bibliothek“ gegenüber „ungespielt“ | Eigene Empfehlungen können auch bekannte Spiele meinen. | MVP für ungespielte Titel; gespielte Titel separat über Wiederentdecken. |
| Last played gegenüber recently played | Aktuelle Minuten belegen keine genaue Chronologie. | Zeitpunkte prüfen; fallback klar als ungeordnete jüngste Aktivität benennen. |
| Current Taste gegenüber eigener Historie | Ein aktuelles Profil müsste sonst wochenlang auf neue Messpunkte warten. | 14-Tage-Signal für MVP; eigene Snapshots als Should ab Erfassungsbeginn. |
| Präferenzprofil gegenüber Dashboard | Genregewichte und tatsächliche Minuten sind verschiedene Größen. | Einfache Profilübersicht Must; grafisches Dashboard Should, Metriken getrennt. |
| Gesamtspielzeit gegenüber „enjoyed“ | Lange Spielzeit beweist keine positive Einstellung. | Persönliches Loved It als explizites Signal; sonst Näherung kenntlich machen. |
| Tags, Likes und Filter | Verstärkungen könnten Ausschlüsse übergehen. | Vorrang für Ausschlüsse; Wirkung je Funktion ausdrücklich definiert. |
| Externe Empfehlungen und Feedback | Feedback ohne externe Vorschläge hat keinen vollständigen Anwendungsfall. | US-07 abhängig von US-06; externe Kandidatenquelle vorab validieren. |
| Genres fehlen | Ohne Metadaten kann kein Genreprofil berechnet werden. | API plus Cache gewählt; Zuordnung und Abdeckung anzeigen; Demo-Daten nicht als Live-Katalog ausgeben. |
| Produktname „Queue“ | Eine eigene persistente Warteschlange war im ersten Entwurf erfunden. | Kein verbindliches Zusatzfeature; durch die wiedergefundene Liste ersetzt. |
| Umfang | Alle Funktionen gleichzeitig als Must würden das Semester gefährden. | Sieben Produkt-/Daten-Stories einschließlich API-Cache plus vier unterstützende Stories Must; Priorisierung bleibt Reviewvorschlag. |
| API-Ausfall | Demo könnte den Importerfolg nur vortäuschen. | Offline-Demo und erfolgreicher Live-Import getrennt nachweisen. |

### Vor Umsetzung zu validieren

- **Daten-Spike:** Erfolgreiche Bibliotheksabfrage, verfügbare aktuelle Minuten, Zeitpunkte und leere/private Antworten prüfen. Sind die für beide Profile nötigen Daten nicht zugänglich, muss der Scope ausdrücklich neu bewertet werden; ein Demoergebnis allein erfüllt das Live-Ziel nicht.
- **Metadaten:** Anbieterzugang, zulässige Speicherung, eindeutiges AppID-Mapping und Cache-Wiederverwendung mit tatsächlichen Bibliothekstiteln nachweisen. Anbieter noch nicht gewählt.
- **Nutzwert:** Drei freiwillige Personen sollen Kernablauf und Erklärungen ausprobieren. Es handelt sich um einen geplanten qualitativen Check, keine repräsentative oder schon durchgeführte Studie.
- **Anmeldung:** Lokalen Steam-Callback und sichere OpenID-Verifikation nachweisen. Anmeldewechsel darf keine Daten löschen oder vermischen; Abmeldung und Profil-Löschung getrennt prüfen.
- **Offene Methoden-/Refresh-Entscheidung:** Algorithmus, Gewichtungen, Datenalter, Trigger und Cache-TTL vor Umsetzung des jeweiligen Verhaltens festlegen.
- **Planung:** Teamgröße, Semestertermine und Zeitbudget sind noch nicht bekannt; Prioritäten und Etappen sind ein Reviewvorschlag.

## 10. Quellen

Offizielle Dokumentation am 05.11.2026 geprüft; kein authentifizierter Live-Test in Phase 1.

- [S1 – Valve: IPlayerService](https://partner.steamgames.com/doc/webapi/IPlayerService?language=english)
- [S2 – Valve: Steam Web API Terms of Use](https://steamcommunity.com/dev/apiterms)
- [S3 – Valve: Web API Overview](https://partner.steamgames.com/doc/webapi_overview?language=english)
- [S4 – Valve: Steam OpenID Provider](https://steamcommunity.com/dev)
- [S5 – IGDB: API-Dokumentation](https://api-docs.igdb.com/)
- [S6 – FastAPI: Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)

Die Quellen begründen die externe Abhängigkeit. Produktprioritäten, Zeitgrenzen, Kataloggröße, Formeln und Akzeptanzkriterien sind Entwurfsentscheidungen, keine Vorgaben von Valve.
