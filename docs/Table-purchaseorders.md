# Table: PurchaseOrders

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| PurchaseOrderID | Unknown |  |
| OrderDate | Unknown |  |
| ContactPersonID | Unknown |  |
| ExpectedDeliveryDate | Unknown |  |
| PurchaseOrderLineID | Unknown |  |
| StockItemID | Unknown |  |
| OrderedOuters | Unknown |  |
| ExpectedUnitPricePerOuter | Unknown |  |

## Measures

| Measure | Expression |
|---------|------------|
| [Spend](Measures#spend) | `SUMX(PurchaseOrders, PurchaseOrders[OrderedOuters]...` |
| [Average Purchase Order](Measures#average-purchase-order) | `DIVIDE([Spend], [Purchase Orders])` |
| [In Stock](Measures#in-stock) | `[Purchase Order Units in Stock]-[Units]` |
| [Purchase Order Units](Measures#purchase-order-units) | `SUM(PurchaseOrders[OrderedOuters])` |
| [Purchase Order Units in Stock](Measures#purchase-order-units-in-stock) | `SUMX(FILTER(PurchaseOrders, PurchaseOrders[Expecte...` |
| [Purchase Order Units Planned](Measures#purchase-order-units-planned) | `SUMX(FILTER(PurchaseOrders, PurchaseOrders[Expecte...` |
| [Purchase Orders](Measures#purchase-orders) | `DISTINCTCOUNT(PurchaseOrders[PurchaseOrderID])` |


---

[← Back to Home](Home.md)
