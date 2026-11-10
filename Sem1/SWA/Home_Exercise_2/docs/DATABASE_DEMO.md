# Optionaler Technikeinblick: Datenbank und Code

Plane dafür etwa zwei zusätzliche Minuten ein. Zeige zuerst, dass die Anforderungen tatsächlich als Vektoren gespeichert sind, und anschließend den kurzen Datenbankaufruf für die Gruppierung. Die weiteren Abfragen eignen sich für Rückfragen.

## Vorbereitung

Starte Docker Desktop. Öffne PowerShell im Projektordner:

```powershell
docker compose up -d --wait
```

Öffne [Neo4j Browser](http://127.0.0.1:7474). Falls ein Verbindungsdialog erscheint, verwende `bolt://127.0.0.1:7687` und die Authentifizierungsoption ohne Anmeldung. Die mitgelieferte lokale Projektkonfiguration benötigt keine Zugangsdaten.

Öffne daneben [die vorbereiteten Abfragen](../db/presentation.cypher). Kopiere jeweils einen vollständigen Abfrageblock bis zum Semikolon in Neo4j Browser und führe ihn aus. Die Abfragen lesen vorhandene Daten; sie verändern keine Gruppierungen.

## 1. Eine echte Anforderung und ihre 768 Zahlen zeigen

**Ausführen:** Abfrage 3 aus `db/presentation.cypher`. Wähle im Ergebnis die Tabellenansicht.

Du siehst die Stornierungsregel `R29.a`, die Anzahl ihrer Vektorwerte und die ersten acht dieser Werte. Erwartet werden **768 Dimensionen**.

**Sprechen:**

> Hier liegt eine konkrete Anforderung direkt in der Datenbank. Neben ihrem Text ist der Vektor mit 768 Zahlen gespeichert. Diese Zahlen geben ihre Position im hochdimensionalen Bedeutungsraum an. Hier zeige ich nur die ersten acht Werte, damit die Ausgabe lesbar bleibt.

## 2. Den Vektorindex zeigen

**Ausführen:** Abfrage 2. Die Tabelle zeigt den Index `eb_vectors_768`, den Zustand `ONLINE`, die Dimensionszahl `768` und die Kosinusmetrik.

**Sprechen:**

> Neo4j stellt für diese Vektoren einen eigenen Index bereit. Er ist für 768 Dimensionen konfiguriert und unterstützt die Ähnlichkeitssuche. Die Gruppierung übernimmt anschließend das Analyse-Plugin.

## 3. Den eigentlichen Gruppierungsaufruf im Code zeigen

**Öffnen:** [db/cluster.cypher](../db/cluster.cypher). Zeige den kurzen Aufruf `gds.kmeans.stream`.

**Sprechen:**

> Das ist der tatsächliche Aufruf, den die Anwendung an Neo4j sendet. Das Feld `embedding` liefert die 768 Werte. `k` legt die gewünschte Gruppenzahl fest, und `randomSeed` steuert die Startkonfiguration. Die Datenbank gibt für jede Anforderung die berechnete Gruppennummer zurück.

Die Datei wird von Python mit Parametern ausgeführt. Sie benötigt eine vorbereitete GDS-Projektion im Arbeitsspeicher. Zeige sie im Vortrag als Code; die vorbereiteten Präsentationsabfragen funktionieren direkt mit den gespeicherten Ergebnissen.

## Optional: die sieben Gruppen direkt aus der Datenbank lesen

**Ausführen:** Abfrage 4. Sie liefert sieben Tabellenzeilen mit Gruppennummer, Anzahl und den zugeordneten Anforderungskennungen. Der ausgewählte Kandidat hat Gruppengrößen von **7, 10, 4, 2, 8, 7 und 5**.

**Sprechen:**

> Hier lese ich dieselben Gruppenzuordnungen direkt aus der Datenbank, die das Dashboard anzeigt. Die Ergebnisse sind mit dem konkreten Versuchslauf verknüpft und dadurch nachvollziehbar.

## Weitere Abfragen für Rückfragen

- **Abfrage 1:** Zeigt Datenbank- und GDS-Version.
- **Abfrage 5:** Zeigt die fünf inhaltlich nächsten Anforderungen zur Stornierungsregel. Sie vergleicht die 43 Vektoren exakt und benötigt dafür keinen Indexzugriff. Die angezeigte Kosinusskala entspricht der gespeicherten Dashboard-Ansicht.
- **Abfrage 6:** Zeigt einen Versuchslauf und die sieben Anforderungen seiner Gruppe 0 als Graph.

Bei der Graph-Ansicht bedeutet jede Kante, dass der Lauf eine Anforderung einer Gruppe zuordnet. **Die Anordnung der Knoten im Neo4j-Fenster ist keine Projektion der 768-dimensionalen Koordinaten.** Die PCA-Ansicht des Dashboards erfüllt diesen Darstellungszweck. In Neo4j Browser kann bei Anforderungsknoten `item_id` als Beschriftung gewählt werden, damit kurze Kennungen angezeigt werden.

## Welche Python-Stellen sind interessant?

| Datei und Stelle | Was du daran erklären kannst |
| --- | --- |
| `src/earlybird/embeddings.py`, Aufruf `self.model.encode(...)` | Wie die Anforderungstexte in Vektoren umgewandelt werden. `normalize_embeddings=True` normiert die Vektoren auf Länge 1. |
| `src/earlybird/database.py`, Methode `ingest` | Wie Text, Quellenkennung und Vektor gemeinsam gespeichert und der Vektorindex erstellt werden. |
| `db/cluster.cypher` | Dass die Gruppierung tatsächlich durch GDS in Neo4j ausgeführt wird. |
| `src/earlybird/analysis.py`, Funktion `consensus` | Wie gezählt wird, wie oft zwei Anforderungen über mehrere Läufe gemeinsam in einer Gruppe landen. Daraus entsteht die Heatmap. |
| `src/earlybird/analysis.py`, Funktion `display_evidence` | Dass die PCA-Projektion die zweidimensionale Anzeige erzeugt. Die Gruppierung hat zu diesem Zeitpunkt bereits im vollständigen Raum stattgefunden. |

Für den kurzen Vortrag reichen der Vektor in der Datenbank und der K-Means-Aufruf. Mit `consensus` kannst du bei Interesse die zusätzliche Stabilitätsuntersuchung erklären:

> Die Funktion vergleicht für jeden Lauf die Gruppenzuordnungen aller Anforderungspaare. Wenn zwei Anforderungen in acht von zehn Läufen gemeinsam gruppiert werden, zeigt ihre Heatmap-Zelle den Wert 0,8. Das ist eine beobachtete Häufigkeit.

## Hinweis zur Ähnlichkeitsskala

Neo4j bildet den Kosinuswert auf das Intervall von 0 bis 1 ab. Die Anwendung rechnet Live-Werte mit `2 * Wert - 1` auf den Rohkosinus von −1 bis 1 zurück, den auch die gespeicherte NumPy-Auswertung verwendet. So stimmen Datenbank-Demo und Dashboard innerhalb der numerischen Genauigkeit überein.

Die Definition der Neo4j-Skala ist in der [offiziellen Dokumentation](https://neo4j.com/docs/cypher-manual/current/indexes/search-indexes/vector-indexes/#similarity-functions) beschrieben.
