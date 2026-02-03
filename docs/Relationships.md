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
    Reseller ||--o{ Customer : "ResellerID"
    Date ||--o{ Sales : "InvoiceDate"
    Date ||--o{ PurchaseOrders : "OrderDate"
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
| PurchaseOrders | ExpectedDeliveryDate |  |  | ✓ | Single |
| Customer | ResellerID | Reseller | ResellerID | ✓ | Single |
| Date | Date |  |  | ✓ | Single |
| Date | StartOfMonth |  |  | ✓ | Single |
| Sales | InvoiceDate | Date | Date | ✓ | Single |
| PurchaseOrders | OrderDate | Date | Date | ✓ | Single |

---

[← Back to Home](Home.md)
