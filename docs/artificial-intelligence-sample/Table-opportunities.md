# Table: Opportunities

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| Budget | Int64 |  |
| Topic | string |  |
| Purchase Process | string |  |
| Decision Maker Identified | bool |  |
| Status | string |  |
| PipelineStep | string |  |
| Value | Int64 |  |
| CloseDate | datetime64[ns] |  |
| Opportunity Created On | datetime64[ns] |  |
| Weeks Open | object |  |
| DaysToClose | Int64 |  |
| Discount | Float64 |  |
| Probability | Float64 |  |
| Rating | string |  |
| Days Remaining In Pipeline | object |  |
| Probability (raw) | Float64 |  |
| AccountSeq | Int64 |  |
| Opportunity Owner Name | string |  |
| OpportunitySeq | Int64 |  |
| ProductSeq | Int64 |  |
| SystemUserSeq | string |  |
| Product Name | string |  |
| CampaignSeq | string |  |
| Campaign Name | string |  |
| Blank | object |  |

## Measures

| Measure | Expression |
|---------|------------|
| [Revenue Won](Measures.md) | `CALCULATE( SUMX(Opportunities, Opportunities[Value...` |
| [Revenue In Pipeline](Measures.md) | `VAR Revenue = CALCULATE ( SUMX ( Opportunities, Op...` |
| [Forecast %](Measures.md) | `(([Revenue Won]+[Revenue In Pipeline]))/ [Rev Goal...` |
| [Forecast](Measures.md) | `([Revenue Won]+[Revenue In Pipeline])` |
| [Opportunity Count In Pipeline](Measures.md) | `CALCULATE ( COUNT( Opportunities[Value] ), FILTER ...` |
| [Opportunity Count](Measures.md) | `COUNTAX(Opportunities,TRUE())` |
| [Count of Won](Measures.md) | `COUNTAX( FILTER( KEEPFILTERS(Opportunities),Opport...` |
| [Count of Lost](Measures.md) | `COUNTAX( FILTER( KEEPFILTERS(Opportunities),Opport...` |
| [Close %](Measures.md) | `[Count of Won]/([Count of Won]+[Count of Lost])` |
| [Revenue Open](Measures.md) | `CALCULATE( SUMX(Opportunities, Opportunities[Value...` |


---

[← Back to Home](Home.md)
