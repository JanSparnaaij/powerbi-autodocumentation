# Table: Supplier

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| SupplierID | Int64 |  |
| SupplierName | string |  |
| SupplierCategoryID | Int64 |  |
| WebsiteURL | string |  |
| SupplierCategoryName | string |  |

## Measures

| Measure | Expression |
|---------|------------|
| [Supplier by Sales](Measures.md) | `CALCULATE([Sales])` |


---

[← Back to Home](Home.md)
