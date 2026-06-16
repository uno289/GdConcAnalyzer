# ============================================
# Gadolinium Concentration Grapher
# Purpose: Graphs data values from ExpFit into
#   24 hour, 1 month, 1 year graphs
# ============================================
# Imports and File Definitions

import plotly as pl
import numpy as np
import FileImport
from FileImport import file0000, file0001, file1233, file1255, file1278, file1283, file1288, file1293, file1298, file1303
import SignalProcessor
import ExponentialFit

# ============================================
# Code

# Currently, all placeholders test the old data sets
# --------------------------------------------
# Test graphing

class Grapher():
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
                    name="Bi-exponential fit",
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