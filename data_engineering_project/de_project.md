Data Engineering bootcamp from the Udemy Course: Building a Modern Data Warehouse - Data Engineering Bootcamp.

Objective:
Develop a modern data warehouse using SQL Server to consolidate sales ata, enabling analytical reporting and informed decision making.

Specifications:
Data Sources: provided through course (datasets folder).
Data Quality: Cleanse and resolve data quality issues prior to analysis.
Integration: Combine both sources into a single, user friendly model designed for analytical queries.
Scope: Focus on the latest dataset only; hisotrization of data is not required.
Documentation: Provide clear documentation of the data model to support both business stakeholders and analytics teams.

Notes:
Choosing the right data modeling approach
Inmon: source --> stage --> edw (3nf) --> data mart
Kimball: source --> stage --> data mart (speed)
Data Vault: source --> stage --> raw vault --> business vault --> data marts
Medallion Architecture: source --> bronze (raw data--very few transforms) --> silver (transform layer, clean and standardize) --> gold (add biz logic)

Using Medallion Architecture in the Project:
Bronze: raw data for debugging and tracebility --> table; full load (truncate and insert)
Silver: clean & standardize data, prep for analysis --> table; full load (truncate and insert)
Gold: biz ready logic, data to be consumed for analytics and reporting --> view (helps with speed); no load method