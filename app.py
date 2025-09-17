import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page config
st.set_page_config(
    page_title="KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

# Cache data loading to prevent re-reading on every interaction
@st.cache_data
def load_excel_data(uploaded_file):
    return pd.read_excel(uploaded_file)

# Cache chart creation to prevent regeneration
@st.cache_data
def create_bar_chart(df, column, limit=20):
    data = df.head(limit)
    fig = px.bar(data, y=column, title=f"{column} - Top {limit} Values", 
                 color=column, color_continuous_scale="viridis")
    return fig

@st.cache_data
def create_line_chart(df, column, limit=50):
    data = df.head(limit)
    fig = px.line(data, y=column, title=f"{column} - Trend Analysis", markers=True)
    return fig

@st.cache_data
def create_histogram(df, column):
    fig = px.histogram(df, x=column, title=f"{column} - Distribution", nbins=20)
    return fig

@st.cache_data
def create_pie_chart(df, cat_col, val_col):
    pie_data = df.groupby(cat_col)[val_col].sum().reset_index()
    # Limit to top 10 categories for performance
    pie_data = pie_data.nlargest(10, val_col)
    fig = px.pie(pie_data, values=val_col, names=cat_col, title=f"{val_col} by {cat_col}")
    return fig

# Title
st.title("📊 KPI Dashboard")
st.markdown("Upload your Excel file to generate interactive KPI visualizations")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an Excel file",
    type=['xlsx', 'xls'],
    help="Upload an Excel file containing your KPI data"
)

if uploaded_file is not None:
    try:
        # Read Excel file with caching
        df = load_excel_data(uploaded_file)
        
        # Limit data size for performance
        if len(df) > 10000:
            st.warning(f"⚠️ Large dataset detected ({len(df)} rows). Using first 10,000 rows for performance.")
            df = df.head(10000)
        
        st.success(f"✅ File uploaded successfully! Found {len(df)} rows and {len(df.columns)} columns.")
        
        # Show data preview
        with st.expander("📋 Data Preview", expanded=False):
            st.dataframe(df.head(10))
        
        # Data info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            st.metric("Numeric Columns", len(numeric_cols))
        
        # Column selection for KPIs
        st.subheader("🎯 Configure Your KPIs")
        
        # Get numeric columns for KPI calculations
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_columns) > 0:
            # KPI Cards
            st.subheader("📈 Key Performance Indicators")
            
            # Select columns for KPI display
            selected_kpi_cols = st.multiselect(
                "Select columns for KPI cards:",
                numeric_columns,
                default=numeric_columns[:4] if len(numeric_columns) >= 4 else numeric_columns
            )
            
            if selected_kpi_cols:
                # Display KPI cards
                cols = st.columns(len(selected_kpi_cols))
                for i, col in enumerate(selected_kpi_cols):
                    with cols[i]:
                        total_value = df[col].sum()
                        avg_value = df[col].mean()
                        st.metric(
                            label=col,
                            value=f"{total_value:,.2f}",
                            delta=f"Avg: {avg_value:.2f}"
                        )
            
            # Charts section
            st.subheader("📊 Visualizations")
            
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                # Bar chart
                if len(numeric_columns) >= 1:
                    bar_col = st.selectbox("Select column for bar chart:", numeric_columns, key="bar")
                    if bar_col:
                        fig_bar = create_bar_chart(df, bar_col)
                        st.plotly_chart(fig_bar, use_container_width=True)
            
            with chart_col2:
                # Line chart
                if len(numeric_columns) >= 1:
                    line_col = st.selectbox("Select column for trend line:", numeric_columns, key="line")
                    if line_col:
                        fig_line = create_line_chart(df, line_col)
                        st.plotly_chart(fig_line, use_container_width=True)
            
            # Additional charts
            chart_col3, chart_col4 = st.columns(2)
            
            with chart_col3:
                # Histogram
                if len(numeric_columns) >= 1:
                    hist_col = st.selectbox("Select column for distribution:", numeric_columns, key="hist")
                    if hist_col:
                        fig_hist = create_histogram(df, hist_col)
                        st.plotly_chart(fig_hist, use_container_width=True)
            
            with chart_col4:
                # Pie chart (if categorical columns exist)
                categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                if len(categorical_cols) > 0 and len(numeric_columns) > 0:
                    cat_col = st.selectbox("Select category for pie chart:", categorical_cols, key="pie_cat")
                    val_col = st.selectbox("Select value for pie chart:", numeric_columns, key="pie_val")
                    
                    if cat_col and val_col:
                        fig_pie = create_pie_chart(df, cat_col, val_col)
                        st.plotly_chart(fig_pie, use_container_width=True)
            
            # Summary statistics
            st.subheader("📋 Summary Statistics")
            st.dataframe(df[numeric_columns].describe())
            
        else:
            st.warning("⚠️ No numeric columns found in your data. Please ensure your Excel file contains numeric data for KPI calculations.")
            
    except Exception as e:
        st.error(f"❌ Error reading the Excel file: {str(e)}")
        st.info("Please make sure your file is a valid Excel format (.xlsx or .xls)")

else:
    # Instructions when no file is uploaded
    st.info("👆 Please upload an Excel file to get started")
    
    st.markdown("""
    ### 📋 Instructions:
    1. **Upload** your Excel file using the file uploader above
    2. **Review** the data preview to ensure it loaded correctly
    3. **Configure** your KPIs by selecting relevant columns
    4. **Analyze** the generated charts and metrics
    
    ### 📊 What you'll get:
    - **KPI Cards** showing key metrics and totals
    - **Interactive Charts** including bar, line, histogram, and pie charts
    - **Summary Statistics** for all numeric columns
    - **Data Preview** to verify your upload
    
    ### 📁 Supported formats:
    - Excel files (.xlsx, .xls)
    - Data should include column headers
    - Numeric columns for KPI calculations
    """)