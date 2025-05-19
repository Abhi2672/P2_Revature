
# 🌍 Global Sales Analysis & Forecasting - ETL Project

## 🧩 Project Overview

This project builds an ETL pipeline for analyzing global sales across 8 countries, each contributing data in different formats and currencies. The goal is to:

- Collect and clean data from all sources
- Normalize all prices to INR (Indian Rupees)
- Combine all data into a centralized warehouse
- Generate analysis, visualizations, and forecasting for decision-making

---

## 🌐 Participating Countries and Data Sources

| Country      | Source Format              | Currency | Exchange Rate (to INR) |
|--------------|----------------------------|----------|-------------------------|
| India        | SQL Server / CSV           | INR      | 1.00                    |
| Japan        | CSV in Storage Bucket      | JPY      | 1.65                    |
| Norway       | PostgreSQL (AlloyDB)       | NOK      | 12.10                   |
| Sri Lanka    | JSON (Storage Bucket)      | LKR      | 3.10                    |
| Hong Kong    | Excel (XLSX)               | HKD      | 10.93                   |
| Oman         | MySQL                      | OMR      | 215.40                  |
| Germany      | MySQL                      | EUR      | 90.25                   |
| Qatar        | MySQL                      | QAR      | 22.00                   |

---

## 🗃️ File Structure

```
project-root/
│
├── data/
│   ├── India_sales.csv
│   ├── Japan_sales.csv
│   ├── Norway_sales.csv
│   ├── SriLanka_sales.json
│   ├── HongKong_sales.xlsx
│   ├── Oman_sales.csv
│   ├── Germany_sales.csv
│   └── Qatar_sales.csv
│
├── etl/
│   └── etl_pipeline.py     # ETL script for reading, cleaning, converting, and storing data
│
├── output/
│   ├── Final_Cleaned_Sales_INR.csv
│   └── Graphs/              # Visuals and charts
│
├── forecasting/
│   └── next_month_forecast.csv
│
└── README.md
```

---

## 📊 Fields in Source Files

Each dataset contains approximately 1000 rows and the following fields (8–10):

- `SaleId`: Unique identifier
- `Country`: Country of sale
- `SaleDate`: Date of sale
- `Category`: Product category (e.g., Tshirts, Shoes)
- `ProductId`: Internal product ID
- `ProductName`: Product name
- `Qty`: Quantity sold
- `Price`: Price in local currency
- `Currency`: Currency code (added during ETL)
- `Amount`: Qty × Price

---

## 🔁 ETL Pipeline Summary

### 1. **Extract**
- Pull CSV, Excel, JSON, and MySQL/PostgreSQL data
- Add a `Currency` column based on country

### 2. **Transform**
- Handle `null` values (drop or impute)
- Convert `Price` and `Amount` to INR using exchange rates
- Format dates and unify schemas

### 3. **Load**
- Merge all datasets
- Store final cleaned dataset in:
  - CSV file (`Final_Cleaned_Sales_INR.csv`)
  - Google BigQuery / Cloud Storage (optional)
  - Dashboard tool for visualization

---

## 📈 Stakeholder Deliverables

### A. **Downloadable Report (CSV/Excel)**  
- Fields: `ProductId`, `ProductName`, `Category`, `QtySold`, `Price_INR`, `Amount_INR`  
- 📎 [Link to Final Report (CSV)](./output/Final_Cleaned_Sales_INR.csv)

---

### B. **Dashboard (Visualizations)**
- Charts by:
  - Category-wise sales
  - Country-wise sales
  - Product-wise revenue
- 📊 Pie charts, bar graphs, and time series using **Matplotlib / Plotly**

---

### C. **Tax Department Report**
- Country-wise tax table (5% GST on `Amount_INR`)
- Format:
  - `Country`, `Total Sales`, `Tax (5%)`, `Category`, `Product`

---

### D. **Extra Charts for Management**
- Monthly trends
- Top 10 selling products
- Region-wise best-selling categories
- Forecast for next month (using time-series model like ARIMA)

---

## 🛡️ Theme & Branding
- All visuals use a **single dark/light theme**
- Each chart contains:
  - Organization logo (optional)
  - Copyright footer

---

## 📅 Forecasting
- Forecasting next month’s quantity and sales for each product using time-series analysis
- Output stored in: `forecasting/next_month_forecast.csv`

---

## 🧪 Technologies Used

- **Languages**: Python, SQL
- **Libraries**: Pandas, NumPy, Matplotlib, Plotly, Seaborn, Statsmodels
- **Tools**: Google Cloud Storage, MySQL, PostgreSQL, AlloyDB, Excel, JSON, BigQuery (optional)
- **Scheduler**: Apache Airflow / Cron (optional)

---

## 👨‍💼 Contributors

- Abhishek more
- Chetlapalle Sai Deekshitha
- Allamsetti Pardha vishnu vardhan
- chinchinada sumasri
- manjunatha poojari
- chethana G

---

## 📬 Contact

If you have questions or need help setting up the project, reach out to:

📧 your.email@example.com  
🌐 www.yourwebsite.com  

---
