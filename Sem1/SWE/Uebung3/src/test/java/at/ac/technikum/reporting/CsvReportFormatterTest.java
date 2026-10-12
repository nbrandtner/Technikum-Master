package at.ac.technikum.reporting;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.stream.Stream;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

class CsvReportFormatterTest {
    private final ReportFormatter formatter = new CsvReportFormatter();

    @Test
    void preservesOriginalOrdinaryOutputAndIterationOrder() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("status", "OK");
        data.put("count", 3);
        data.put("active", true);
        assertEquals("status,OK\ncount,3\nactive,true\n", formatter.format(data));
    }

    @Test
    void formatsEmptyInputAsEmptyText() {
        assertEquals("", formatter.format(Map.of()));
    }

    @ParameterizedTest
    @MethodSource("specialFields")
    void escapesCsvKeysAndValues(String field, String escaped) {
        assertEquals(escaped + "," + escaped + "\n", formatter.format(Map.of(field, field)));
    }

    static Stream<Arguments> specialFields() {
        return Stream.of(
                Arguments.of("a,b", "\"a,b\""),
                Arguments.of("a\"b", "\"a\"\"b\""),
                Arguments.of("a\nb", "\"a\nb\""),
                Arguments.of("a\rb", "\"a\rb\""),
                Arguments.of("a\r\nb", "\"a\r\nb\""),
                Arguments.of("", ""),
                Arguments.of("Wien \u00e4", "Wien \u00e4"));
    }

    @Test
    void preservesNullValueAsTheStringNull() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("missing", null);
        assertEquals("missing,null\n", formatter.format(data));
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
