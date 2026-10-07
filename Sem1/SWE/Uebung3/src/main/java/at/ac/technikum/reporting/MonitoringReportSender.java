package at.ac.technikum.reporting;

import java.util.Objects;
import java.util.function.Consumer;
import java.util.logging.Level;
import java.util.logging.Logger;

/** Adds monitoring delivery events around an injected synchronous transport. */
public final class MonitoringReportSender implements ReportSender {
    private static final Logger LOGGER = Logger.getLogger(MonitoringReportSender.class.getName());
    private final Consumer<String> transport;

    public MonitoringReportSender(Consumer<String> transport) {
        this.transport = Objects.requireNonNull(transport, "transport must not be null");
    }

    @Override
    public void send(String report) {
        Objects.requireNonNull(report, "report must not be null");
        LOGGER.log(Level.INFO, "event=monitoring_send_started characters={0}", report.length());
        transport.accept(report);
        LOGGER.info("event=monitoring_send_completed status=success");
    }
}
