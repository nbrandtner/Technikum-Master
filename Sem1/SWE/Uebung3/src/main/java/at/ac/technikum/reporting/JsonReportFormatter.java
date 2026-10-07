package at.ac.technikum.reporting;

import java.util.Locale;
import java.util.Map;
import java.util.Objects;
import java.util.StringJoiner;

/** Serializes a flat map as a JSON object whose values are strings. */
public final class JsonReportFormatter implements ReportFormatter {
    @Override
    public String format(Map<String, Object> data) {
        Objects.requireNonNull(data, "data must not be null");
        StringJoiner fields = new StringJoiner(",", "{", "}");
        for (Map.Entry<String, Object> entry : data.entrySet()) {
            String key = Objects.requireNonNull(entry.getKey(), "report keys must not be null");
            fields.add(quote(key) + ": " + quote(String.valueOf(entry.getValue())));
        }
        return fields.toString();
    }

    private static String quote(String value) {
        StringBuilder escaped = new StringBuilder().append('"');
        for (int index = 0; index < value.length(); index++) {
            char character = value.charAt(index);
            if (character == '"' || character == '\\') {
                escaped.append('\\').append(character);
            } else if (character < 0x20 || Character.isSurrogate(character)) {
                // Escape controls and UTF-16 surrogate units, including emoji pairs.
                escaped.append(String.format(Locale.ROOT, "\\u%04x", (int) character));
            } else {
                escaped.append(character);
            }
        }
        return escaped.append('"').toString();
    }
}
