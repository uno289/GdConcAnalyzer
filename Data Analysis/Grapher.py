# ============================================
# Gadolinium Concentration Grapher
# Purpose: Graphs data values from ExpFit into
#   24 hour, 1 month, 1 year graphs
# ============================================
# Imports and File Definitions

import plotly as pl
import pandas as pd
import config

current_trace = config.singleTrace
# ============================================

# Code
# --------------------------------------------

# Single-trace graphing
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
                hovertemplate="t: %{x:.3e} s<br>V: %{y:.3e%} V<extra></extra>"
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
            title= f"{config.TRACE_COUNT} Traces Averaged",
            xaxis_title="Time",
            yaxis_title="Calibrated Voltage (mV)",
            font=dict(family="Rajdhani,sans-serif")
            )

        fig.update_yaxes(range=[-6,0])

        fig.write_html(
            r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\Results\current_trace.html", auto_open=False
        )
        with open(current_trace, "r", encoding="utf-8") as f:
            html=f.read()

        font_tag = """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&display=swap" rel="stylesheet">
        """
        html = html.replace("<head>","<head\n>" + font_tag)
        with open(current_trace, "w", encoding="utf-8") as f:
            f.write(html)
# --------------------------------------------

# Graphs the minutely data once a minute (through app)
class MinutelyGraph:
    def __init__(self,data):
        self.data = data
    def plotMinutely(self):
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
                mode="lines",
                hovertemplate='Time: %{x}<br>Concentration: %{y:.3%}<extra></extra>'
            )
        )
        fig.update_layout(
            title= "Minutely Concentration",
            xaxis_title="Time (JST)",
            yaxis_title="Concentration",
        )
        fig.update_yaxes(
            tickformat=".1%"
        )
        fig.update_xaxes(
            tickformat='%b %d %H:%M:%S'
        )
        fig.write_html(
            r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\Results\minutely_graph.html",auto_open=False
        )
        return fig

# Graphs hourly data once each hour (updater in app)
class HourlyGraph:
    def __init__(self,data):
        self.data = data
    def plotHourly(self):
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
                name='Long-term Concentration (Hourly)',
                x=df['date'],
                y=df['y_data'],
                error_y=dict(type="data", array=self.error_data, visible=True),
                mode="lines+markers",
                hovertemplate='Time: %{x}<br>Concentration: %{y:.3%}<extra></extra>'
            )
        )
        fig.update_layout(
            title= "Hourly Concentration",
            xaxis_title="Time (JST)",
            yaxis_title="Concentration",
        )
        fig.update_xaxes(
            tickformat='%b %d, %H:%M'
        )
        fig.update_yaxes(
            tickformat=".1%"
        )
        fig.write_html(
            r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\Results\hourly_graph.html",auto_open=False
        )
        return fig

# Graphs daily data, updates once a day (app.py)
class DailyGraph:
    def __init__(self,data):
        self.data = data
    def plotDaily(self):
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
                name='Long-term Concentration (Daily)',
                x=df['date'],
                y=df['y_data'],
                error_y=dict(type="data", array=self.error_data, visible=True),
                mode="lines+markers",
                hovertemplate='Date: %{x}<br>Concentration: %{y:.3%}<extra></extra>'
            )
        )
        fig.update_xaxes(
            title="Time (JST)",
            tickformat='%b %d %Y, %H:%M'
        )
        fig.update_yaxes(
            tickformat=".1%"
        )
        fig.update_layout(
            title= "Daily Concentration",
            xaxis_title="Date (JST)",
            yaxis_title="Concentration",
        )
        fig.write_html(
            r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\Results\daily_graph.html",auto_open=False
        )
        return fig

