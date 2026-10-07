package at.ac.technikum.reporting;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.logging.Logger;

/** Minimal command-line example with a local, simulated monitoring destination. */
public final class ReportApplication {
    private static final Logger LOGGER = Logger.getLogger(ReportApplication.class.getName());

    private ReportApplication() {
        // Utility entry point; no instances are needed.
    }

    @SuppressWarnings("PMD.SystemPrintln") // CLI report output, not diagnostic logging.
    public static void main(String[] args) {
        if (args.length > 1) {
            throw new IllegalArgumentException("Usage: java -jar exercise3-reporting-1.0.0.jar [json|csv]");
        }
        String format = args.length == 0 ? "json" : args[0];
        ReportFormatter formatter = selectFormatter(format);
        ReportSender sender = new MonitoringReportSender(
                report -> LOGGER.info("event=monitoring_received mode=simulation"));
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("service", "reporting");
        data.put("status", "OK");
        data.put("count", 3);
        String report = new ReportGenerator(formatter, sender).generateReport(data);
        System.out.print(report);
    }

    private static ReportFormatter selectFormatter(String format) {
        return switch (format) {
            case "json" -> new JsonReportFormatter();
            case "csv" -> new CsvReportFormatter();
            default -> throw new IllegalArgumentException("Unsupported report format: " + format);
        };
    }
}
