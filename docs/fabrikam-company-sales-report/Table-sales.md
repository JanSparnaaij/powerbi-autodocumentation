# Table: Sales

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| InvoiceLineID | Int64 |  |
| InvoiceID | Int64 |  |
| StockItemID | Int64 |  |
| Quantity | Int64 |  |
| UnitPrice | Float64 |  |
| TaxRate | Int64 |  |
| TaxAmount | Float64 |  |
| ResellerID | Int64 |  |
| SalespersonPersonID | Int64 |  |
| InvoiceDate | datetime64[ns] |  |
| LineProfit | Float64 |  |
| ExtendedPrice | Float64 |  |
| Sales Amount | Float64 |  |

## Measures

| Measure | Expression |
|---------|------------|
| [Average Order](Measures.md) | `DIVIDE([Sales], [Sales Orders])` |
| [Gross Margin](Measures.md) | `SUM(Sales[LineProfit])` |
| [Gross Margin %](Measures.md) | `DIVIDE([Gross Margin], [Sales])` |
| [Items](Measures.md) | `DISTINCTCOUNT(Sales[StockItemID])` |
| [Sales](Measures.md) | `SUM(Sales[Sales Amount])` |
| [Sales Orders](Measures.md) | `DISTINCTCOUNT(Sales[InvoiceID])` |
| [Sales Year over Year %](Measures.md) | `VAR __PREV_YEAR = CALCULATE([Sales], DATEADD('Date...` |
| [Units](Measures.md) | `SUM(Sales[Quantity])` |
| [Highest Selling Product Sales](Measures.md) | `VAR TopProduct = TOPN( 1, ALL('Product'), [Sales],...` |
| [Total Sales Best Selling](Measures.md) | `VAR TopProduct = TOPN( 1, // Retrieve only the top...` |
| [Best Selling Units Sold](Measures.md) | `VAR TopProduct = TOPN( 1, ALL('Product'), // Consi...` |
| [Top units sold unit count](Measures.md) | `VAR TopProduct = TOPN( 1, // Retrieve only the top...` |
| [Total Sales of Top Selling Unit](Measures.md) | `VAR TopProduct = TOPN( 1, // Retrieve only the top...` |
| [Profit of Best Selling Item](Measures.md) | `VAR TopProduct = TOPN( 1, ALL('Product'), [Sales],...` |
| [Trend Icon](Measures.md) | `IF( [Sales Year over Year %] > 0, // If sales year...` |
| [Sales by Average Order](Measures.md) | `DIVIDE([Sales], [Sales Orders])` |
| [SalesNet](Measures.md) | `SUM('Sales'[Sales Amount]) - SUM('Sales'[UnitPrice...` |
| [SalesExtendedPrice](Measures.md) | `SUMX( 'Sales', 'Sales'[ExtendedPrice] * 'Sales'[Un...` |
| [Total Units Sold](Measures.md) | `SUM('Sales'[Quantity])` |
| [Sales Including VAT](Measures.md) | `SUM(Sales[Sales Amount]) * 1.21` |
| [Netto Omzet incl BTW](Measures.md) | `SUM(Sales[Sales Amount]) + SUM(Sales[TaxAmount])` |


---

[← Back to Home](Home.md)
