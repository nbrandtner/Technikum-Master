# Exercise 3 - Reporting module refactoring
Phase 4 | Java 17 / Maven | Verified 7 October 2026

## Original problems
Fifteen mapped issues covered mixed responsibilities (SRP), format branches
(OCP), concrete side effects (DIP), missing small interfaces (ISP), duplicated
delivery (DRY), a pointless delay (KISS), swallowed exceptions, repeated string
copying, invalid empty JSON, missing JSON/CSV escaping, ambiguous null returns,
weak naming, poor observability and difficult isolated testing.

## Redesigned architecture
`ReportApplication -> ReportGenerator -> ReportFormatter + ReportSender`.
JSON and CSV implement the formatter contract. MonitoringReportSender wraps an
injected synchronous transport. Constructor injection keeps the generator
independent of formats and destinations; each interface has one operation.

## Refactored code
Seven production files define the two interfaces, two formatters, sender,
generator and CLI. Six test/support files provide five JUnit suites and log capture.
Core excerpt from ReportGenerator.generateReport; surrounding validation,
logging and stage tracking are omitted here. Full implementation: src/main/java.

```java
String report = Objects.requireNonNull(formatter.format(data), "formatter returned null");
sender.send(report);
return report;
```

## Craftsmanship improvements
Short cohesive methods, final dependencies, StringBuilder/StringJoiner,
explicit contracts and JDK event logging replace branching and global prints.
Ordinary JSON/CSV output, order and string conversion are preserved. Correct
escaping, empty JSON, fail-fast invalid input and removal of the delay are
intentional fixes. Failures retain their causes and are propagated without retry.

## Actual verification and static analysis
OpenJDK 17.0.19 / Maven 3.9.10: compilation, executable JAR and `mvn verify`
succeeded. All 48 JUnit cases passed (0 failures, errors or skips). PMD 7.17.0
via plugin 3.28.0, using 20 focused rules: original 13 findings (10 console calls,
2 string-append warnings, 1 empty catch); refactored 0 unsuppressed findings,
1 documented CLI-output suppression, 0 analysis errors. Two initial rule-reference
errors were corrected; genuine logs and XML are saved in `verification`.
JAR demos, five legacy-output comparisons and independent JSON/CSV parser
round trips passed. Monitoring is a local simulation, not an external service.

## Integration benefits
Formats and transports evolve independently; fakes isolate failure paths and
stable event/stage fields make delivery failures diagnosable. One shared workflow
reduces inconsistent changes. Committed tests and analysis rules support future
maintenance. Detailed analysis, architecture, review and evidence accompany the code.

Review scope: the separate referenced checklist was absent. This automated
implementation/review does not replace the assignment's required student team work.
