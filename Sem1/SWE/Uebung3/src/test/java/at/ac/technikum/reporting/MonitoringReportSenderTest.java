package at.ac.technikum.reporting;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

class MonitoringReportSenderTest {
    @Test
    void deliversTheExactPayloadOnceAndRecordsCompletion() {
        List<String> delivered = new ArrayList<>();
        ReportSender sender = new MonitoringReportSender(delivered::add);
        try (LogCapture logs = new LogCapture(MonitoringReportSender.class)) {
            sender.send("report text");
            assertEquals(List.of("report text"), delivered);
            assertEquals(2, logs.records.size());
            assertTrue(logs.records.get(0).getMessage().contains("started"));
            assertEquals("event=monitoring_send_completed status=success", logs.records.get(1).getMessage());
        }
    }

    @Test
    void propagatesTransportFailureWithoutAFalseSuccessEvent() {
        IllegalStateException failure = new IllegalStateException("delivery failed");
        ReportSender sender = new MonitoringReportSender(report -> { throw failure; });
        try (LogCapture logs = new LogCapture(MonitoringReportSender.class)) {
            assertSame(failure, assertThrows(IllegalStateException.class, () -> sender.send("report")));
            assertEquals(1, logs.records.size());
            assertFalse(logs.records.stream().anyMatch(record -> record.getMessage().contains("completed")));
        }
    }

    @Test
    void acceptsEmptyReports() {
        List<String> delivered = new ArrayList<>();
        new MonitoringReportSender(delivered::add).send("");
        assertEquals(List.of(""), delivered);
    }

    @Test
    void rejectsNullTransport() {
        assertThrows(NullPointerException.class, () -> new MonitoringReportSender(null));
    }

    @Test
    void rejectsNullReportBeforeDelivery() {
        List<String> delivered = new ArrayList<>();
        ReportSender sender = new MonitoringReportSender(delivered::add);
        assertThrows(NullPointerException.class, () -> sender.send(null));
        assertTrue(delivered.isEmpty());
    }
}
