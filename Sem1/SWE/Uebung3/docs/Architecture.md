# Phase 2 - Architecture and behavior contract

```text
ReportApplication (composition root / CLI)
  -> ReportGenerator
       -> ReportFormatter
            <- JsonReportFormatter
            <- CsvReportFormatter
       -> ReportSender
            <- MonitoringReportSender -> injected Consumer<String> transport
```

- **SRP:** formatters serialize; the sender delivers; the generator coordinates.
- **OCP:** inject a new ReportFormatter without changing ReportGenerator.
  The CLI's json/csv selection is an explicit composition choice, not core logic.
- **ISP / DIP:** each interface has one operation; the generator's dependencies
  are supplied through its constructor and stored in final fields.
- **LSP:** both formatters accept the same flat-map contract, return non-null
  strings, preserve iteration order and reject null maps/keys consistently.
- **DRY / KISS / YAGNI:** one format-then-send path, no sleep, registry, framework,
  retry policy, configuration system or speculative network protocol.
- **Observability:** JDK logging uses levels and stable key=value event/stage
  fields, counts and original exceptions. Payloads are not logged. JUL's default
  handler adds human-readable timestamps; this is event logging, not JSON logs.
- **Error handling:** fail fast for null dependencies/data/keys, reject invalid
  CLI formats, log formatting/delivery failures at the generator boundary and
  rethrow the same exception. A success event follows successful delivery only.

## Preserved behavior and explicit corrections

| Case | Behavior |
| --- | --- |
| Ordinary JSON | Exact legacy layout: `{"status": "OK","count": "3"}` |
| Ordinary CSV | Headerless `key,value` rows with trailing LF, as before |
| Object and null values | `String.valueOf(value)`; JSON numbers/booleans/null remain strings |
| Ordering | The map's iteration order; use LinkedHashMap for deterministic insertion order |
| Empty input | Correct JSON `{}`; CSV empty text; both can be sent |
| Special characters | Correct JSON escaping and CSV quoting; deliberate bug fixes |
| Invalid input / format | Explicit exception rather than a null success result |
| API | Instance generator with injected strategies replaces static `(data, format)` API |
| Operational effects | Delay and diagnostic prints removed; structured events added |
| Monitoring | Original had only print statements; demo uses an explicitly labeled local simulation |

This is a flat textual report, not general object-graph serialization. JSON
escaping covers quotes, backslashes, all U+0000-U+001F controls and UTF-16
surrogate units. CSV quoting covers commas, quotes, CR and LF. Consumers needing
spreadsheet formula neutralization or a different line-ending policy can add a
specialized formatter when those requirements exist.

The formatters contain no IO and do not mutate input. Callers must not mutate
data concurrently. Sending is synchronous; the transport's return/failure defines
completion. Real network delivery requires a supplied transport with its own
timeout and exception policy. No external transmission is attempted by the demo.
