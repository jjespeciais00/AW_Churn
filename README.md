# AW_Churn

AI-powered churn analytics system built in Microsoft Fabric for reducing analysis time for sales teams.

## Objective

AW_Churn aims to reduce manual effort from commercial teams by centralizing sales data and enabling AI-assisted insights such as:

- Product revenue decline detection
- Sales trend identification
- Territory performance analysis
- Profitability analysis
- Pattern detection using AI agents

Examples:

- "Product X experienced a decline in region Y due to reason B"
- "Product A experienced a decline during time X in territory Z"
- "Territory X is experiencing a decline in Y product category"
- "Product Y is experiencing a decline in regions X, Y, and Z over time A, and this affects profit in B"


## Architecture

Bronze → Silver → Semantic Model → Ontology → GraphQL → AI Agent

Current implementation:

✓ Bronze ingestion  
✓ Silver transformation layer  
✓ Semantic model  
✓ Relationships  
✓ Git integration  

In progress:

DAX measures  
Ontology  
GraphQL  
Data Agent  
Application layer

{The documentation is being prepared in conjunction with production.}

---

## Data Flow

### Bronze

Raw AdventureWorks ingestion into Delta Lake.

Main tasks:

- Data ingestion
- Delta conversion
- Initial storage

---

### Silver

Business-oriented transformation layer.

Actions performed:

- Keep relationship keys
- Rename technical fields
- Remove unnecessary multilingual fields
- Remove low-value attributes
- Standardize naming

Silver tables:

- currency
- date
- geography
- product
- productcategory
- productsubcategory
- salesreason
- salesterritory
- internetsales
- productinventory

---

## Semantic Model

Relationships implemented:

- InternetSales → Product
- InternetSales → Date
- InternetSales → Currency
- InternetSales → SalesTerritory
- Product → ProductSubcategory
- ProductSubcategory → ProductCategory
- ProductInventory → Product
- ProductInventory → Date
- Geography → SalesTerritory

Relationship configuration:

- Cardinality: One-to-many
- Filter direction: Single

---

## Technical decisions

### Gold layer removed

Reason:

The project uses an AI agent for dynamic interpretation and pattern detection.

Creating static analytical rules in Gold would reduce flexibility and duplicate logic.

---

### Git integration

Repository configured with:

- Fine-grained access token
- Least privilege principle
- Separate Fabric folder
- Main branch strategy

---

## Challenges solved

### Direct Lake relationship issue

Problem:

```text
ProductSubcategoryKey

Double ≠ Int64
