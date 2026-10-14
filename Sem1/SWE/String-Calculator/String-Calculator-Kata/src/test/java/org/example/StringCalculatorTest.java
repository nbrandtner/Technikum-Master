package org.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class StringCalculatorTest {

    // Step 1: Empty string, one number, and two numbers.
    @Test
    void step1_emptyStringReturnsZero() {
        assertEquals(0, Main.Add(""));
    }

    @Test
    void step1_oneNumberReturnsThatNumber() {
        assertEquals(1, Main.Add("1"));
    }

    @Test
    void step1_twoNumbersReturnTheirSum() {
        assertEquals(3, Main.Add("1,2"));
    }

    // Step 2: Any amount of numbers.
    @Test
    void step2_addsMoreThanTwoNumbers() {
        assertEquals(15, Main.Add("1,2,3,4,5"));
    }

    @Test
    void step2_handlesZeroAmongNumbers() {
        assertEquals(9, Main.Add("2,3,0,4"));
    }

    // Step 3: Newlines can separate numbers too.
    @Test
    void step3_addsNumbersSeparatedByNewlines() {
        assertEquals(6, Main.Add("1\n2\n3"));
    }

    @Test
    void step3_addsNumbersSeparatedByNewlinesAndCommas() {
        assertEquals(6, Main.Add("1\n2,3"));
    }

    // Step 4: An optional header defines a custom delimiter.
    @Test
    void step4_usesCustomDelimiter() {
        assertEquals(3, Main.Add("//;\n1;2"));
    }

    @Test
    void step4_newlinesStillWorkWithCustomDelimiter() {
        assertEquals(6, Main.Add("//;\n1\n2;3"));
    }

    @Test
    void step4_headerIsOptional() {
        assertEquals(6, Main.Add("1,2\n3"));
    }

    // Step 5: Reject negatives and include all of them in the message.
    @Test
    void step5_rejectsOneNegativeNumber() {
        IllegalArgumentException exception = assertThrows(
                IllegalArgumentException.class, () -> Main.Add("-1,2"));

        assertEquals("negatives not allowed: [-1]", exception.getMessage());
    }

    @Test
    void step5_listsAllNegativeNumbers() {
        IllegalArgumentException exception = assertThrows(
                IllegalArgumentException.class, () -> Main.Add("1,-2\n-3"));

        assertEquals("negatives not allowed: [-2, -3]", exception.getMessage());
    }

    @Test
    void step5_rejectsNegativesWithCustomDelimiter() {
        IllegalArgumentException exception = assertThrows(
                IllegalArgumentException.class, () -> Main.Add("//;\n-1;2;-3"));

        assertEquals("negatives not allowed: [-1, -3]", exception.getMessage());
    }

    // Step 6: Ignore numbers greater than 1000, but include 1000.
    @Test
    void step6_ignoresNumbersGreaterThan1000() {
        assertEquals(2, Main.Add("2,1001"));
    }

    @Test
    void step6_includesExactly1000() {
        assertEquals(1002, Main.Add("1000,1001,2"));
    }

    @Test
    void step6_returnsZeroWhenAllNumbersAreIgnored() {
        assertEquals(0, Main.Add("1001,2000"));
    }

    @Test
    void step6_stillRejectsLargeNegativeNumbers() {
        IllegalArgumentException exception = assertThrows(
                IllegalArgumentException.class, () -> Main.Add("-1001,1001"));

        assertEquals("negatives not allowed: [-1001]", exception.getMessage());
    }

    // Step 7: A bracketed delimiter can have any length.
    @Test
    void step7_usesLongDelimiter() {
        assertEquals(6, Main.Add("//[***]\n1***2***3"));
    }

    @Test
    void step7_usesDelimiterMadeOfDifferentCharacters() {
        assertEquals(6, Main.Add("//[abc]\n1abc2abc3"));
    }

    @Test
    void step7_usesSingleCharacterInBrackets() {
        assertEquals(3, Main.Add("//[.]\n1.2"));
    }

    // Step 8: Multiple single-character delimiters.
    @Test
    void step8_usesMultipleDelimiters() {
        assertEquals(6, Main.Add("//[*][%]\n1*2%3"));
    }

    @Test
    void step8_treatsSpecialCharactersAsLiteralDelimiters() {
        assertEquals(6, Main.Add("//[.][|]\n1.2|3"));
    }

    // Step 9: Multiple delimiters can also be longer than one character.
    @Test
    void step9_usesMultipleLongDelimiters() {
        assertEquals(6, Main.Add("//[***][%%]\n1***2%%3"));
    }

    @Test
    void step9_usesDelimitersOfDifferentLengths() {
        assertEquals(10, Main.Add("//[***][%][;;]\n1***2%3;;4"));
    }

    @Test
    void step9_handlesDelimitersThatShareAPrefix() {
        assertEquals(6, Main.Add("//[*][**]\n1**2*3"));
    }
}
