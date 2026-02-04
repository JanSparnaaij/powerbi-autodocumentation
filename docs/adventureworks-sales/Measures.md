# All Measures

> Total Measures: 1


## Sales

### Sales Amount by Due Date

**Expression**:
```dax
CALCULATE(SUM(Sales[Sales Amount]), USERELATIONSHIP(Sales[DueDateKey],'Date'[DateKey])) 
```

---


[← Back to Home](Home.md)
