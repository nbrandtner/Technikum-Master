package at.ac.technikum.reporting;

import java.util.Map;
import java.util.Objects;
import java.util.logging.Level;
import java.util.logging.Logger;

/** Coordinates one formatting operation followed by one synchronous delivery. */
public final class ReportGenerator {
    private static final Logger LOGGER = Logger.getLogger(ReportGenerator.class.getName());
    private final ReportFormatter formatter;
    private final ReportSender sender;

    public ReportGenerator(ReportFormatter formatter, ReportSender sender) {
        this.formatter = Objects.requireNonNull(formatter, "formatter must not be null");
        this.sender = Objects.requireNonNull(sender, "sender must not be null");
    }

    /**
     * Formats, sends once, and returns exactly the delivered text.
     * Failures are logged and propagated unchanged; delivery is never retried here.
     *
     * @param data non-null flat report data
     * @return the report after successful delivery
     * @throws RuntimeException if validation, formatting or delivery fails
     */
    public String generateReport(Map<String, Object> data) {
        Objects.requireNonNull(data, "data must not be null");
        LOGGER.log(Level.INFO, "event=report_generation_started entries={0}", data.size());
        String stage = "format";
        try {
            String report = Objects.requireNonNull(formatter.format(data), "formatter returned null");
            stage = "send";
            sender.send(report);
            LOGGER.log(Level.INFO, "event=report_generation_completed characters={0}", report.length());
            return report;
        } catch (RuntimeException failure) {
            // This orchestration boundary records context and preserves the original cause.
            LOGGER.log(Level.SEVERE, "event=report_generation_failed stage=" + stage, failure);
            throw failure;
        }
    }
}
