# ============================================
# Gadolinium Concentration Grapher
# Purpose: Graphs data values from ExpFit into
#   24 hour, 1 month, 1 year graphs
# ============================================
# Imports and File Definitions

import csv
import plotly as pl
import numpy as np
import os
import scipy
import FileImport
from FileImport import file0000, file0001, file1233, file1255, file1278, file1283, file1288, file1293, file1298, file1303
import SignalProcessor

# ============================================
# Code

# Currently, all placeholders test the old data sets
# --------------------------------------------

#This chunk here is just to import the file into the grapher

file = FileImport.load_waveform(file0001)

# --------------------------------------------
# Test exp fit
processor = SignalProcessor.SignalProcessor(file.Ch1V)

Ch1V = processor.zero_baseline()

timeAxis = np.arange(len(file.Ch1V)) * file.deltaTime

start = np.argmax(abs(Ch1V)) + 5
t_peak = timeAxis[np.argmax(abs(Ch1V))]

def exp_fit(t, V_0, tau, V_BG):
    return V_0 * np.exp(-(t - t_peak) / tau) + V_BG

x_fit = timeAxis[start:]
y_fit = Ch1V[start:]

# Just tested random values here and these seemed to work

p1 = [
    -0.002,                 # V_0
    0.005,                # tau
    0                       # V_BG
]

# Try to fit the curve to the data, if it fails then it just skips

try:
    popt, pcov = scipy.optimize.curve_fit(exp_fit, x_fit, y_fit, p0=p1,maxfev=10000)

    V_0, tau, V_BG = popt

    y_model = exp_fit(x_fit, *popt)
    print(abs(V_0+V_BG) * tau)
    print(V_0, tau, t_peak, V_BG)

except RuntimeError:
    print("Fit failed: skipping curve fit")
    popt = None
    y_model = None
    eq_text = "Fit failed"

# --------------------------------------------
# Test graphing

'''fig = pl.graph_objs.Figure()

fig.add_trace(
    pl.graph_objs.Scatter(
        name='Ch1 V',
        x=timeAxis,
        y=Ch1V,
        mode="lines",
        hovertemplate="t: %{x:.3e} s<br>V: %{y:.3e} V<extra></extra>"
    )
)
if y_model is not None:
    fig.add_trace(
        pl.graph_objs.Scatter(
            x=x_fit,
            y=y_model,
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
'''