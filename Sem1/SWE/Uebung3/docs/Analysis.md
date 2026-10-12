# Phase 1 - Analysis of the original Java module

Source: `Class 3 - Assignment-SWEN.pdf`, pages 3-4. These are manual findings,
not an invented static-analysis count. The comparison source is in `docs/original`.

1. **SRP / bloater:** one method validates, selects a format, serializes, prints,
   simulates delivery and handles failures. Several reasons to change share one unit.
2. **OCP / change preventer:** adding a format requires editing the generator's
   conditional branches rather than adding a formatter implementation.
3. **DIP / coupling:** the generator directly depends on console output and a
   concrete sending procedure, with no injectable formatting or delivery boundary.
4. **ISP / missing abstraction:** there are no small contracts for clients that
   only need formatting or sending; they must call the entire workflow.
5. **DRY / duplication:** the two branches repeat the report-printing and send
   messages. A delivery change must be made twice.
6. **KISS / dispensable:** an unconditional one-second sleep adds latency without
   serving report generation or any stated requirement.
7. **Error handling / refactoring discipline:** the empty broad catch silently
   consumes failures, including InterruptedException, losing interruption intent.
8. **Performance / clean code:** `+=` in each loop repeatedly copies growing
   strings; a builder or joiner expresses accumulation directly.
9. **Correctness / function contract:** empty JSON input produces `}` because the
   code blindly removes the last character of `{`.
10. **Correctness / boundary validation:** JSON keys and values are not escaped;
    quotes, backslashes and control characters can produce invalid JSON.
11. **Correctness / boundary validation:** CSV fields containing commas, quotes
    or line breaks are not quoted, changing the apparent columns or rows.
12. **Explicit contracts / clean code:** unknown formats return null, while a
    null format crashes at equals and null data fails later inside a branch.
13. **Readability / primitive obsession:** magic format strings and generic names
    such as `result` obscure the separate formatting and delivery intentions.
14. **Observability:** global prints lack levels and stable event fields; success
    is announced without an actual destination and report contents are printed.
15. **Testability / encapsulation:** the static method's console side effects,
    hard-coded delay and delivery logic prevent isolated, fast failure-path tests.

LSP is a redesign constraint: both implementations must honor one formatter
contract. The original has no subtype hierarchy, so an original LSP violation
would be an unsupported claim. Static analysis cannot prove every SOLID issue.
