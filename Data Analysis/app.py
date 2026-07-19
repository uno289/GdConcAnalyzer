# ============================================
# GdConc App Script
# Purpose: Creates and updates the GdConc
# HTML webpage for the remote analysis
# feature.
# NOTE: Stays running 24/7 if not aborted!
# ============================================
# Imports
import csv
import pathlib
import datetime
import time
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, ctx, dash_table, State
import pandas as pd
import collections

import eventlogger
import Grapher
import EmailAlert
from flask import send_file
import config

# File declarations
processedData = pathlib.Path(r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\Processed")

singleTrace = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\Results\current_trace.html"
oneMinuteCSV = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\oneMinuteData.csv"
oneHourCSV = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\hourlyData.csv"
oneDayCSV = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\dailyData.csv"

heartbeat = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\Heartbeat.csv"
startup = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\startup.csv"
errorLog = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\errorLog.csv"
runs = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\runcount.csv"

eventlog = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\eventlogger.csv"
# ============================================
# Versioning (For footer)
VERSION = "1.1"
UPDATED = "2026-07-13"
# --------------------------------------------
# Startup Code

with open(startup, "r") as f:
    starttime = float(f.read())
    STARTUP = datetime.datetime.fromtimestamp(int(starttime))
    UPTIME = datetime.timedelta(seconds=(int(time.time()-(starttime))))
with open(runs,"r") as f:
    runcount = f.read()

app = Dash(__name__, external_stylesheets=[dbc.icons.BOOTSTRAP,dbc.themes.FLATLY],suppress_callback_exceptions=True,title="SK-Gc Concentration Monitor",update_title=None)

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>SK-Gd Concentration Monitor</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

@app.server.route("/trace")
def serve_trace():
    return send_file(
        singleTrace
    )

# --------------------------------------------
# Data frames for each graph. df1 = minutely, df2 = hourly, df3 = daily
df1 = pd.read_csv(oneMinuteCSV)
df1["Timestamp"] = pd.to_numeric(df1["Timestamp"])
x1 = df1["Timestamp"]
y1 = df1["Concentration"]
err1 = df1["Error"]
data1 = [x1,y1,err1]
dataDeque = collections.deque(maxlen=1440)

df2 = pd.read_csv(oneHourCSV)
df2["Timestamp"] = pd.to_numeric(df2["Timestamp"])
x2 = df2["Timestamp"]
y2 = df2["Concentration"]
err2 = df2["Error"]
data2 = [x2,y2,err2]
dataDeque2 = collections.deque(maxlen=168)

df3 = pd.read_csv(oneDayCSV)
df3["Timestamp"] = pd.to_numeric(df3["Timestamp"])
x3 = df3["Timestamp"]
y3 = df3["Concentration"]
err3 = df3["Error"]
data3 = [x3,y3,err3]
dataDeque3 = collections.deque(maxlen=365)

# --------------------------------------------
# Graphing callers, for each of the 3 main graphs
graphMinutely = Grapher.MinutelyGraph(dataDeque)
fig1 = graphMinutely.plotMinutely()
fig1.update_layout(uirevision="constant",template="plotly_dark")

graphHourly = Grapher.HourlyGraph(dataDeque2)
fig2 = graphHourly.plotHourly()
fig2.update_layout(uirevision="constant",template="plotly_dark")

graphDaily = Grapher.DailyGraph(dataDeque3)
fig3 = graphDaily.plotDaily()
fig3.update_layout(uirevision="constant",template="plotly_dark")

mailer = EmailAlert.EmailAlert()

# --------------------------------------------
# HTML layout of the app
app.layout =(
    dbc.Container([
        dbc.Card(
            dbc.Row([
                dbc.Col(
                    dbc.CardBody(
                        html.H3(
                            "Super-Kamiokande Gadolinium Concentration Monitor",
                            className="text-white display-6 mb-0",
                            style={
                                "lineHeight": "1",
                                "fontFamily": "Rajdhani, sans-serif"
                            }
                        )
                    ),
                    width=9
                ),
                dbc.Col(
                    dbc.CardBody(
                        dbc.Button(
                        [html.I(className="bi bi-github me-2"), "GitHub"],
                            href="https://github.com/uno289/GdConcAnalyzer/",
                            target="_blank",
                            color="light",
                            className="float-end"
                        )
                    ),
                    width=3
                ),
            ]),
            color="primary",
            inverse=True,
            className="mb-2 mt-2"),
        dbc.Card([
            dbc.Row([
                dbc.Col(
                    dbc.Card([dbc.CardHeader("Analysis Process Status",style={"fontFamily":"Rajdhani"}),
                          dbc.CardBody([html.H5(id="main-status",children="Checking...",className="mb-2"),html.P(id="main-status-detail",children="",className="card-text")])],color="dark",inverse=True
                         ,id="main-status-card"),width=3),
                dbc.Col(
                    dbc.Card([dbc.CardHeader("WaveDump File Status",style={"fontFamily":"Rajdhani"}),
                          dbc.CardBody([html.H5(id="wavedump-status",children="Checking...",className="mb-2"),html.P(id="wavedump-status-detail",children="",className="card-text")])],color="dark",inverse=True
                         ,id="wavedump-status-card"),width=3),
                dbc.Col(
                    dbc.Card([dbc.CardHeader("Analysis Quality",style={"fontFamily":"Rajdhani"}),
                          dbc.CardBody([html.H5(id="analysis-status",children="Checking...",className="mb-2"),html.P(id="analysis-status-detail",children="",className="card-text")])],color="dark",inverse=True
                         ,id="analysis-status-card"),width=3),
                dbc.Col(
                    dbc.Card([dbc.CardHeader("Latest Concentration",style={"fontFamily":"Rajdhani"}),
                          dbc.CardBody([html.H5(id="concentration-status", children="Checking...", className="mb-2"),
                                        html.P(id="concentration-status-detail", children="", className="card-text")])],
                         color="dark", inverse=True
                         , id="concentration-status-card"), width=3,),
        ],className="g-4 mb-4"),
        dbc.Alert(
                id="error-alert",
                children=[html.H4(id="error-title",children="Python Exception"),html.Hr(),html.Div(id="error-message")],
                color="danger",
                is_open=False,
                dismissable=True,
                className="mb-4"
            ),
        dcc.Interval(
            id="refresh-minutely",
            interval=60*1000, #Once per minute
            n_intervals=0
        ),
        dbc.Card(dcc.Graph(
            id = "hourly-graph",
            figure=fig2
        )),
        dcc.Interval(
            id="refresh-hourly",
            interval=60*60*1000, #Once per hour
            n_intervals = 0
        ),
        dbc.Tabs([
            dbc.Tab(label="Daily Graph",children=[
                dcc.Graph(
                        id = "daily-graph",
                        figure = fig3
                    ),
            ],tab_id="Daily Graph",style={"fontFamily":"Rajdhani"}
                    ),
            dbc.Tab(label="Minutely Graph", children=[
                dcc.Graph(
                        id = "minutely-graph",
                        figure = fig1
                    ),
            ],style={"fontFamily":"Rajdhani"}),
            dbc.Tab(label="Single Trace",children=[
                dbc.Card(html.Iframe(
                    id="single-trace",
                    src="/trace",
                    style={"width":"100%", "height": "400px", "border": "none"}
                )),
            ],tab_id="Single Trace",style={"fontFamily":"Rajdhani"})
        ],active_tab="Single Trace"),
        dcc.Interval(
            id = "refresh-daily",
            interval=60*60*24*1000, #Once per day
            n_intervals=0
        ),
        dcc.Interval(
            id="uptime-refresh",
            interval=1000,
            n_intervals=0
        ),
        dbc.Tabs([
            dbc.Tab(label="System Log",children=[
                dbc.Row(children=[
                    dbc.Col(dbc.Card(children=[dbc.CardHeader("System Stats"),dbc.CardBody(children=[
                        html.Div(id="startup-time"),
                        html.Div(id="runs-completed"),
                        html.Div(id="uptime")
                    ])]),width=3),
                    dbc.Col(dbc.Card(children=[dbc.CardHeader("Event Log"),dbc.CardBody(children=[
                        dash_table.DataTable(
                            id="event-log",
                            data=[],
                            columns=[],
                            page_size=15,
                            style_table={"overflowY": "auto","height":"500px"},
                            style_cell={"textAlign":"left","whiteSpace": "normal","fontFamily":"Rajdhani"}
                        )
                    ])]),width=9),
                ],className="mt-4"),
            ],style={"fontFamily":"Rajdhani"},tab_id="event-tab"),
            dbc.Tab(label="Error Log",children=[
                dbc.Card(children=[dbc.CardBody(dash_table.DataTable(
                    id="errorLogTable",
                    data=[],
                    columns=[],
                    page_size=15,
                    style_table={"overflowY":"auto","height":"300px"},
                    style_cell={"textAlign":"left","whiteSpace": "normal","fontFamily":"Rajdhani"}
                ))]),
            ],style={"fontFamily":"Rajdhani"}),
            dbc.Tab(
                label="Downloads",
                children=[
                    dbc.Card([
                        dbc.CardHeader("Download Processed Datasets",className="text-center",style={"fontFamily":"Rajdhani"}),
                        dbc.CardBody([

                            dbc.Button(
                                "📥 Download Minutely Dataset",
                                id="download-minute-button",
                                color="primary",
                                className="mb-3 w-100",
                                style={"fontFamily":"Rajdhani"}
                            ),
                            dcc.Download(id="download-minute"),

                            dbc.Button(
                                "📥 Download Hourly Dataset",
                                id="download-hour-button",
                                color="success",
                                className="mb-3 w-100",
                                style={"fontFamily": "Rajdhani"}
                            ),
                            dcc.Download(id="download-hour"),

                            dbc.Button(
                                "📥 Download Daily Dataset",
                                id="download-day-button",
                                color="info",
                                className="w-100",
                                style={"fontFamily": "Rajdhani"}
                            ),
                            dcc.Download(id="download-day"),
                        ])
                    ])
                ]
            )],active_tab="event-tab"),
        dcc.Store(
            id="error-count",
            data=0),
        ],style={"backgroundColor":"#e9edf2","minHeight":"100vh","padding":"20px"}),
    html.Footer(
        dbc.Card(
            dbc.CardBody(dbc.Row([
                dbc.Col(f"Sk-Gd Concentration Monitor v{VERSION}",width=4),
                dbc.Col(f"Updated {UPDATED}",width=4),
                dbc.Col("Yoshihiro Iwata, Keshav Anand, Hiroyuki Sekiya",width=4),
            ],style={"textAlign":"center"}))
        )
    ,className="mt-4 mb-2")
    ],
    ))

# --------------------------------------------
# Updaters and Callbacks

# Minutely Updater
@app.callback(
    Output("minutely-graph","figure"),
    Input(component_id='refresh-minutely', component_property='n_intervals'),
)

def update_minutely(n):
    with open(oneMinuteCSV,'r') as f:
        reader = csv.reader(f)
        newest_rows = collections.deque(reader,maxlen=1440)
    if newest_rows and newest_rows[0][0] == "Timestamp":
        newest_rows.popleft()
    dataDeque.clear()
    for row in newest_rows:
        dataDeque.append(
            [row[0],row[1],row[2]]
        )
    graphMinutely = Grapher.MinutelyGraph(dataDeque)
    fig1 = graphMinutely.plotMinutely()
    fig1.update_layout(uirevision="constant",font=dict(family="Rajdhani,sans-serif",size=14))
    return fig1

# Hourly updater
@app.callback(
    Output("hourly-graph","figure"),
    Input(component_id='refresh-hourly', component_property='n_intervals'),
)

def update_hourly(n):
    with open(oneHourCSV,'r') as f:
        reader = csv.reader(f)
        newest_rows = collections.deque(reader, maxlen=168)
    if newest_rows and newest_rows[0][0] == "Timestamp":
        newest_rows.popleft()
    dataDeque2.clear()
    for row in newest_rows:
        dataDeque2.append(
            [row[0], row[1], row[2]]
        )
    graphHourly = Grapher.HourlyGraph(dataDeque2)
    fig2 = graphHourly.plotHourly()
    fig2.update_layout(uirevision="constant",font=dict(family="Rajdhani,sans-serif",size=14))
    return fig2

# Daily updater
@app.callback(
    Output("daily-graph","figure"),
    Input(component_id='refresh-daily', component_property='n_intervals'),
)

def update_daily(n):
    eventlogger.log_event("Dashboard","INFO","Updating daily graph")
    with open(oneDayCSV,'r') as f:
        reader = csv.reader(f)
        newest_rows = collections.deque(reader, maxlen=365)
    if newest_rows and newest_rows[0][0] == "Timestamp":
        newest_rows.popleft()
    dataDeque3.clear()
    for row in newest_rows:
        dataDeque3.append(
            [row[0], row[1], row[2]]
        )
    graphDaily = Grapher.DailyGraph(dataDeque3)
    fig3 = graphDaily.plotDaily()
    fig3.update_layout(uirevision="constant",font=dict(family="Rajdhani,sans-serif",size=14))
    return fig3

@app.callback(
    Output("single-trace","src"),
    Input("refresh-minutely","n_intervals")
)
def update_single_trace(n):
    return f"/trace?t={n}"

# Downloads
@app.callback(
    Output("download-minute","data"),
    Output("download-hour","data"),
    Output("download-day","data"),
    Input("download-minute-button","n_clicks"),
    Input("download-hour-button","n_clicks"),
    Input("download-day-button","n_clicks"),
    prevent_initial_call=True
)
def download(minute,hour,day):
    match ctx.triggered_id:
        case "download-minute-button":
            return dcc.send_file(oneMinuteCSV), None, None
        case "download-hour-button":
            return None, dcc.send_file(oneHourCSV), None
        case "download-day-button":
            return None, None, dcc.send_file(oneDayCSV)

# Error Log
@app.callback(
Output("errorLogTable","data"),
    Output("errorLogTable","columns"),
    Output("error-count","data"),
    Output("error-alert","is_open"),
    Output("error-title","children"),
    Output("error-message","children"),
    Input("refresh-minutely","n_intervals"),
    State("error-count","data")
)
def update_error_log(_,previous_count):
    df=pd.read_csv(errorLog)

    current_count = len(df)
    latest = df.iloc[-1]
    title = "Python Exception"
    message = latest["Error"]

    if previous_count == 0:
        alert=False
    else:
        alert = current_count > previous_count

    df["Timestamp"] = pd.to_datetime(df["Timestamp"].astype(float),unit="s",utc=True).dt.tz_convert("Asia/Tokyo").dt.strftime("%Y-%m-%d %H:%M:%S")
    return(df.to_dict("records"),[{"name":c,"id":c} for c in df.columns],current_count,alert, title, message)

# Status bar
@app.callback(
    Output("main-status","children"),
    Output("main-status-detail","children"),
    Output("main-status-card","color"),
    Input("refresh-minutely","n_intervals")
)

def update_main_status(_):

    try:
        with open(heartbeat,"r") as f:
            last=float(f.read())
            current=time.time()
            age = current-last

            if age < 120:
                return ("Running",f"Last heartbeat: {int(age)}s ago","success")
            elif 120 < age < 300:
                eventlogger.log_event("Analyzer","WARNING",f"Analyzer idle. Last data: {int(age)}s ago")
                return ("Idle", f"Last data: {int(age)}s ago","warning")
            else:
                eventlogger.log_event("Analyzer","ERROR","No heartbeat detected. Check analysis script.")
                mailer.sendEmail("ERROR", "HBX001")
                return ("Unknown","No heartbeat detected","danger")
    except Exception as e:
        return("Unknown","Heartbeat file unavailable","secondary")

def get_wavedump_latest_filetime():
    files=list(processedData.glob("*"))
    try:
        newest = max(processedData.iterdir(),key=lambda x:x.stat().st_mtime)
        return newest.stat().st_mtime
    except Exception as e:
        return None

# Wavedump status
@app.callback(
    Output("wavedump-status","children"),
    Output("wavedump-status-detail","children"),
    Output("wavedump-status-card","color"),
    Input("refresh-minutely","n_intervals")
)
def update_wavedump(_):
    latest = get_wavedump_latest_filetime()
    wavedumpcheck = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\wavedumpHB.csv"
    with open(wavedumpcheck,"r") as f:
        if latest is None:
            return ("No data","No file found","secondary")
        age = time.time() - latest
        importerheartbeat = time.time() - float(f.read())
        if importerheartbeat > 300 and age > 300:
            eventlogger.log_event("Analyzer","ERROR",f"Critical error. Wavedump AND Analyzer down, last file {int(age)}s ago")
            mailer.sendEmail("ERROR","WDP002",int(age))
            return ("Critical error", f"Last file: {int(age)}s ago, check WaveDump AND Analyzer", "danger")
        elif age > 120:
            eventlogger.log_event("Analyzer","ERROR",f"Analyzer stopped. Last file: {int(age)}s ago, check FileImport.")
            mailer.sendEmail("ERROR","FIM002",int(age))
            return("Stopped",f"Last file: {int(age)}s ago, check Analyzer","danger")
        elif importerheartbeat > 120:
            eventlogger.log_event("Analyzer","ERROR",f"Analyzer stopped. Last file: {int(age)}s ago, check WaveDump.")
            mailer.sendEmail("ERROR","WDP001",int(age))
            return("Stopped",f"Last file: {int(age)}s ago, check WaveDump","danger")
        elif 120 < age < 300:
            eventlogger.log_event("Analyzer","WARNING",f"Analyzer delayed. Last file: {int(age)}s ago, check FileImport.")
            return ("Delayed",f"Last file: {int(age)}s ago, check Analyzer","warning")
        elif 120 < importerheartbeat < 300:
            eventlogger.log_event("Analyzer","WARNING", f"Analyzer delayed. Last file:{int(age)}s ago, check WaveDump.")
            return ("Delayed", f"Last file: {int(age)}s ago, check WaveDump", "warning")
        if age < 120 and importerheartbeat <120:
            return ("Active",f"Last file: {int(age)}s ago","success")

def check_analysis_quality():
    df = pd.read_csv(oneMinuteCSV)

    if len(df) < 2:
        return ("Waiting","Not enough data","secondary")

    latest = df.iloc[-1]["Concentration"]
    previous = df.iloc[-2]["Concentration"]
    error = df.iloc[-1]["Error"]
    change = (latest-previous)/previous

    if change < 0.1:
        eventlogger.log_event("Analyzer","INFO",f"Nominal operation. Concentration changed by {round(change,3)}%")
        return ("Nominal", f"Concentration changed by {round(change,3)}%","success")
    if change > 0.1:
        eventlogger.log_event("Potential Analysis Error","WARNING",f"Check analysis. Concentration changed by {round(change,3)}%")
        mailer.sendEmail("WARNING","ANX001",round(change,3))
        return ("Potential Error",f"Check analysis. Concentration changed by {round(change,3)}%","warning")
    if latest < 0:
        eventlogger.log_event(("Analyzer","ERROR",f"Check analysis. Latest concentration analysis was {round(latest,3)}"))
        mailer.sendEmail("ERROR","ANX002",round(latest,3))
        return ("Analysis Error",f"Check analysis. Latest concentration analysis was {round(latest,3)}.","danger")
    if abs(change) > 3*error:
        eventlogger.log_event(("Analysis Error","WARNING",f"Check analysis. Concentration changed by {round(change,3)}%"))
        mailer.sendEmail("WARNING", "ANX001", round(change, 3))
        return ("Large Change",f"Check analysis. Concentration changed by {round(change,3)}%","warning")

# Status cards
@app.callback(
    Output("analysis-status","children"),
    Output("analysis-status-detail","children"),
    Output("analysis-status-card","color"),
    Input("refresh-minutely","n_intervals")
)
def update_analysis_status(_):
    return check_analysis_quality()

def check_latest_concentration():
    df = pd.read_csv(oneMinuteCSV)
    latest_conc = df.iloc[-1]["Concentration"]
    latest_err = df.iloc[-1]["Error"]
    if len(df) > 0:
        return latest_conc,latest_err
    else:
        return None,None

# Concentration status
@app.callback(
    Output("concentration-status","children"),
    Output("concentration-status-detail","children"),
    Output("concentration-status-card","color"),
    Input("refresh-minutely","n_intervals")
)
def update_concentration(_):
    conc,error = check_latest_concentration()
    if conc is None:
        return ("No data", "Waiting for analysis...","secondary")
    return ("Successful Analysis", f"Concentration is {round(conc*100,3)} ± {round(error*100,3)}%.","success")

# Run counter
@app.callback(
    Output("runs-completed","children"),
    Output("startup-time","children"),
    Output("uptime","children"),
    Input("uptime-refresh","n_intervals")
)
def update_status(_):
    with open(startup, "r") as f:
        starttime = float(f.read())
        STARTUP = datetime.datetime.fromtimestamp(int(starttime))
        UPTIME = datetime.timedelta(seconds=(int(time.time() - (starttime))))

    with open(runs, "r") as f:
        runcount = f.read()

    return (
        f"Process Started: {STARTUP}",
        f"Runs Completed: {runcount}",
        f"Uptime: {UPTIME}"
    )

# Event log
@app.callback(
    Output("event-log","data"),
    Output("event-log","columns"),
    Input("uptime-refresh","n_intervals")
)

def update_event_log(_):
    try:
        df = pd.read_csv(eventlog)
        df = df.iloc[::-1].reset_index(drop=True)

        return(df.to_dict("records"),[{"name": c, "id": c} for c in df.columns])

    except Exception as e:

        return [],[]

# Website startup
if __name__ == "__main__":
    if config.USE_WAITRESS:
        if config.WEBPROD:
            from waitress import serve
            serve(app.server, host="10.4.7.158", port=8050, threads=16)
        else:
            from waitress import serve
            serve(app.server, host = "0.0.0.0", port = 8050, threads=16)
    else:
        app.run(host="0.0.0.0",port=8050,debug=False,threaded=True)