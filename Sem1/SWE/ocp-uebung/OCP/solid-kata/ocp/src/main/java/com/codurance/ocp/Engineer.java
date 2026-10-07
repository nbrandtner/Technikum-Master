package com.codurance.ocp;

public class Engineer extends AbstractEmployee {

    private int salary;
    Engineer(int salary) {
        this.salary = salary;
        this.type = EmployeeType.ENGINEER;
    }

    public int payAmount() {
        return salary;
    }

}