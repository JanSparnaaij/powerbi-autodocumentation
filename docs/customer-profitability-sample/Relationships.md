# Relationships

> Total Relationships: 9

## Entity Relationship Diagram

```mermaid
erDiagram
    BU ||--o{ Fact : "BU Key"
    Date ||--o{ Fact : "YearPeriod"
    Scenario ||--o{ Fact : "Scenario Key"
    Product ||--o{ Fact : "Product Key"
    Customer ||--o{ Fact : "Customer Key"
    Executive ||--o{ BU : "Executive_id"
    Industry ||--o{ Customer : "Industry ID"
    State ||--o{ Customer : "State"
    LocalDateTable_39c22ddb_27f3_4e6c_8a44_a3380850fcb4 ||--o{ Date : "Date"
    DateTableTemplate_fe310476_3bb5_422b_85ff_9fd23f2cad67 {
        string placeholder
    }
```

## Relationship Details

| From Table | From Column | To Table | To Column | Active | Cross Filter |
|------------|-------------|----------|-----------|--------|--------------|
| Fact | BU Key | BU | BU Key | ✓ | OneDirection |
| Fact | YearPeriod | Date | YearPeriod | ✓ | OneDirection |
| Fact | Scenario Key | Scenario | Scenario Key | ✓ | OneDirection |
| Fact | Product Key | Product | Product Key | ✓ | OneDirection |
| Fact | Customer Key | Customer | Customer | ✓ | OneDirection |
| BU | Executive_id | Executive | ID | ✓ | OneDirection |
| Customer | Industry ID | Industry | ID | ✓ | OneDirection |
| Customer | State | State | StateCode | ✓ | OneDirection |
| Date | Date | LocalDateTable_39c22ddb-27f3-4e6c-8a44-a3380850fcb4 | Date | ✓ | OneDirection |

---

[← Back to Home](Home.md)
