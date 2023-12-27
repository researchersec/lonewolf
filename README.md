[![UpDays](https://github.com/researchersec/lonewolf/actions/workflows/update-days.yml/badge.svg)](https://github.com/researchersec/lonewolf/actions/workflows/update-days.yml)


[![Test SQLite](https://github.com/researchersec/lonewolf/actions/workflows/sqlite.yml/badge.svg)](https://github.com/researchersec/lonewolf/actions/workflows/sqlite.yml)


| Table       | Columns                                   |
|-------------------|-------------------------------------------|
| pricing_data      | id (INTEGER, PRIMARY KEY AUTOINCREMENT),  |
|                   | timestamp (TEXT)                          |
| items             | id (INTEGER, PRIMARY KEY AUTOINCREMENT),  |
|                   | item_id (INTEGER),                        |
|                   | item_name (TEXT)                          |
| pricing_details   | id (INTEGER, PRIMARY KEY AUTOINCREMENT),  |
|                   | pricing_id (INTEGER, FOREIGN KEY),        |
|                   | item_id (INTEGER, FOREIGN KEY),           |
|                   | price (INTEGER)                           |
