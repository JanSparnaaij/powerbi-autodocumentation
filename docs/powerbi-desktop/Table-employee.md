# Table: Employee

## Overview

**Row Count**: N/A

## Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| RowNumber-2662979B-1795-4F74-8F37-6A1BA8059B61 | Int64 |  |
| date | DateTime |  |
| EmplID | Int64 |  |
| Gender | String |  |
| Age | Int64 |  |
| EthnicGroup | String |  |
| FP | String |  |
| TermDate | DateTime |  |
| isNewHire | Int64 |  |
| BU | String |  |
| HireDate | DateTime |  |
| PayTypeID | String |  |
| TermReason | String |  |
| AgeGroupID | Int64 |  |
| TenureDays | Double |  |
| TenureMonths | Int64 |  |
| BadHires | Double |  |

## Measures

| Measure | Expression |
|---------|------------|
| [EmpCount](Measures.md) | `CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[Perio...` |
| [Seps](Measures.md) | `CALCULATE(COUNT([EmplID]), FILTER(Employee, NOT(IS...` |
| [Actives](Measures.md) | `CALCULATE([EmpCount], FILTER(Employee, ISBLANK(Emp...` |
| [New Hires](Measures.md) | `SUM([isNewHire])` |
| [AVG Tenure Days](Measures.md) | `AVERAGE([TenureDays])` |
| [AVG Tenure Months](Measures.md) | `ROUND([AVG Tenure Days]/30, 1)-1` |
| [AVG Age](Measures.md) | `ROUND(AVERAGE([Age]), 0)` |
| [Sum of BadHires](Measures.md) | `SUM([BadHires])` |
| [New Hires SPLY](Measures.md) | `CALCULATE([New Hires],SAMEPERIODLASTYEAR('Date'[Da...` |
| [Actives SPLY](Measures.md) | `CALCULATE([Actives],SAMEPERIODLASTYEAR('Date'[Date...` |
| [Seps SPLY](Measures.md) | `CALCULATE([Seps],SAMEPERIODLASTYEAR('Date'[Date]))` |
| [EmpCount SPLY](Measures.md) | `CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[Perio...` |
| [Seps YoY Var](Measures.md) | `[Seps]-[Seps SPLY]` |
| [Actives YoY Var](Measures.md) | `[Actives]-[Actives SPLY]` |
| [New Hires YoY Var](Measures.md) | `[New Hires]-[New Hires SPLY]` |
| [Seps YoY % Change](Measures.md) | `DIVIDE([Seps YoY Var], [Seps SPLY])` |
| [Actives YoY % Change](Measures.md) | `DIVIDE([Actives YoY Var], [Actives SPLY])` |
| [New Hires YoY % Change](Measures.md) | `DIVIDE([New Hires YoY Var], [New Hires SPLY])` |
| [Bad Hires SPLY](Measures.md) | `CALCULATE([Sum of BadHires],SAMEPERIODLASTYEAR('Da...` |
| [Bad Hires YoY Var](Measures.md) | `[Sum of BadHires]-[Bad Hires SPLY]` |
| [Bad Hires YoY % Change](Measures.md) | `DIVIDE([Bad Hires YoY Var], [Bad Hires SPLY])` |
| [TO %](Measures.md) | `DIVIDE([Seps], [Actives])` |
| [TO % Norm](Measures.md) | `CALCULATE([TO %], all(Gender[Gender]), ALL(Ethnici...` |
| [TO % Var](Measures.md) | `[TO %]-[TO % Norm]` |
| [Sep%ofActive](Measures.md) | `DIVIDE([Seps],[Actives])` |
| [Sep%ofSMLYActives](Measures.md) | `DIVIDE([Seps SPLY],[Actives SPLY])` |
| [BadHire%ofActives](Measures.md) | `DIVIDE([Sum of BadHires],[Actives])` |
| [BadHire%ofActiveSPLY](Measures.md) | `DIVIDE([Bad Hires SPLY],[Actives SPLY])` |
| [blank](Measures.md) | `""` |


---

[← Back to Home](Home.md)
