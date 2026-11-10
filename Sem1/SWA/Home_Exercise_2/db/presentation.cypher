// EarlyBird: kurze Datenbank-Demo fuer den Vortrag.
// Neo4j Browser: http://127.0.0.1:7474
// Jeweils EINE Abfrage bis zum Semikolon kopieren und ausfuehren.
// Alle Abfragen lesen vorhandene Daten; sie starten keine neuen Versuche.

// 1. Welche Datenbank und welches Analyse-Plugin laufen?
CALL dbms.components() YIELD name, versions
RETURN name AS Datenbank, versions[0] AS Version, gds.version() AS GDS;

// 2. Der echte Vektorindex: erwartet ONLINE, 768 Dimensionen und COSINE.
SHOW VECTOR INDEXES YIELD name, state, options
RETURN name AS Indexname, state AS Status,
       options.indexConfig['vector.dimensions'] AS Dimensionen,
       options.indexConfig['vector.similarity_function'] AS Metrik;

// 3. Eine Anforderung ist mit einem Vektor aus 768 Zahlen gespeichert.
// Der ausgewaehlte Lauf begrenzt die Abfrage auf die passende Eingabeversion.
MATCH (:EBRun {id: 'a983874ded32c47593dd23c6'})-[:ASSIGNS]->
      (r:EBRequirement {item_id: 'R29.a'})
RETURN r.item_id AS Anforderung, r.text AS Text,
       size(r.embedding) AS Dimensionen, r.embedding[0..8] AS Erste_acht_Werte;

// 4. Die sieben berechneten Gruppen des Kandidaten, als uebersichtliche Tabelle.
// Erwartete Groessen nach Gruppennummer: 7, 10, 4, 2, 8, 7, 5.
MATCH (:EBRun {id: 'a983874ded32c47593dd23c6'})-[a:ASSIGNS]->(r:EBRequirement)
WITH a.cluster AS Gruppe, r ORDER BY Gruppe, r.item_id
RETURN Gruppe, count(*) AS Anzahl, collect(r.item_id) AS Teilanforderungen
ORDER BY Gruppe;

// 5. Optional: Welche Anforderungen liegen inhaltlich nahe an der Stornierungsregel?
// Neo4j bildet den Kosinus auf [0,1] ab. 2*Wert-1 liefert den Rohkosinus
// auf [-1,1], den auch die gespeicherte Dashboard-Ansicht verwendet.
// Dies ist eine exakte Suche auf den 43 Vektoren, keine Indexabfrage.
MATCH (run:EBRun {id: 'a983874ded32c47593dd23c6'})-[:ASSIGNS]->
      (q:EBRequirement {item_id: 'R29.a'})
MATCH (run)-[:ASSIGNS]->(r:EBRequirement)
WHERE r <> q
RETURN r.item_id AS Anforderung, r.text AS Text,
       2.0 * vector.similarity.cosine(q.embedding, r.embedding) - 1.0 AS Kosinusaehnlichkeit
ORDER BY Kosinusaehnlichkeit DESC
LIMIT 5;

// 6. Optional: Graph-Ansicht eines Versuchs mit den sieben Mitgliedern von Gruppe 0.
// WICHTIG: Die Kanten bedeuten "Lauf ordnet Anforderung einer Gruppe zu".
// Die Bildschirmpositionen sind KEINE Darstellung der 768D-Vektorkoordinaten.
MATCH (run:EBRun {id: 'a983874ded32c47593dd23c6'})-[a:ASSIGNS]->(r:EBRequirement)
WHERE a.cluster = 0
RETURN run, a, r;
