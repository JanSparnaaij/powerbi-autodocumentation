# Table: Cases

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| Case Created On | datetime64[ns] |  |
| Status | string |  |
| Agent | string |  |
| Title | string |  |
| Origin | string |  |
| Is Escalated | bool |  |
| Subject | string |  |
| CSAT Label | string |  |
| Resolution Minutes | Int64 |  |
| Severity | string |  |
| Is SLA Violation | bool |  |
| CSAT | Int64 |  |
| SLA Compliance Goal | object |  |
| Resolution Minutes Goal | object |  |
| CSAT Goal | object |  |
| Escalations Goal | object |  |
| Minutes to First Contact | Int64 |  |
| Activities | Int64 |  |
| Topic | object |  |
| CaseSeq | Int64 |  |
| SystemUserSeq | Int64 |  |
| AccountSeq | Int64 |  |
| ProductSeq | Int64 |  |

## Measures

| Measure | Expression |
|---------|------------|
| [Case Count](Measures.md) | `COUNTROWS('Cases')` |
| [Escalations](Measures.md) | `DIVIDE(CALCULATE(COUNTROWS('Cases'),'Cases'[Is Esc...` |
| [SLA Compliance](Measures.md) | `DIVIDE(CALCULATE(COUNTROWS('Cases'),'Cases'[Is SLA...` |
| [Cases MoM%](Measures.md) | `VAR __PREV_MONTH = CALCULATE([Case Count], DATEADD...` |
| [Cases % by Product](Measures.md) | `DIVIDE( [Case Count], CALCULATE( [Case Count],All(...` |
| [Cases % by Subject](Measures.md) | `DIVIDE( [Case Count], CALCULATE( [Case Count],All(...` |
| [CSAT Impact](Measures.md) | `VAR FactorAvg = AVERAGE ( 'Cases'[CSAT] ) VAR AllA...` |
| [CSAT Impact - Subject](Measures.md) | `VAR FactorAvg = AVERAGE ( 'Cases'[CSAT] ) VAR AllA...` |
| [CSAT Impact - Products](Measures.md) | `VAR FactorAvg = AVERAGE ( 'Cases'[CSAT] ) VAR AllA...` |
| [CSAT Impact - Agent](Measures.md) | `VAR FactorAvg = AVERAGE ( 'Cases'[CSAT] ) VAR AllA...` |


---

[← Back to Home](Home.md)
