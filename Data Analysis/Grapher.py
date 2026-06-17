# ============================================
# Gadolinium Concentration Grapher
# Purpose: Graphs data values from ExpFit into
#   24 hour, 1 month, 1 year graphs
# ============================================
# Imports and File Definitions

import plotly as pl
import pandas as pd

# ============================================
# Code

# Currently, all placeholders test the old data sets
# --------------------------------------------
# Test graphing

class Grapher:
    def __init__(self, testrun, Ch1V, timeAxis):
        self.testrun = testrun
        self.error_y=dict(type="data", array=(0.1 * testrun.y_fit), visible=True)
        self.Ch1V = Ch1V
        self.timeAxis = timeAxis

    def plot(self):
        fig = pl.graph_objs.Figure()

        fig.add_trace(
            pl.graph_objs.Scatter(
                name='Ch1 V',
                x=self.testrun.time_axis,
                y=self.Ch1V,
                mode="lines",
                hovertemplate="t: %{x:.3e} s<br>V: %{y:.3e} V<extra></extra>"
            )
        )
        if self.testrun.y_model is not None:
            fig.add_trace(
                pl.graph_objs.Scatter(
                    x=self.testrun.x_fit,
                    y=self.testrun.y_model,
                    # error_y=self.error_y,
                    mode="lines",
                    name="Exponential fit",
                    line=dict(dash="dash"),
                    line_color="red"
                )
            )

        fig.update_layout(
            title= "Placeholder",
            xaxis_title="Time (s)",
            yaxis_title="Voltage (V) (ZEROED)",
        )

        fig.show()

class MinutelyGraph:
    def __init__(self,data):
        self.data = data
    def plotLongTerm(self):
        self.timeStamp = []
        self.y_data = []
        self.error_data = []

        for i in self.data:
            self.timeStamp.append(float(i[0]))
            self.y_data.append(float(i[1]))
            self.error_data.append(float(i[2]))

        data = {'timestamp': self.timeStamp, 'y_data': self.y_data, 'error': self.error_data}
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['timestamp'], unit='s')

        fig = pl.graph_objs.Figure()
        fig.add_trace(
            pl.graph_objs.Scatter(
                name='Long-term Concentration (Minutely)',
                x=df['date'],
                y=df['y_data'],
                error_y=dict(type="data", array=self.error_data, visible=True),
                mode="lines",
                hovertemplate='Time: %{x:.3e} s<br>Concentration: %{y:.3e} V<extra></extra>'
            )
        )
        fig.update_layout(
            title= "Minutely Concentration",
            xaxis_title="Time (Unix)",
            yaxis_title="Concentration",
        )
        fig.show()

