töte möglichst viele pfeile sonst töten sie dich

ATAM Methode - Architecture Tradeoff Analysis Method

### Group Exercise:

- Dont Repeat Yourself

- High Cohesion (Charts should be its own object)

- Software Bloodtypes (Charts is T, Core is A)

- CCP+CRP (Charts and Common Core are not gonna be used or changed together)

### Group Exercise 2:

- Ripple Effect from FCA goes to alot of dependencies
- Cycle for APPG ->CHK -> FCA -> APPG
- APPG disregards SRP or High Cohesion
- APC disregards SRP or High Cohesion -> JSON converter block or smth (this is also T and not A so it disregards bloodtypes)
- Too many dependencies in general
- DE1 macht das gleiche wie DE nur weniger -> DRY
- DE should use APPG, not the other way around, since APPG only keeps data, shouldnt calculate anything
- NNW should be part of FCA since it only performs parts of forecasting while FCA is already performing forecasts
- NNW should depend on APPG

7 Points :)

## Home Exercise:

Takes alot of time :')