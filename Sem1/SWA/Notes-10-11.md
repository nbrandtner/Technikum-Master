Blutgruppen A, T, 0
Services indentifizieren
Subsysteme

Notes for next time:
How do I evaluate and describe an architecture
ATAM Architecture Tradeoff Analysis Method, for measuring how good architecture is:
-> Change Request: percentage of components that dont have to be changed. higher is better ofc
!!Zu jeder Schnittstelle, 2 Dokumentationen, Implementation-Comments und Interface-Comments

Group Exercise:
How to measure good Architecture:

- Zyklisch
- Möglichst wenig Dependencies (Wie viele Dependencies im Vergleich zu wie viele Komponenten)
- DRY
- KISS
- SRP
- SOLID

ATAM:

- Enter playing Ability of MateMate
    - 57.1%
- Simplified Blitz Chess (5 Sec per Turn otherwise game is over)
    - 71.4%
- Choose between classical and neural evaluation
    - 57.1%
- Letter Chess - Input via Email
    - 85.7%
- Chess 960 - Starting Positions is chosen at random out of 960 different ones.
    - 85.7%
- Dame soll spielbar sein
    - 71.4%
- Märchenschach - Anderes Board, Andere Figuren, Andere Regeln
    - 42.8%

Describe an Interface:
ISearchProduct: Enter Search Query ("Alle Produkte unter 100ml"->"Champagner oder so")
Diese Schnittstelle beschreiben für Benutzer, nicht für Programmierer

Description:
GET Request

- Authentifizierung:
    - API Key
- Parameters:
    - Search String
- Output:
    - Result String
- Search String Structure:
    - JSON Structure
        - Contain
        - !Contain
        - Calories
        - Weight
        - Volume
        - FoodPreference
            - Vegetarian, Vegan, Kosher, Halal
        - Nutrients
        - Vitamins
        - Cuisine
            - Italian, French
        - Alcohol
- Output String Structure:
    - JSON Structure
        - Result Array with Parameters, Pagination

XXXXXXXXXXXXXXX
