# Relationships

> Total Relationships: 14

## Entity Relationship Diagram

```mermaid
erDiagram
    Date ||--o{ Employee : "date"
    FP ||--o{ Employee : "FP"
    Ethnicity ||--o{ Employee : "EthnicGroup"
    Gender ||--o{ Employee : "Gender"
    PayType ||--o{ Employee : "PayTypeID"
    BU ||--o{ Employee : "BU"
    AgeGroup ||--o{ Employee : "AgeGroupID"
    SeparationReason ||--o{ Employee : "TermReason"
    LocalDateTable_6f19fed3_1fc0_4f7a_878d_34aca93d6782 ||--o{ Date : "Date"
    LocalDateTable_d2ea5b26_668d_4c17_b228_695669b066a6 ||--o{ Date : "MonthStartDate"
    LocalDateTable_c9dde99e_7ac1_4e8e_a5f2_c5ffc41d9cac ||--o{ Date : "MonthEndDate"
    LocalDateTable_cc28ef26_f63a_4bc3_b357_93ab34cd6d9b ||--o{ Employee : "TermDate"
    LocalDateTable_c04ce649_6e25_466f_9bbc_faabfec0fe29 ||--o{ Employee : "HireDate"
    Separation_Reasons ||--o{ SeparationReason : "SeparationTypeID"
    DateTableTemplate_92fd358c_bb4c_4d52_9f5b_e9a59dc2315d {
        string placeholder
    }
```

## Relationship Details

| From Table | From Column | To Table | To Column | Active | Cross Filter |
|------------|-------------|----------|-----------|--------|--------------|
| Employee | date | Date | Date | ✓ | OneDirection |
| Employee | FP | FP | FP | ✓ | OneDirection |
| Employee | EthnicGroup | Ethnicity | Ethnic Group | ✓ | OneDirection |
| Employee | Gender | Gender | ID | ✓ | OneDirection |
| Employee | PayTypeID | PayType | PayTypeID | ✓ | OneDirection |
| Employee | BU | BU | BU | ✓ | OneDirection |
| Employee | AgeGroupID | AgeGroup | AgeGroupID | ✓ | OneDirection |
| Employee | TermReason | SeparationReason | SeparationTypeID | ✓ | OneDirection |
| Date | Date | LocalDateTable_6f19fed3-1fc0-4f7a-878d-34aca93d6782 | Date | ✓ | OneDirection |
| Date | MonthStartDate | LocalDateTable_d2ea5b26-668d-4c17-b228-695669b066a6 | Date | ✓ | OneDirection |
| Date | MonthEndDate | LocalDateTable_c9dde99e-7ac1-4e8e-a5f2-c5ffc41d9cac | Date | ✓ | OneDirection |
| Employee | TermDate | LocalDateTable_cc28ef26-f63a-4bc3-b357-93ab34cd6d9b | Date | ✓ | OneDirection |
| Employee | HireDate | LocalDateTable_c04ce649-6e25-466f-9bbc-faabfec0fe29 | Date | ✓ | OneDirection |
| SeparationReason | SeparationTypeID | Separation Reasons | SeparationTypeID | ✓ | BothDirections |

---

[← Back to Home](Home.md)
