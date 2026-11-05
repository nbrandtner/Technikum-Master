# QuestQueue – Anforderungen

Stand: 05.11.2026 · Version 1.0 · Phase 1 – Project Definition & Requirements

## 1. Grundlage und Begriffe

Diese Spezifikation beschreibt die funktionalen und qualitativen Anforderungen an QuestQueue. Die Produktvision umfasst Spielübersichten, Präferenzprofile, Empfehlungen innerhalb und außerhalb der Bibliothek, Feedback, Spielzeitverlauf, Wiederentdeckung, persönliche Tags, Ausschlussfilter und einen „What should I play?“-Button. Die Funktionsübersicht im [README](../README.md) ordnet die 13 Produktfunktionen ihren Stories zu.

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

### Technischer und organisatorischer Rahmen

QuestQueue wird als lokale Webanwendung mit Python/FastAPI, Vue/TypeScript und PostgreSQL umgesetzt. Steam OpenID bestätigt die Identität; die Steam Web API liefert zugängliche persönliche Spieldaten. IGDB liefert allgemeine Metadaten, die in PostgreSQL gecacht werden. Die Anmeldung gewährt keinen zusätzlichen Zugriff auf private Spieldaten. QuestQueue erhebt keine Steam-Passwörter.

Persönliche Daten sind an die verifizierte SteamID gebunden und von allgemeinen Metadaten getrennt. Kontowechsel darf keine Daten anderer Konten offenlegen oder löschen. Öffentlicher Hostingbetrieb und Lastziele für größere Nutzerzahlen liegen außerhalb des MVP.

| Bereich | Festlegung |
| --- | --- |
| Empfehlung | Genrebasierte inhaltsbasierte Baseline v1 gemäß Abschnitt 5 |
| Aktualisierung | Manueller Import und anmeldebezogene Aktualisierung gemäß Abschnitt 7 |
| Metadaten | IGDB mit PostgreSQL-Cache; SteamSpy als mögliche Alternative bei unzureichender Abdeckung |
| MVP | Elf Must-Stories und N-01 bis N-07 |
| Erweiterungen | Sieben Should-Stories und eine Could-Story |
| Team und Zeitraum | Zwei Personen, Wintersemester 2026/27; Phasenplan in [mvp.md, Abschnitt 6](mvp.md#6-umsetzungsetappen) |
| Betrieb und Kosten | Lokaler Betrieb; 0 Euro Budget für zusätzliche laufende Dienste |

Für Live-Import und Integrationsnachweise werden Internetzugang, Entwicklerzugänge sowie ein Steam-Konto mit zugänglichen Spieldaten benötigt. Die externe Integration wird in Phase 2 anhand des Prüfplans in Abschnitt 7 validiert. Änderungen an Datenregeln oder MVP-Umfang werden begründet und in Anforderungen sowie Akzeptanzbeispielen konsistent nachgeführt.

## 2. Prioritäten und Abdeckung

**Must:** unverzichtbar für den ersten vollständigen Anwendungsfall oder dessen verlässlichen Betrieb. **Should:** Bestandteil der Produktvision und nächste Ausbaustufe, aber nicht für die MVP-Abnahme erforderlich. **Could:** optionale Komfortfunktion. Should- und Could-Funktionen gehören nicht zur MVP-Abnahme.

Die 19 User Stories umfassen elf Must-, sieben Should- und eine Could-Story. Sieben Must-Stories beschreiben Produkt- und Datenfunktionen einschließlich API-Metadaten; vier sichern Anmeldung/Import, Fehlerbehandlung, Datenkontrolle und Demonstration. Alle sieben nichtfunktionalen Anforderungen gelten im MVP.

Die Zuordnung der 13 Produktfunktionen steht im [README](../README.md). Der MVP und die Erweiterungsreihenfolge stehen in [mvp.md](mvp.md).

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

- Nach erfolgreichem Import und verfügbarer Metadatenanreicherung werden die verfügbaren Profile nach der genre- und minutenbasierten Baseline v1 aus Abschnitt 5 berechnet. Die Regelversion wird gespeichert.
- Eine einfache Profilübersicht zeigt Profilname, Zeitfenster, berücksichtigte Spiele, Datenstand und eine verständliche Genre-Zusammenfassung mit Prozentwerten. Die Prozentwerte entsprechen den normalisierten Genregewichten aus Abschnitt 5.
- Die Gewichte über alle berücksichtigten Genres summieren sich vor Anzeigerundung zu 100 Prozent. Fehlende Metadaten werden nicht erfunden.
- Die Abdeckung wird als „X von Y importierten Spielen mit Genre-Metadaten“ sowie die Zahl tatsächlich verwendeter Referenzspiele angezeigt.
- Ohne passende positive Spielzeitwerte wird kein Profil erfunden. Die Oberfläche erklärt die fehlende Grundlage.

### US-04 · Analyse-Dashboard · Should

Als Nutzer:in möchte ich meine meistgespielten Genres und Spielschwerpunkte in einem Dashboard sehen, damit ich mein Verhalten leichter verstehe.

- Das Dashboard zeigt mindestens Genreanteile nach Spielminuten, die meistgespielten Titel und das ausgewählte Zeitfenster.
- Bei Spielen mit mehreren Genres werden Minuten gleichmäßig auf die Genres verteilt, damit die Summe nicht mehrfach gezählt wird. Die Grafik benennt die berücksichtigte Teilmenge.
- Tatsächliche Spielminuten und aus US-03 abgeleitete Präferenzwerte werden unterschiedlich beschriftet; Präferenzwerte folgen Baseline v1, tatsächliche Minuten bleiben getrennt ausgewiesen.
- Der Wechsel zwischen Current Taste und All-Time Taste aktualisiert alle betroffenen Kennzahlen. Unbekannte Daten bleiben erkennbar.

### US-05 · Empfehlungen aus der Bibliothek · Must

Als Nutzer:in möchte ich zu meinem Präferenzprofil passende eigene Spiele entdecken, damit ich meine vorhandene Bibliothek besser nutze.

- Die erste Empfehlungsart berücksichtigt ausschließlich importierte ungespielte Spiele mit Genre-Metadaten und positivem Score nach Abschnitt 5.
- Die Ergebnisliste enthält höchstens fünf unterschiedliche Spiele, absteigend nach Score; Gleichstände löst die AppID aufsteigend auf.
- Jeder Vorschlag nennt das verwendete Profil, mindestens ein gemeinsames Genre und ein gespieltes Referenzspiel. Die Begründung verwendet ausschließlich die tatsächlich berücksichtigten Metadaten und Spielzeiten.
- Bei unveränderten Daten, Profilen und Regeln bleibt die Reihenfolge identisch. Es werden keine unpassenden Platzhalter zum Auffüllen ausgegeben.
- Bei fehlendem Profil oder fehlenden Kandidaten erscheint ein verständlicher Leerzustand. Die Bibliothek bleibt zugänglich.

### US-06 · Empfehlungen außerhalb der Bibliothek · Should

Als Nutzer:in möchte ich passende neue Spiele außerhalb meiner Bibliothek entdecken, damit ich zusätzliche Spielmöglichkeiten finde.

- Ein getrennter Bereich verwendet denselben gewählten Profiltyp, aber Kandidaten aus einem bestätigten Metadatenkatalog, deren AppIDs nicht in der importierten Bibliothek stehen.
- Ergebnisse werden als „Nicht in deiner importierten Bibliothek“ gekennzeichnet; der Importzeitpunkt und mögliche Unvollständigkeit bleiben sichtbar.
- Höchstens fünf Ergebnisse werden mit Profilbezug und Begründung angezeigt. Importierte AppIDs dürfen nicht erscheinen.
- Ohne geeignete zusätzliche Katalogeinträge erscheint ein erklärter Leerzustand; die Ansicht benennt den verwendeten Kandidatenbestand.
- Preise, Verfügbarkeit und sichere Nichtbesitzaussagen werden ohne entsprechende geprüfte Datenquelle nicht behauptet.

### US-07 · Like/Dislike für externe Empfehlungen · Should

Als Nutzer:in möchte ich Empfehlungen außerhalb meiner Bibliothek liken oder disliken, damit ich deren Auswahl beeinflussen kann.

- Pro AppID ist genau eine Bewertung aus Like, Dislike oder neutral gespeichert; sie lässt sich ändern und zurücksetzen.
- Dislike entfernt den Titel aus zukünftigen externen Vorschlägen. Like bevorzugt bei exakt gleichem ungerundetem Score einen Titel vor neutral bewerteten Titeln; anschließend entscheidet die AppID aufsteigend. Like verändert den Score nicht und macht keinen 0-Score-Kandidaten zulässig.
- Feedback bleibt nach Neustart erhalten und ist in einer Übersicht reversibel. Es wird nach einem Neuimport nicht automatisch gelöscht, nur weil die AppID nun in der Bibliothek erscheint.
- Feedback beeinflusst nur den externen Empfehlungsbereich; seine Wirkung wird in der Oberfläche erklärt. Die Genregewichte des Präferenzprofils bleiben unverändert.
- Bei aktiven Tags oder Filtern haben deren Ausschlüsse Vorrang vor Like.

### US-08 · Playtime over Time · Should

Als Nutzer:in möchte ich die Entwicklung meiner Spielzeit verfolgen, damit ich Veränderungen meiner Spielschwerpunkte erkennen kann.

- Jeder erfolgreich ausgeführte Import speichert nach Einführung dieser Funktion einen Snapshot mit Erfassungszeitpunkt, AppID und bekannter kumulierter Spielzeit, unabhängig davon, ob er manuell oder bei Anmeldung ausgelöst wurde. Fehlgeschlagene Imports erzeugen keinen Messpunkt.
- Nach mindestens zwei Messpunkten wird pro Spiel die Differenz zweier aufeinanderfolgender bekannter Stände mit dem tatsächlichen Intervall angezeigt. 120 auf 180 Minuten ergibt 60 beobachtete zusätzliche Minuten.
- Beim ersten Messpunkt gibt es nur eine Basislinie. Fehlende Werte, neu auftauchende Titel oder sinkende Zähler erzeugen keine erfundene oder negative Nutzungsdauer; ein sinkender Stand beginnt ein markiertes neues Vergleichssegment.
- Beobachtungsdaten beginnen mit QuestQueue. Lange Intervalle werden nicht gleichmäßig auf Tage verteilt und nicht als einzelne Sitzungen interpretiert.
- Die Verlaufsansicht zeigt beobachtete Spielzeitzuwächse und Erfassungsabdeckung. Current Taste verwendet weiterhin die verfügbaren 14-Tage-Minuten aus Steam; eigene Verlaufsdaten verändern Baseline v1 nicht.
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
- Finished, Dropped und Not Interested schließen einen Titel als Empfehlung aus. Loved It verdoppelt als explizites positives Signal den Minutenbeitrag des Referenzspiels vor der Genreaufteilung und Normalisierung gemäß Abschnitt 5.
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
- Ein Datenhinweis erklärt vor dem Erstimport Datenarten, lokale Speicherung einschließlich Speicherland, Zweck, anlassbezogene Aktualisierung und Löschung. Erst nach Bestätigung wird importiert. Eine Anmeldung allein gilt nicht als Zustimmung zu laufenden Hintergrundabfragen.
- Der Import gehört zur angemeldeten Identität, dedupliziert Spiele nach AppID und speichert bekannte Gesamtspielzeit sowie verfügbare aktuelle Minuten und letzte Spielzeitpunkte. Fehlende Werte bleiben unbekannt. Manuelle und anmeldebezogene Aktualisierung erfüllen die prüfbaren Auslöser-, Alters- und Sperrregeln in Abschnitt 7.
- Erfolgreiche Datenstände und spätere Nutzereingaben bleiben in PostgreSQL nach Neustart erhalten. Abmelden beendet die eigene Sitzung, löscht aber keine gespeicherten Profildaten. Erneutes Anmelden desselben Kontos zeigt dessen Bestand wieder.
- Ein anderes Steam-Konto erhält einen getrennten Datenbestand. Demo-Daten sind separat und überschreiben keine Kontodaten.
- Erfolgreiche Anmeldung und Datenzugriff werden getrennt geprüft: Bei verifizierter Identität, aber nicht zugänglichen Spieldaten bleibt die Sitzung gültig und die Oberfläche erklärt den fehlenden Datenzugriff.

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
- Das eingestellte Erfassungsintervall wird vor Aktivierung angezeigt und hält die Mindestabstände sowie Anbietersperren aus Abschnitt 7 ein. Automatische Aktualisierung setzt ein laufendes Backend mit Zeitsteuerung voraus; bei ausgeschaltetem Rechner entstehen keine Beobachtungen.
- Fehler erzeugen keine Messpunkte und keine unbegrenzten Wiederholungen. Abmeldung und Datenlöschung stoppen kontobezogene Jobs und verhindern das Speichern verspäteter persönlicher Importergebnisse.

### US-19 · API-Metadaten mit Cache · Must

Als Nutzer:in möchte ich automatisch bezogene Spielmerkmale auch nach dem ersten Abruf schnell wieder nutzen können, damit Profile und Empfehlungen auf verfügbaren und wiederverwendbaren Metadaten beruhen.

- Das Backend ordnet Steam-AppIDs bestätigten Einträgen des ausgewählten Metadatenanbieters zu und speichert normalisierte Merkmale, Provider-ID, Herkunft und Abrufzeitpunkt in PostgreSQL.
- Eine fehlende oder mehrdeutige Zuordnung wird angezeigt und nicht allein durch ähnliche Spielnamen als sicher erklärt. Das Spiel bleibt in der Bibliothek sichtbar.
- Bereits vorhandene, nach der 7-Tage-Regel aus Abschnitt 7 gültige Metadaten werden wiederverwendet. Ein Test mit unverändertem gültigem Cache erzeugt keinen erneuten Anbieterabruf für dieselben Daten.
- Scheitert ein Abruf, bleiben frühere Daten erhalten. Ein vorhandener abgelaufener Stand darf nur mit sichtbarer Kennzeichnung verwendet werden; ohne Daten werden keine Merkmale erfunden.
- Der Cache enthält allgemeine Spielmetadaten, keine privaten Steam-Profilantworten. Kontolöschung entfernt persönliche Daten, ohne den allgemeinen Cache für andere Konten zu löschen.
- Ein Live-Test weist den API-Abruf, die eindeutige AppID-Zuordnung und die Cache-Wiederverwendung nach Neustart nach. Test- und Demodaten sind vom Live-Bestand getrennt.
- IGDB dient als primärer Metadatenanbieter und erlaubt laut FAQ lokales Caching [S5]. Die Abnahme umfasst authentifizierten Zugriff, Steam-Zuordnung und Wiederverwendung gespeicherter Daten.

## 4. Funktionale Anforderungen und Nachverfolgbarkeit

| ID | Anforderung | Priorität | Story |
| --- | --- | --- | --- |
| F-01 | Letzte Aktivität anzeigen und fehlende Zeitpunkte kennzeichnen | Must | US-01 |
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

## 5. Empfehlungsmethode: inhaltsbasierte Baseline v1

Der MVP verwendet normalisierte Genres und bekannte Spielminuten. Diese einfache Baseline ist ohne Trainingsdaten, kostenpflichtige AI-Aufrufe oder zusätzliche Modelle implementierbar und erklärt ihre Ergebnisse über belegte gemeinsame Genres. Themen, Freitextähnlichkeit und weitere Merkmale gehören erst zu einer späteren Regelversion.

| Alternative | Bewertung und Entscheidung |
| --- | --- |
| Genrebasierte inhaltsbasierte Empfehlung | MVP-Baseline: geringer Integrationsaufwand und nachvollziehbare Gründe; grobe Genres und sehr lange Spielzeiten können die Auswahl verzerren |
| Embeddings aus Beschreibungen | Spätere Option für feinere semantische Ähnlichkeit; benötigt Modellwahl und Vergleich mit der Baseline |
| Kollaborative Empfehlungen | Außerhalb des MVP: geeignete Mehrnutzer-Datengrundlage fehlt |
| LLM als primäre Empfehlungsquelle | Außerhalb des MVP: zusätzliche Kosten, Faktenprüfung und erschwerte Reproduzierbarkeit |

### Profil und Score

1. Referenzen sind importierte Spiele mit positivem bekanntem Minutenwert im gewählten Zeitfenster und mindestens einem normalisierten Genre. All-Time verwendet Gesamtminuten, Current die verfügbaren 14-Tage-Minuten desselben Imports. Fehlende aktuelle Werte werden nicht aus Gesamtminuten abgeleitet. Genre-IDs werden pro Spiel dedupliziert.
2. Für ein Referenzspiel i werden seine Minuten m(i) gleichmäßig auf seine Genres G(i) verteilt. Der Genrebeitrag lautet m(i) / Anzahl(G(i)). Im MVP gibt es keinen weiteren Faktor. Nach Einführung von US-11 wird bei Loved It vor der Aufteilung mit 2 multipliziert; Dropped und Not Interested entfernen die Referenz vollständig.
3. Alle Beiträge eines Genres werden addiert. Das Profilgewicht p(g) ist diese Summe geteilt durch die Summe sämtlicher Genrebeiträge. Die Gewichte summieren sich zu 1. Ohne positive Gesamtsumme gibt es kein verwendbares Profil.
4. Kandidaten aus US-05 sind importierte Spiele mit explizit 0 Gesamtminuten und mindestens einem Genre. Ihr Score ist der Mittelwert der Profilgewichte ihrer Genres: Score(c) = Summe(p(g) für g in G(c)) / Anzahl(G(c)). Ein im Profil nicht vorkommendes Genre trägt 0 bei. Scorewerte liegen zwischen 0 und 1; nur Werte größer 0 sind zulässig.
5. Rangfolge: ungerundeter Score absteigend, dann numerische AppID aufsteigend. Anzeige höchstens fünf Titel; der Button liefert Rang 1. Rundung erfolgt nur in der Darstellung, nicht vor Sortierung oder Kandidatenprüfung. US-07 ergänzt ausschließlich bei externen Empfehlungen den Like-Gleichstandsvorrang vor der AppID.
6. Die Begründung nennt ein gemeinsames Genre mit dem größten positiven Profilgewicht; bei Gleichstand entscheidet dessen stabile Genre-ID aufsteigend. Dazu wird die verwendete Referenz mit dem größten Beitrag zu diesem Genre genannt; bei Gleichstand entscheidet die AppID. Aussagen über Freude oder einen Abschluss werden daraus nicht abgeleitet.
7. Datenstand, Profiltyp und Regelversion bleiben sichtbar. Listen und Button verwenden denselben Kandidatenbestand und dieselbe Rangfolge. Nach Import oder Profilwechsel wird aus vorhandenen Daten neu berechnet; eine Netzabfrage ist dafür nicht nötig.

Filter und persönliche Ausschlüsse werden nach Einführung der jeweiligen Should-Story vor der Rangbildung angewendet. Externe und Wiederentdeckungs-Kandidaten bleiben getrennte Bereiche mit denselben Profilgewichten und eigenen Zulassungsregeln.

### Festes Akzeptanzbeispiel

Der folgende synthetische Testbestand definiert die erwartete Profilberechnung und Rangfolge. Titel und AppIDs sind Testkennungen. Alle Werte beziehen sich auf denselben Import; 0 und unbekannt sind unterschiedliche Eingaben.

| AppID | Testtitel | Genres | Gesamtminuten | 14-Tage-Minuten |
| --- | --- | --- | --- | --- |
| 101 | RPG-Referenz | RPG | 600 | 0 |
| 102 | Strategie-Referenz | Strategie | 60 | 60 |
| 103 | Action-Referenz | Action | 60 | 0 |
| 201 | RPG-Kandidat | RPG | 0 | 0 |
| 202 | Strategie-Kandidat | Strategie | 0 | 0 |
| 203 | Action-Kandidat | Action | 0 | 0 |
| 204 | Gemischter Kandidat | RPG, Strategie | 0 | 0 |
| 205 | Puzzle-Kandidat | Puzzle | 0 | 0 |
| 206 | Ohne Metadaten | unbekannt | 0 | 0 |
| 207 | Unbekannte Spielzeit | RPG | unbekannt | unbekannt |

**Erwartung All-Time:** RPG 5/6, Strategie 1/12, Action 1/12; Reihenfolge 201 (5/6), 204 (11/24), 202 (1/12), 203 (1/12). 205 hat Score 0; 206 hat keine Genres; 207 ist nicht nachweisbar ungespielt. Keiner dieser drei Titel wird vorgeschlagen.

**Erwartung Current:** Strategie 100 Prozent; Reihenfolge 202 (1), 204 (1/2). Der Button wechselt damit von 201 auf 202. Bei 201 verweist die Begründung auf RPG und Referenz 101, bei 202 auf Strategie und Referenz 102.

**Grenzfälle:** Alle aktuellen Minuten explizit 0 → kein Current-Profil; aktuelle Quelle nicht zugänglich → Current-Daten nicht verfügbar; alle Kandidaten ohne Genres oder positiven Score → leere Empfehlung. Ein Referenzspiel mit zwei Genres verteilt seine Minuten je zur Hälfte, sodass die Gesamtminuten nicht doppelt gezählt werden. Änderungen an Gewichtung oder Score erfordern eine neue Regelversion mit angepassten Akzeptanzerwartungen.

## 6. Regeln für Tags, Feedback und Filter

Bei Umsetzung der jeweiligen Should-Funktion gelten die folgenden Regeln. Ausschlüsse werden vor der Rangbildung angewendet.

| Angabe | Als Empfehlung zulässig? | Als positive Profilreferenz zulässig? |
| --- | --- | --- |
| Finished | Nein, auch nicht in Wiederentdecken | Ja, wenn positive Minuten und Genres vorhanden |
| Dropped | Nein | Nein |
| Loved It | Ja, wenn der jeweilige Kandidatenbereich passt | Minutenbeitrag × 2 vor Genreaufteilung und Normalisierung |
| Not Interested | Nein, in allen Bereichen | Nein |
| Externes Dislike | Nein, im externen Bereich | Keine Änderung am Profil |
| Externes Like | Bei gleichem Score vor neutral, dann AppID; keine Scoreänderung | Keine Änderung am Genreprofil |
| Ausgeschlossenes Genre | Nein, wenn mindestens ein Kandidatengenre ausgeschlossen ist | Keine Änderung am Profil |

Ausschlüsse haben stets Vorrang vor Verstärkung. Beispielsweise wird ein Spiel mit Loved It und Not Interested weder vorgeschlagen noch als Referenz verwendet. Finished und Dropped können nicht gleichzeitig gesetzt sein. Loved It darf mit Finished kombiniert werden: Das Spiel wird dann nicht empfohlen, kann aber weiterhin die Vorlieben verstärken.

Genres und persönliche Tags sind getrennte Datenarten. Tags werden nicht aus Spielzeit erraten. Explizite Präferenzen sind wichtiger als die implizite Annahme „lange gespielt bedeutet gemocht“.

## 7. Daten, externe Abhängigkeiten und Kosten

### Import und Datenqualität

Die offizielle Steam-Dokumentation beschreibt Methoden für Bibliotheksdaten und zuletzt gespielte Titel; die Sichtbarkeit begrenzt den Bibliothekszugriff [S1]. Der öffentliche API-Host ist in [S3] beschrieben. Der frühe Spike prüft die konkreten Rückgabefelder und Berechtigungen für Gesamtspielzeit, 14-Tage-Spielzeit und letzte Spielzeitpunkte. Letztere werden nicht allein aus dem Namen einer API-Methode als garantiert verfügbar angenommen.

Ein erfolgreicher Bibliotheksimport ersetzt den Bibliotheksstand vollständig und erhält bei gleicher SteamID vorhandene Nutzereingaben. Ist die aktuelle Aktivitätsquelle erfolgreich, werden deren nachgewiesene Daten demselben Import zugeordnet. Fällt nur diese Quelle aus und fehlen aktuelle Werte auch in der Bibliotheksantwort, bleibt der neue All-Time-Stand nutzbar; Current Taste wird als nicht verfügbar markiert. Alte aktuelle Minuten werden nicht mit neuem Importdatum versehen. Die vorige Bibliothek bleibt erhalten, wenn der Bibliotheksabruf selbst scheitert.

Negative Minuten, aktuelle Minuten größer als eine bekannte Gesamtspielzeit, unplausible zukünftige letzte Spielzeitpunkte und ungültige AppIDs werden nicht für Profile oder Rangfolgen verwendet. Ein ungültiger aktueller Wert verwirft nicht automatisch einen gültigen Gesamtwert. Verworfene Datensätze und Datenlücken werden als Anzahl gemeldet. Leere, unlesbare oder mehrdeutige Bibliotheksantworten überschreiben keinen gültigen Bestand; nur eine im Adapter nachweisbar gültige leere Bibliothek darf einen leeren Stand ersetzen.

### API-Metadaten, Cache und Kandidatenbestand

Der gewählte Integrationsansatz verbindet Steam für persönliche Bibliotheks-/Aktivitätsdaten mit IGDB für allgemeine Spielmetadaten und einem PostgreSQL-Cache. IGDB dokumentiert Genres, externe Spielkennungen, kostenlosen nichtkommerziellen Zugang und erlaubtes lokales Caching [S5]. Der Zugriff erfolgt über Twitch-Anwendungszugangsdaten im Backend und ist vom Steam-Login der Nutzer:innen getrennt. Themen und Keywords sind spätere Erweiterungsoptionen.

Allgemeine Metadaten werden mit Provider-ID, Steam-AppID, Herkunft, Schema-/Normalisierungsversion und Abrufzeitpunkt in PostgreSQL gespeichert. Metadaten gelten ab erfolgreichem Abruf für weniger als sieben Tage als frisch; die Ablaufstrategie steht unten. Fehlende Einträge dürfen nachgeladen werden; ein ungültiger Cache oder Rate-Limit-Fehler löst keine unkontrollierte Wiederholung aus. Veraltete vorhandene Daten werden kenntlich gemacht. Nicht zuordenbare Titel bleiben in der Bibliothek sichtbar, können aber nicht mit erfundenen Merkmalen personalisiert werden.

Live-Metadaten werden über IGDB und den Cache bereitgestellt. Ein separater fester Demo-/Testbestand ermöglicht reproduzierbare Prüfungen. Der Live-Test benötigt mindestens zwei tatsächlich zugeordnete gespielte und zwei ungespielte Bibliothekstitel. Sichtbare Abdeckung bleibt erforderlich; vollständige Steam-Abdeckung wird nicht garantiert.

US-06 verwendet zusätzliche bestätigte API-/Cache-Einträge mit Steam-AppID außerhalb des importierten Bestands. Für den reproduzierbaren Test dieser Erweiterung enthält der feste Testbestand mindestens zehn zusätzliche externe Kandidaten; daraus folgt keine Mindestgröße oder Vollerfassung des Live-Katalogs.

Die Metadatenanreicherung kann schrittweise nach dem Steam-Import erfolgen. Fortschritt und fehlende Abdeckung werden angezeigt; ein einzelner Metadatenfehler verwirft weder den erfolgreichen Bibliotheksimport noch vorhandene Profildaten.

### API-Validierung in Phase 2

1. **Zugang:** Steam-Anmeldung und Bibliotheksimport sowie separat IGDB-Anwendungszugang einrichten. Entwicklergeheimnisse bleiben im Backend; Nutzer:innen benötigen keinen Twitch-Login.
2. **Stichprobe:** Etwa 50 tatsächliche Spiele aus einer zugänglichen Steam-Bibliothek prüfen, darunter gespielte und ungespielte Titel sowie ältere, kleinere und unterschiedlich benannte Editionen. Bei kleinerem Bestand alle geeigneten Spiele prüfen; Umfang und Auswahl dokumentieren.
3. **Zuordnung und Metadaten:** Über IGDB-External-Game-Einträge die Steam-AppID zur IGDB-ID auflösen, danach Genres abrufen. Das aktuelle Feld `external_game_source` verwenden; das alte `category`-Feld ist als veraltet dokumentiert [S5]. Eindeutige Zuordnungen, verfügbare Genres, Mehrdeutigkeiten und Lücken jeweils zählen; reine Namensähnlichkeit genügt nicht als sichere Zuordnung.
4. **Nachweis:** Mindestens zwei gespielte und zwei ungespielte Titel eindeutig zuordnen, beide Profile mit geeigneten Daten aufbauen und eine Live-Empfehlung erzeugen. Cache-Wiederverwendung nach Neustart, fehlende Zuordnung und 429-/Fehlerverhalten getrennt prüfen. Die Mindestzahl beweist den Ablauf, keine repräsentative Katalogabdeckung.
5. **Entscheidung:** Reichen Zuordnung und Genreabdeckung für den Kernfall, bleibt IGDB die einzige Metadatenquelle des MVP. Bei relevanten Lücken zuerst Ursache und betroffene Titel prüfen. SteamSpy als mögliche Ergänzung erst nach eigener Zugriffs-, Datenqualitäts- und Nutzungsprüfung aufnehmen; andernfalls Anbieter- oder Scope-Anpassung dokumentieren.

SteamSpy bietet AppID-basierte Abfragen, Genres und Community-Tags [S7]. Eine Nutzung als ergänzende Quelle erfordert die dokumentierte Prüfung von Zugang, Datenqualität und Nutzungsbedingungen. Herkunft und Genre-/Tag-Vokabulare bleiben getrennt; Anbieterwechsel und Normalisierungsregeln werden explizit versioniert.

### Speicherung und Zeitbezug

Der MVP speichert die verifizierte SteamID als Kontozuordnung, Sitzungsinformationen, AppIDs, Namen, bekannte Minutenwerte, verfügbare letzte Spielzeitpunkte, Importstatus, Zeitstempel und Metadaten-/Regelversionen in PostgreSQL. Erweiterungen ergänzen Snapshots, persönliche Tags, Bewertungen und Filtereinstellungen. Ein erneuter Import entfernt Tags oder Feedback nicht stillschweigend, auch wenn ein Spiel zeitweise nicht mehr zurückgegeben wird.

Zeitpunkte werden intern in UTC gespeichert und bei Anzeige mit erkennbarer Zeitzone dargestellt. Die 90-Tage-Grenze verwendet volle 24-Stunden-Intervalle bis zum Importzeitpunkt. Playtime over Time erfasst nur beobachtete Änderungen seit Beginn der eigenen Aufzeichnung. Ohne Messpunkte wird keine frühere Historie rekonstruiert.

Eigene Verlaufsdaten dienen der Darstellung beobachteter Änderungen. Ihr Einsatz als zusätzliches Rankinggewicht liegt außerhalb der Baseline v1.

### Aktualisierung und Cache: Baseline für den MVP

Drei Datenarten werden getrennt behandelt: persönliche Steam-Daten, allgemeine Metadaten und daraus berechnete Profile. Die folgenden Werte legen Datenalter, Auslöser und Abfragebegrenzung für den MVP fest.

| Auslöser / Zustand | Gefordertes Verhalten |
| --- | --- |
| Erstimport | Erst nach verifizierter Anmeldung und bestätigtem Datenhinweis; die Person startet den Import bewusst |
| Erneute Anmeldung nach bestätigtem Datenhinweis | Automatischer Import genau dann, wenn kein erfolgreicher Stand vorliegt oder der letzte erfolgreiche Bibliotheksimport mindestens 24 Stunden alt ist; ohne gültigen Datenhinweis weiterhin Erstimport-Ablauf |
| Manueller Refresh | Auch vor Ablauf von 24 Stunden möglich; mindestens 60 Sekunden Abstand zwischen Importstarts je Konto, höchstens ein laufender Import je Konto |
| Importfehler | Letzter erfolgreicher Zeitpunkt bleibt unverändert; kein automatischer Retry. Erneute manuelle Auslösung erst nach Cooldown und gegebenenfalls späterem Retry-After-Zeitpunkt |
| Metadaten unter 7 Tage alt | Vorhandene passende Cache-Einträge verwenden; keine erneute Anbieteranfrage |
| Fehlende oder mindestens 7 Tage alte Metadaten | Bei Importanreicherung nachladen; alte Werte bis zum Erfolg sichtbar als veraltet weiterverwenden. Ohne vorhandene Werte bleibt die Lücke sichtbar |
| Profilwahl, Button, Tag oder Filter | Aus vorhandenen Daten neu berechnen; kein Steam- oder Metadatenabruf allein wegen dieser Aktion |
| Abmeldung oder Löschung | Keine weiteren kontobezogenen Imports; laufende persönliche Importergebnisse dürfen danach nicht mehr gespeichert werden. Löschung beendet alle zugehörigen Sitzungen |

Grenztests: 23 Stunden 59 Minuten Datenalter → kein Anmeldeimport; genau 24 Stunden → Import. Bei 59 Sekunden seit dem letzten Start → gesperrt; bei 60 Sekunden und ohne laufenden Import → freigegeben. Cache-Alter knapp unter sieben Tagen → Treffer; genau sieben Tage → erneuern. Schema- oder Anbieterwechsel kann einen Eintrag unabhängig vom Alter ungültig machen.

Fehlende Metadaten werden in einem Durchlauf je AppID höchstens einmal angefragt, nicht bei jedem Seitenaufruf. Anbieteranfragen laufen begrenzt; für IGDB gilt eine anwendungsseitige Begrenzung auf höchstens eine Anfrage pro Sekunde und eine gleichzeitig laufende Anfrage. Batching ist erlaubt. Bei 429 pausiert die Anreicherung bis zu einem angegebenen Retry-After, mindestens aber 60 Sekunden, und benötigt danach einen erneuten manuellen Start. Bei anderen Fehlern endet der betroffene Abruf ohne Retry-Schleife. Strengere Anbieterbedingungen haben Vorrang und werden dokumentiert.

Nach bestätigtem Datenhinweis und fehlgeschlagenem Erstimport kann die nächste Anmeldung erneut versuchen zu importieren; Cooldown und Fehler-Sperre gelten weiterhin. Eine inaktive Sitzung oder ein laufender lokaler Server löst allein keine Abfragen aus. Periodische Erfassung gehört nur zu US-18 nach US-08. FastAPI-Aufgaben nach einer HTTP-Antwort sind für sich noch kein periodischer Scheduler [S6].

### Zugriff, Betrieb und Kosten

Steam Sign-In verwendet Steam OpenID [S4]. Steam- und Metadaten-Zugangsdaten bleiben im FastAPI-Backend; Nutzer:innen sollen weder ihr Steam-Passwort in QuestQueue noch einen eigenen API-Schlüssel eingeben. Laut API-Bedingungen ist die Nutzung kostenlos, hat eine Aufrufgrenze und kann sich ändern [S2]. Erstimport und anmeldebezogene Aktualisierung folgen dem bestätigten Datenhinweis und den oben festgelegten Auslösern. Steam-Anmeldung ist keine pauschale Zustimmung zu fortlaufender Erfassung.

Kostenpflichtiges Hosting und kostenpflichtige AI-Aufrufe sind nicht vorgesehen; bestehender Entwicklungsrechner und Internetzugang werden vorausgesetzt. IGDB beschreibt kostenlosen nichtkommerziellen Zugang mit Twitch-Entwicklerkonto, Client-ID und Backend-Token [S5]. Lokales Caching ist laut IGDB-FAQ erlaubt; der authentifizierte Zugriff ist im Spike nachzuweisen. Für zusätzliche laufende Dienste ist im MVP ein Budget von 0 Euro angesetzt; fallen Gebühren an oder ist Zugang nicht möglich, wird vor einer kostenpflichtigen Nutzung eine Alternative oder Scope-Anpassung dokumentiert. Öffentlicher Betrieb benötigt eine gesonderte Betriebs- und Kostenentscheidung. Steam-Authentifizierung ist Bestandteil des lokalen MVP.

## 8. Nichtfunktionale Anforderungen

| ID | Überprüfbare Anforderung | Nachweis |
| --- | --- | --- |
| N-01 | Profilberechnung und Ranking benötigen für 1.000 Bibliotheksspiele und bis zu 1.000 Katalogeinträge auf dem dokumentierten Entwicklungsrechner in 20 aufeinanderfolgenden Läufen jeweils höchstens 2 Sekunden. | Zeitmessung für beide Profiltypen nach Laden der Daten; keine externen API-Zeiten einrechnen. |
| N-02 | Ein Steam-Datenimport endet innerhalb von 30 Sekunden mit Erfolg, nutzbarem Teilergebnis nach Abschnitt 7 oder erklärtem Abbruch. Separate Metadatenanreicherung zeigt Fortschritt; einzelne Anbieteranfragen enden nach spätestens 30 Sekunden mit Erfolg oder Fehler. | Simulation wartender Quellen sowie 429-/Fehlerantworten; kein unbegrenzter Retry. |
| N-03 | Der API-Schlüssel erscheint weder im Browser noch im Repository oder in Logs; externe API-Anfragen verwenden HTTPS. | Konfigurations-, Netzwerk- und Logprüfung mit Testschlüssel. |
| N-04 | Personenbezogene Daten bleiben im lokalen aktiven Datenspeicher; keine Telemetrie. Logs enthalten keine SteamID oder rohen Antworten. US-16 entfernt sämtliche aktiven Profildaten einschließlich späterer Verlaufs- und Feedbackdaten. | Speicherprüfung vor/nach Löschung und Neustart; keine durch den MVP erstellten externen Backups. |
| N-05 | Der vollständige Kernablauf ist per Tastatur nutzbar; alle Bedienelemente besitzen verständliche Namen und sichtbaren Fokus. Fehler und Status sind auch textlich erkennbar. | Manueller Ablauf ohne Maus; Profilwahl und Button einschließen. |
| N-06 | Profile, Ranking, Gleichstände und Fehlerbehandlung sind ohne Live-Zugriff überprüfbar; Datenadapter und Profil-/Empfehlungslogik sind getrennt austauschbar. | Tests mit den festen Erwartungen aus Abschnitt 5 und simulierten Importantworten. |
| N-07 | Persönliche Bibliothek, Profile, Tags, Feedback und Snapshots sind nur mit einer verifizierten Sitzung des zugehörigen Kontos zugänglich. Abmelden beendet den Zugriff; eine fremde SteamID im Request reicht nicht. | Tests mit zwei getrennten Konten/Sitzungen, manipulierten Kontoparametern und abgemeldeter Sitzung; allgemeiner Metadaten-Cache enthält keine persönlichen Daten. |

## 9. Konsistenzprüfung und Projektrisiken

### Geklärte Abgrenzungen

| Prüfpunkt | Festgelegte Regel |
| --- | --- |
| Eigene Empfehlungen und Wiederentdeckung | Der MVP empfiehlt ungespielte Titel; bereits gespielte Titel gehören zum separaten Should-Bereich US-10. |
| Last played und kürzliche Aktivität | Nur belegte Zeitpunkte werden zeitlich sortiert; reine Aktivitätsdaten erhalten eine entsprechende Beschriftung. |
| Current Taste und eigener Verlauf | Current Taste verwendet das 14-Tage-Signal aus Steam; eigene Snapshots beginnen erst mit Umsetzung von US-08. |
| Präferenzprofil und Dashboard | Profilgewichte gehören zum MVP; grafische Analysen sind Should. Gemessene Minuten und Präferenzwerte bleiben getrennte Größen. |
| Spielzeit und Zufriedenheit | Spielzeit ist ein implizites Interessenssignal. Persönliche Bewertungen werden nur aus expliziten Angaben übernommen. |
| Tags, Likes und Filter | Ausschlüsse haben Vorrang; Feedback verändert nur den vorgesehenen Empfehlungsbereich. |
| Anmeldung, Abmeldung und Löschung | Anmeldung verifiziert die Identität, Abmeldung beendet den Zugriff und bestätigte Löschung entfernt die persönlichen Daten. |
| Persönliche Daten und Metadaten | Bibliotheken, Profile und Feedback sind kontogebunden; allgemeine Metadaten liegen im getrennten Cache. |
| Live-Daten und Demo | Offline-Ergebnisse prüfen die Rechenregeln; erfolgreicher Live-Import und API-Zuordnung werden separat nachgewiesen. |

### Risiken und Maßnahmen

| Risiko | Auswirkung | Maßnahme / Prüfzeitpunkt |
| --- | --- | --- |
| Steam-Sichtbarkeit oder Antwortfelder reichen nicht aus | Import oder Current Taste ist für einzelne Konten nicht verfügbar. | In Phase 2 Anmeldung und Datenzugriff getrennt prüfen; fehlende Daten nach US-15 behandeln. |
| IGDB-Zuordnung oder Genreabdeckung ist lückenhaft | Weniger Referenzen und Kandidaten stehen zur Verfügung. | Stichprobe und Cache-Prüfung nach Abschnitt 7; Lücken anzeigen und bei Bedarf SteamSpy als Alternative bewerten. |
| Integration überschreitet die Kapazität von zwei Personen | Vollständiger MVP ist zur Phase-3-Abgabe gefährdet. | Aufwandsprüfung nach dem frühen Integrationsnachweis; Must-Funktionen priorisieren und notwendige Scope-Änderungen vor Implementierung dokumentieren. |
| Breite Genres und dominante Langzeitspiele liefern wenig hilfreiche Vorschläge | Rechenregeln funktionieren, aber Empfehlungen treffen den Geschmack nur eingeschränkt. | In Phase 5 drei freiwillige Personen den Kernablauf und die Begründungen qualitativ beurteilen lassen; Befunde und Verbesserungsmöglichkeiten dokumentieren. |
| Sehr kurzer Abstand zwischen Phase 4 und 5 | Evaluation und Reflexion werden zu spät vorbereitet. | Entscheidungen und Testergebnisse fortlaufend sammeln; Abschlussreflexion am 22.12.2026 fertigstellen. |

Die Berechnungsregeln werden mit dem festen Beispiel aus Abschnitt 5 geprüft. Alters-, Cooldown- und Cache-Grenzen werden anhand der Fälle in Abschnitt 7 getestet. Der Terminplan steht in [mvp.md, Abschnitt 6](mvp.md#6-umsetzungsetappen).

## 10. Quellen

Recherche- und Dokumentationsstand: 05.11.2026.

- [S1 – Valve: IPlayerService](https://partner.steamgames.com/doc/webapi/IPlayerService?language=english)
- [S2 – Valve: Steam Web API Terms of Use](https://steamcommunity.com/dev/apiterms)
- [S3 – Valve: Web API Overview](https://partner.steamgames.com/doc/webapi_overview?language=english)
- [S4 – Valve: Steam OpenID Provider](https://steamcommunity.com/dev)
- [S5 – IGDB: API-Dokumentation](https://api-docs.igdb.com/)
- [S6 – FastAPI: Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [S7 – SteamSpy: API-Dokumentation](https://steamspy.com/api.php)

Die Quellen dokumentieren die externen Schnittstellen und Zugangsbedingungen. Profilberechnung, Prioritäten und Produktgrenzen sind projektspezifische Festlegungen.
