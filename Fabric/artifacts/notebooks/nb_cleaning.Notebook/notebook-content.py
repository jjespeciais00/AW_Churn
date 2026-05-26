# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "f91f2980-69ea-4d03-a5fa-ece9e09724b8",
# META       "default_lakehouse_name": "lh_Bronze",
# META       "default_lakehouse_workspace_id": "86cfb1d8-84ae-4e97-83d6-6de876acf922",
# META       "known_lakehouses": [
# META         {
# META           "id": "f91f2980-69ea-4d03-a5fa-ece9e09724b8"
# META         },
# META         {
# META           "id": "e878495b-de05-4da2-a723-1d9f175d278f"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

bronze_base = "abfss://AW_Churn_Dev@onelake.dfs.fabric.microsoft.com/lh_Bronze.Lakehouse/Tables/dbo"
silver_base = "abfss://AW_Churn_Dev@onelake.dfs.fabric.microsoft.com/lh_Silver.Lakehouse/Tables/dbo"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
spark.read.format("delta")
.load(f"{bronze_base}/dimdate")

.selectExpr(
    "DateKey",
    "FullDateAlternateKey as Date",
    "EnglishDayNameOfWeek as DayName",
    "EnglishMonthName as MonthName",
    "CalendarQuarter",
    "CalendarYear",
    "FiscalQuarter",
    "FiscalYear"
)

.write
.mode("overwrite")
.format("delta")
.save(f"{silver_base}/date")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
spark.read.format("delta")
.load(f"{bronze_base}/dimgeography")

.selectExpr(
    "GeographyKey",
    "City",
    "StateProvinceName",
    "EnglishCountryRegionName as Country",
    "PostalCode",
    "SalesTerritoryKey"
)

.write
.mode("overwrite")
.format("delta")
.save(f"{silver_base}/geography")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
spark.read.format("delta")
.load(f"{bronze_base}/dimproductcategory")

.selectExpr(
"ProductCategoryKey",
"ProductCategoryAlternateKey as ProductCategoryCode",
"EnglishProductCategoryName as ProductCategoryName"
)

.write
.mode("overwrite")
.format("delta")
.save(f"{silver_base}/productCategory")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
spark.read.format("delta")
.load(f"{bronze_base}/dimproductsubcategory")

.selectExpr(
"ProductSubcategoryKey",
"ProductSubcategoryAlternateKey as ProductSubcategoryCode",
"EnglishProductSubcategoryName as ProductSubcategoryName",
"ProductCategoryKey"
)

.write
.mode("overwrite")
.format("delta")
.save(f"{silver_base}/productsubcategory")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
spark.read.format("delta")
.load(f"{bronze_base}/dimproduct")

.selectExpr(
"ProductKey",
"ProductAlternateKey as ProductCode",
"ProductSubcategoryKey",
"EnglishProductName as ProductName",
"StandardCost",
"ListPrice",
"SafetyStockLevel",
"ReorderPoint",
"Size",
"Weight",
"ProductLine",
"Status"
)

.write
.mode("overwrite")
.format("delta")
.save(f"{silver_base}/product")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# SalesReason
(
spark.read.format("delta").load(f"{bronze_base}/dimsalesreason")
.selectExpr(
    "SalesReasonKey",
    "SalesReasonAlternateKey as SalesReasonCode",
    "SalesReasonName",
    "SalesReasonReasonType as SalesReasonType"
)
.write.mode("overwrite").format("delta").save(f"{silver_base}/salesreason")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# SalesTerritory
(
spark.read.format("delta").load(f"{bronze_base}/dimsalesterritory")
.selectExpr(
    "SalesTerritoryKey",
    "SalesTerritoryAlternateKey as SalesTerritoryCode",
    "SalesTerritoryRegion",
    "SalesTerritoryCountry",
    "SalesTerritoryGroup"
)
.write.mode("overwrite").format("delta").save(f"{silver_base}/salesterritory")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# InternetSales
(
spark.read.format("delta").load(f"{bronze_base}/factinternetsales")
.selectExpr(
    "ProductKey",
    "OrderDateKey",
    "DueDateKey",
    "ShipDateKey",
    "CustomerKey",
    "PromotionKey",
    "CurrencyKey",
    "SalesTerritoryKey",
    "SalesOrderNumber",
    "SalesOrderLineNumber",
    "RevisionNumber",
    "OrderQuantity",
    "UnitPrice",
    "ExtendedAmount",
    "UnitPriceDiscountPct",
    "DiscountAmount",
    "ProductStandardCost",
    "TotalProductCost",
    "SalesAmount",
    "TaxAmt",
    "Freight",
    "OrderDate",
    "DueDate",
    "ShipDate"
)
.where("CustomerKey IS NOT NULL AND ProductKey IS NOT NULL AND OrderQuantity > 0 AND SalesAmount >= 0")
.write.mode("overwrite").format("delta").save(f"{silver_base}/internetsales")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ProductInventory
(
spark.read.format("delta").load(f"{bronze_base}/factproductinventory")
.selectExpr(
    "ProductKey",
    "DateKey",
    "MovementDate",
    "UnitCost",
    "UnitsIn",
    "UnitsOut",
    "UnitsBalance"
)
.where("ProductKey IS NOT NULL")
.write.mode("overwrite").format("delta").save(f"{silver_base}/productinventory")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

for table in [
    "Currency", "date", "geography", "product",
    "productCategory", "productsubcategory", "salesreason",
    "salesterritory", "internetsales", "productinventory"
]:
    df = spark.read.format("delta").load(f"{silver_base}/{table}")
    print(table, df.count())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## corrigir productsubcategorykey pra long(int64)

# CELL ********************

from pyspark.sql import functions as F

bronze_base = "abfss://AW_Churn_Dev@onelake.dfs.fabric.microsoft.com/lh_Bronze.Lakehouse/Tables/dbo"
silver_base = "abfss://AW_Churn_Dev@onelake.dfs.fabric.microsoft.com/lh_Silver.Lakehouse/Tables/dbo"

product = (
    spark.read.format("delta")
    .load(f"{silver_base}/product")
    .withColumn(
        "ProductSubcategoryKey",
        F.col("ProductSubcategoryKey").cast("long")
    )
)

(
    product.write
    .mode("overwrite")
    .option("overwriteSchema","true")
    .format("delta")
    .save(f"{silver_base}/product")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#validar
spark.read.format("delta")\
.load(f"{silver_base}/product")\
.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.read.format("delta")\
.load(f"{silver_base}/productsubcategory")\
.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
