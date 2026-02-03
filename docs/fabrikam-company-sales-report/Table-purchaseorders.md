# Table: PurchaseOrders

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| PurchaseOrderID | Int64 |  |
| OrderDate | datetime64[ns] |  |
| ContactPersonID | Int64 |  |
| ExpectedDeliveryDate | datetime64[ns] |  |
| PurchaseOrderLineID | Int64 |  |
| StockItemID | Int64 |  |
| OrderedOuters | Float64 |  |
| ExpectedUnitPricePerOuter | Float64 |  |

## Measures

| Measure | Expression |
|---------|------------|
| [Spend](Measures.md) | `SUMX(PurchaseOrders, PurchaseOrders[OrderedOuters]...` |
| [Average Purchase Order](Measures.md) | `DIVIDE([Spend], [Purchase Orders])` |
| [In Stock](Measures.md) | `[Purchase Order Units in Stock]-[Units]` |
| [Purchase Order Units](Measures.md) | `SUM(PurchaseOrders[OrderedOuters])` |
| [Purchase Order Units in Stock](Measures.md) | `SUMX(FILTER(PurchaseOrders, PurchaseOrders[Expecte...` |
| [Purchase Order Units Planned](Measures.md) | `SUMX(FILTER(PurchaseOrders, PurchaseOrders[Expecte...` |
| [Purchase Orders](Measures.md) | `DISTINCTCOUNT(PurchaseOrders[PurchaseOrderID])` |


---

[← Back to Home](Home.md)
