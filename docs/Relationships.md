# Relationships

> Total Relationships: 14

## Entity Relationship Diagram

```mermaid
erDiagram
    Product ||--o{ Sales : "StockItemID"
    People ||--o{ Sales : "SalespersonPersonID"
    Supplier ||--o{ Product : "SupplierID"
    Geo ||--o{ Reseller : "PostalCityID"
    Product ||--o{ PurchaseOrders : "StockItemID"
    People ||--o{ PurchaseOrders : "ContactPersonID"
    Product ||--o{ ProductDetails : "StockItemID"
    Reseller ||--o{ Sales : "ResellerID"
    LocalDateTable ||--o{ PurchaseOrders : "ExpectedDeliveryDate"
    Reseller ||--o{ Customer : "ResellerID"
    LocalDateTable ||--o{ Date : "Date"
    LocalDateTable ||--o{ Date : "StartOfMonth"
    Date ||--o{ Sales : "InvoiceDate"
    Date ||--o{ PurchaseOrders : "OrderDate"
    DateTableTemplate_f0f8abcf_79a8_4914_adcb_eda52d0258f6 {
        string placeholder
    }
    LocalDateTable_26f52010_5d90_4c5c_83d1_f853724817b0 {
        string placeholder
    }
    LocalDateTable_d5d93083_b295_4a13_972e_d3b526636400 {
        string placeholder
    }
    LocalDateTable_ee7963ef_1821_445f_8c31_2b70951dc67b {
        string placeholder
    }
```

## Relationship Details

| From Table | From Column | To Table | To Column | Active | Cross Filter |
|------------|-------------|----------|-----------|--------|--------------|
| Sales | StockItemID | Product | StockItemID | ✓ | Single |
| Sales | SalespersonPersonID | People | PersonID | ✓ | Single |
| Product | SupplierID | Supplier | SupplierID | ✓ | Both |
| Reseller | PostalCityID | Geo | CityID | ✓ | Both |
| PurchaseOrders | StockItemID | Product | StockItemID | ✓ | Single |
| PurchaseOrders | ContactPersonID | People | PersonID | ✓ | Single |
| ProductDetails | StockItemID | Product | StockItemID | ✓ | Both |
| Sales | ResellerID | Reseller | ResellerID | ✓ | Single |
| PurchaseOrders | ExpectedDeliveryDate | LocalDateTable |  | ✓ | Single |
| Customer | ResellerID | Reseller | ResellerID | ✓ | Single |
| Date | Date | LocalDateTable |  | ✓ | Single |
| Date | StartOfMonth | LocalDateTable |  | ✓ | Single |
| Sales | InvoiceDate | Date | Date | ✓ | Single |
| PurchaseOrders | OrderDate | Date | Date | ✓ | Single |

---

[← Back to Home](Home.md)
