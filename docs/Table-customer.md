# Table: Customer

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| CustomerID | string |  |
| Address | string |  |
| Age | Int64 |  |
| BrandAffinity | string |  |
| City | string |  |
| Country | string |  |
| FullName | string |  |
| Generation | string |  |
| InterestAffinity1 | string |  |
| InterestAffinity2 | string |  |
| ResellerID | Int64 |  |
| State | string |  |
| ZipCode | string |  |

## Measures

| Measure | Expression |
|---------|------------|
| [No of Customers](Measures.md) | `COUNTROWS(Customer)` |
| [Distinct Products Sold](Measures.md) | `CALCULATE( DISTINCTCOUNT(Sales[StockItemID]) )` |
| [Total Sales Without Lowest Supplier](Measures.md) | `VAR _LowestSupplier = MAXX( TOPN( 1, ALL('Supplier...` |
| [Total Sales by Unit Price](Measures.md) | `CALCULATE( [Sales], REMOVEFILTERS('Sales'[UnitPric...` |
| [Sales by Customer Count](Measures.md) | `DIVIDE([Sales], [Number of Customers])` |


---

[← Back to Home](Home.md)
