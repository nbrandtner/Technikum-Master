package org.example;

import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        System.out.println(Add("//[***][%]\n1***2%3"));
    }

    public static int Add(String numbers) {
        if (numbers == null || numbers.isEmpty()) {
            return 0;
        }

        if (numbers.startsWith("//")) {
            int lineEnd = numbers.indexOf('\n');
            String header = numbers.substring(2, lineEnd);
            numbers = numbers.substring(lineEnd + 1);

            String[] delimiters = {header};
            if (header.startsWith("[")) {
                delimiters = header.substring(1, header.length() - 1).split("\\]\\[");
            }

            // Replace longer delimiters first, then shorter ones.
            for (int length = header.length(); length > 0; length--) {
                for (String delimiter : delimiters) {
                    if (delimiter.length() == length) {
                        numbers = numbers.replace(delimiter, ",");
                    }
                }
            }
        }

        numbers = numbers.replace('\n', ',');
        if (numbers.isEmpty()) {
            return 0;
        }

        int sum = 0;
        List<Integer> negatives = new ArrayList<>();
        for (String part : numbers.split(",", -1)) {
            int number = Integer.parseInt(part.trim());
            if (number < 0) {
                negatives.add(number);
            } else if (number <= 1000) {
                sum += number;
            }
        }

        if (!negatives.isEmpty()) {
            throw new IllegalArgumentException("negatives not allowed: " + negatives);
        }
        return sum;
    }
}
