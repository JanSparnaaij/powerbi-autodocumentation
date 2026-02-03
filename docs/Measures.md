# All Measures

> Total Measures: 41


## Customer

### No of Customers

**Expression**:
```dax
COUNTROWS(Customer)
```

---

### Distinct Products Sold

**Expression**:
```dax

CALCULATE(
    DISTINCTCOUNT(Sales[StockItemID])
)

```

---

### Total Sales Without Lowest Supplier

**Expression**:
```dax

VAR _LowestSupplier =
    MAXX(
        TOPN(
            1,
            ALL('Supplier'),
            [Supplier Sales],
            ASC
        ),
        'Supplier'[SupplierID]
    )
RETURN
    CALCULATE(
        [Sales],
        FILTER(
            ALL('Supplier'),
            'Supplier'[SupplierID] <> _LowestSupplier
        )
    )
```

---

### Total Sales by Unit Price

**Expression**:
```dax

CALCULATE(
    [Sales],
    REMOVEFILTERS('Sales'[UnitPrice])
)
```

---

### Sales by Customer Count

**Expression**:
```dax
DIVIDE([Sales], [Number of Customers])

```

---


## Product

### Highest Sold StockName

**Expression**:
```dax

    VAR _TopProduct =
      TOPN(
        1,                      // Only the top record
        ALL('Product'),         // Evaluate over all products
        [Units],                // Order by the [Units] measure from Sales
        DESC                    // Descending order to get the highest sold units
      )
    RETURN
      MAXX(
        _TopProduct,
        'Product'[StockItemName]  // Retrieve the StockItemName for the top product 
      )


```

---

### Top N1 Sales

**Expression**:
```dax

    VAR _ProductRank = RANKX(ALL('Product'), [Sales], , DESC)
    RETURN IF(_ProductRank = 1, [Sales])
    

```

---

### BestSellingUnitPrice

**Expression**:
```dax

    VAR TopProduct =
      TOPN(
        1,
        ALL('Product'),  // Consider all products
        [Sales],         // Rank by total sales from the Sales table
        DESC             // Descending order to get the best selling product
      )
    RETURN
      MAXX(TopProduct, 'Product'[UnitPrice])  // Retrieve the unit price of the top product

```

---

### Unit price of most sold unit

**Expression**:
```dax

    VAR TopProduct =
      TOPN(
        1,
        ALL('Product'),
        [Units], // [Units] is a measure from the Sales table that sums the quantity sold
        DESC
      )
    RETURN
      MAXX(TopProduct, 'Product'[UnitPrice])
      

```

---

### Highest sold product name

**Expression**:
```dax

    VAR _TopProduct =
      TOPN(
        1,                         // Retrieve only the top product
        ALL('Product'),            // Evaluate over all products
        [Sales],                   // Rank products based on the total Sales measure
        DESC                       // Descending order so the best selling product comes first
      )
    RETURN
      MAXX(                       // Extract the StockItemName of the top product
        _TopProduct,
        'Product'[StockItemName]
      )


```

---


## PurchaseOrders

### Spend

**Expression**:
```dax
SUMX(PurchaseOrders, PurchaseOrders[OrderedOuters]*PurchaseOrders[ExpectedUnitPricePerOuter])
```

---

### Average Purchase Order

**Expression**:
```dax
DIVIDE([Spend], [Purchase Orders])
```

---

### In Stock

**Expression**:
```dax
[Purchase Order Units in Stock]-[Units]
```

---

### Purchase Order Units

**Expression**:
```dax
SUM(PurchaseOrders[OrderedOuters])
```

---

### Purchase Order Units in Stock

**Expression**:
```dax
SUMX(FILTER(PurchaseOrders, PurchaseOrders[ExpectedDeliveryDate]<TODAY()), PurchaseOrders[OrderedOuters])
```

---

### Purchase Order Units Planned

**Expression**:
```dax
SUMX(FILTER(PurchaseOrders, PurchaseOrders[ExpectedDeliveryDate]>=TODAY()), PurchaseOrders[OrderedOuters])
```

---

### Purchase Orders

**Expression**:
```dax
DISTINCTCOUNT(PurchaseOrders[PurchaseOrderID])
```

---


## Reseller

### Sales by reseller

**Expression**:
```dax

VAR StartDate = DATE(2022, 12, 1)
VAR EndDate   = EOMONTH(StartDate, 0)
VAR Ranked =
    TOPN (
        1,
        ADDCOLUMNS (
            ALL ( 'Reseller'[ResellerName] ),
            "Total Sales",
                CALCULATE (
                    [Sales],
                    DATESBETWEEN ( 'Date'[Date], StartDate, EndDate )
                )
        ),
        [Total Sales], DESC
    )
RETURN
    MAXX ( Ranked, 'Reseller'[ResellerName] )

```

---

### Reseller Sales

**Expression**:
```dax

    VAR TopResellerTable = 
      TOPN(
        1, 
        ALL('Reseller'),
        CALCULATE([Sales]),  // Compute total overall sales per reseller
        DESC
      )
    RETURN
      MAXX(TopResellerTable, 'Reseller'[ResellerName])
      

```

---


## Sales

### Average Order

**Expression**:
```dax
DIVIDE([Sales], [Sales Orders])
```

---

### Gross Margin

**Expression**:
```dax
SUM(Sales[LineProfit])
```

---

### Gross Margin %

**Expression**:
```dax
DIVIDE([Gross Margin], [Sales])
```

---

### Items

**Expression**:
```dax
DISTINCTCOUNT(Sales[StockItemID])
```

---

### Sales

**Expression**:
```dax
SUM(Sales[Sales Amount])
```

---

### Sales Orders

**Expression**:
```dax
DISTINCTCOUNT(Sales[InvoiceID])
```

---

### Sales Year over Year %

**Expression**:
```dax

	VAR __PREV_YEAR = CALCULATE([Sales], DATEADD('Date'[Date].[Date], -1, YEAR))
	RETURN
		DIVIDE([Sales] - __PREV_YEAR, __PREV_YEAR)

```

---

### Units

**Expression**:
```dax
SUM(Sales[Quantity])
```

---

### Highest Selling Product Sales

**Expression**:
```dax

    VAR TopProduct =
      TOPN(
        1,
        ALL('Product'),
        [Sales],
        DESC
      )
    VAR TopProductID =
      MAXX(TopProduct, 'Product'[StockItemID])
    RETURN
      CALCULATE(
        [Sales],
        'Product'[StockItemID] = TopProductID
      )


```

---

### Total Sales Best Selling

**Expression**:
```dax

    VAR TopProduct =
      TOPN(
        1,                  // Retrieve only the top product
        ALL('Product'),     // Consider all products in the model
        [Sales],            // Rank products by the total sales measure
        DESC                // Descending order so that the best selling comes first
      )
    VAR TopProductID =
      MAXX(
        TopProduct, 
        'Product'[StockItemID]  // Retrieve the StockItemID for the top product
      )
    RETURN
      CALCULATE(
        [Sales],
        'Product'[StockItemID] = TopProductID  // Filter Sales measure by the best selling product
      )


```

---

### Best Selling Units Sold

**Expression**:
```dax

    VAR TopProduct =
      TOPN(
        1,
        ALL('Product'),  // Consider all products without any filter
        [Sales],         // Use the Sales measure to determine ranking
        DESC             // Descending order to get the best selling product
      )
    VAR TopProductID =
      MAXX(TopProduct, 'Product'[StockItemID])  // Retrieve the StockItemID for the top product
    RETURN
      CALCULATE(
        SUM(Sales[Quantity]),  // Sum of units sold
        'Product'[StockItemID] = TopProductID  // Filter for the best selling product
      )


```

---

### Top units sold unit count

**Expression**:
```dax

    VAR TopProduct =
      TOPN(
        1,                    // Retrieve only the top product based on units sold
        ALL('Product'),       // Consider all products regardless of filters
        [Units],              // Measure that sums Sales[Quantity] giving total units sold per product
        DESC                  // Order descending to get the product with the most units sold
      )
    // Get the StockItemID of the top product
    VAR TopProductID = MAXX(TopProduct, 'Product'[StockItemID])
    // Calculate the total units sold for the product with StockItemID equal to TopProductID
    RETURN
      CALCULATE(
        [Units],
        'Product'[StockItemID] = TopProductID
      )


```

---

### Total Sales of Top Selling Unit

**Expression**:
```dax

    VAR TopProduct =
      TOPN(
        1,              // Retrieve only the top product based on units sold
        ALL('Product'), // Consider all products without filters
        [Units],        // Use the [Units] measure to rank products by total units sold
        DESC            // Descending order to pick the product with the most units sold
      )
  // Get the StockItemID of the top product
  VAR TopProductID =
      MAXX(TopProduct, 'Product'[StockItemID])
  RETURN
    CALCULATE(
      [Sales],
      'Product'[StockItemID] = TopProductID  // Filter Sales measure for the best selling product
    )


```

---

### Profit of Best Selling Item

**Expression**:
```dax
			
			    VAR TopProduct =
			      TOPN(
			        1,
			        ALL('Product'),
			        [Sales],
			        DESC
			      )
			    VAR TopProductID =
			      MAXX(TopProduct, 'Product'[StockItemID])
			    RETURN
			      CALCULATE(
        [Gross Margin],
```

---

### Trend Icon

**Expression**:
```dax
	
	    IF(
      [Sales Year over Year %] > 0,  // If sales year-over-year growth is positive
	
```

---

### Sales by Average Order

**Expression**:
```dax

    DIVIDE([Sales], [Sales Orders])

```

---

### SalesNet

**Expression**:
```dax

      SUM('Sales'[Sales Amount]) - SUM('Sales'[UnitPrice])
      

```

---

### SalesExtendedPrice

**Expression**:
```dax

    SUMX(
      'Sales',
      'Sales'[ExtendedPrice] * 'Sales'[UnitPrice]
    )

```

---

### Total Units Sold

**Expression**:
```dax
SUM('Sales'[Quantity])

```

---

### Sales Including VAT

**Expression**:
```dax
SUM(Sales[Sales Amount]) * 1.21
```

---

### Netto Omzet incl BTW

**Expression**:
```dax
SUM(Sales[Sales Amount]) + SUM(Sales[TaxAmount])
```

---


## Supplier

### Supplier by Sales

**Expression**:
```dax
CALCULATE([Sales])
  

```

---


[← Back to Home](Home)
