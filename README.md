# Streamlit Energy Dashboards

Energy analytics and lifecycle cost dashboards built with Streamlit.

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Demo Videos](#demo-videos)  
3. [Dashboard Features](#dashboard-features)  
4. [Technologies Used](#technologies-used)  
5. [Getting Started](#getting-started)  
6. [Folder Structure](#folder-structure)  
7. [How to Run](#how-to-run)  
8. [Future Improvements](#future-improvements)  
9. [Contact](#contact)  

---

## Project Overview

This repository contains two interactive dashboards designed to analyze and visualize energy consumption, lifecycle cost, and environmental impact data. Built with Streamlit and Plotly, these dashboards provide intuitive filtering and rich visualizations to support decision-making and insights for energy management and sustainability projects.

The dashboards allow users to upload their own Excel datasets, explore detailed cost breakdowns, lifecycle assessments, and energy distribution flows with dynamic Sankey diagrams, heatmaps, scatter plots, and waterfall charts.

---

## Demo Videos

### Life Cycle Cost Dashboard

<video width="700" controls>
  <source src="videos/LCT_Dashboard_Video.mov" type="video/quicktime">
  Your browser does not support the video tag.
</video>

---

### Energy Distribution Sankey Dashboard

<video width="700" controls>
  <source src="videos/Energy_Dashboard_Video.mov" type="video/quicktime">
  Your browser does not support the video tag.
</video>

---

## Dashboard Features

### Life Cycle Costing & Assessment Dashboard

- Upload Excel files with life cycle data.
- Filter by geographic scenario, year, car type, and environmental indicators.
- Visualize:
  - Bar charts showing reference flow quantities.
  - Heatmaps of indicator distributions across scenarios.
  - Scatter plots comparing lifecycle differences.
  - Detailed waterfall charts of cost categories with interactive pie breakdowns.
  - Sunburst charts for lifecycle phase and process distribution.
  - Correlation matrix heatmaps of environmental indicators.

### Energy Distribution Sankey Dashboard

- Upload time-series Excel data on energy consumption.
- Select dates to explore detailed Sankey diagrams of energy flows.
- Visualize energy sources (gas, electricity, heat, oil, water, etc.) and consumption by multiple machines.
- Use high-contrast color schemes for clear flow tracing.

---

## Technologies Used

- **Python 3.7+**  
- **Streamlit**: For building interactive web apps quickly.  
- **Pandas**: Data manipulation and cleaning.  
- **Plotly**: Advanced visualizations including Sankey diagrams, heatmaps, scatter plots, and sunburst charts.  
- **Regex**: For text normalization and cleaning in data preprocessing.  
- **streamlit-plotly-events**: For interactivity in Plotly charts.

---

## Getting Started

### Prerequisites

- Python 3.7 or newer installed.
- Recommended: Create and activate a virtual environment.

### Installation

Install the required packages with:

```bash
pip install streamlit pandas plotly openpyxl streamlit-plotly-events

---

### Folder Structure

streamlit-energy-dashboards/
│
├── python_files/                # Python dashboard scripts
│   ├── main_dashboard.py        # Life Cycle Costing & Assessment dashboard
│   └── energy_distribution.py  # Energy Distribution Sankey dashboard
│
├── videos/                     # Demo videos of dashboards
│   ├── LCT_Dashboard_Video.mov
│   └── Energy_Dashboard_Video.mov
│
├── README.md                   # Project overview and instructions
├── LICENSE                    # MIT License
└── .gitignore                 # Python-specific ignores

---

## How to Run

1. Clone this repository:

```bash
git clone https://github.com/DCodesIt/streamlit-energy-dashboards.git
cd streamlit-energy-dashboards

2. Run the Life Cycle Cost dashboard:

```bash
streamlit run python_files/main_dashboard.py

3. Run the Energy Distribution Sankey dashboard:

```bash
streamlit run python_files/energy_distribution.py

4. Upload your Excel files in the app interface and interact with the dashboards.

---

## Future Improvements

- Add synthetic sample datasets to allow users to test the dashboards without confidential data.
- Enhance UI with custom themes and layouts.
- Integrate caching and performance optimizations for larger datasets.
- Add automated tests and CI/CD pipeline.
- Extend dashboards with real-time data integration and alerts.

---

Contact

Divesh Chonkar
Email: diveshchonkar.ds@gmail.com  
GitHub: https://github.com/DCodesIt  
LinkedIn: https://linkedin.com/in/diveshchonkar

Thank you for reviewing my project.
