# KPI Dashboard

A web-based KPI dashboard that allows you to upload Excel files and automatically generates interactive visualizations and key performance indicators.

## Features

- 📊 **Interactive Charts**: Bar charts, line charts, histograms, and pie charts
- 🎯 **KPI Cards**: Automatic calculation of totals and averages
- 📋 **Data Preview**: View your uploaded data before analysis
- 📈 **Summary Statistics**: Comprehensive statistical overview
- 🔄 **Real-time Updates**: Charts update based on column selection

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the dashboard**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser** and go to `http://localhost:8501`

4. **Upload your Excel file** and start analyzing!

## Usage

1. Upload an Excel file (.xlsx or .xls format)
2. Review the data preview to ensure correct loading
3. Select columns for KPI calculations
4. Explore the generated visualizations
5. Use the summary statistics for detailed analysis

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- Plotly
- OpenPyXL
- NumPy

## File Structure

```
kpi-dashboard/
├── app.py              # Main dashboard application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Tips for Best Results

- Ensure your Excel file has clear column headers
- Include numeric columns for meaningful KPI calculations
- Keep data reasonably sized for optimal performance
- Use categorical columns for grouping in pie charts