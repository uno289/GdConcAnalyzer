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

#This chunk here is just to import the file into the grapher

file = FileImport.load_waveform(file1233)

# --------------------------------------------
# Gather exp fit

processor = SignalProcessor.SignalProcessor(file.Ch1V)

Ch1V = processor.zero_baseline()
timeAxis = np.arange(len(file.Ch1V)) * file.deltaTime

testrun = ExponentialFit.ExponentialFit(Ch1V, timeAxis)

fit = testrun.estimate_fit()

# --------------------------------------------
# Test graphing


error_y=dict(type="data", array=(0.1 * testrun.y_fit), visible=True)
fig = pl.graph_objs.Figure()

fig.add_trace(
    pl.graph_objs.Scatter(
        name='Ch1 V',
        x=testrun.time_axis,
        y=Ch1V,
        mode="lines",
        hovertemplate="t: %{x:.3e} s<br>V: %{y:.3e} V<extra></extra>"
    )
)
if testrun.y_model is not None:
    fig.add_trace(
        pl.graph_objs.Scatter(
            x=testrun.x_fit,
            y=testrun.y_model,
            error_y=error_y,
            mode="lines",
            name="Bi-exponential fit",
            line=dict(dash="dash"),
            line_color="red"
        )
    )

fig.update_layout(
    title= file.fileName,
    xaxis_title="Time (s)",
    yaxis_title="Voltage (V) (ZEROED)",
)

fig.show()