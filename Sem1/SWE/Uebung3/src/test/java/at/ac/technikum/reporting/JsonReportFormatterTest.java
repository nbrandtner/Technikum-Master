package at.ac.technikum.reporting;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.LinkedHashMap;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class JsonReportFormatterTest {
    private final ReportFormatter formatter = new JsonReportFormatter();

    @Test
    void preservesOriginalOrdinaryOutputAndIterationOrder() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("status", "OK");
        data.put("count", 3);
        data.put("active", true);
        assertEquals("{\"status\": \"OK\",\"count\": \"3\",\"active\": \"true\"}", formatter.format(data));
    }

    @Test
    void formatsEmptyInputAsAnEmptyObject() {
        assertEquals("{}", formatter.format(Map.of()));
    }

    @Test
    void escapesQuotesAndBackslashesInKeysAndValues() {
        assertEquals("{\"a\\\"\\\\\": \"b\\\"\\\\\"}", formatter.format(Map.of("a\"\\", "b\"\\")));
    }

    @ParameterizedTest
    @CsvSource({"0, 0000", "8, 0008", "9, 0009", "10, 000a", "12, 000c", "13, 000d", "31, 001f"})
    void escapesJsonControlCharacters(int codePoint, String hexadecimal) {
        String value = String.valueOf((char) codePoint);
        assertEquals("{\"value\": \"\\u" + hexadecimal + "\"}", formatter.format(Map.of("value", value)));
    }

    @Test
    void preservesUnicodeAndEscapesSurrogatePairs() {
        assertEquals("{\"city\": \"Wien \u00e4 \\ud83d\\ude42\"}",
                formatter.format(Map.of("city", "Wien \u00e4 \ud83d\ude42")));
    }

    @Test
    void preservesNullValueAsTheStringNull() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("missing", null);
        assertEquals("{\"missing\": \"null\"}", formatter.format(data));
    }

    @Test
    void preservesObjectToStringBehavior() {
        assertEquals("{\"version\": \"17\"}", formatter.format(Map.of("version", new StringBuilder("17"))));
    }

    @Test
    void rejectsNullData() {
        assertThrows(NullPointerException.class, () -> formatter.format(null));
    }

    @Test
    void rejectsNullKeys() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put(null, "value");
        assertThrows(NullPointerException.class, () -> formatter.format(data));
    }

    @Test
    void leavesTheInputUnchanged() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("status", "OK");
        Map<String, Object> original = new LinkedHashMap<>(data);
        formatter.format(data);
        assertEquals(original, data);
    }
}
