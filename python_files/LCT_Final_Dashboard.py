import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
import plotly.express as px
import re

# Function to load the Excel data file into a DataFrame.
# This function is cached to optimize performance, so it doesn't reload the file multiple times.
# It reads the file and returns the DataFrame containing the data.

@st.cache_data
def load_data(file):
    return pd.read_excel(file)

# Function to normalize text by stripping extra spaces and converting to lowercase.
# This ensures that column values like 'Car Type', 'Country', and 'Indicator' are consistent
# for filtering and comparison, avoiding issues with inconsistent capitalization and extra spaces.

def normalize_text(text):
    if isinstance(text, str):
        return re.sub(' +', ' ', text.strip()).lower()
    return text

def main():

    """
    Main function to handle user interactions, including uploading files, selecting filters, 
    and displaying the respective visualizations. The app allows users to interactively select
    filters and visualize life cycle cost and assessment data based on their selections.
    """

    # Sidebar for uploading the LCT Antriebsystem DataSheet file
    st.sidebar.title("Upload LCT Antriebsystem DataSheet")
    uploaded_file_1 = st.sidebar.file_uploader("Upload an Excel file for Data Visualization (File 1)", type=["xls", "xlsx"])

    # Sidebar for uploading the Cost Analysis Data file
    st.sidebar.title("Upload Cost Analysis Data")
    uploaded_file_2 = st.sidebar.file_uploader("Upload an Excel file for Data Visualization (File 2)", type=["xls", "xlsx"])

    # Sidebar for applying general filters to the data
    st.sidebar.title("Selection Filters")
    
    # Filters for selecting geographic scenarios
    geographic_scenario = st.sidebar.multiselect(
        "Select Geographic Scenario",
        ['China Owner City', 'China Shuttle', 'Germany Car Sharing', 'Germany Countryside',
         'Germany Owner City', 'Germany Shuttle', 'Hong Kong Car Sharing',
         'Hong Kong Owner City', 'Hong Kong Shuttle', 'Poland Car Sharing', 'Poland Owner City']
    )

    # Filters for selecting years
    year = st.sidebar.multiselect(
        "Select Year",
        ['2020', '2030', '2040']
    )

    # Filters for selecting car types
    car_type = st.sidebar.multiselect(
        "Select Car Type",
        ['BEV', 'Diesel', 'Otto', 'FCEV', 'PHEV o*', 'PHEV 0*', 'PHEV e*']
    )

    # Filters for selecting environmental impact indicators
    indicator = st.sidebar.multiselect(
        "Select Indicator",
        ['Carcinogenic effects - Total', 'Biogenic', 'Climate change - Total', 'Fossils', 'Fossil', 'Freshwater and terrestrial acidification', 'Freshwater ecotoxicity - Total', 'Freshwater eutrophication', 'Ionizing radiation', 'Land use', 'Land use and land use change', 'Marine eutrophication', 'Minerals and metals', 'Non-carcinogenic effects - Total', 'Ozone layer depletion', 'Photochemical ozone creation', 'Terrestrial eutrophication', 'Water scarcity']
    )

    # Session state to keep track of which visualization is being shown
    # Each session state flag corresponds to a specific section of the app
    if 'show_waterfall' not in st.session_state:
        st.session_state.show_waterfall = False
    if 'show_assessment' not in st.session_state:
        st.session_state.show_assessment = False
    if 'show_correlation_matrix' not in st.session_state:
        st.session_state.show_correlation_matrix = False

    # If the user has uploaded a file, process it and generate visualizations
    if uploaded_file_1 is not None:
        try:
            # Load the uploaded file into a DataFrame
            df = load_data(uploaded_file_1)

            # Ensure the necessary columns are present in the uploaded file
            required_columns = ['Country', 'Year', 'Car Type', 'ReferenceFlow', 'Quantity', 'LifeCyclePhase', 'Indicator', 'Process']
            if not all(col in df.columns for col in required_columns):
                st.error(f"Missing columns in the uploaded file.")
                return

            # Normalize the 'Year' column and convert it to integer for comparison
            df['Year'] = df['Year'].astype(str).str.replace(',', '').astype(int)

            # Normalize relevant columns to handle extra spaces and inconsistencies in the data
            df['Country'] = df['Country'].apply(normalize_text)
            df['Car Type'] = df['Car Type'].apply(normalize_text)
            df['Indicator'] = df['Indicator'].apply(normalize_text)

            # Normalize the filter selections to ensure they match the format in the DataFrame
            geographic_scenario = [normalize_text(scenario) for scenario in geographic_scenario]
            car_type = [normalize_text(ctype) for ctype in car_type]
            indicator = [normalize_text(ind) for ind in indicator]

            # Filter the dataset based on user-selected values in the filters
            filtered_df = df.copy()
            if geographic_scenario:
                filtered_df = filtered_df[filtered_df['Country'].isin(geographic_scenario)]
            if year:
                filtered_df = filtered_df[filtered_df['Year'].isin([int(y) for y in year])]
            if car_type:
                filtered_df = filtered_df[filtered_df['Car Type'].isin(car_type)]
            if indicator:
                filtered_df = filtered_df[filtered_df['Indicator'].isin(indicator)]

            # Further filter the data based on specific reference flows of interest
            reference_flows = ['Bauteil Tür (eingebaut)_Funier-50/50-Stahl', 'Bauteil Tür (eingebaut)_Stahl A-50/50-Stahl B', 'Serienbauteil Hutprofil (eingebaut)', 'Hybridbauteil Hutprofil (eingebaut)']
            filtered_df = filtered_df[filtered_df['ReferenceFlow'].isin(reference_flows)]

            # Create a bar chart visualization based on the filtered data
            create_bar_chart_1(filtered_df, indicator)

            # Only create the heatmap if Year and Car Type are selected
            if year and car_type:
                heatmap_filtered_df = df.copy()  # Use the original DataFrame to include all scenarios and indicators
                heatmap_filtered_df = heatmap_filtered_df[heatmap_filtered_df['Year'].isin([int(y) for y in year])]
                heatmap_filtered_df = heatmap_filtered_df[heatmap_filtered_df['Car Type'].isin(car_type)]
                create_heatmap(heatmap_filtered_df)

            # Display buttons to toggle between different visualizations
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Detailed Life Cycle Costing", key="button_middle", help="Click for detailed life cycle costing"):
                    st.session_state.show_waterfall = not st.session_state.show_waterfall
                    st.session_state.show_assessment = False
                    st.session_state.show_correlation_matrix = False
            with col2:
                if st.button("Detailed LifeCycle Assessment", key="button_assessment", help="Click for detailed life cycle assessment"):
                    st.session_state.show_assessment = not st.session_state.show_assessment
                    st.session_state.show_waterfall = False
                    st.session_state.show_correlation_matrix = False
            with col3:
                if st.button("Correlation Matrix", key="button_correlation_matrix", help="Click to show the correlation matrix"):
                    st.session_state.show_correlation_matrix = not st.session_state.show_correlation_matrix
                    st.session_state.show_waterfall = False
                    st.session_state.show_assessment = False

            # Store the filtered DataFrame in session state for later use
            st.session_state.filtered_df = filtered_df

        except Exception as e:
            st.error(f"Error: {e}")
            st.write("Please make sure the uploaded file is a valid Excel file.")

    # Display the selected visualizations based on button states
    if st.session_state.show_waterfall:
        if uploaded_file_2 is not None:
            detailed_life_cycle_costing(uploaded_file_2)
        else:
            st.error("Please upload the second Excel file for detailed life cycle costing.")

    if st.session_state.show_assessment:
        if "filtered_df" in st.session_state:
            detailed_lifecycle_assessment(st.session_state.filtered_df)
            
            # Show scatter plot after the detailed lifecycle assessment is displayed
            if indicator:
                create_scatter_plot_with_difference(df, indicator)

        else:
            st.error("Filtered data not available. Please apply filters and try again.")

    if st.session_state.show_correlation_matrix:
        if "filtered_df" in st.session_state:
            create_correlation_matrix(st.session_state.filtered_df, geographic_scenario, year, car_type)
        else:
            st.error("Filtered data not available. Please apply filters and try again.")

# Function to create and display the correlation matrix heatmap
# The correlation matrix visualizes the relationships between different environmental indicators
# The indicator names are replaced by abbreviations for a more concise and readable display
            
def create_correlation_matrix(df, selected_scenarios, selected_years, selected_car_types):
    """
    This function generates a correlation matrix heatmap for the selected indicators.
    It calculates the correlation between different environmental indicators based on the filtered data
    and displays it as a heatmap.
    """
    # Define a mapping from full indicator names to abbreviations for better readability
    indicator_abbreviations = {
        'carcinogenic effects - total': 'CT',
        'biogenic': 'BG',
        'climate change - total': 'CC',
        'fossils': 'FS',
        'fossil': 'FO',
        'freshwater and terrestrial acidification': 'FTA',
        'freshwater ecotoxicity - total': 'FET',
        'freshwater eutrophication': 'FE',
        'ionizing radiation': 'IR',
        'land use': 'LU',
        'land use and land use change': 'LUC',
        'marine eutrophication': 'ME',
        'minerals and metals': 'MM',
        'non-carcinogenic effects - total': 'NCT',
        'ozone layer depletion': 'OLD',
        'photochemical ozone creation': 'POC',
        'terrestrial eutrophication': 'TE',
        'water scarcity': 'WS'
    }

    # Filter the data based on the selected indicators and other filters (geographic scenario, year, car type)
    filtered_df = df[df['Indicator'].isin(indicator_abbreviations.keys())]
    
    # Apply filters based on selected geographic scenarios, car types, and years
    if selected_scenarios:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_scenarios)]
    if selected_years:
        filtered_df = filtered_df[filtered_df['Year'].isin([int(y) for y in selected_years])]
    if selected_car_types:
        filtered_df = filtered_df[filtered_df['Car Type'].isin(selected_car_types)]
    
    # Pivot the data to calculate quantities for each indicator across the selected categories
    pivot_df = filtered_df.pivot_table(index=['Country', 'Year', 'Car Type'], 
                                       columns='Indicator', 
                                       values='Quantity', 
                                       aggfunc='sum', fill_value=0)
    
    # Calculate the correlation matrix between the indicators
    correlation_matrix = pivot_df.corr()

    # Replace full indicator names with their abbreviations in the correlation matrix
    correlation_matrix.columns = [indicator_abbreviations.get(col, col) for col in correlation_matrix.columns]
    correlation_matrix.index = [indicator_abbreviations.get(idx, idx) for idx in correlation_matrix.index]

    # Create and display the heatmap for the correlation matrix using Plotly
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale='Viridis',
        zmin=-1,
        zmax=1
    ))

    fig.update_layout(
        title="Correlation Matrix of Indicators",
        xaxis_title="Indicators",
        yaxis_title="Indicators",
        template="plotly_dark"
    )

    st.plotly_chart(fig)

# Function to generate the scatter plot comparing differences between pairs of reference flows
def create_scatter_plot_with_difference(df, selected_indicators):
    """
    This function generates a scatter plot comparing the differences in quantities
    between pairs of reference flows for the selected indicator.
    The scatter plot allows for a visual comparison of how the quantities for different
    reference flows differ across years and car types.
    """
    if not selected_indicators:
        st.write("Please select at least one indicator to generate the scatter plot.")
        return

    # Ensure we only work with the selected indicator
    indicator = selected_indicators[0]
    df = df[df['Indicator'] == indicator]

    if df.empty:
        st.write("No data available for the selected indicator to generate the scatter plot.")
        return

    # Define the pairs of reference flows to compare
    reference_pairs = [
        ('Hybridbauteil Hutprofil (eingebaut)', 'Serienbauteil Hutprofil (eingebaut)'),
        ('Bauteil Tür (eingebaut)_Funier-50/50-Stahl', 'Bauteil Tür (eingebaut)_Stahl A-50/50-Stahl B')
    ]

    scatter_data = []

    # Loop through the years and car types to calculate the difference in quantities for each reference flow pair
    for year in df['Year'].unique():
        for car_type in df['Car Type'].unique():
            car_type_year_df = df[(df['Car Type'] == car_type) & (df['Year'] == year)]
            
            for pair in reference_pairs:
                # Check if both reference flows are present in the filtered data
                if set(pair).issubset(set(car_type_year_df['ReferenceFlow'])):
                    # Calculate the difference in Quantity between the two reference flows
                    ref_flow_1_quantity = car_type_year_df[car_type_year_df['ReferenceFlow'] == pair[0]]['Quantity'].sum()
                    ref_flow_2_quantity = car_type_year_df[car_type_year_df['ReferenceFlow'] == pair[1]]['Quantity'].sum()
                    
                    # Calculate difference in the correct order (first - second)
                    diff = ref_flow_1_quantity - ref_flow_2_quantity
                    
                    # Append the calculated difference to the scatter data
                    scatter_data.append({
                        'Car Type': car_type,
                        'Year': year,
                        'Reference Flow 1': pair[0],
                        'Reference Flow 2': pair[1],
                        'Difference': diff,
                        'Indicator': indicator
                    })

    # Convert the scatter data to a DataFrame for plotting
    scatter_df = pd.DataFrame(scatter_data)

    if not scatter_df.empty:
        # Create and display the scatter plot using Plotly
        fig = px.scatter(
            scatter_df,
            x='Car Type',
            y='Difference',
            color='Year',
            title=f"Scatter Plot for Indicator: {indicator.title()}",
            labels={'Difference': 'Difference (Quantity)', 'Car Type': 'Car Type', 'Year': 'Year'},
            template="plotly_dark"
        )

        fig.update_traces(
            customdata=scatter_df[['Year', 'Difference', 'Car Type', 'Reference Flow 1', 'Reference Flow 2']].values,
            hovertemplate="<b>Car Type:</b> %{customdata[2]}<br>" +
                          "<b>Difference:</b> %{customdata[1]:,.2f}<br>" +
                          "<b>Year:</b> %{customdata[0]}<br>" +
                          "<b>Reference Flow 1:</b> %{customdata[3]}<br>" +
                          "<b>Reference Flow 2:</b> %{customdata[4]}<extra></extra>"
        )

        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected filters to generate the scatter plot.")

# Function to create and display the bar chart of reference flows and their quantities
def create_bar_chart_1(df, selected_indicators):
    """
    This function generates a bar chart that visualizes the quantities of selected reference flows
    for the chosen indicators. The chart is grouped by the reference flows, and it shows the sum
    of the quantities for each reference flow.
    """
    reference_flows = [
        'Bauteil Tür (eingebaut)_Funier-50/50-Stahl',
        'Bauteil Tür (eingebaut)_Stahl A-50/50-Stahl B',
        'Serienbauteil Hutprofil (eingebaut)',
        'Hybridbauteil Hutprofil (eingebaut)'
    ]
    new_names = [
        'Bauteil Tür Reference',
        'Bauteil Tür Hybrid',
        'Serienbauteil',
        'Hybridbauteil'
    ]

    quantities = [df[df['ReferenceFlow'] == rf]['Quantity'].sum() for rf in reference_flows]

    # Mapping of indicators to their respective units for the y-axis
    y_axis_titles = {
        'carcinogenic effects - total': 'CTUh',
        'biogenic': 'kg CO2-Eq',
        'climate change - total': 'kg CO2-Eq',
        'fossils': 'MJ',
        'fossil': 'kg CO2-Eq',
        'freshwater and terrestrial acidification': 'mol H+-Eq',
        'freshwater ecotoxicity - total': 'CTUe',
        'freshwater eutrophication': 'kg P-Eq',
        'ionizing radiation': 'kBq U235-Eq',
        'land use': 'points',
        'land use and land use change': 'kg CO2-Eq',
        'marine eutrophication': 'kg N-Eq',
        'minerals and metals': 'kg Sb-Eq',
        'non-carcinogenic effects - total': 'CTUh',
        'ozone layer depletion': 'kg CFC-11-Eq',
        'photochemical ozone creation': 'kg NMVOC-Eq',
        'terrestrial eutrophication': 'mol N-Eq',
        'water scarcity': 'm3 world-Eq deprived'
    }

    y_axis_title = y_axis_titles.get(selected_indicators[0], 'Units') if selected_indicators else 'Units'

    # Prepare the data for the bar chart
    bar_chart_data = pd.DataFrame({
        'ReferenceFlow': new_names,
        'Quantity': quantities
    })

    if bar_chart_data['Quantity'].sum() != 0:
        # Customize bar colors and create the bar chart
        custom_colors = ['#F57600', '#395d78', '#FF8C00', '#808080']

        fig = go.Figure()

        for index, row in bar_chart_data.iterrows():
            fig.add_trace(go.Bar(
                x=[row['ReferenceFlow']],
                y=[row['Quantity']],
                name=row['ReferenceFlow'],
                marker_color=custom_colors[index],
                hovertext=[row['Quantity']]
            ))

        # Update layout with titles and styling
        fig.update_layout(
            title={
                'text': "Overview of LifeCycle Costing and Assessment",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Reference Flow",
            yaxis_title=y_axis_title,
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            barmode='group'
        )

        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected filters.")
    
# Function to create a heatmap visualizing the distribution of indicators across scenarios
def create_heatmap(df):
    """
    This function generates a heatmap that visualizes the percentage distribution of selected environmental indicators
    across different geographic scenarios. The heatmap helps identify how different indicators are distributed
    across the scenarios.
    """
    indicators = [
        'carcinogenic effects - total', 'biogenic', 'climate change - total',
        'fossils', 'fossil', 'freshwater and terrestrial acidification',
        'freshwater ecotoxicity - total', 'freshwater eutrophication',
        'ionizing radiation', 'land use', 'land use and land use change',
        'marine eutrophication', 'minerals and metals',
        'non-carcinogenic effects - total', 'ozone layer depletion',
        'photochemical ozone creation', 'terrestrial eutrophication',
        'water scarcity'
    ]

    heatmap_data = []
    for scenario in df['Country'].unique():
        scenario_data = df[df['Country'] == scenario]
        total_quantity = scenario_data['Quantity'].sum()
        scenario_percentages = [scenario_data[scenario_data['Indicator'] == indicator]['Quantity'].sum() / total_quantity * 100 if total_quantity else 0 for indicator in indicators]
        heatmap_data.append(scenario_percentages)

    # Prepare the data for the heatmap
    heatmap_df = pd.DataFrame(heatmap_data, columns=indicators, index=df['Country'].unique())

    # Create the heatmap using Plotly
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_df.values,
        x=heatmap_df.columns,
        y=heatmap_df.index,
        colorscale='Viridis',
        zmin=0,
        zmax=100
    ))

    # Update layout with titles and styling
    fig.update_layout(
        title="Heatmap of Indicators by Geographic Scenario",
        xaxis_title="Indicator",
        yaxis_title="Scenario",
        template="plotly_dark"
    )

    st.plotly_chart(fig)

# Function to create the waterfall chart displaying detailed cost breakdowns
def detailed_life_cycle_costing(uploaded_file):
    """
    This function generates a waterfall chart to visualize the detailed breakdown of life cycle costs
    based on the second uploaded file (cost analysis data). It shows cost distribution across different categories
    (Material, Production, Nutzung, and End-of-Life).
    """
    try:
        df = load_data(uploaded_file)

        # Calculate the total cost in each category
        hybrid_m_total = df.groupby('Hybrid_M')['KostM'].sum().sum()
        hybrid_p_total = df.groupby('Hybrid_P')['KostP'].sum().sum()
        hybrid_n_total = df.groupby('Hybrid_N')['KostN'].sum().sum()
        hybrid_e_total = df.groupby('Hybrid_E')['KostE'].sum().sum()

        # Prepare data for the waterfall chart
        waterfall_data = {
            'Category': ['Material', 'Production', 'Nutzung', 'End-of-Life'],
            'Kosten': [hybrid_m_total, hybrid_p_total, hybrid_n_total, hybrid_e_total]
        }

        # Create the waterfall chart using Plotly
        waterfall_fig = go.Figure(
            go.Waterfall(
                name="Produktion",
                orientation="v",
                measure=["relative", "relative", "relative", "relative"],
                x=waterfall_data['Category'],
                y=waterfall_data['Kosten'],
                textposition="none",
                connector={"line":{"color":"black"}},
                decreasing={"marker":{"color":"#b04238"}},
                increasing={"marker":{"color":"#b04238"}},
                totals={"marker":{"color":"#b04238"}}
            )
        )

        # Update layout for the waterfall chart
        waterfall_fig.update_layout(
            xaxis_title="Category",
            yaxis_title="Total Kosten [€]",
            template="plotly_dark"
        )

        # Display the chart
        selected_points = plotly_events(waterfall_fig, click_event=True, hover_event=False)

        # Handle click events on the chart
        if selected_points:
            selected_category = selected_points[0]['x']
            if selected_category == 'Material':
                pie_data = df.groupby('Hybrid_M')['KostM'].sum()
                title = "Material Kosten Distribution"
            elif selected_category == 'Production':
                pie_data = df.groupby('Hybrid_P')['KostP'].sum()
                title = "Production Kosten Distribution"
            elif selected_category == 'Nutzung':
                pie_data = df.groupby('Hybrid_N')['KostN'].sum()
                title = "Nutzung Kosten Distribution"
            elif selected_category == 'End-of-Life':
                pie_data = df.groupby('Hybrid_E')['KostE'].sum()
                title = "End-of-Life Kosten Distribution"

            # Create a pie chart for the selected category
            pie_chart = go.Figure(data=[go.Pie(labels=pie_data.index, values=pie_data.values, textinfo='value')])
            pie_chart.update_layout(
                title=title,
                template="plotly_dark"
            )
            
            # Display the pie chart
            st.plotly_chart(pie_chart)

    except Exception as e:
        st.error(f"Error: {e}")
        st.write("Please make sure the uploaded file is a valid Excel file.")

# Function to perform detailed life cycle assessment and generate a sunburst chart
def detailed_lifecycle_assessment(df):
    """
    This function generates a sunburst chart that visualizes the life cycle processes and phases.
    It shows how processes are distributed across different life cycle phases and helps users understand
    the overall life cycle assessment in a hierarchical way.
    """
    try:
        processes = df['Process'].unique()

        df['Count'] = 1

        df_grouped = df.groupby(['LifeCyclePhase', 'Process']).size().reset_index(name='Count')
        df_grouped['Percentage'] = df_grouped.groupby('LifeCyclePhase')['Count'].apply(lambda x: 100 * x / float(x.sum())).reset_index(drop=True)

        # Define color sequence for different life cycle phases
        color_sequence = ['#FF6500', '#FA6E00', '#F57600', '#F8891B', '#FA9B35']

        # Generate sunburst chart using Plotly
        fig = px.sunburst(df_grouped, path=['LifeCyclePhase', 'Process'], values='Count',
                          hover_data={'Percentage': ':.2f'},
                          color='LifeCyclePhase',
                          color_discrete_sequence=color_sequence)

        fig.update_traces(textinfo='label+percent entry')

        # Update layout
        fig.update_layout(
            margin=dict(t=50, l=25, r=25, b=25),
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )

        # Display the sunburst chart
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error: {e}")
        st.write("Please make sure the uploaded data is valid.")

# Run the main function to launch the app
if __name__ == "__main__":
    main()
