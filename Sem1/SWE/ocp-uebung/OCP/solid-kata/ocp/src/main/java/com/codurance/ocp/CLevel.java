package com.codurance.ocp;

public class CLevel extends AbstractEmployee {

    private int bonus;
    private int stocks;


    CLevel(int bonus, int stocks) {
        this.bonus = bonus;
        this.stocks = stocks;
        this.type = EmployeeType.CLEVEL;
    }

    public int payAmount() {
        return stocks + bonus;
    }

}