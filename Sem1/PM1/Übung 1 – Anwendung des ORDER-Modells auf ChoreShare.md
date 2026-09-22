# Übung 1 – Anwendung des ORDER-Modells auf ChoreShare

## 1. Zehn Unklarheiten, die vor der Angebotslegung geklärt werden müssen

| Nr.  | Unklarheit                                                   | Klärungsbedarf und Auswirkung auf das Angebot                |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1    | **Ziele und Erfolgskriterien**                               | Begriffe wie „mehr Übersicht“, „faire Aufgabenverteilung“ und „einfache digitale Lösung“ sind nicht messbar definiert. Zu klären ist, woran der Auftraggeber den Erfolg erkennt, etwa an weniger vergessenen Aufgaben, weniger Konflikten oder einer bestimmten Nutzungsquote. Davon hängen Konzeption, Funktionsumfang und Abnahme ab. |
| 2    | **Zielgruppen und Nutzungskontext**                          | Es ist unklar, wer die App tatsächlich verwendet: nur Bewohner, auch Betreuer oder Administratoren des Start-ups? Ebenso fehlen Angaben zu Alter, technischen Kenntnissen, Sprachen, Barrierefreiheit und typischer WG-Größe. Diese Informationen beeinflussen Bedienkonzept, Berechtigungen und Testaufwand. |
| 3    | **Funktionsumfang der ersten Version**                       | Die Angabe nennt zahlreiche Funktionen, legt aber nicht fest, welche davon zwingend im MVP enthalten sein müssen. Zu klären ist beispielsweise, ob Rotation, Tausch, Kommentare, Historie und E-Mail-Benachrichtigungen bereits Bestandteil der ersten Version sind. Ohne Priorisierung ist keine belastbare Aufwands- und Kostenschätzung möglich. |
| 4    | **Registrierung und Beitritt zu einem Haushalt**             | Offen ist, ob ein Einladungslink, ein Zugangscode oder beides benötigt wird und ob eine Registrierung per E-Mail verpflichtend ist. Zusätzlich ist zu klären, ob eine Person mehreren Haushalten angehören darf, wie Einladungen ablaufen und was bei verlorenen Zugangsdaten geschieht. |
| 5    | **Rollen und Berechtigungen**                                | Es ist nicht definiert, welche Rollen es gibt und wer Aufgaben, Mitglieder oder Haushalte verwalten darf. Zu klären ist etwa, ob es Eigentümer, Administratoren und normale Mitglieder gibt und ob Berechtigungen pro Haushalt konfigurierbar sein sollen. Ein flexibles Rollenmodell verursacht deutlich mehr Aufwand als feste Rollen. |
| 6    | **Lebenszyklus einer Aufgabe**                               | Die möglichen Zustände einer Aufgabe sind nicht vollständig beschrieben. Offen ist, wer Aufgaben zuweist, ob eine Zuweisung angenommen werden muss, wer die Erledigung bestätigt und was bei einer irrtümlichen Bestätigung passiert. Auch Löschung, Überfälligkeit, Wiedereröffnung und Darstellung in der Historie müssen geklärt werden. |
| 7    | **Wiederkehrende Aufgaben und faire Rotation**               | „Möglichst fair“ ist nicht eindeutig. Fairness könnte eine gleichmäßige Anzahl von Aufgaben, einen vergleichbaren Zeitaufwand oder die Berücksichtigung früherer Leistungen bedeuten. Zu klären sind außerdem Abwesenheiten, Präferenzen, neue Mitglieder, manuelle Änderungen und der Beginn der Rotation. Die gewählte Logik hat großen Einfluss auf die technische Komplexität. |
| 8    | **Tausch und Freigabe von Aufgaben**                         | Der Unterschied zwischen einer Tauschanfrage und einer allgemeinen Freigabe ist nicht vollständig beschrieben. Offen ist, wer einen Wechsel bestätigen muss, ob ein direkter Tausch zweier Aufgaben möglich ist und was geschieht, wenn niemand eine freigegebene Aufgabe übernimmt. |
| 9    | **Benachrichtigungen und Kommunikation**                     | „Rechtzeitig“ und „nicht mit Meldungen überlasten“ sind nicht konkretisiert. Benötigt werden Regeln für Zeitpunkt, Häufigkeit, Kanäle, persönliche Einstellungen und mögliche Eskalationen. Bei Kommentaren ist außerdem zu klären, ob diese bearbeitet oder gelöscht werden können und wer sie sehen darf. |
| 10   | **Technische, rechtliche und betriebliche Rahmenbedingungen** | Unterstützte Smartphones, Browser und Bildschirmgrößen sind noch offen. Ebenso fehlen Anforderungen an Datenschutz, Datenspeicherung, Kontolöschung, Sicherheit, Verfügbarkeit, Backups, Hosting und Betrieb nach der Einführung. Diese Punkte beeinflussen Architektur, Entwicklungsaufwand und laufende Kosten erheblich. |

## 2. Fragen zur Decision-Process-Phase

In dieser Phase muss geklärt werden, **wer welche Entscheidungen trifft, wie Entscheidungen zustande kommen und wie verbindlich sie dokumentiert werden**.

1. Wer ist auf Auftraggeberseite berechtigt, den Auftrag und das Budget endgültig freizugeben?
2. Wer übernimmt während des Projekts die Rolle des fachlichen Ansprechpartners beziehungsweise Product Owners?
3. Welche Personen dürfen verbindlich über Funktionsumfang, Prioritäten und Änderungen entscheiden?
4. Müssen neben den Gründern auch Bewohner, Betreuungspersonal, Datenschutzverantwortliche oder andere Stakeholder in die Entscheidungen einbezogen werden?
5. Wer entscheidet bei unterschiedlichen Interessen, beispielsweise wenn Bewohner möglichst wenig Kontrolle wünschen, das Start-up aber mehr Nachvollziehbarkeit verlangt?
6. Nach welchen Kriterien wird entschieden, welche Funktionen in die erste Version aufgenommen werden: Nutzen, Kosten, Fertigstellungstermin, technisches Risiko oder Wünsche der Pilot-WGs?
7. Wie werden Anforderungen validiert? Sind Interviews, Workshops, Prototypen oder Tests mit Bewohnern vorgesehen?
8. Wer genehmigt wichtige Zwischenergebnisse wie Anforderungskatalog, Rollenmodell, Oberflächenentwurf und MVP-Umfang?
9. Wer nimmt die fertige Anwendung ab und anhand welcher Kriterien erfolgt die Abnahme?
10. Innerhalb welcher Frist muss der Auftraggeber offene Fragen und vorgelegte Entscheidungen beantworten?
11. Wie werden Entscheidungen dokumentiert und allen Beteiligten mitgeteilt?
12. Wie wird mit Änderungswünschen nach Angebotslegung umgegangen? Gibt es ein formelles Change-Request-Verfahren mit einer neuen Bewertung von Kosten und Terminen?
13. Gibt es fixe Entscheidungstermine oder Meilensteine, etwa Freigabe des MVP-Umfangs, Start der Entwicklung, Pilotbetrieb und Produktivsetzung?
14. Wer trifft eine Go-/No-Go-Entscheidung, falls Kosten, Termin oder technische Risiken den geplanten Rahmen überschreiten?

## 3. Fragen zur Resource-Phase

In der Resource-Phase wird geklärt, **welche finanziellen, personellen, zeitlichen und technischen Mittel zur Verfügung stehen**.

### Finanzielle Ressourcen

1. Welches Budget steht für Konzeption, Entwicklung, Tests und Inbetriebnahme zur Verfügung?
2. Gibt es eine verbindliche Kostenobergrenze oder einen Budgetkorridor, an dem der MVP-Umfang ausgerichtet werden muss?
3. Sind laufende Kosten für Hosting, E-Mail-Versand, Überwachung, Wartung und Support im Budget berücksichtigt?
4. Ist nach der ersten Version bereits ein Budget für Weiterentwicklung und Fehlerbehebung vorgesehen?

### Zeitliche Ressourcen

1. Gibt es einen gewünschten oder fixen Fertigstellungstermin?
2. Ist vor der allgemeinen Einführung ein Pilotbetrieb mit ausgewählten Wohngemeinschaften geplant?
3. Welche Zwischentermine sind vorgesehen, beispielsweise für Anforderungsfreigabe, Prototyp, Testversion und Produktivsetzung?
4. Wie viel Zeit steht auf Auftraggeberseite für Workshops, Rückfragen, Tests und Freigaben zur Verfügung?

### Personelle Ressourcen

1. Welche Personen stellt das Start-up für fachliche Fragen und Entscheidungen bereit?
2. Stehen Bewohner aus den betreuten Wohngemeinschaften für Interviews, Usability-Tests und den Pilotbetrieb zur Verfügung?
3. Gibt es beim Auftraggeber bereits Personen mit technischem, datenschutzrechtlichem oder betrieblichem Know-how?
4. Wer übernimmt nach der Einführung Benutzerverwaltung, Support, Bearbeitung von Datenschutzanfragen und Kommunikation mit den Wohngemeinschaften?

### Technische und organisatorische Ressourcen

1. Existieren bereits eine technische Infrastruktur, ein Hosting-Anbieter, eine Domain oder ein E-Mail-Dienst?
2. Gibt es bestehende Systeme oder Kundendaten, die übernommen beziehungsweise angebunden werden müssen?
3. Stellt der Auftraggeber Inhalte wie Logo, Farben, Texte, Datenschutzinformationen und Nutzungsbedingungen bereit?
4. Welche Testgeräte und Browser können vom Auftraggeber zur Verfügung gestellt werden?
5. Wer ist für Betrieb, Backups, Sicherheitsupdates und die Behandlung technischer Störungen verantwortlich?
6. Welche Mittel stehen für Schulung, Dokumentation und Einführung in den Pilot-WGs zur Verfügung?

## Zusammenfassung

Vor einer seriösen Angebotslegung müssen besonders der MVP-Umfang, das Rollen- und Berechtigungskonzept, die faire Rotation, der Aufgabenwechsel sowie die technischen und rechtlichen Rahmenbedingungen konkretisiert werden. Parallel dazu muss klar sein, wer diese Punkte entscheidet und welche finanziellen, zeitlichen, personellen und technischen Ressourcen zur Verfügung stehen. Andernfalls müsste das Angebot mit zahlreichen Annahmen und entsprechend hohen Risikoaufschlägen erstellt werden.