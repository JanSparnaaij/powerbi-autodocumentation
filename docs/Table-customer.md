# Table: Customer

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| CustomerID | Unknown |  |
| Address | Unknown |  |
| Age | Unknown |  |
| BrandAffinity | Unknown |  |
| City | Unknown |  |
| Country | Unknown |  |
| FullName | Unknown |  |
| Generation | Unknown |  |
| InterestAffinity1 | Unknown |  |
| InterestAffinity2 | Unknown |  |
| ResellerID | Unknown |  |
| State | Unknown |  |
| ZipCode | Unknown |  |

## Measures

| Measure | Expression |
|---------|------------|
| [No of Customers](Measures#no-of-customers) | `COUNTROWS(Customer)...` |
| [Distinct Products Sold](Measures#distinct-products-sold) | `
CALCULATE(
    DISTINCTCOUNT(Sales[StockItemID])
...` |
| [Total Sales Without Lowest Supplier](Measures#total-sales-without-lowest-supplier) | `
VAR _LowestSupplier =
    MAXX(
        TOPN(
   ...` |
| [Total Sales by Unit Price](Measures#total-sales-by-unit-price) | `
CALCULATE(
    [Sales],
    REMOVEFILTERS('Sales'...` |
| [Sales by Customer Count](Measures#sales-by-customer-count) | `DIVIDE([Sales], [Number of Customers])
...` |


---

[← Back to Home](Home.md)
