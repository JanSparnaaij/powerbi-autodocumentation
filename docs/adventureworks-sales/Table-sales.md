# Table: Sales

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| SalesOrderLineKey | Int64 |  |
| ResellerKey | Int64 |  |
| CustomerKey | Int64 |  |
| ProductKey | Int64 |  |
| OrderDateKey | Int64 |  |
| DueDateKey | Int64 |  |
| ShipDateKey | Int64 |  |
| SalesTerritoryKey | Int64 |  |
| Order Quantity | Int64 |  |
| Unit Price | Float64 |  |
| Extended Amount | Float64 |  |
| Unit Price Discount Pct | Int64 |  |
| Product Standard Cost | Float64 |  |
| Total Product Cost | Float64 |  |
| Sales Amount | Float64 |  |

## Measures

| Measure | Expression |
|---------|------------|
| [Sales Amount by Due Date](Measures.md) | `CALCULATE(SUM(Sales[Sales Amount]), USERELATIONSHI...` |


---

[← Back to Home](Home.md)
