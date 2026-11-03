# EarlyBird: Präsentationsskript für etwa 7–8 Minuten

Nutze die Webanwendung als visuelle Begleitung. Der rote Faden lautet: **Wie weit kommen wir bei der Architekturentwicklung, wenn wir Anforderungen nach ihrer inhaltlichen Ähnlichkeit gruppieren?**

Die Abschnitte enthalten jeweils eine konkrete Bildschirmauswahl und einen Vorschlag zum Sprechen. Die englischen Bezeichnungen in **Fettdruck** entsprechen den Beschriftungen der Anwendung und helfen dir bei der Navigation. Der Vortragstext ist auf Deutsch.

## Vorbereitung vor der Präsentation

Öffne PowerShell im Projektordner und starte die Anwendung:

```powershell
.\run.ps1
```

Öffne anschließend [das Dashboard](http://127.0.0.1:8501) und lasse das Terminal geöffnet. Verwende die gespeicherten Versuchsergebnisse und lasse **Query live neighbors** ausgeschaltet. Diese Ergebnisse stammen aus tatsächlich ausgeführten Datenbankläufen. Beim Ändern der Auswahl wird ein gespeicherter Lauf angezeigt.

Übe die folgende Reihenfolge einmal durch. Halte das [Bildschirmfoto](screenshots/discover.png) und den [Architekturentwurf](ARCHITECTURE.md) als Ersatz bereit.

Wenn du zusätzlich die gespeicherten Gruppenzuordnungen direkt gegen die Datenbank prüfen möchtest, starte vorher Docker Desktop und führe in einem zweiten Terminal Folgendes aus:

```powershell
docker compose up -d --wait
.\run.ps1 verify
```

Bei der dokumentierten Prüfung vom 2. November 2026 stimmten alle 300 gespeicherten Gruppierungen mit der Datenbank überein. Führe den Befehl vor der Präsentation erneut aus, wenn du eine aktuelle Prüfung zeigen möchtest. Ein erneuter vollständiger Versuchslauf benötigt Zeit und ersetzt die gespeicherten Ergebnisse; bereite ihn daher bei Bedarf vor dem Vortrag vor.

## 1. Die Fragestellung erklären — etwa 30 Sekunden

**Zeigen:** **Discover**, mit **Reviewed future-system clauses** als Eingabe.

**Sprechen:**

> Die Aufgabe verlangt, die funktionalen EarlyBird-Anforderungen als Embeddings darzustellen, in einer Vektordatenbank zu gruppieren und daraus benannte Softwarekomponenten abzuleiten. Ich habe das um eine Frage erweitert: Woran erkennen wir, ob diese Gruppen sinnvolle Komponentengrenzen ergeben?
>
> Die Anwendung zeigt die berechneten Gruppen, ihre Stabilität und einen anschließend fachlich überprüften Architekturvorschlag. Für die Präsentation verwende ich gespeicherte Ergebnisse aus tatsächlich ausgeführten Datenbankläufen.

## 2. Die Anforderungen vorbereiten — etwa 45 Sekunden

**Zeigen:** **Sources**. Suche nach `R07` und ersetze die Suche anschließend durch `R32`.

**Sprechen:**

> Das Dokument beschreibt sowohl den bisherigen Telefonprozess als auch die zukünftige Webanwendung. In R07 wird telefonisch bestellt; R32 ersetzt diese Interaktion. Bei der Architektur für das zukünftige System müssen wir diese Aussagen gemeinsam betrachten.
>
> Alle 44 nummerierten Aussagen bleiben erhalten. Daraus wurden 43 einzelne funktionale Teilanforderungen für das zukünftige System aufbereitet. Manche Absätze enthalten mehrere Verpflichtungen und wurden aufgeteilt. Abgelöste Interaktionen, physische Arbeitsschritte und andere Vorgaben wurden gesondert eingeordnet. Jede Entscheidung ist zur ursprünglichen Aussage zurückverfolgbar.

## 3. Den Ansatz mit den „Sternen“ erklären — etwa 75 Sekunden

**Zeigen:** Zurück zu **Discover**. Zeige auf die Punktdarstellung. Öffne bei Bedarf unten **Experiment details**, um das Modell und den Datenbankaufruf zu zeigen.

**Sprechen:**

> Das Grundprinzip entspricht dem beschriebenen Ansatz mit Anforderungen als Punkten in einem hochdimensionalen Raum. Man kann sich die Anforderungen dabei wie Sterne vorstellen: Anforderungen mit ähnlichem Inhalt sollen nahe beieinanderliegen und zu Gruppen zusammengefasst werden.
>
> In unserem Projekt wandelt ein lokales Sprachmodell jede Teilanforderung in einen Vektor mit 768 Zahlen um. Jede Anforderung ist damit ein Punkt in einem 768-dimensionalen Raum. Die Zahl der Dimensionen wird durch das verwendete Embedding-Modell festgelegt. Der Vergleich mit einem Raum mit ungefähr 1000 Dimensionen beschreibt dasselbe Grundprinzip.
>
> Neo4j speichert und indexiert diese Vektoren. Das Graph-Data-Science-Plugin führt darauf K-Means aus. Dabei wählen wir eine Gruppenzahl, und der Algorithmus ordnet jeden Punkt dem nächstgelegenen Gruppenzentrum zu. Die Zentren werden wiederholt angepasst. Für diese Berechnung werden alle 768 Dimensionen verwendet.
>
> Die Darstellung hier ist eine vereinfachte Projektion auf zwei Dimensionen, damit wir die Punkte am Bildschirm betrachten können. Die eigentliche Gruppierung findet im vollständigen Raum statt.

**Merksatz für dich:** Anforderung → 768 Zahlen → Punkt im 768-dimensionalen Raum → Gruppierung nach Abstand → möglicher Architekturbaustein.

**Einordnung:** Aus der Sternen-Analogie allein lässt sich das genaue Verfahren des anderen Beispiels nicht bestimmen. Unser konkretes Verfahren ist K-Means mit vorgegebener Gruppenzahl. Andere Verfahren könnten Gruppen über Nachbarschaften oder Dichte bestimmen. Die zusätzlichen Untersuchungen unseres Projekts betreffen die Stabilität und die fachliche Eignung der Gruppen.

## 4. Das überraschende Ergebnis zeigen — etwa 45 Sekunden

**Zeigen:** **Discover** → **Reviewed future-system clauses** → bei **Components to explore** den Wert **2** → **Seed 2**. Öffne darunter **Component membership**.

**Sprechen:**

> Es wurden zwei bis zehn Gruppen mit jeweils zehn unterschiedlichen Startkonfigurationen untersucht. Die Gruppenzahl ist bei K-Means eine Eingabe des Verfahrens.
>
> Zwei Gruppen erreichen im Durchschnitt den höchsten Silhouettenwert. Dieser Wert beschreibt, wie klar die Gruppen im Zahlenraum getrennt sind. Der hier ausgewählte Lauf legt aber 41 Teilanforderungen in eine Gruppe und trennt nur die beiden Anforderungen zur Produktsuche ab.
>
> Das liefert wenig brauchbare Architekturstruktur. Deshalb müssen wir zusätzlich prüfen, welche fachlichen Verantwortlichkeiten hinter den Gruppen stehen.

**Wichtig für eine genaue Aussage:** `k=2` hat den höchsten durchschnittlichen Silhouettenwert über die untersuchten Startkonfigurationen. Der angezeigte Lauf mit Seed 2 ist der beste innerhalb von `k=2`. Bezeichne ihn nicht pauschal als den höchsten Einzelwert aller untersuchten Läufe.

## 5. Einen brauchbaren Kandidaten und seine Unsicherheit zeigen — etwa 1 Minute

**Zeigen:** **Discover** → **7** Gruppen → **Seed 0**. Öffne **Component membership**. Wechsle danach zu **Stability** und stelle **Inspect consensus at k** auf **7**.

**Sprechen:**

> Dieses Ergebnis mit sieben Gruppen wurde für die genauere Architekturbetrachtung ausgewählt. Darin sind Themen wie Stornierung, Verpackung und Zustellung, Produkte sowie Berichte erkennbar. Andere Gruppen vermischen mehrere Verantwortlichkeiten. Die ursprünglichen Zuordnungen bleiben deshalb sichtbar.
>
> Außerdem wurde untersucht, wie stark die Gruppierung von der Startkonfiguration abhängt. Bei sieben Gruppen beträgt die mittlere Übereinstimmung ungefähr 0,269. Ein Wert von 1 würde identische Gruppierungen bedeuten. Das zeigt also deutliche Unterschiede zwischen den Läufen. Der Wert bedeutet nicht, dass die Architektur zu 26,9 Prozent korrekt ist.
>
> In der Heatmap bedeutet ein dunkles Feld, dass zwei Teilanforderungen über die zehn Startkonfigurationen hinweg häufig zusammenbleiben.

**Optional bei ausreichender Zeit:**

> Zusätzlich wurden vier einzelne Anforderungen sinngleich umformuliert. Die durchschnittliche Übereinstimmung mit den ursprünglichen Gruppierungen lag dabei etwa zwischen 0,96 und 0,97. Einzelne Läufe veränderten sich allerdings stärker.

## 6. Den überprüften Architekturvorschlag erklären — etwa 1 Minute

**Zeigen:** **Inspect**. Zeige auf das Diagramm und öffne danach die Entscheidung **D02** zur Aufteilung von Kennungen und Zugriffskanälen.

**Sprechen:**

> Der überprüfte Entwurf besteht aus sechs Kernkomponenten: Produktkatalog, Kundenidentität und Bestellberechtigung, Bestellverwaltung, Verpackung und Zustellung, Rechnungsdokumente und Zahlungsschnittstelle sowie tägliche Geschäftsberichte. Web- und SMS-Zugänge liegen um diesen Anwendungskern herum.
>
> In diese Aufteilung fließen ausdrücklich Architekturentscheidungen ein. Eine berechnete Gruppe enthält zum Beispiel Kundennummern, Produktcodes, Bestellnummern und Felder von Zahlungsdatensätzen. Die Begriffe sind ähnlich, gehören aber zu unterschiedlichen fachlichen Verantwortlichkeiten: Produktcodes zum Produktkatalog, Kundennummern zur Kundenkomponente und Bestellnummern zur Bestellverwaltung.
>
> Die Pfeile zeigen erlaubte Abhängigkeiten. Die Bestellverwaltung benötigt zum Beispiel Produkt- und Preisinformationen aus dem Katalog. Diese Richtung ergibt sich aus den benötigten Leistungen und dem fachlichen Wissen der Komponenten.

**Zuordnung zu den englischen Namen im Diagramm:**

| Name in der Anwendung | Deutsche Erklärung |
| --- | --- |
| Product Catalog | Produktkatalog mit Paketen, Preisen und Suche |
| Customer Eligibility | Kundenidentität, Bestellberechtigung und hinterlegte Adresse |
| Order Lifecycle | Bestellverwaltung mit Status, Vorlagen und Stornierungsregeln |
| Packing and Delivery | Verpackung, Zuordnung der Zustellkraft, Routen und Lieferbestätigung |
| Documents and Payment Exchange | Rechnungsdokumente und Schnittstelle für erwartete Zahlungen |
| Daily Business Reporting | Tägliche Geschäftsberichte |
| Web and SMS Entry Points | Zugänge über Web und SMS |

**Für Rückfragen:** Die endgültige Zuständigkeitsverteilung ist ein ausgearbeiteter Architekturvorschlag. Die berechneten Gruppen dienen als Ausgangspunkt; das Modell hat diesen konkreten Entwurf mit sechs Kernkomponenten nicht selbstständig erzeugt.

## 7. Eine Grenze anhand einer Geschäftsregel begründen — etwa 75 Sekunden

**Zeigen:** **Challenge** → **The last cancellable moment**. Öffne **Source evidence** und bewege den Schieberegler nacheinander durch die Schritte 1, 2 und 3.

**Sprechen:**

> Stellen wir uns vor, eine Bestellung wird genau dann storniert, wenn das Verpacken abgeschlossen wird. R29 verbietet die Stornierung nach dem Zusammenstellen der Bestellung. R43 verlangt zu diesem Zeitpunkt die Übertragung eines Datensatzes über die erwartete Zahlung.
>
> Wenn Verpackung und Stornierung jeweils einen unabhängigen Status führen, könnten widersprüchliche Entscheidungen entstehen. Deshalb verwaltet die Bestellkomponente den verbindlichen Status. Sie akzeptiert entweder die Stornierung oder den Abschluss der Zusammenstellung. Der Verpackungsbereich meldet den Abschluss an diese zentrale Stelle. Nur ein akzeptierter Abschluss löst die Übertragung des Zahlungsdatensatzes aus.
>
> Damit haben wir eine fachliche Begründung für die Zuständigkeit und für das Zusammenspiel der Komponenten. Der Schieberegler führt durch diesen vorgeschlagenen Ablauf.

Die Darstellung ist eine Erläuterung der Architektur. Eine tatsächliche gleichzeitige Verarbeitung von Bestellungen wird hier nicht ausgeführt. Halte die anderen beiden Szenarien — erneuter Rechnungsdruck und gemeinsame Regeln für Web und SMS — für Rückfragen bereit.

## 8. Das Ergebnis einordnen — etwa 30 Sekunden

**Sprechen:**

> Insgesamt wurden 300 Gruppierungsläufe in der Datenbank durchgeführt. Die dokumentierten Prüfungen bestätigten die gespeicherten Zuordnungen, reproduzierten den ausgewählten Lauf und umfassten acht bestandene automatisierte Tests für das Analysewerkzeug.
>
> Die automatische Gruppierung hatte eine gemischte Qualität und erforderte eine deutliche fachliche Überarbeitung. Das Ergebnis ist ein reproduzierbarer Ausgangspunkt mit sichtbaren Unsicherheiten und einem Architekturvorschlag, dessen Entscheidungen sich auf Anforderungen und Geschäftsszenarien zurückführen lassen.

## Mögliche Rückfragen und verständliche Antworten

**Ist das derselbe Ansatz wie Anforderungen als „Sterne“ in ungefähr 1000 Dimensionen?**

Das Grundprinzip ist gleich: Anforderungen werden als Punkte in einem hochdimensionalen Bedeutungsraum dargestellt und anhand ihrer Abstände gruppiert. Unser Modell liefert 768 Dimensionen. Das genaue Gruppierungsverfahren des anderen Beispiels lässt sich aus der Analogie allein nicht ableiten.

**Warum 768 und nicht 1000 Dimensionen?**

Das verwendete Modell `all-mpnet-base-v2` erzeugt Vektoren mit 768 Zahlen. Die Dimensionszahl ist eine Eigenschaft dieses Modells. Ob ein anderes Modell mit mehr Dimensionen bessere Ergebnisse liefert, wurde in diesem Versuch nicht untersucht.

**Was bedeutet eine einzelne Dimension?**

Es handelt sich um gelernte numerische Merkmale. Einzelne Achsen haben normalerweise keine einfache feste Bedeutung wie „Preis“ oder „Lieferung“. Die Bedeutung entsteht durch das Zusammenspiel der Werte.

**Wird tatsächlich im hochdimensionalen Raum gruppiert oder nur auf der zweidimensionalen Grafik?**

K-Means verwendet alle 768 Dimensionen. Die zweidimensionale Grafik wird anschließend mit PCA für die Anzeige erzeugt. Deshalb können Punkte im Bild näher oder weiter voneinander entfernt wirken, als es ihre vollständigen Vektoren nahelegen.

**Finden sich die Gruppen dabei von selbst?**

Bei unserem K-Means-Verfahren wird die Gruppenzahl vorgegeben. Das Verfahren sucht passende Zentren und ordnet die Anforderungen zu. Verfahren wie hierarchische oder dichtebasierte Gruppierung setzen andere Regeln ein; diese wurden im aktuellen Versuch nicht verglichen.

**Warum zuerst sieben Gruppen und dann sechs Kernkomponenten?**

Sieben ist der ausgewählte berechnete Kandidat. Die fachliche Überprüfung ordnet seine Mitglieder nach Zuständigkeiten neu. Daraus ergeben sich sechs Kernkomponenten und ein Bereich für Web- und SMS-Zugänge. Beide Sichtweisen bleiben sichtbar.

**Warum wurde gerade der Kandidat mit sieben Gruppen ausgewählt?**

Er hatte nach zwei Gruppen den zweithöchsten durchschnittlichen Silhouettenwert und zeigte erkennbare Verantwortlichkeiten, die sich näher untersuchen ließen. Das ist eine dokumentierte Auswahl für die Betrachtung und kein Beweis für eine optimale Gruppenzahl.

**Wurden dem Algorithmus die gewünschten Komponenten bereits vorgegeben?**

Die eingebetteten Texte enthalten die Anforderungen ohne vorgeschlagene Komponentennamen oder Zuständigkeitszuordnungen. Die Datenbank berechnet die Gruppen. Die Benennung und der endgültige Architekturvorschlag entstehen danach in einer gesonderten Bewertung.

**Was macht der Seed?**

Er steuert die zufällige Startkonfiguration. Eine feste Konfiguration ermöglicht die Wiederholung eines Laufs. Mehrere Seeds zeigen, wie stark das Ergebnis vom gewählten Start abhängt.

**Warum sind die Gruppierungswerte so niedrig?**

Die Ergebnisse zeigen überlappende Gruppen. Viele EarlyBird-Anforderungen teilen Begriffe und verbinden mehrere Verantwortlichkeiten. Das ist eine plausible Erklärung, deren Ursache hier nicht gesondert nachgewiesen wurde. Untersucht wurden ein Embedding-Modell und ein Gruppierungsverfahren; daraus lässt sich keine allgemeine Aussage über alle solchen Ansätze ableiten.

**Hat die Aufbereitung der Anforderungen die Architektur verbessert?**

Die ursprüngliche und die aufbereitete Eingabe unterscheiden sich in Umfang und Granularität. Ihre Werte sind daher ein erkundender Vergleich. Sie beweisen keine Verbesserung der Architekturqualität durch die Aufbereitung.

**Führt Neo4j die Gruppierung wirklich selbst aus?**

Ja. Neo4j speichert die Embeddings und stellt den Vektorindex bereit. Das Graph-Data-Science-Plugin führt `gds.kmeans.stream` aus. Python berechnet die Kennzahlen und bereitet die Darstellung auf. Die Gruppierung selbst übernimmt das Plugin; der Vektorindex unterstützt die Ähnlichkeitssuche.

**Welche Rolle spielt KI, und wo wurde Unterstützung eingesetzt?**

Das Embedding-Modell erzeugt die numerische Darstellung der Texte. GDS führt die mathematische Gruppierung aus. Bei der Implementierung und beim ersten Entwurf der Architekturprüfung wurde KI-Unterstützung verwendet. Quellenbezüge, gespeicherte Läufe und dokumentierte Entscheidungen machen diese Arbeit überprüfbar. Beschreibe im Vortrag deine eigene Überprüfung und dein Verständnis zutreffend.

**Beweisen die Tests, dass die Architektur korrekt ist?**

Die Tests prüfen die Analysesoftware und die Konsistenz ihrer Ergebnisse. Die Szenarien sind fachlich begründete Durchgänge durch die vorgeschlagene Architektur. Eine verbindliche Referenzarchitektur zur Messung ihrer Korrektheit lag nicht vor.

**Was wäre ein sinnvoller nächster Untersuchungsschritt?**

Ein weiteres Embedding-Modell oder ein anderes Gruppierungsverfahren bei unveränderter Anforderungseingabe vergleichen. So könnte untersucht werden, ob wichtige Beziehungen stabiler werden. Das wäre eine Erweiterung der bisherigen Untersuchung.

## Kurzer Spickzettel für die Bedienung

Für einen zusätzlichen Einblick in die technische Umsetzung gibt es eine [Datenbank- und Code-Demo](DATABASE_DEMO.md) mit vorbereiteten Abfragen und deutschen Sprechtexten. Plane dafür bei Bedarf zwei zusätzliche Minuten ein.

| Anzeige | Bedeutung für den Vortrag |
| --- | --- |
| Clauses | Anzahl der betrachteten Teilanforderungen |
| Components to explore / k | Angeforderte Anzahl der Gruppen |
| Seed | Nummer der Startkonfiguration |
| Silhouette | Numerische Trennung der Gruppen; ein höherer Wert bedeutet eine klarere Trennung |
| Seed agreement | Übereinstimmung zwischen Startkonfigurationen; 1 bedeutet identische Gruppierungen |
| Singletons | Gruppen mit genau einer Teilanforderung |
| Nearest clauses | Anforderungen mit besonders ähnlichen Vektoren |
| PCA 1 / PCA 2 | Achsen der vereinfachten Darstellung |
| Saved experiment replay | Anzeige gespeicherter Ergebnisse tatsächlich ausgeführter Versuche |

Die entscheidende Abfolge: **Quellen verstehen → Anforderungen als Punkte darstellen → Gruppen berechnen → Stabilität prüfen → Zuständigkeiten fachlich begründen.**
