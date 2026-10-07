package at.ac.technikum.reporting;

import java.util.Map;

/** Converts flat report data into text without logging, sending or changing it. */
@FunctionalInterface
public interface ReportFormatter {
    /**
     * Preserves the map's iteration order and converts values with String.valueOf.
     * Null values become the text "null"; the map and its keys must be non-null.
     *
     * @param data flat report fields
     * @return non-null formatted report; an empty map is valid
     * @throws NullPointerException if the map or a key is null
     */
    String format(Map<String, Object> data);
}
