# Phase 3 - Integration and review

The PDF refers to an attached principles document / Code Review Checklist, but
that separate document was not present in the supplied folder. The review below
uses the explicit criteria in the assignment; it does not claim a human team review.
The assignment's required student collaboration still needs the students' participation.

- **Maintainability:** one format-send path removes delivery duplication; private
  formatting helpers keep the rules beside the format they describe.
- **Evolvability:** a custom formatter is accepted through the same interface;
  a JUnit test proves that the generator needs no format-specific changes.
- **Testability:** lambda fakes capture ordering, payloads and delivery attempts
  without sleeps, external services or a mocking framework.
- **Readability:** purpose-specific classes, final dependencies, short methods,
  named events and documented input/output contracts expose intent.
- **Correctness:** ordinary output is characterized, while empty input, escaping,
  nulls, Unicode and sender/formatter failures have explicit regression cases.
- **Observability:** real LogRecord tests check event order, stage, retained causes
  and the absence of false completion events on failed delivery.
- **Long-term quality:** Java 17 lint warnings fail compilation; a pinned PMD
  plugin and committed focused ruleset enforce checks during `mvn verify`.
- **Integration:** formatters are interchangeable; transport errors reach callers
  unchanged, enabling a caller to apply a policy without a hidden retry.

## Review decisions

Two one-method interfaces are enough. A format registry, DI framework, background
thread and HTTP client would add requirements absent from this small module.
The generator deliberately catches RuntimeException only at its orchestration
boundary to log stage and preserve the original exception. Errors are not caught.
The CLI deliberately prints the requested report; its SystemPrintln suppression
is local, documented, and does not suppress diagnostics in library components.

PMD results and actual test counts are recorded in `verification/Results.md`.
The original source is an analysis fixture only, never part of the application JAR.
