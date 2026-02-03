# Table: Sales

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| InvoiceLineID | Unknown |  |
| InvoiceID | Unknown |  |
| StockItemID | Unknown |  |
| Quantity | Unknown |  |
| UnitPrice | Unknown |  |
| TaxRate | Unknown |  |
| TaxAmount | Unknown |  |
| ResellerID | Unknown |  |
| SalespersonPersonID | Unknown |  |
| InvoiceDate | Unknown |  |
| LineProfit | Unknown |  |
| ExtendedPrice | Unknown |  |
| Sales Amount | Unknown |  |

## Measures

| Measure | Expression |
|---------|------------|
| [Average Order](Measures#average-order) | `DIVIDE([Sales], [Sales Orders])...` |
| [Gross Margin](Measures#gross-margin) | `SUM(Sales[LineProfit])...` |
| [Gross Margin %](Measures#gross-margin-%) | `DIVIDE([Gross Margin], [Sales])...` |
| [Items](Measures#items) | `DISTINCTCOUNT(Sales[StockItemID])...` |
| [Sales](Measures#sales) | `SUM(Sales[Sales Amount])...` |
| [Sales Orders](Measures#sales-orders) | `DISTINCTCOUNT(Sales[InvoiceID])...` |
| [Sales Year over Year %](Measures#sales-year-over-year-%) | `
	VAR __PREV_YEAR = CALCULATE([Sales], DATEADD('Da...` |
| [Units](Measures#units) | `SUM(Sales[Quantity])...` |
| [Highest Selling Product Sales](Measures#highest-selling-product-sales) | `
    VAR TopProduct =
      TOPN(
        1,
     ...` |
| [Total Sales Best Selling](Measures#total-sales-best-selling) | `
    VAR TopProduct =
      TOPN(
        1,      ...` |
| [Best Selling Units Sold](Measures#best-selling-units-sold) | `
    VAR TopProduct =
      TOPN(
        1,
     ...` |
| [Top units sold unit count](Measures#top-units-sold-unit-count) | `
    VAR TopProduct =
      TOPN(
        1,      ...` |
| [Total Sales of Top Selling Unit](Measures#total-sales-of-top-selling-unit) | `
    VAR TopProduct =
      TOPN(
        1,      ...` |
| [Profit of Best Selling Item](Measures#profit-of-best-selling-item) | `			
			    VAR TopProduct =
			      TOPN(
			    ...` |
| [Trend Icon](Measures#trend-icon) | `	
	    IF(
      [Sales Year over Year %] > 0,  //...` |
| [Sales by Average Order](Measures#sales-by-average-order) | `
    DIVIDE([Sales], [Sales Orders])
...` |
| [SalesNet](Measures#salesnet) | `
      SUM('Sales'[Sales Amount]) - SUM('Sales'[Un...` |
| [SalesExtendedPrice](Measures#salesextendedprice) | `
    SUMX(
      'Sales',
      'Sales'[ExtendedPr...` |
| [Total Units Sold](Measures#total-units-sold) | `SUM('Sales'[Quantity])
...` |
| [Sales Including VAT](Measures#sales-including-vat) | `SUM(Sales[Sales Amount]) * 1.21...` |
| [Netto Omzet incl BTW](Measures#netto-omzet-incl-btw) | `SUM(Sales[Sales Amount]) + SUM(Sales[TaxAmount])...` |


---

[← Back to Home](Home.md)
