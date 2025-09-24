**Sales Analytics Dashboard (Demo)**

This is a professional business intelligence dashboard built with Streamlit, Pandas, and Plotly.
It transforms a simple sales CSV into interactive, investor-ready insights.

**Features**

KPI Metrics: Total Revenue, Transactions, Average Order Value, Categories

Interactive Filters: Date range, Product categories

**Charts**:

Daily Revenue Trend (line chart)

Top Categories by Revenue (bar chart)

Pareto Analysis (80/20 revenue concentration)

Monthly Sales Heatmap

Customer Demographics (age, gender)

Growth Consistency by Category


**Demo Dataset**

The included dataset (retail_sales_dataset.csv) is a sample for demonstration purposes.
For your business, I build a custom dashboard with your data in 48h.

**Tech Stack**
Streamlit
 (frontend & deployment)

Pandas
 (data wrangling)

Plotly
 (interactive charts)

NumPy
 (numeric operations)


**Work With Me**

I offer Dashboard-as-a-Service for startups, founders, and small businesses.

You send me your sales CSV
I deliver a private, interactive, and catered to you dashboard with insights in 48h

**For custom dashboards with your sales data, contact me on LinkedIn or email:**

**Email**: farajh083@gmail.com

**LinkedIn**: linkedin.com/in/hadifaraj/

**Built by Hadi Faraj – AI & Data Science @ Aivancity**

# Sales Analytics Dashboard

Deploying to Streamlit Community Cloud:

1. Ensure these files exist in repo root:
   - `app.py`
   - `requirements.txt`
2. Recommended Python version: 3.10–3.12.
3. Required Python dependencies are pinned in `requirements.txt`.

Local run:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
streamlit run app.py
```