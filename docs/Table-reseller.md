# Table: Reseller

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| PostalCityID | Unknown |  |
| PhoneNumber | Unknown |  |
| FaxNumber | Unknown |  |
| WebsiteURL | Unknown |  |
| DeliveryAddressLine1 | Unknown |  |
| DeliveryAddressLine2 | Unknown |  |
| DeliveryPostalCode | Unknown |  |
| PostalAddressLine1 | Unknown |  |
| PostalAddressLine2 | Unknown |  |
| PostalPostalCode | Unknown |  |
| ResellerID | Unknown |  |
| ResellerName | Unknown |  |
| ResellerCompany | Unknown |  |

## Measures

| Measure | Expression |
|---------|------------|
| [Sales by reseller](Measures#sales-by-reseller) | `
VAR StartDate = DATE(2022, 12, 1)
VAR EndDate   =...` |
| [Reseller Sales](Measures#reseller-sales) | `
    VAR TopResellerTable = 
      TOPN(
        1...` |


---

[← Back to Home](Home.md)
