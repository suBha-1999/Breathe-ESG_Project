# DECISIONS.md

## Ambiguities Resolved & Subsets Handled

**1. SAP Data (Subset: Flat File Export)**
* **The Ambiguity:** SAP can export data via OData APIs, BAPIs, or IDocs, but the prompt noted the exports are "not friendly." 
* **The Decision:** I chose to handle CSV/Flat File exports generated from SAP ALV grids. I resolved ambiguities around European number formatting (e.g., `1.200,50`) by implementing a string-cleaning parser before database insertion. I specifically chose semicolon-delimited files to avoid column-shifting conflicts with comma-based decimal values.
* **What I Ignored:** I ignored API-based ingestion (like OData) because legacy flat files represent a more common and painful bottleneck for sustainability teams. 

**2. Utility Data (Subset: Portal CSV Export)**
* **The Ambiguity:** Billing periods rarely align with calendar months, creating ambiguity around how to report monthly emissions.
* **The Decision:** I chose to handle portal CSV exports. I wrote ingestion logic that calculates the exact number of days in the billing cycle (`end_date - start_date`). While the prototype saves the total raw value, this architectural decision ensures the frontend or reporting layer can calculate accurate daily averages for month-over-month reporting.

**3. Corporate Travel (Subset: Expense Export)**
* **The Ambiguity:** The prompt stated distances aren't always given, only airport codes.
* **The Decision:** I implemented a backend lookup mechanism. When the ingestion script reads an IATA code pair (e.g., SFO to JFK), it queries a distance matrix to find the exact mileage before multiplying it by the cabin-specific emission factor.