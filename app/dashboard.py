import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Utility functions can be directly placed here or imported from utils.py
class Dashboard:
    def __init__(self, df):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

    def create_pie_chart(self, column):
        """Create a Pie Chart for a specific column."""
        return px.pie(self.df, names=column, title=f"Distribution of {column}")

    def create_donut_chart(self, columns):
        """Create a Donut Chart for a specific column."""
        # If only one column is selected
        if len(columns) == 1:
            selected_column = columns[0]
            mean_value = self.df[selected_column].mean()
            median_value = self.df[selected_column].median()

            fallback_data = {
                'Metric': ['Mean', 'Median'],
                'Value': [mean_value, median_value]
            }

            fallback_chart = px.pie(
                fallback_data,
                names='Metric',
                values='Value',
                hole=0.4,
                title=f"Summary of {selected_column}"
            )

            st.plotly_chart(fallback_chart, use_container_width=True)

        # If more than one column is selected
        elif len(columns) > 1:
            averages = {col: self.df[col].mean() for col in columns}

            donut_data = {
                'Subject': list(averages.keys()),
                'Average': list(averages.values())
            }

            donut_chart = px.pie(
                donut_data,
                names='Subject',
                values='Average',
                hole=0.4,
                title=f"Average of {', '.join(columns)}"
            )

            return st.plotly_chart(donut_chart, use_container_width=True)
    

    def create_area_plot(self, x_column, y_columns):
        """Create an Area Plot with X and Y columns."""
        return px.area(self.df, x=x_column, y=y_columns, title=f"Area Plot of {x_column} & {', '.join(y_columns)}")

    def create_radar_chart(self, columns):
        """Create a Radar Chart from selected columns."""
        radar_data = self.df[columns].mean().reset_index()
        radar_data.columns = ['Metric', 'Value']

        fig = go.Figure(go.Scatterpolar(
            r=radar_data['Value'],                # The values for the radar chart
            theta=radar_data['Metric'],           # The metrics (column names)
            fill='toself',                        
            name='Radar Chart',                   
            line_color='red',       
            fillcolor='orange'
        ))
        
        fig.update_layout(
            title=f'Radar Chart of {", ".join(columns)}',
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(radar_data['Value'])]  # Adjust axis range based on data
                )
            )
        )
        return fig
        

    def create_gauge_chart(self, column, metric_type="mean", bar_color="orange", width=100, height=200):
        """Create a Gauge Chart for a specific column and metric type."""
        if metric_type == "mean":
            value = self.df[column].mean()
            title = f"Mean of {column}"
        elif metric_type == "median":
            value = self.df[column].median()
            title = f"Median of {column}"
        elif metric_type == "mode":
            value = self.df[column].mode().iloc[0] if not self.df[column].mode().empty else 0
            title = f"Mode of {column}"

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': title},
            gauge={
                'axis': {'range': [0, self.df[column].max()]},
                'bar': {'color': f"{bar_color}"},
            }
        ))

        fig.update_layout(
            width=width,      # Width of the gauge chart (default is 300)
            height=height,    # Height of the gauge chart (default is 300)
            margin=dict(t=50, b=0, l=0, r=0)  # Optionally, remove the margins for a tighter fit
        )

        return fig

    def render(self):
        """Render the entire dashboard."""
        # Overall Visualizations
        st.subheader("Overall Visualizations", anchor=False)
        # Gauge Metrics
        st.subheader("⏲ Gauge Metrics",  anchor=False)
        st.caption("Visualize key metrics like mean, median, or mode for selected numeric columns.")
        gauge1, gauge2, gauge3 = st.columns(3)

        with gauge1:
            # Gauge configuration with metric selection
            with st.popover("Configure Chart"):
                gauge1_col = st.selectbox("Select a column for Gauge Chart (numeric only):", self.numeric_cols, key="gauge1_col")
                gauge1_metric = st.radio("Select Metric Type:", ("mean", "median", "mode"), index=0, horizontal=True)

                # Set color based on metric type
                metric_color = {"mean": "red", "median": "blue", "mode": "green"}[gauge1_metric]

            if gauge1_col:
                fig = self.create_gauge_chart(gauge1_col, metric_type=gauge1_metric, bar_color=metric_color)
                try:
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.error("Duplicate Chart!")
                

        with gauge2:
            # Gauge configuration with metric selection
            with st.popover("Configure Chart"):
                gauge2_col = st.selectbox("Select a column for Gauge Chart (numeric only):", self.numeric_cols, key="gauge2_col")
                gauge2_metric = st.radio("Select Metric Type:", ("mean", "median", "mode"), index=1, horizontal=True)

                # Set color based on metric type
                metric_color = {"mean": "red", "median": "blue", "mode": "green"}[gauge2_metric]

            if gauge2_col:
                fig = self.create_gauge_chart(gauge2_col, metric_type=gauge2_metric, bar_color=metric_color)
                try:
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.error("Duplicate Chart!")

        with gauge3:
            # Gauge configuration with metric selection
            with st.popover("Configure Chart"):
                gauge3_col = st.selectbox("Select a column for Gauge Chart (numeric only):", self.numeric_cols, key="gauge3_col")
                gauge3_metric = st.radio("Select Metric Type:", ("mean", "median", "mode"), index=2, horizontal=True)

                # Set color based on metric type
                metric_color = {"mean": "red", "median": "blue", "mode": "green"}[gauge3_metric]

            if gauge3_col:
                fig = self.create_gauge_chart(gauge3_col, metric_type=gauge3_metric, bar_color=metric_color)
                try:
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.error("Duplicate Chart!")

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            # Pie Chart
            st.subheader("🎯 Pie Chart", anchor=False)
            st.caption("Show distribution of categorical data using an intuitive pie chart.")
            with st.popover("Configure Chart"):
                column_for_pie = st.selectbox("Select a column for the Pie Chart:", self.df.columns)
            if column_for_pie:
                pie_chart = self.create_pie_chart(column_for_pie)
                st.plotly_chart(pie_chart, use_container_width=True)

        with col2:
            # Donut Chart
            st.subheader("🎯 Donut Chart", anchor=False)
            st.caption("Display averages or distributions for numeric columns in a donut-style visualization.")
            numeric_cols_for_donut = [col for col in self.df.columns if self.df[col].dtype in ['float64', 'int64']]

            with st.popover("Configure Chart"):
                # Multi-select for numeric columns to include in the donut chart
                columns_for_donut = st.multiselect(
                    "Select columns for Donut Chart (e.g., grades):", numeric_cols_for_donut
                )

            self.create_donut_chart(columns_for_donut)

        st.markdown("---")  

        # Trend Analysis
        st.subheader("Trend Analysis", anchor=False)
        col3, col4 = st.columns(2)

        with col3:
            # Area Plot
            st.subheader("📈 Area Plot", anchor=False)
            st.caption("Analyze trends over time or across categories using an area plot.")
            with st.popover("Configure Chart"):
                area_x = st.selectbox("Select X-axis for Area Plot:", self.numeric_cols, key="area_x")
                area_y = st.multiselect("Select Y-axis for Area Plot:", self.numeric_cols, key="area_y")
            if area_x and area_y:
                area_plot = self.create_area_plot(area_x, area_y)
                st.plotly_chart(area_plot, use_container_width=True)

        with col4:
            # Radar Chart
            st.subheader("🧭 Radar Chart", anchor=False)
            st.caption("Compare multiple metrics on a radar chart for better insights.")
            with st.popover("Configure Chart"):
                radar_cols = st.multiselect("Select columns for Radar Chart (numeric only):", self.numeric_cols, key="radar_cols")
            if radar_cols:
                radar_chart = self.create_radar_chart(radar_cols)
                st.plotly_chart(radar_chart, use_container_width=True)
