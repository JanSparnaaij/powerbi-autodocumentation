# Relationships

> Total Relationships: 12

## Entity Relationship Diagram

```mermaid
erDiagram
    LocalDateTable ||--o{ Date : "Date"
    LocalDateTable ||--o{ Date : "Month"
    LocalDateTable ||--o{ Date : "Full Date"
    Customer ||--o{ Sales : "CustomerKey"
    Product ||--o{ Sales : "ProductKey"
    Reseller ||--o{ Sales : "ResellerKey"
    Sales ||--o{ Sales_Order : "SalesOrderLineKey"
    Sales_Territory ||--o{ Sales : "SalesTerritoryKey"
    Date ||--o{ Sales : "OrderDateKey"
    Date ||..o{ Sales : "DueDateKey"
    Date ||..o{ Sales : "ShipDateKey"
    Table ||--o{ Product : "Category"
    DateTableTemplate_788642c5_9a9d_4431_b350_9f47f7e53393 {
        string placeholder
    }
    LocalDateTable_1635aca9_f5cf_4673_8bd0_6cbe59eca959 {
        string placeholder
    }
    LocalDateTable_d1146ef7_6f90_4647_b97e_2ffae90ba854 {
        string placeholder
    }
    LocalDateTable_dc06deb5_c3da_486c_acde_3111d75ed696 {
        string placeholder
    }
```

## Relationship Details

| From Table | From Column | To Table | To Column | Active | Cross Filter |
|------------|-------------|----------|-----------|--------|--------------|
| Date | Date | LocalDateTable |  | ✓ | Single |
| Date | Month | LocalDateTable |  | ✓ | Single |
| Date | Full Date | LocalDateTable |  | ✓ | Single |
| Sales | CustomerKey | Customer | CustomerKey | ✓ | Single |
| Sales | ProductKey | Product | ProductKey | ✓ | Single |
| Sales | ResellerKey | Reseller | ResellerKey | ✓ | Single |
| Sales Order | SalesOrderLineKey | Sales | SalesOrderLineKey | ✓ | Both |
| Sales | SalesTerritoryKey | Sales Territory | SalesTerritoryKey | ✓ | Single |
| Sales | OrderDateKey | Date | DateKey | ✓ | Single |
| Sales | DueDateKey | Date | DateKey | ✗ | Single |
| Sales | ShipDateKey | Date | DateKey | ✗ | Single |
| Product | Category | Table | Category | ✓ | Single |

---

[← Back to Home](Home.md)
