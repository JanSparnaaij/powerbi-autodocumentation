# Table: Fact

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| Customer Key | Int64 |  |
| Product Key | String |  |
| BU Key | Double |  |
| Scenario Key | Int64 |  |
| Revenue | Double |  |
| Material Costs | Double |  |
| Labor Costs Variable | Double |  |
| Taxes | Double |  |
| Rev for Exp Travel | Double |  |
| Travel Expenses | Double |  |
| Cost Third Party | Double |  |
| Subscription Revenue | Double |  |
| YearPeriod | String |  |

## Measures

| Measure | Expression |
|---------|------------|
| [Total Revenue](Measures.md) | `SUM([Revenue])` |
| [Sum of Material Costs](Measures.md) | `SUM([Material Costs])` |
| [Sum of Labor Costs Variable](Measures.md) | `SUM([Labor Costs Variable])` |
| [Sum of Taxes](Measures.md) | `SUM([Taxes])` |
| [Sum of Rev for Exp Travel](Measures.md) | `SUM([Rev for Exp Travel])` |
| [Sum of Travel Expenses](Measures.md) | `SUM([Travel Expenses])` |
| [Sum of Cost Third Party](Measures.md) | `SUM([Cost Third Party])` |
| [Sum of Subscription Revenue](Measures.md) | `SUM([Subscription Revenue])` |
| [Gross Margin](Measures.md) | `[Total Revenue]-[Total COGS]` |
| [GM%](Measures.md) | `DIVIDE([Gross Margin],[Total Revenue])` |
| [YTD Revenue](Measures.md) | `TOTALYTD(SUM([Revenue]),'Date'[Date])` |
| [Total COGS](Measures.md) | `[Sum of Material Costs]+[Sum of Labor Costs Variab...` |
| [YTD COGS](Measures.md) | `TOTALYTD([Total COGS],'Date'[Date])` |
| [YTD Gross Margin](Measures.md) | `TOTALYTD([Gross Margin],'Date'[Date])` |
| [Revenue SPLY](Measures.md) | `CALCULATE([Total Revenue],SAMEPERIODLASTYEAR('Date...` |
| [Gross Margin SPLY](Measures.md) | `CALCULATE([Gross Margin],SAMEPERIODLASTYEAR('Date'...` |
| [GM% SPLY](Measures.md) | `[Gross Margin SPLY]/[Revenue SPLY]` |
| [YTD GM%](Measures.md) | `[YTD Gross Margin]/[YTD Revenue]` |
| [YTD Revenue SPLY](Measures.md) | `CALCULATE([YTD Revenue],SAMEPERIODLASTYEAR(DATESYT...` |
| [COGS SPLY](Measures.md) | `CALCULATE([Total COGS],SAMEPERIODLASTYEAR('Date'[D...` |
| [YTD COGS SPLY](Measures.md) | `CALCULATE([YTD COGS],SAMEPERIODLASTYEAR(DATESYTD('...` |
| [YTD GM% SPLY](Measures.md) | `[YTD GM SPLY]/[YTD Revenue SPLY]` |
| [YTD GM SPLY](Measures.md) | `CALCULATE([YTD Gross Margin],SAMEPERIODLASTYEAR(DA...` |
| [YoY Rev Var](Measures.md) | `[Total Revenue]-[Revenue SPLY]` |
| [YoY GM Var](Measures.md) | `[Gross Margin]-[Gross Margin SPLY]` |
| [YoY Rev Growth](Measures.md) | `IF([Revenue SPLY],[YoY Rev Var]/[Revenue SPLY],BLA...` |
| [YoY GM Growth](Measures.md) | `IF([Gross Margin SPLY],[YoY GM Var]/[Gross Margin ...` |
| [YoY YTD Rev Var](Measures.md) | `[YTD Revenue]-[YTD Revenue SPLY]` |
| [YoY COGS Var](Measures.md) | `[Total COGS]-[COGS SPLY]` |
| [YoY YTD COGS Var](Measures.md) | `[YTD COGS]-[YTD COGS SPLY]` |
| [YoY YTD GM% Var](Measures.md) | `[YTD GM%]-[YTD GM% SPLY]` |
| [YoY YTD GM Var](Measures.md) | `[YTD Gross Margin]-[YTD GM SPLY]` |
| [YoY GM %Var](Measures.md) | `[GM%]-[GM% SPLY]` |
| [YoY YTD Rev Growth](Measures.md) | `IF([YTD Revenue SPLY],[YoY YTD Rev Var]/[YTD Reven...` |
| [YoY COGS Growth](Measures.md) | `IF([COGS SPLY],[YoY COGS Var]/[COGS SPLY],BLANK())` |
| [YoY YTD COGS Growth](Measures.md) | `IF([YTD COGS SPLY],[YoY YTD COGS Var]/[YTD COGS SP...` |
| [YoY YTD GM Growth](Measures.md) | `IF([YTD GM SPLY],[YoY YTD GM Var]/[YTD GM SPLY],BL...` |
| [# of Customers](Measures.md) | `DISTINCTCOUNT([Customer Key])` |
| [# of Products](Measures.md) | `DISTINCTCOUNT([Product Key])` |
| [Revenue Budget](Measures.md) | `CALCULATE([Total Revenue], FILTER(Scenario, Scenar...` |
| [Revenue Var to Budget](Measures.md) | `[RevenueTY]-[Revenue Budget]` |
| [Revenue Var % to Budget](Measures.md) | `DIVIDE([Revenue Var to Budget], [RevenueTY])` |
| [RevenueTY](Measures.md) | `CALCULATE([Total Revenue], FILTER(Scenario, Scenar...` |
| [Sum of Revenue](Measures.md) | `SUM('Fact'[Revenue])` |


---

[← Back to Home](Home.md)
