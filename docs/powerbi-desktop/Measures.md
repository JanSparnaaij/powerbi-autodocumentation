# All Measures

> Total Measures: 31


## BU

### Count of BU

**Expression**:
```dax
COUNTA('BU'[BU])
```

---


## Date

### Count of Date

**Expression**:
```dax
COUNTA('Date'[Date])
```

---


## Employee

### EmpCount

**Format**: `#,0`

**Expression**:
```dax
CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[PeriodNumber]), 'Date'[PeriodNumber] = MAX('Date'[PeriodNumber])))
```

---

### Seps

**Format**: `#,0`

**Expression**:
```dax
CALCULATE(COUNT([EmplID]), FILTER(Employee, NOT(ISBLANK(Employee[TermDate]))))
```

---

### Actives

**Format**: `#,0`

**Expression**:
```dax
CALCULATE([EmpCount], FILTER(Employee, ISBLANK(Employee[TermDate])))
```

---

### New Hires

**Format**: `#,0`

**Expression**:
```dax
SUM([isNewHire])
```

---

### AVG Tenure Days

**Format**: `#,0`

**Expression**:
```dax
AVERAGE([TenureDays])
```

---

### AVG Tenure Months

**Format**: `0`

**Expression**:
```dax
ROUND([AVG Tenure Days]/30, 1)-1
```

---

### AVG Age

**Expression**:
```dax
ROUND(AVERAGE([Age]), 0)
```

---

### Sum of BadHires

**Format**: `#,0`

**Expression**:
```dax
SUM([BadHires])
```

---

### New Hires SPLY

**Format**: `#,0`

**Expression**:
```dax
CALCULATE([New Hires],SAMEPERIODLASTYEAR('Date'[Date]))
```

---

### Actives SPLY

**Format**: `#,0`

**Expression**:
```dax
CALCULATE([Actives],SAMEPERIODLASTYEAR('Date'[Date]))
```

---

### Seps SPLY

**Format**: `#,0`

**Expression**:
```dax
CALCULATE([Seps],SAMEPERIODLASTYEAR('Date'[Date]))
```

---

### EmpCount SPLY

**Format**: `#,0`

**Expression**:
```dax
CALCULATE(COUNT([EmplID]), FILTER(ALL('Date'[PeriodNumber]), 'Date'[PeriodNumber] = MAX('Date'[PeriodNumber])),SAMEPERIODLASTYEAR('Date'[Date]))
```

---

### Seps YoY Var

**Format**: `#,0`

**Expression**:
```dax
[Seps]-[Seps SPLY]
```

---

### Actives YoY Var

**Format**: `#,0`

**Expression**:
```dax
[Actives]-[Actives SPLY]
```

---

### New Hires YoY Var

**Format**: `#,0`

**Expression**:
```dax
[New Hires]-[New Hires SPLY]
```

---

### Seps YoY % Change

**Format**: `#,0.0%;-#,0.0%;#,0.0%`

**Expression**:
```dax
DIVIDE([Seps YoY Var], [Seps SPLY])
```

---

### Actives YoY % Change

**Format**: `#,0.0%;-#,0.0%;#,0.0%`

**Expression**:
```dax
DIVIDE([Actives YoY Var], [Actives SPLY])
```

---

### New Hires YoY % Change

**Format**: `#,0.0%;-#,0.0%;#,0.0%`

**Expression**:
```dax
DIVIDE([New Hires YoY Var], [New Hires SPLY])
```

---

### Bad Hires SPLY

**Format**: `#,0`

**Expression**:
```dax
CALCULATE([Sum of BadHires],SAMEPERIODLASTYEAR('Date'[Date]))
```

---

### Bad Hires YoY Var

**Format**: `#,0`

**Expression**:
```dax
[Sum of BadHires]-[Bad Hires SPLY]
```

---

### Bad Hires YoY % Change

**Format**: `#,0.0%;-#,0.0%;#,0.0%`

**Expression**:
```dax
DIVIDE([Bad Hires YoY Var], [Bad Hires SPLY])
```

---

### TO %

**Format**: `0.00%;-0.00%;0.00%`

**Expression**:
```dax
DIVIDE([Seps], [Actives])
```

---

### TO % Norm

**Format**: `0.00%;-0.00%;0.00%`

**Expression**:
```dax
CALCULATE([TO %], all(Gender[Gender]), ALL(Ethnicity[Ethnicity]))
```

---

### TO % Var

**Format**: `0.00%;-0.00%;0.00%`

**Expression**:
```dax
[TO %]-[TO % Norm]
```

---

### Sep%ofActive

**Format**: `0.00%;-0.00%;0.00%`

**Expression**:
```dax
DIVIDE([Seps],[Actives])
```

---

### Sep%ofSMLYActives

**Format**: `0.00%;-0.00%;0.00%`

**Expression**:
```dax
DIVIDE([Seps SPLY],[Actives SPLY])
```

---

### BadHire%ofActives

**Format**: `0.00%;-0.00%;0.00%`

**Expression**:
```dax
DIVIDE([Sum of BadHires],[Actives])
```

---

### BadHire%ofActiveSPLY

**Format**: `0.00%;-0.00%;0.00%`

**Expression**:
```dax
DIVIDE([Bad Hires SPLY],[Actives SPLY])
```

---

### blank

**Expression**:
```dax
""
```

---


[← Back to Home](Home.md)
