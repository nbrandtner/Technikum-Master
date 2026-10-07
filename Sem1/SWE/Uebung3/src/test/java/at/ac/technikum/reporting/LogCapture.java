package at.ac.technikum.reporting;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Handler;
import java.util.logging.Level;
import java.util.logging.LogRecord;
import java.util.logging.Logger;

/** Captures real JUL records and restores shared logger state after each test. */
final class LogCapture extends Handler implements AutoCloseable {
    final List<LogRecord> records = new ArrayList<>();
    private final Logger logger;
    private final Level previousLevel;
    private final boolean previousParentHandlers;

    LogCapture(Class<?> source) {
        logger = Logger.getLogger(source.getName());
        previousLevel = logger.getLevel();
        previousParentHandlers = logger.getUseParentHandlers();
        logger.setLevel(Level.ALL);
        logger.setUseParentHandlers(false);
        logger.addHandler(this);
    }

    @Override
    public void publish(LogRecord record) {
        records.add(record);
    }

    @Override
    public void flush() {
        // Records are kept in memory, so no flush is needed.
    }

    @Override
    public void close() {
        logger.removeHandler(this);
        logger.setLevel(previousLevel);
        logger.setUseParentHandlers(previousParentHandlers);
    }
}
