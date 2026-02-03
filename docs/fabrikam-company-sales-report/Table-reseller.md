# Table: Reseller

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| PostalCityID | Int64 |  |
| PhoneNumber | string |  |
| FaxNumber | string |  |
| WebsiteURL | string |  |
| DeliveryAddressLine1 | string |  |
| DeliveryAddressLine2 | string |  |
| DeliveryPostalCode | Int64 |  |
| PostalAddressLine1 | string |  |
| PostalAddressLine2 | string |  |
| PostalPostalCode | Int64 |  |
| ResellerID | Int64 |  |
| ResellerName | string |  |
| ResellerCompany | string |  |

## Measures

| Measure | Expression |
|---------|------------|
| [Sales by reseller](Measures.md) | `VAR StartDate = DATE(2022, 12, 1) VAR EndDate = EO...` |
| [Reseller Sales](Measures.md) | `VAR TopResellerTable = TOPN( 1, ALL('Reseller'), C...` |


---

[← Back to Home](Home.md)
