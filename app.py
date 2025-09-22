import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sales Story Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("retail_sales_dataset.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['year_month'] = df['Date'].dt.to_period('M').dt.to_timestamp()
    return df

df = load_data()

st.title(" Sales Analytics Dashboard")
st.markdown("**Professional business intelligence dashboard with advanced analytics and visualizations by Hadi Faraj**")

col1, col2, col3, col4 = st.columns(4)
total_revenue = df['Total Amount'].sum()
total_transactions = len(df)
avg_order_value = total_revenue / total_transactions
unique_categories = df['Product Category'].nunique()

with col1:
    st.metric("Total Revenue", f"${total_revenue:,.0f}")
with col2:
    st.metric("Total Transactions", f"{total_transactions:,}")
with col3:
    st.metric("Avg Order Value", f"${avg_order_value:.0f}")
with col4:
    st.metric("Product Categories", f"{unique_categories}")

with st.sidebar:
    st.header(" Filters")
    date_min, date_max = df['Date'].min(), df['Date'].max()
    sel_range = st.date_input("Date range", value=(date_min, date_max))
    if isinstance(sel_range, tuple) and len(sel_range) == 2:
        df = df[(df['Date'] >= pd.to_datetime(sel_range[0])) & (df['Date'] <= pd.to_datetime(sel_range[1]))]
    categories = sorted(df['Product Category'].unique())
    sel_cats = st.multiselect("Categories", categories, default=categories)
    df = df[df['Product Category'].isin(sel_cats)]
    
    st.header(" Chart Settings")
    show_annotations = st.checkbox("Show Annotations", value=True)
    
    if st.button("🔄 Refresh Charts"):
        st.cache_data.clear()
        st.rerun()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader(" Daily Sales Trend")
    daily_sales = df.groupby('Date')['Total Amount'].sum().reset_index()
    fig1 = px.line(daily_sales, x='Date', y='Total Amount', 
                   title="Revenue Over Time", 
                   labels={'Total Amount': 'Daily Revenue ($)'})
    fig1.update_layout(template="plotly_white", height=400, font=dict(size=12))
    fig1.update_traces(line=dict(width=3), marker=dict(size=6))
    if show_annotations and not daily_sales.empty:
        latest = daily_sales.iloc[-1]
        fig1.add_annotation(x=latest['Date'], y=latest['Total Amount'], 
                           text=f"Latest: ${latest['Total Amount']:,.0f}", 
                           showarrow=True, arrowhead=2, ax=50, ay=-50,
                           bgcolor="rgba(255,255,255,0.8)", bordercolor="black", borderwidth=1,
                           font=dict(size=14, color="black"))
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader(" Top Product Categories")
    top_cats = df.groupby('Product Category')['Total Amount'].sum().sort_values(ascending=False).head(8)
    fig2 = px.bar(x=top_cats.index, y=top_cats.values, 
                  title="Revenue by Category", 
                  labels={'x': 'Category', 'y': 'Total Revenue ($)'},
                  color=top_cats.values, color_continuous_scale='viridis')
    fig2.update_layout(template="plotly_white", height=500, showlegend=False, font=dict(size=12),
                      xaxis=dict(tickangle=45, tickfont=dict(size=11), automargin=True),
                      margin=dict(b=100))
    fig2.update_traces(text=top_cats.values, texttemplate='$%{text:,.0f}', textposition='outside', 
                      textfont=dict(size=12, color='black'))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

st.subheader(" Pareto Analysis — Revenue Concentration")
col1, col2 = st.columns([3, 1])
with col1:
    cat_rev = df.groupby('Product Category', as_index=False)['Total Amount'].sum().sort_values('Total Amount', ascending=False)
    cat_rev['cum_pct'] = cat_rev['Total Amount'].cumsum() / cat_rev['Total Amount'].sum()
    
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=cat_rev['Product Category'], y=cat_rev['Total Amount'], 
                         name='Revenue', marker_color='#3498db', opacity=0.8))
    fig3.add_trace(go.Scatter(x=cat_rev['Product Category'], y=100*cat_rev['cum_pct'], 
                             name='Cumulative %', mode='lines+markers', yaxis='y2', 
                             marker_color='#e74c3c', line=dict(width=3)))
    fig3.update_layout(template="plotly_white", height=500, font=dict(size=12),
                      yaxis=dict(title='Revenue ($)', tickprefix='$'),
                      yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 100]),
                      xaxis_title='Product Category',
                      legend=dict(x=1.15, y=0.9, xanchor='left', yanchor='top', bgcolor='rgba(255,255,255,0.8)'),
                      margin=dict(r=150))
    fig3.add_hline(y=80, yref='y2', line_dash='dash', line_color='red', 
                   annotation_text="80% Line", annotation_position="top right")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.metric("Top 3 Categories", f"{((cat_rev['cum_pct'] <= 0.8).sum())} categories")
    st.metric("Revenue Share", f"{(cat_rev['cum_pct'].iloc[2]*100):.1f}%")
    st.metric("Concentration Risk", "High" if (cat_rev['cum_pct'].iloc[2] > 0.7) else "Medium")

st.subheader("Sales Heatmap — Monthly Performance by Category")
monthly_cat = df.groupby([df['Date'].dt.to_period('M'), 'Product Category'])['Total Amount'].sum().unstack(fill_value=0)
monthly_cat.index = monthly_cat.index.astype(str)

fig4 = px.imshow(monthly_cat.T, 
                 labels=dict(x="Month", y="Category", color="Revenue ($)"),
                 title="Monthly Revenue Heatmap",
                 color_continuous_scale='RdYlBu_r',
                 aspect='auto')
fig4.update_layout(template="plotly_white", height=400, font=dict(size=12))
st.plotly_chart(fig4, use_container_width=True)

st.subheader(" Customer Demographics & Spending Patterns")
col1, col2 = st.columns(2)

with col1:
    age_spending = df.groupby('Age')['Total Amount'].agg(['sum', 'count']).reset_index()
    age_spending['avg_spending'] = age_spending['sum'] / age_spending['count']
    
    fig5a = px.scatter(age_spending, x='Age', y='avg_spending', size='count',
                      title="Average Spending by Age Group",
                      labels={'avg_spending': 'Avg Spending ($)', 'count': 'Transaction Count'},
                      color='avg_spending', color_continuous_scale='plasma')
    fig5a.update_layout(template="plotly_white", height=350, font=dict(size=12))
    st.plotly_chart(fig5a, use_container_width=True)

with col2:
    gender_analysis = df.groupby('Gender')['Total Amount'].agg(['sum', 'count', 'mean']).reset_index()
    gender_analysis.columns = ['Gender', 'Total_Revenue', 'Transaction_Count', 'Avg_Order_Value']
    
    fig5b = px.bar(gender_analysis, x='Gender', y='Total_Revenue',
                   title="Revenue by Gender",
                   labels={'Total_Revenue': 'Total Revenue ($)'},
                   color='Gender', color_discrete_map={'Male': '#3498db', 'Female': '#e91e63'})
    fig5b.update_layout(template="plotly_white", height=350, showlegend=False, font=dict(size=12))
    st.plotly_chart(fig5b, use_container_width=True)

st.subheader(" Revenue Quality & Growth Trajectory")
col1, col2 = st.columns(2)

with col1:
    price_analysis = df.groupby('Product Category')[['Total Amount', 'Quantity']].sum()
    price_analysis['price_per_unit'] = price_analysis['Total Amount'] / price_analysis['Quantity']
    price_analysis = price_analysis.reset_index()
    
    fig6a = px.scatter(price_analysis, x='price_per_unit', y='Quantity', 
                      size='Total Amount', color='Total Amount',
                      hover_name='Product Category',
                      title="Price Elasticity Analysis",
                      labels={'price_per_unit': 'Price per Unit ($)', 'Quantity': 'Total Quantity Sold'},
                      color_continuous_scale='plasma')
    fig6a.update_layout(template="plotly_white", height=400, font=dict(size=12))
    st.plotly_chart(fig6a, use_container_width=True)

with col2:
    cat_month = df.groupby(['Product Category', df['Date'].dt.to_period('M')])['Total Amount'].sum().reset_index()
    cat_month['prev_month'] = cat_month.groupby('Product Category')['Total Amount'].shift(1)
    cat_month['growth_rate'] = (cat_month['Total Amount'] - cat_month['prev_month']) / cat_month['prev_month']
    cat_month['is_positive'] = cat_month['growth_rate'] > 0
    
    consistency = cat_month.groupby('Product Category')['is_positive'].mean().reset_index()
    consistency.columns = ['Category', 'Growth_Consistency']
    consistency = consistency.sort_values('Growth_Consistency', ascending=False)
    
    fig6b = px.bar(consistency, x='Category', y='Growth_Consistency',
                   title="Growth Consistency by Category",
                   labels={'Growth_Consistency': 'Months with Growth (%)'},
                   color='Growth_Consistency', color_continuous_scale='RdYlGn')
    fig6b.update_layout(template="plotly_white", height=400, yaxis=dict(range=[0, 1]), font=dict(size=12))
    st.plotly_chart(fig6b, use_container_width=True)

st.markdown("---")
st.subheader(" Key Insights Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"**Top Category:** {cat_rev.iloc[0]['Product Category']} (${cat_rev.iloc[0]['Total Amount']:,.0f})")
with col2:
    best_consistency = consistency.iloc[0]
    st.success(f"**Most Consistent:** {best_consistency['Category']} ({best_consistency['Growth_Consistency']*100:.0f}% growth months)")
with col3:
    top_price = price_analysis.iloc[0]
    st.warning(f"**Highest Price Point:** {top_price['Product Category']} (${top_price['price_per_unit']:.2f}/unit)")

st.info(" **Pro Tip:** Use the sidebar filters to drill down into specific time periods or categories for deeper analysis.")