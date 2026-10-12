import java.util.Map;

// Assignment PDF, pages 3-4. Only the missing import and whitespace were added.
// This comparison fixture is deliberately outside Maven's source directories.
public class ReportGenerator {
    public static String generateReport(Map<String, Object> data, String format) {
        System.out.println("Starting report generation...");
        try { Thread.sleep(1000); } catch (Exception e) {}

        if (format.equals("json")) {
            System.out.println("Generating JSON report...");
            String result = "{";
            for (String key : data.keySet()) {
                result += "\"" + key + "\": \"" + data.get(key) + "\",";
            }
            result = result.substring(0, result.length() - 1) + "}";
            System.out.println(result);
            System.out.println("Sending report to monitoring system...");
            System.out.println("Report sent!");
            return result;
        }

        if (format.equals("csv")) {
            System.out.println("Generating CSV report...");
            String csv = "";
            for (String key : data.keySet()) {
                csv += key + "," + data.get(key) + "\n";
            }
            System.out.println(csv);
            System.out.println("Sending report to monitoring system...");
            System.out.println("Report sent!");
            return csv;
        }

        System.out.println("Unknown format!");
        return null;
    }
}
