package at.ac.technikum.reporting;

/** Delivers a formatted report; returning normally means delivery completed. */
@FunctionalInterface
public interface ReportSender {
    /**
     * @param report non-null report, possibly empty
     * @throws NullPointerException if report is null
     * @throws RuntimeException if delivery fails; implementations must propagate failures
     */
    void send(String report);
}
