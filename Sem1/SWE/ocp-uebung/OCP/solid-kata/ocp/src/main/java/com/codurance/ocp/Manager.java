package com.codurance.ocp;

public class Manager extends AbstractEmployee {

    private int salary;
    private int bonus;

    Manager(int salary, int bonus) {
        this.salary = salary;
        this.bonus = bonus;
        this.type = EmployeeType.MANAGER;
    }

    public int payAmount() {
        return salary + bonus;
    }
}