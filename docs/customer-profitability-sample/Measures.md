# All Measures

> Total Measures: 44


## Fact

### Total Revenue

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
SUM([Revenue])
```

---

### Sum of Material Costs

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
SUM([Material Costs])
```

---

### Sum of Labor Costs Variable

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
SUM([Labor Costs Variable])
```

---

### Sum of Taxes

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
SUM([Taxes])
```

---

### Sum of Rev for Exp Travel

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
SUM([Rev for Exp Travel])
```

---

### Sum of Travel Expenses

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
SUM([Travel Expenses])
```

---

### Sum of Cost Third Party

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
SUM([Cost Third Party])
```

---

### Sum of Subscription Revenue

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
SUM([Subscription Revenue])
```

---

### Gross Margin

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
[Total Revenue]-[Total COGS]
```

---

### GM%

**Format**: `0.0%;-0.0%;0.0%`

**Expression**:
```dax
DIVIDE([Gross Margin],[Total Revenue])
```

---

### YTD Revenue

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
TOTALYTD(SUM([Revenue]),'Date'[Date])
```

---

### Total COGS

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
[Sum of Material Costs]+[Sum of Labor Costs Variable]+[Sum of Taxes]+[Sum of Rev for Exp Travel]+[Sum of Travel Expenses]+[Sum of Cost Third Party]
```

---

### YTD COGS

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
TOTALYTD([Total COGS],'Date'[Date])
```

---

### YTD Gross Margin

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
TOTALYTD([Gross Margin],'Date'[Date])
```

---

### Revenue SPLY

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
CALCULATE([Total Revenue],SAMEPERIODLASTYEAR('Date'[Date]))
```

---

### Gross Margin SPLY

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
CALCULATE([Gross Margin],SAMEPERIODLASTYEAR('Date'[Date]))
```

---

### GM% SPLY

**Format**: `0.0%;-0.0%;0.0%`

**Expression**:
```dax
[Gross Margin SPLY]/[Revenue SPLY]
```

---

### YTD GM%

**Format**: `0.0%;-0.0%;0.0%`

**Expression**:
```dax
[YTD Gross Margin]/[YTD Revenue]
```

---

### YTD Revenue SPLY

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
CALCULATE([YTD Revenue],SAMEPERIODLASTYEAR(DATESYTD('Date'[Date])))
```

---

### COGS SPLY

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
CALCULATE([Total COGS],SAMEPERIODLASTYEAR('Date'[Date]))
```

---

### YTD COGS SPLY

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
CALCULATE([YTD COGS],SAMEPERIODLASTYEAR(DATESYTD('Date'[Date])))
```

---

### YTD GM% SPLY

**Format**: `0.0%;-0.0%;0.0%`

**Expression**:
```dax
[YTD GM SPLY]/[YTD Revenue SPLY]
```

---

### YTD GM SPLY

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
CALCULATE([YTD Gross Margin],SAMEPERIODLASTYEAR(DATESYTD('Date'[Date])))
```

---

### YoY Rev Var

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
[Total Revenue]-[Revenue SPLY]
```

---

### YoY GM Var

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
[Gross Margin]-[Gross Margin SPLY]
```

---

### YoY Rev Growth

**Format**: `0.0%;-0.0%;0.0%`

**Expression**:
```dax
IF([Revenue SPLY],[YoY Rev Var]/[Revenue SPLY],BLANK())
```

---

### YoY GM Growth

**Format**: `0.0%;-0.0%;0.0%`

**Expression**:
```dax
IF([Gross Margin SPLY],[YoY GM Var]/[Gross Margin SPLY],BLANK())
```

---

### YoY YTD Rev Var

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
[YTD Revenue]-[YTD Revenue SPLY]
```

---

### YoY COGS Var

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
[Total COGS]-[COGS SPLY]
```

---

### YoY YTD COGS Var

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
[YTD COGS]-[YTD COGS SPLY]
```

---

### YoY YTD GM% Var

**Format**: `#,0`

**Expression**:
```dax
[YTD GM%]-[YTD GM% SPLY]
```

---

### YoY YTD GM Var

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
[YTD Gross Margin]-[YTD GM SPLY]
```

---

### YoY GM %Var

**Expression**:
```dax
[GM%]-[GM% SPLY]
```

---

### YoY YTD Rev Growth

**Format**: `0.0%;-0.0%;0.0%`

**Expression**:
```dax
IF([YTD Revenue SPLY],[YoY YTD Rev Var]/[YTD Revenue SPLY],BLANK())
```

---

### YoY COGS Growth

**Format**: `0.0%;-0.0%;0.0%`

**Expression**:
```dax
IF([COGS SPLY],[YoY COGS Var]/[COGS SPLY],BLANK())
```

---

### YoY YTD COGS Growth

**Format**: `0.0%;-0.0%;0.0%`

**Expression**:
```dax
IF([YTD COGS SPLY],[YoY YTD COGS Var]/[YTD COGS SPLY],BLANK())
```

---

### YoY YTD GM Growth

**Format**: `0.0%;-0.0%;0.0%`

**Expression**:
```dax
IF([YTD GM SPLY],[YoY YTD GM Var]/[YTD GM SPLY],BLANK())
```

---

### # of Customers

**Expression**:
```dax
DISTINCTCOUNT([Customer Key])
```

---

### # of Products

**Expression**:
```dax
DISTINCTCOUNT([Product Key])
```

---

### Revenue Budget

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
CALCULATE([Total Revenue], FILTER(Scenario, Scenario[Scenario]="Budget"))
```

---

### Revenue Var to Budget

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
[RevenueTY]-[Revenue Budget]
```

---

### Revenue Var % to Budget

**Format**: `0.00%;-0.00%;0.00%`

**Expression**:
```dax
DIVIDE([Revenue Var to Budget], [RevenueTY])
```

---

### RevenueTY

**Format**: `\$#,0;(\$#,0);\$#,0`

**Expression**:
```dax
CALCULATE([Total Revenue], FILTER(Scenario, Scenario[Scenario]="Actual"))
```

---

### Sum of Revenue

**Expression**:
```dax
SUM('Fact'[Revenue])
```

---


[← Back to Home](Home.md)
