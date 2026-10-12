package com.codurance.ocp;

import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

class EmployeeShould {

    private static final int BONUS = 100;
    private static final int SALARY = 1000;
    private static final int STOCKS = 10000;

    @Test
    public void not_add_bonus_to_the_engineer_pay_amount() {
        AbstractEmployee employee = EmployeeFactory.create(EmployeeType.ENGINEER, SALARY, BONUS, STOCKS);
        assertThat(employee.payAmount())
            .isEqualTo(SALARY);
    }

    @Test
    public void add_bonus_to_the_manager_pay_amount() {
        AbstractEmployee employee = EmployeeFactory.create(EmployeeType.MANAGER, SALARY, BONUS, STOCKS);
        assertThat(employee.payAmount())
            .isEqualTo(SALARY + BONUS);
    }

    @Test
    public void add_bonus_and_stocks_for_clevel_pay_amount() {
        AbstractEmployee employee = EmployeeFactory.create(EmployeeType.CLEVEL, SALARY, BONUS, STOCKS);
        assertThat(employee.payAmount())
            .isEqualTo(BONUS + STOCKS);
    }
}