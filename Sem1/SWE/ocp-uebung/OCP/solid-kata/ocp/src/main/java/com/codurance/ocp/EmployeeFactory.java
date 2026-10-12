package com.codurance.ocp;

public class EmployeeFactory {
    public static AbstractEmployee create(EmployeeType type, int salary, int bonus, int stocks) {
        if (type == EmployeeType.MANAGER) {
            return new Manager(salary, bonus);
        } else if (type == EmployeeType.ENGINEER) {
            return new Engineer(salary);
        } else if (type == EmployeeType.CLEVEL) {
            return new CLevel(bonus, stocks);
        }
        throw new IllegalArgumentException("Invalid employee type");
    }
}