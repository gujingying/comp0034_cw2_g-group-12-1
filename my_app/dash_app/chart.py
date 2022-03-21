import plotly.graph_objects as go


class AirQualityChart:
    """ Creates the recycling line chart to be used in the dashboard"""

    def __init__(self, data):
        self.data = data

    def create_chart(self, area, airtype):
        area_data = self.data.AirQuality_area
        eng_data = self.data.AirQuality_eng
        area = go.Scatter(x=area_data['utc'], y=area_data[airtype],
                          mode='markers',
                          name=area,
                          line=dict(color='lightseagreen', width=0.1))

        eng = go.Scatter(x=eng_data['utc'], y=eng_data[airtype],
                         mode='markers',
                         name='London',
                         line=dict(color='lightblue', width=0.1))

        # Create the layout
        layout = go.Layout(showlegend=True, plot_bgcolor="#ffffff")

        # Create the figure
        figure = go.Figure(layout=layout)

        # Update the figure and add the traces
        figure.add_trace(area)
        figure.add_trace(eng)

        # Update the layout of the axes to look a little closer to the original chart we are copyin
        figure.update_layout(yaxis_title=airtype)
        figure.update_yaxes(title_font=dict(size=14, color='#4D4D4D'),
                            tickfont=dict(color='#4D4D4D', size=12), ticksuffix="",
                            showgrid=True, gridwidth=1, gridcolor='#4D4D4D',
                            tick0=0.0, dtick=10.0)
        figure.update_xaxes(tickangle=90, tickfont=dict(color='#4D4D4D', size=12),
                            showline=True, linewidth=2, linecolor='#4D4D4D')

        return figure
