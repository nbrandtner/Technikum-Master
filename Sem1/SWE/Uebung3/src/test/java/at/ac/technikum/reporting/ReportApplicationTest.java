package at.ac.technikum.reporting;

import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class ReportApplicationTest {
    @Test
    void rejectsAnUnknownFormatBeforeGeneratingOrSending() {
        assertThrows(IllegalArgumentException.class, () -> ReportApplication.main(new String[]{"xml"}));
    }

    @Test
    void rejectsExtraArguments() {
        assertThrows(IllegalArgumentException.class, () -> ReportApplication.main(new String[]{"json", "csv"}));
    }
}
