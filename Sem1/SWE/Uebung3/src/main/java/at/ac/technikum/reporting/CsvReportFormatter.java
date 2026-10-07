package at.ac.technikum.reporting;

import java.util.Map;
import java.util.Objects;

/** Produces headerless key,value rows, retaining the original LF line ending. */
public final class CsvReportFormatter implements ReportFormatter {
    @Override
    public String format(Map<String, Object> data) {
        Objects.requireNonNull(data, "data must not be null");
        StringBuilder report = new StringBuilder();
        for (Map.Entry<String, Object> entry : data.entrySet()) {
            String key = Objects.requireNonNull(entry.getKey(), "report keys must not be null");
            report.append(escapeField(key)).append(',')
                    .append(escapeField(String.valueOf(entry.getValue()))).append('\n');
        }
        return report.toString();
    }

    private static String escapeField(String value) {
        if (value.indexOf(',') >= 0 || value.indexOf('"') >= 0
                || value.indexOf('\r') >= 0 || value.indexOf('\n') >= 0) {
            return "\"" + value.replace("\"", "\"\"") + "\"";
        }
        return value;
    }
}
