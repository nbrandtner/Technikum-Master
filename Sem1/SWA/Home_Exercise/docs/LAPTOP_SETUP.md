# Einrichtung auf dem Laptop (Windows)

Für das Dashboard mit den gespeicherten Ergebnissen brauchst du Python und die Projektdateien. Docker und das Embedding-Modell werden erst benötigt, wenn du die Datenbank verwenden oder die Versuche erneut ausführen möchtest.

## 1. Die Projektdateien übertragen

Kopiere den Projektordner auf den Laptop, zum Beispiel per USB-Stick, ZIP-Datei oder Git. Der Ordner darf auf dem Laptop einen anderen Pfad haben.

Übertrage insbesondere:

- `app.py`, `run.ps1`, `pyproject.toml`, `requirements-lock.txt` und `compose.yaml`.
- Die Ordner `src`, `data`, `db`, `docs`, `scripts`, `tests` und `.streamlit`.
- **`experiments/latest.json`** mit den fertigen Versuchsergebnissen. Ohne diese Datei kann das Dashboard die gespeicherten Gruppierungen nicht anzeigen.

Lasse diese Ordner beim Kopieren weg:

- **`.venv`**: Die Python-Umgebung enthält Verweise auf den Interpreter des Heim-PCs. Sie wird auf dem Laptop neu erstellt.
- `.cache`: Heruntergeladene Modelle und zwischengespeicherte Embeddings. Für die gespeicherte Präsentation nicht erforderlich.
- `tmp`, `.pytest_cache`, `__pycache__` und erzeugte `*.egg-info`-Ordner: Zwischenstände und lokale Installationsdateien.

Verwende eine Projektkopie ohne die alte `.venv`. Die Original-PDFs werden für die Präsentation und die bereits aufbereiteten Eingabedaten nicht benötigt.

## 2. Python installieren und eine neue Umgebung erstellen

Verwende auf dem Windows-Laptop **Python 3.12**, mit dem dieses Projekt geprüft wurde. Öffne ein Terminal im kopierten Projektordner, also dort, wo `app.py` liegt.

Prüfe zunächst:

```powershell
python --version
```

Wenn hier Python 3.12 angezeigt wird, führe aus:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip install -e . --no-deps
```

Damit werden die aufgezeichneten Paketversionen installiert und anschließend der lokale Projektcode registriert. Die erste Installation benötigt Internet und kann einige Minuten dauern. Die Umgebung muss nicht separat aktiviert werden.

Falls mehrere Python-Versionen installiert sind und der Windows-Python-Launcher verfügbar ist, kannst du die Umgebung gezielt mit `py -3.12 -m venv .venv` erstellen.

Der kürzere Befehl `.\run.ps1 setup` erstellt ebenfalls eine Umgebung und installiert die Abhängigkeiten. Er verwendet allerdings die Versionsbereiche aus `pyproject.toml`; für dieselben Paketversionen wie auf dem Heim-PC ist die obige Installation mit `requirements-lock.txt` vorgesehen.

## 3. Das Dashboard öffnen

```powershell
.\run.ps1
```

Öffne anschließend [das Dashboard](http://127.0.0.1:8501). Lasse das Terminal während der Nutzung geöffnet.

Falls PowerShell das Starten der Skriptdatei blockiert, kannst du die Anwendung direkt über Python starten:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Prüfe vor der Präsentation:

- Der Hinweis auf **300 genuine runs** wird angezeigt.
- **Discover**, **Stability**, **Inspect**, **Challenge** und **Sources** funktionieren.
- **Query live neighbors** bleibt für die gespeicherte Präsentation ausgeschaltet.

Für diese Nutzung werden weder Docker noch ein API-Schlüssel oder ein erneuter Modelldownload benötigt. Nach der Paketinstallation funktioniert die gespeicherte Präsentation lokal ohne Internet.

## 4. Optional: Datenbank und Analyse auf dem Laptop einrichten

**Wichtig:** Die Neo4j-Datenbank des Heim-PCs liegt in einem Docker-Volume. Durch das Kopieren des Projektordners wird dieses Volume nicht mit übertragen. `docker compose up` allein startet auf dem Laptop daher zunächst eine leere Projektdatenbank.

Für eine neue Datenbank mit Versuchsergebnissen:

1. Installiere und starte Docker Desktop mit Linux-Containern.
2. Sichere vor dem erneuten Versuchslauf `experiments/latest.json` sowie die bisherigen Berichte, falls du die Präsentationsfassung unverändert aufbewahren möchtest. Der Versuchslauf ersetzt die aktuelle Ergebnisdatei und erzeugt die Berichte neu.
3. Führe im Projektordner aus:

```powershell
.\run.ps1 experiment
.\run.ps1 verify
```

Der erste Versuchslauf lädt das Datenbank-Image, das Analyse-Plugin und das festgelegte Embedding-Modell herunter. Er berechnet die Versuche erneut und speichert ihre Zuordnungen in der Datenbank des Laptops. Dafür wird Internet benötigt; es entstehen keine API-Kosten.

Danach kannst du [Neo4j Browser](http://127.0.0.1:7474) öffnen und die [Datenbank-Demo](DATABASE_DEMO.md) verwenden. Falls ein Verbindungsdialog erscheint, verwende `bolt://127.0.0.1:7687` und die Option ohne Anmeldung.

An späteren Tagen genügt bei bereits befüllter Datenbank:

```powershell
docker compose up -d --wait
```

Zum Stoppen der Projektdatenbank:

```powershell
.\run.ps1 stop
```

Das Stoppen erhält die gespeicherten Daten im Docker-Volume.

## Falls etwas fehlt

| Beobachtung | Nächster Schritt |
| --- | --- |
| `python` wird nicht gefunden | Python 3.12 installieren beziehungsweise dessen Aufruf im Terminal einrichten; danach das Terminal neu öffnen. |
| Der Interpreter verweist auf den Heim-PC oder einen Codex-Pfad | Eine frische Projektkopie ohne die übertragene `.venv` verwenden und Schritt 2 ausführen. |
| Es werden keine Versuchsergebnisse angezeigt | Prüfen, ob `experiments/latest.json` vom Heim-PC mitkopiert wurde. |
| Die Live-Datenbank ist nicht erreichbar | Docker Desktop starten und bei bereits befüllter Datenbank `docker compose up -d --wait` ausführen. |
| Die Datenbank läuft, aber die Demo-Abfragen liefern keine Anforderungen | Die Datenbank ist wahrscheinlich noch leer. Den vollständigen Versuchslauf gemäß Schritt 4 ausführen. |
| Die PowerShell-Skriptdatei lässt sich nicht starten | Für das Dashboard den direkten Python-Befehl aus Schritt 3 verwenden. |

Diese Anleitung beschreibt Windows. Auf einem Laptop mit macOS oder Linux unterscheiden sich die Umgebungspfade und die Startbefehle.
