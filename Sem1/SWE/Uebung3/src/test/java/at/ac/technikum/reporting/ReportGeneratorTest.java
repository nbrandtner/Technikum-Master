package at.ac.technikum.reporting;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.LogRecord;
import java.util.stream.Stream;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

class ReportGeneratorTest {
    @ParameterizedTest
    @MethodSource("formatters")
    void returnsExactlyTheReportDeliveredOnce(ReportFormatter formatter) {
        List<String> delivered = new ArrayList<>();
        Map<String, Object> data = Map.of("count", 3);
        ReportGenerator generator = new ReportGenerator(formatter, delivered::add);
        String report = generator.generateReport(data);
        assertEquals(formatter.format(data), report);
        assertEquals(List.of(report), delivered);
    }

    static Stream<ReportFormatter> formatters() {
        return Stream.of(new JsonReportFormatter(), new CsvReportFormatter());
    }

    @Test
    void acceptsANewFormatterWithoutChangingCoreCodeAndFormatsBeforeSending() {
        List<String> events = new ArrayList<>();
        Map<String, Object> data = Map.of("key", "value");
        ReportFormatter customFormatter = input -> {
            assertSame(data, input);
            events.add("format");
            return "custom report";
        };
        ReportGenerator generator = new ReportGenerator(customFormatter, report -> events.add("send:" + report));
        assertEquals("custom report", generator.generateReport(data));
        assertEquals(List.of("format", "send:custom report"), events);
    }

    @Test
    void propagatesAndLogsFormatterFailureWithoutSending() {
        IllegalArgumentException failure = new IllegalArgumentException("bad input");
        List<String> delivered = new ArrayList<>();
        ReportGenerator generator = new ReportGenerator(input -> { throw failure; }, delivered::add);
        try (LogCapture logs = new LogCapture(ReportGenerator.class)) {
            assertSame(failure, assertThrows(IllegalArgumentException.class,
                    () -> generator.generateReport(Map.of())));
            assertTrue(delivered.isEmpty());
            LogRecord error = logs.records.get(logs.records.size() - 1);
            assertEquals(Level.SEVERE, error.getLevel());
            assertEquals("event=report_generation_failed stage=format", error.getMessage());
            assertSame(failure, error.getThrown());
            assertFalse(logs.records.stream().anyMatch(record -> record.getMessage().contains("completed")));
        }
    }

    @Test
    void propagatesAndLogsSenderFailureWithoutRetrying() {
        IllegalStateException failure = new IllegalStateException("monitor unavailable");
        List<String> attempted = new ArrayList<>();
        ReportGenerator generator = new ReportGenerator(new JsonReportFormatter(), report -> {
            attempted.add(report);
            throw failure;
        });
        try (LogCapture logs = new LogCapture(ReportGenerator.class)) {
            assertSame(failure, assertThrows(IllegalStateException.class,
                    () -> generator.generateReport(Map.of("count", 3))));
            assertEquals(1, attempted.size());
            LogRecord error = logs.records.get(logs.records.size() - 1);
            assertEquals("event=report_generation_failed stage=send", error.getMessage());
            assertSame(failure, error.getThrown());
            assertFalse(logs.records.stream().anyMatch(record -> record.getMessage().contains("completed")));
        }
    }

    @Test
    void recordsSuccessfulEventsWithoutLoggingTheReportPayload() {
        ReportGenerator generator = new ReportGenerator(new JsonReportFormatter(), report -> { });
        try (LogCapture logs = new LogCapture(ReportGenerator.class)) {
            generator.generateReport(Map.of("secret", "private-payload"));
            assertEquals(2, logs.records.size());
            assertTrue(logs.records.get(0).getMessage().contains("started"));
            assertTrue(logs.records.get(1).getMessage().contains("completed"));
            assertFalse(logs.records.stream().anyMatch(record -> record.getMessage().contains("private-payload")));
        }
    }

    @Test
    void rejectsNullFormatter() {
        assertThrows(NullPointerException.class, () -> new ReportGenerator(null, report -> { }));
    }

    @Test
    void rejectsNullSender() {
        assertThrows(NullPointerException.class, () -> new ReportGenerator(new JsonReportFormatter(), null));
    }

    @Test
    void rejectsNullInputWithoutFormattingOrSending() {
        List<String> events = new ArrayList<>();
        ReportGenerator generator = new ReportGenerator(input -> {
            events.add("format");
            return "report";
        }, report -> events.add("send"));
        assertThrows(NullPointerException.class, () -> generator.generateReport(null));
        assertTrue(events.isEmpty());
    }

    @Test
    void rejectsANullReportFromACustomFormatterWithoutSending() {
        List<String> delivered = new ArrayList<>();
        ReportGenerator generator = new ReportGenerator(input -> null, delivered::add);
        assertThrows(NullPointerException.class, () -> generator.generateReport(Map.of()));
        assertTrue(delivered.isEmpty());
    }

    @ParameterizedTest
    @MethodSource("formatters")
    void sendsAnEmptyInputReportOnce(ReportFormatter formatter) {
        List<String> delivered = new ArrayList<>();
        ReportGenerator generator = new ReportGenerator(formatter, delivered::add);
        String result = generator.generateReport(Map.of());
        assertEquals(List.of(formatter.format(Map.of())), delivered);
        assertEquals(delivered.get(0), result);
    }
}
