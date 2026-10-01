package com.codurance.ocp;

abstract public class AbstractEmployee {
    protected EmployeeType type;

    public abstract int payAmount();
    public EmployeeType getType() {
        return type;
    }
}