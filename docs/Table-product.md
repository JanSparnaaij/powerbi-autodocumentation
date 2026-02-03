# Table: Product

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| StockItemID | Unknown |  |
| StockItemName | Unknown |  |
| SupplierID | Unknown |  |
| Size | Unknown |  |
| IsChillerStock | Unknown |  |
| TaxRate | Unknown |  |
| UnitPrice | Unknown |  |
| RecommendedRetailPrice | Unknown |  |
| TypicalWeightPerUnit | Unknown |  |
| StockGroupName | Unknown |  |
| StockGroupID | Unknown |  |

## Measures

| Measure | Expression |
|---------|------------|
| [Highest Sold StockName](Measures#highest-sold-stockname) | `VAR _TopProduct = TOPN( 1, // Only the top record ...` |
| [Top N1 Sales](Measures#top-n1-sales) | `VAR _ProductRank = RANKX(ALL('Product'), [Sales], ...` |
| [BestSellingUnitPrice](Measures#bestsellingunitprice) | `VAR TopProduct = TOPN( 1, ALL('Product'), // Consi...` |
| [Unit price of most sold unit](Measures#unit-price-of-most-sold-unit) | `VAR TopProduct = TOPN( 1, ALL('Product'), [Units],...` |
| [Highest sold product name](Measures#highest-sold-product-name) | `VAR _TopProduct = TOPN( 1, // Retrieve only the to...` |


---

[← Back to Home](Home.md)
