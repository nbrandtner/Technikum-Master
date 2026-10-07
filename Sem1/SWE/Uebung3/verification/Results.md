# Genuine verification results - 7 October 2026

Project: `F:\Technikum-Master\Sem1\SWE\Uebung3`.
Verification was executed locally in that folder using Azul Zulu OpenJDK
**17.0.19** and Apache Maven **3.9.10**. Log timestamps use Europe/Vienna.

## Compilation, tests and packaging

Command: `mvn -B -ntp verify`. Final result: **BUILD SUCCESS**, exit code **0**.
Seven production Java files and six test/support Java files were compiled on
the initial run. Later runs reused compiled classes. The compiler enables
`-Xlint:all -Werror`; no compiler warnings or compilation errors were reported.
The executable `target/exercise3-reporting-1.0.0.jar` was built.

| Suite | Test cases | Failures | Errors | Skipped |
| --- | ---: | ---: | ---: | ---: |
| CsvReportFormatterTest | 13 | 0 | 0 | 0 |
| JsonReportFormatterTest | 16 | 0 | 0 | 0 |
| MonitoringReportSenderTest | 5 | 0 | 0 | 0 |
| ReportApplicationTest | 2 | 0 | 0 | 0 |
| ReportGeneratorTest | 12 | 0 | 0 | 0 |
| **Total** | **48** | **0** | **0** | **0** |

Parameterized invocations count individually. The saved aggregated JUnit XML
preserves all five Surefire suites. Some negative tests intentionally produce
SEVERE logs and stack traces; these are expected paths, not test failures.

## Static analysis

Tool: **PMD 7.17.0**, supplied by Maven PMD Plugin **3.28.0**.
Committed configuration: `config/pmd-ruleset.xml`, **20 focused rules** with
default thresholds. The final scan includes **all 7 main and 6 test/support
Java files**. The baseline scan covers only `docs/original/ReportGenerator.java`.
It is not compiled into the application. Commands:

```powershell
mvn -B -ntp verify
mvn -B -ntp -Pbaseline-analysis pmd:pmd
```

| Rule | Original findings | Refactored findings |
| --- | ---: | ---: |
| EmptyCatchBlock | 1 | 0 |
| SystemPrintln | 10 | 0 |
| UseStringBufferForStringAppends | 2 | 0 |
| **Total unsuppressed findings** | **13** | **0** |

Both final scans have **0 processing errors and 0 configuration errors**.
One finding is intentionally suppressed in the CLI main method only:
`PMD.SystemPrintln` for the requested report on stdout. Library diagnostics
use JDK logging. The XML records this suppression; there are no excluded
production files. Complexity/NCSS checks did not trigger at default thresholds
in either version; no numerical complexity improvement is claimed from PMD.
These selected rules do not prove the absence of all defects or SOLID violations.

The baseline goal is report-only: its BUILD SUCCESS means analysis executed,
not that the original passed a quality gate. The refactored `verify` goal does
fail on unsuppressed findings, with a zero permitted violation count.

## Runtime and compatibility checks

- The executable JAR ran successfully for explicit JSON, CSV and default JSON.
- Unsupported XML exited with code 1 and no output/delivery attempt.
- A temporary Java probe compiled the original fixture separately and compared
  five ordinary/null/empty-CSV outputs byte-for-byte with the new formatters.
  All matched. It also confirmed the original empty JSON defect (`}`).
- Independent Python `json` and `csv` parsers read generated special-character
  reports back into the expected six fields, including every U+0000-U+001F
  control, quotes, backslashes, CR/LF, Unicode, null, numeric and empty values.
- The demo's monitoring transport is a labeled local simulation. No external
  endpoint or real monitoring-service integration was provided or tested.

Evidence: `runtime-checks.log`; generated probe/data under `target/runtime-checks`.
The Python probe is an additional one-time verification step; Python is not a
build or runtime requirement of the Java project.

## Initial failures and scope review

The first run compiled and passed all 48 cases, then failed because two PMD
rule references were invalid for PMD 7.17.0. They were corrected to NcssCount
and errorprone/AvoidCatchingThrowable. The original failure log is preserved
as `maven-verify-initial.log`. A subsequent successful scan is preserved as
`maven-verify-before-scope-review.log`.

A preliminary baseline had 14 findings, including DoNotUseThreads, a rule
specifically aimed at J2EE applications. That rule was removed from this CLI
exercise's final ruleset because its stated constraint does not apply here.
The final comparable baseline is 13; the refactored count stayed zero.
The preliminary baseline log is `maven-baseline-before-scope-review.log`.
Removing the pointless sleep is a manual design improvement, independent of
that J2EE rule. No Java compilation or JUnit failure occurred.

## Preservation and review scope

The original assignment PDF was not modified. Its SHA-256 remains:
`17fba0257ea8458f552b3a5cc96d870f1e988ac7245b9027c4228aef3b2ed637`.
The separate principles/checklist document mentioned by the assignment was
absent. `docs/Review.md` applies the supplied assignment's explicit criteria.
Student team participation and a human peer review are not claimed by this run.

Tool references: [Maven PMD check](https://maven.apache.org/plugins/maven-pmd-plugin/check-mojo.html),
[PMD 7.17 design rules](https://docs.pmd-code.org/pmd-doc-7.17.0/pmd_rules_java_design.html),
[PMD 7.17 error-prone rules](https://docs.pmd-code.org/pmd-doc-7.17.0/pmd_rules_java_errorprone.html).
