# All Measures

> Total Measures: 22


## Cases

### Case Count

**Expression**:
```dax

    COUNTROWS('Cases')
```

---

### Escalations

**Expression**:
```dax
DIVIDE(CALCULATE(COUNTROWS('Cases'),'Cases'[Is Escalated] = TRUE()) , [Case Count],0)
```

---

### SLA Compliance

**Expression**:
```dax
DIVIDE(CALCULATE(COUNTROWS('Cases'),'Cases'[Is SLA Violation] = FALSE()) , [Case Count],0)
```

---

### Cases MoM%

**Expression**:
```dax

VAR __PREV_MONTH = CALCULATE([Case Count], DATEADD('Case Calendar'[Date], -1, MONTH))
RETURN
	DIVIDE([Case Count] - __PREV_MONTH, __PREV_MONTH)
```

---

### Cases % by Product

**Expression**:
```dax

DIVIDE(
        [Case Count],
        CALCULATE(
            [Case Count],All('Products')
        )
    )
```

---

### Cases % by Subject

**Expression**:
```dax

DIVIDE(
        [Case Count],
        CALCULATE(
            [Case Count],All('Cases'[Subject])
        )
    )
```

---

### CSAT Impact

**Expression**:
```dax

VAR FactorAvg =
    AVERAGE ( 'Cases'[CSAT] )
VAR AllAvg =
    CALCULATE ( AVERAGE ( 'Cases'[CSAT] ), ALL ( 'Cases' ) )
VAR AllAvgExcept =
    CALCULATE (
        AVERAGE ( 'Cases'[CSAT] ),
        FILTER ( ALL ( 'Cases' ), 'Cases'[Topic] <> SELECTEDVALUE ( 'Cases'[Topic] ) )
    )
RETURN
    1 - ( AllAvgExcept / AllAvg )
```

---

### CSAT Impact - Subject

**Expression**:
```dax

VAR FactorAvg =
    AVERAGE ( 'Cases'[CSAT] )
VAR AllAvg =
    CALCULATE ( AVERAGE ( 'Cases'[CSAT] ), ALL ( 'Cases' ) )
VAR AllAvgExcept =
    CALCULATE (
        AVERAGE ( 'Cases'[CSAT] ),
        FILTER ( ALL ( 'Cases' ), 'Cases'[Subject] <> SELECTEDVALUE ( 'Cases'[Subject] ) )
    )
RETURN
    1 - ( AllAvgExcept / AllAvg )
```

---

### CSAT Impact - Products

**Expression**:
```dax

VAR FactorAvg =
    AVERAGE ( 'Cases'[CSAT] )
VAR AllAvg =
    CALCULATE ( AVERAGE ( 'Cases'[CSAT] ), ALL ( 'Cases' ) )
VAR AllAvgExcept =
    CALCULATE (
        AVERAGE ( 'Cases'[CSAT] ),
        FILTER ( ALL ( 'Cases' ), 'Cases'[ProductSeq] <> SELECTEDVALUE ( 'Cases'[ProductSeq] )  )
    )
RETURN
    1 - ( AllAvgExcept / AllAvg )
```

---

### CSAT Impact - Agent

**Expression**:
```dax

VAR FactorAvg =
    AVERAGE ( 'Cases'[CSAT] )
VAR AllAvg =
    CALCULATE ( AVERAGE ( 'Cases'[CSAT] ), ALL ( 'Cases' ) )
VAR AllAvgExcept =
    CALCULATE (
        AVERAGE ( 'Cases'[CSAT] ),
        FILTER ( ALL ( 'Cases' ), 'Cases'[Agent] <> SELECTEDVALUE ( 'Cases'[Agent] ) )
    )
RETURN
    1 - ( AllAvgExcept / AllAvg )
```

---


## Opportunities

### Revenue Won

**Expression**:
```dax

 CALCULATE(
     SUMX(Opportunities, Opportunities[Value]),
     FILTER(Opportunities, Opportunities[Status] = "Won")
 )
```

---

### Revenue In Pipeline

**Expression**:
```dax

VAR Revenue =
    CALCULATE (
        SUMX ( Opportunities, Opportunities[Value] ),
        FILTER (
            Opportunities,
            Opportunities[Status] = "Open"
            && VALUE(LEFT(Opportunities[PipelineStep],1)) >=2
        )
    )
RETURN
    Revenue + ( Revenue * ( 'Opportunity Forecast Adjustment'[Forecast Adjustment Value] / 100 ) )

```

---

### Forecast %

**Expression**:
```dax
(([Revenue Won]+[Revenue In Pipeline]))/ [Rev Goal]
```

---

### Forecast

**Expression**:
```dax
([Revenue Won]+[Revenue In Pipeline])
```

---

### Opportunity Count In Pipeline

**Expression**:
```dax

    CALCULATE (
        COUNT( Opportunities[Value] ),
        FILTER (
            Opportunities,
            Opportunities[Status] = "Open"
              --  && Opportunities[PipelineStep] IN { "3-Pipeline", "4-Mandate", "5-Close" }
        )
    )

```

---

### Opportunity Count

**Expression**:
```dax

COUNTAX(Opportunities,TRUE())
```

---

### Count of Won

**Expression**:
```dax

COUNTAX(
    FILTER(
        KEEPFILTERS(Opportunities),Opportunities[Status] = "Won"
        ),
    Opportunities[OpportunitySeq]
    ) 
```

---

### Count of Lost

**Expression**:
```dax

COUNTAX(
    FILTER(
        KEEPFILTERS(Opportunities),Opportunities[Status] = "Lost"
        ),
    Opportunities[OpportunitySeq]
    ) 
```

---

### Close %

**Expression**:
```dax
[Count of Won]/([Count of Won]+[Count of Lost])
```

---

### Revenue Open

**Expression**:
```dax

CALCULATE(
     SUMX(Opportunities, Opportunities[Value]),
     FILTER(Opportunities, Opportunities[Status] = "Open")
 )
```

---


## Opportunity Forecast Adjustment

### Forecast Adjustment Value

**Expression**:
```dax
SELECTEDVALUE('Opportunity Forecast Adjustment'[Forecast Adjustment], 0)
```

---


## Owners

### Rev Goal

**Expression**:
```dax

VAR RevenueInPipeline =
    CALCULATE (
        SUMX ( Opportunities, Opportunities[Value] ),
        FILTER (
            Opportunities,
            Opportunities[Status] = "Open"
            && VALUE(LEFT(Opportunities[PipelineStep],1)) >=3
        )
    )
VAR BaseGoal =  
MROUND(([Revenue Won]+ (RevenueInPipeline*.75)),100000)    
RETURN
IF(BaseGoal > 0, BaseGoal, MROUND(([Revenue Won]+ (RevenueInPipeline*.75)),10000))
```

---


[← Back to Home](Home.md)
