# Exercise 3 - Refactoring a reporting mini-module

This Java solution implements the four phases of `Class 3 - Assignment-SWEN.pdf`:
analyze the original report generator, separate responsibilities, refactor and
verify the module, and produce a one-page final summary.

The original combined JSON/CSV formatting, console diagnostics, a hard-coded
delay and simulated delivery. It duplicated sending, swallowed exceptions,
repeatedly concatenated strings and mishandled escaping and empty JSON input.
The 15 concrete findings mapped to principles are in `docs/Analysis.md`.

## Architecture

```text
ReportApplication -> ReportGenerator -> ReportFormatter (JSON / CSV)
                                     -> ReportSender -> MonitoringReportSender
                                                        -> injected transport
```

The generator formats once and sends once through two injected one-method
interfaces. Formatters are pure; the sender owns delivery. A new formatter can
be supplied without editing the generator. JDK logging records event/stage
fields and propagates original failures. The CLI chooses JSON or CSV and prints
the report. Its monitoring destination is an explicitly labeled local simulation.

This is a flat `Map<String, Object>` report: values use `String.valueOf`, including
numbers/booleans as JSON strings and null as the string "null". Map iteration
order is preserved. Null maps/keys/dependencies are rejected. Ordinary output
is unchanged; valid escaping, empty JSON, explicit invalid-format errors and
removal of the delay are documented corrections. See `docs/Architecture.md`.

## Build and run

Requirements: **JDK 17+** and **Maven 3.6.3+**. Confirm `java -version` and
`mvn -version`. Maven downloads pinned plugins and JUnit from Maven Central
on the first build; there are no production dependencies or frameworks.

From PowerShell:

```powershell
Set-Location 'F:\Technikum-Master\Sem1\SWE\Uebung3'
mvn compile
mvn package
java -jar target/exercise3-reporting-1.0.0.jar json
java -jar target/exercise3-reporting-1.0.0.jar csv
```

With no argument the application uses JSON. Unsupported formats throw
IllegalArgumentException and exit unsuccessfully before sending. stdout contains
only the requested report; diagnostic events use stderr through JDK logging.
CSV retains the original LF row endings and has no header.

A JDK-only compile/run is also possible; Maven is needed for JUnit and PMD:

```powershell
New-Item -ItemType Directory -Path target/classes -Force | Out-Null
$sources = Get-ChildItem src/main/java -Filter *.java -Recurse | ForEach-Object FullName
javac -encoding UTF-8 -Xlint:all -Werror -d target/classes $sources
java -cp target/classes at.ac.technikum.reporting.ReportApplication json
```

## Tests and static analysis

```powershell
mvn test                                      # JUnit 5
mvn verify                                    # tests, JAR, PMD quality gate
mvn -Pbaseline-analysis pmd:pmd                # report original findings only
```

`mvn verify` uses **PMD 7.17.0** through Maven PMD Plugin **3.28.0** and the
committed 20-rule configuration. It scans main and test sources and fails on
unsuppressed violations or analysis errors. Compilation enables all javac lint
warnings as errors. PMD's HTML report is `target/reports/pmd.html`; the original
comparison report is `target/baseline/reports/pmd.html`.

Actual verification on **7 October 2026**: compilation and packaging succeeded;
**48 tests passed, 0 failures/errors/skips**. PMD found **13 original findings**
and **0 unsuppressed refactored findings**, with one documented CLI output
suppression and no scan errors. The JAR demos and independent JSON/CSV parser
checks passed. Logs, XML snapshots, initial configuration failure and final
results are in `verification/Results.md`. These are measured selected-rule
results, not a claim of universal defect freedom.

## Submission files

- `Exercise3_Summary.md` - editable Phase 4 summary.
- `Exercise3_Summary_Updated.pdf` - current verified one-page A4 version for submission.
- `Exercise3_Summary.pdf` - earlier version retained because an open viewer locked it.
- `docs/Analysis.md` - Phase 1: 15 issues mapped to principles.
- `docs/Architecture.md` - Phase 2: design, contracts and behavior changes.
- `docs/Review.md` - Phase 3: eight integration/review improvements.
- `docs/original/ReportGenerator.java` - original comparison fixture, outside the build.
- `verification/Results.md` - genuine build, test, static and runtime evidence.
- `verification/FilesCreated.md` / `FileManifest.json` - complete project inventory.

Use `src/main/java` for the seven production files and `src/test/java` for the
five JUnit suites plus their logging helper. `target` is generated build output.
The original PDF is preserved. The separate checklist document referenced by
the assignment was not supplied; human student collaboration is still required
by the assignment and is not represented as completed by generated documentation.

The result improves SRP, OCP, ISP and DIP alignment, removes duplication and
pointless latency, makes failures visible, and supports fast tests and new formats
through a small, explicit API.
