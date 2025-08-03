import streamlit as st
import pandas as pd
import plotly.graph_objects as go


@st.cache_data
def load_data(file):
    # Load data from the uploaded Excel file and convert 'Datum' to datetime format
    data = pd.read_excel(file)
    data["Datum"] = pd.to_datetime(
        data["Datum"], format="%d-%m-%Y %H:%M:%S", errors="coerce"
    )
    return data


def create_sankey_diagram(data, selected_date):
    # Filter data for the selected date
    filtered_data = data[data["Datum"].dt.date == selected_date]

    # Aggregating the total values for all energy sources
    sources = {
        "Gas": filtered_data[["Gas_1", "Gas_2", "Gas_3", "Gas_4", "Gas_5"]]
        .sum()
        .values,
        "Elektrische": filtered_data[
            [
                "Elektrische Energie_1",
                "Elektrische Energie_2",
                "Elektrische Energie_3",
                "Elektrische Energie_4",
                "Elektrische Energie_5",
            ]
        ]
        .sum()
        .values,
        "Waermeenergie": filtered_data[
            [
                "Waermeenergie_1",
                "Waermeenergie_2",
                "Waermeenergie_3",
                "Waermeenergie_4",
                "Waermeenergie_5",
            ]
        ]
        .sum()
        .values,
        "Druckluft": filtered_data[
            ["Druckluft_1", "Druckluft_2", "Druckluft_3", "Druckluft_4", "Druckluft_5"]
        ]
        .sum()
        .values,
        "Oel": filtered_data[["Oel_1", "Oel_2", "Oel_3", "Oel_4", "Oel_5"]]
        .sum()
        .values,
        "Kuehlwasser": filtered_data[
            [
                "Kuehlwasser_1",
                "Kuehlwasser_2",
                "Kuehlwasser_3",
                "Kuehlwasser_4",
                "Kuehlwasser_5",
            ]
        ]
        .sum()
        .values,
        "Heizwasser": filtered_data[
            [
                "Heizwasser_1",
                "Heizwasser_2",
                "Heizwasser_3",
                "Heizwasser_4",
                "Heizwasser_5",
            ]
        ]
        .sum()
        .values,
        "Wasser": filtered_data[
            ["Wasser_1", "Wasser_2", "Wasser_3", "Wasser_4", "Wasser_5"]
        ]
        .sum()
        .values,
    }

    # Define high-contrast colors for nodes (each source has the same color for its links)
    source_colors = [
        "#f87c24",
        "#ff7f0e",
        "#ffb732",
        "#ffd27f",
        "#D4D4D4",
        "#909090",
        "#ffedcc",
        "#778899",
    ]

    # Preparing Sankey diagram input
    source = []
    target = []
    values = []
    link_colors = []

    for i, (key, values_array) in enumerate(sources.items()):
        for j, value in enumerate(values_array):
            source.append(i)  # Energy source
            target.append(len(sources) + j)  # Machines
            values.append(value)
            link_colors.append(
                source_colors[i]
            )  # Use the same color for all links from a source

    # Define node labels
    node_labels = list(sources.keys()) + [f"Maschine {i + 1}" for i in range(5)]

    # Create the Sankey diagram
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="white", width=0.5),
                    label=node_labels,
                    color=source_colors
                    + [
                        "#636efa",
                        "#ef553b",
                        "#00cc96",
                        "#ab63fa",
                        "#FFA15A",
                    ],  # Extend for machines
                ),
                link=dict(
                    source=source,
                    target=target,
                    value=values,
                    color=link_colors,
                    hovertemplate="Value: %{value:.2f}<extra></extra>",
                ),
            )
        ]
    )

    fig.update_layout(
        title_text=f"Sankey Diagram for Energy Distribution on {selected_date}",
        font_size=10,
        width=1400,  # Increased width
        height=700,  # Increased height
        plot_bgcolor="#1e1e1e",
        paper_bgcolor="#1e1e1e",
        font_color="white",
    )
    return fig


def main():
    st.title("Sankey Diagram for Energy Distribution")

    # Sidebar for file upload
    st.sidebar.title("Upload Excel File")
    uploaded_file = st.sidebar.file_uploader(
        "Upload an Excel file", type=["xls", "xlsx"]
    )

    if uploaded_file is not None:
        # Load data from the uploaded file
        data = load_data(uploaded_file)

        # Slider for selecting the date
        st.sidebar.title("Select Date")
        data["Date"] = data["Datum"].dt.date  # Extract date from 'Datum'
        date_options = data["Date"].unique()  # Get unique dates from 'Datum' column
        selected_date = st.sidebar.slider(
            "Select Date",
            min_value=min(date_options),
            max_value=max(date_options),
            value=min(date_options),  # Default to the first date
            format="YYYY-MM-DD",
        )

        # Create the Sankey diagram for the selected date
        sankey_fig = create_sankey_diagram(data, selected_date)
        if sankey_fig:
            st.plotly_chart(sankey_fig)


if __name__ == "__main__":
    main()
