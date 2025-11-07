Here is your README **properly converted into Markdown (.md format)** — you can directly copy-paste this into a **README.md** file:

---

```md
# 📦 Logistics Data Preprocessing Pipeline  
### **Power BI – Data Cleaning • Feature Engineering • Master Dataset Creation**

This repository contains a **complete end-to-end data preprocessing pipeline** designed for a **Logistics Performance Dashboard** built in **Power BI**.  
The script (`powerbi_preprocessing.py`) automates the extraction, cleaning, transformation, merging, validation, and export of logistics datasets required for BI analytics.

---

## ✅ Project Overview

This preprocessing pipeline supports the **Logistics Shipment Dashboard**, a minor project developed using Microsoft Power BI.  
The goal is to transform raw CSV files into clean, analytics-ready data using Python before loading them into Power BI for modeling and visualization.

The pipeline performs:

- Cleaning & validating raw data  
- Feature engineering  
- Creating a **Master Dataset**  
- Generating **Aggregated Tables**  
- Exporting all processed files for Power BI  

---

## 📂 Input Data Sources

The project uses **four CSV files**:

| File | Description |
|------|-------------|
| **SalesPerson.csv** | Sales team details (name, team, picture) |
| **Shipment.csv** | Core fact table containing shipment transactions |
| **Country.csv** | Geography information (country, region) |
| **Product.csv** | Product descriptions and categories |

---

## 🛠️ Features of the Preprocessing Pipeline

### ✅ 1. Data Loading
Loads all CSV files with custom paths.

### ✅ 2. Data Cleaning
- Removes blank rows  
- Normalizes text (trim, clean)  
- Converts date fields  
- Handles missing values  
- Validates numeric fields  

### ✅ 3. Feature Engineering
Adds important analytical features such as:

- Year, Month, Quarter, Week  
- Month name  
- Delivery time (days)  
- Status flags (Active/Completed/Returned)  
- Late delivery indicator  
- Revenue = Sales × Cost  
- Profit = 30% of Revenue  

### ✅ 4. Master Dataset Creation
Combines:

```

Shipment → SalesPerson → Country → Product

````

### ✅ 5. Aggregated Tables
Automatically generates:

- **Monthly summary**
- **Salesperson performance**
- **Product summary**
- **Geographical summary**
- **Status summary**

### ✅ 6. Data Quality Report
Includes:

- Missing value analysis  
- Duplicate checks  
- Date and sales ranges  
- Status distribution  

### ✅ 7. Exporting Output Files
Exports:

- master_dataset.csv  
- Cleaned individual tables  
- Aggregated analytics tables  

---

## ▶️ How to Run

Install required libraries:

```bash
pip install pandas numpy
````

Run:

```bash
python powerbi_preprocessing.py
```

Output files will be stored in:

```
/processed_data/
```

---

## 📊 Usage in Power BI

Recommended workflow:

1. Import cleaned CSVs
2. Build a **Star Schema**
3. Create required DAX measures
4. Use aggregated tables for optimized visuals

---

## 📁 Project Structure

```
│
├── powerbi_preprocessing.py
├── SalesPerson.csv
├── Shipment.csv
├── Country.csv
├── Product.csv
│
└── processed_data/
       ├── master_dataset.csv
       ├── salesperson_cleaned.csv
       ├── shipment_cleaned.csv
       ├── country_cleaned.csv
       ├── product_cleaned.csv
       ├── monthly_aggregated.csv
       ├── product_aggregated.csv
       ├── geography_aggregated.csv
       ├── salesperson_aggregated.csv
       └── status_aggregated.csv
```

---

## 🎯 Why This Pipeline Matters

* Ensures **credibility, reliability & transparency**
* Saves hours of manual cleaning
* Provides a scalable, reusable BI dataset
* Establishes a **single source of truth**
* Supports academic + real-world analytics needs

---

## 👩‍💻 Developer

**Ritu Kumari (03014803622)**
**pranav Rustogi(01314803622)**
**Shivam Dubey (03414803622)**
**Ayush Gupta ( 01914803622)**
Minor Project – B.Tech (Mechanical & Automation Engineering)
Maharaja Agrasen Institute of Technology
