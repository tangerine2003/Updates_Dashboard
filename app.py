# coding: utf-8

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import os
import datetime as dt
import calendar
import numpy as np
from textwrap import dedent


app = dash.Dash(__name__)
server = app.server

# read data for tables (one df per table)

df_status_update = pd.DataFrame([["AR Solution", "QA", "Beta testing within MIA first week in Sept"],["Procurement", "QA", "Something else here"]], columns=['Project name', 'Project Status', 'Project Notes'])

# Employee KPI
time_kpi_x = ["Chris Clifton", "Tyler Cox", "Luis Fernandez", "Dustin Snyder"]
time_kpi_y_percent = ["113", "122", "106", "116"]
time_kpi_y_hours = ["143", "139", "134", "146"]

# Regional/Geo Contributions KPI
reg_geo_kpi_label = ['Regional / Geography', 'Branch / District']
reg_geo_kpi_values = ['81%', '19%']

# Markdown Header Components

# final_h_markdown = 

df_fund_facts = pd.read_csv('https://plot.ly/~bdun9/2754.csv')
df_price_perf = pd.read_csv('https://plot.ly/~bdun9/2756.csv')
df_current_prices = pd.read_csv('https://plot.ly/~bdun9/2753.csv')
df_hist_prices = pd.read_csv('https://plot.ly/~bdun9/2765.csv')
df_avg_returns = pd.read_csv('https://plot.ly/~bdun9/2793.csv')
df_after_tax = pd.read_csv('https://plot.ly/~bdun9/2794.csv')
df_recent_returns = pd.read_csv('https://plot.ly/~bdun9/2795.csv')
df_equity_char = pd.read_csv('https://plot.ly/~bdun9/2796.csv')
df_equity_diver = pd.read_csv('https://plot.ly/~bdun9/2797.csv')
df_expenses = pd.read_csv('https://plot.ly/~bdun9/2798.csv')
df_minimums = pd.read_csv('https://plot.ly/~bdun9/2799.csv')
df_dividend = pd.read_csv('https://plot.ly/~bdun9/2800.csv')
df_realized = pd.read_csv('https://plot.ly/~bdun9/2801.csv')
df_unrealized = pd.read_csv('https://plot.ly/~bdun9/2802.csv')

df_graph = pd.read_csv("https://plot.ly/~bdun9/2804.csv")

# reusable componenets
def make_dash_table(df):
    ''' Return a dash definition of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

def print_button():
    printButton = html.A(['Print PDF'],className="button no-print print",style={'position': "absolute", 'top': '-40', 'right': '0'})
    return printButton

# includes page/full view
def get_logo():
    logo = html.Div([

        html.Div([
            html.Img(src='http://logonoid.com/images/vanguard-logo.png', height='40', width='160')
        ], className="ten columns padded"),

        html.Div([
            dcc.Link('Full View   ', href='/full-view')
        ], className="two columns page-view no-print")

    ], className="row gs-header")
    return logo

def get_header():
    year = dt.datetime.now()
    
    header = html.Div([

        html.Div([
            html.H5('Southeast ED&A/Geo Dev ' + calendar.month_name[8] + ' ' + year.strftime("%Y") + ' Update')
        ], className="twelve columns padded")

    ], className="row gs-header gs-text-header")
    return header

def get_menu():
    menu = html.Div([

        dcc.Link('Overview   ', href='/overview', className="tab first"),

        dcc.Link('Performance   ', href='/performance', className="tab"),

        dcc.Link('All Projects   ', href='/all-projects', className="tab")

    ], className="row ")
    return menu

## Page layouts
overview = html.Div([  # page 1

        print_button(),

        html.Div([

            # Header
            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Row 3

            html.Div([

                html.Div([
                    html.H6('Updates',
                            className="gs-header gs-text-header padded"),

                    html.Br([]),

                    html.P("\
                            - Southeast AR Solution: We are beginning our beta testing within \
                            the MIA Branch\."),

                ], className="six columns"),

                html.Div([
                    html.H6(["Regional Project Status"],
                            className="gs-header gs-table-header padded"),
                    html.Table(make_dash_table(df_status_update)) #Back
                ], className="six columns"),

            ], className="row "),

            # Row 4

            html.Div([
                
                #PMA Recorded Time KPI
                html.Div([
                    html.H6('PMA Recorded Time KPI',
                            className="gs-header gs-text-header padded"),
                    html.P('KPI Record at least 30 hours/ per week of project time for each Analyst/Developer. Goal is over 100% '),
                    dcc.Graph(
                        id = "graph-1",
                        figure={
                            'data': [
                                go.Bar(
                                    x = time_kpi_x,
                                    y = time_kpi_y_percent,
                                    text=time_kpi_y_percent,
                                    textposition='auto',
                                    marker = {
                                      "color": "rgb(255, 153, 102)",
                                      "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2
                                      }
                                    },
                                    name = "Task Recorded KPI %"
                                )
                                , #This is for multiple bars
                                go.Bar(
                                    x = time_kpi_x,
                                    y = time_kpi_y_hours,
                                    text=time_kpi_y_hours,
                                    textposition='auto',
                                    marker = {
                                      "color": "rgb(153, 204, 255)",
                                      "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2
                                        }
                                    },
                                    name = "Task Recorded KPI Hours"
                                ),
                            ],
                            'layout': go.Layout(
                                autosize = False,
                                bargap = 0.35,
                                font = {
                                  "family": "Raleway",
                                  "size": 10
                                },
                                height = 200,
                                hovermode = "closest",
                                legend = {
                                  "x": -0.0228945952895,
                                  "y": -0.189563896463,
                                  "orientation": "h",
                                  "yanchor": "top"
                                },
                                margin = {
                                  "r": 0,
                                  "t": 20,
                                  "b": 10,
                                  "l": 10
                                },
                                showlegend = True,
                                title = "",
                                width = 340,
                                xaxis = {
                                  "autorange": True,
                                  "range": [-0.5, 4.5],
                                  "showline": True,
                                  "title": "",
                                  "type": "category"
                                },
                                yaxis = {
                                  "autorange": True,
                                  "range": [0, 22.9789473684],
                                  "showgrid": True,
                                  "showline": True,
                                  "title": "",
                                  "type": "linear",
                                  "zeroline": False
                                }
                            )
                        },
                        config={
                            'displayModeBar': False
                        }
                    )
                ], className="six columns"),

                html.Div([
                    html.H6("Regional / Geography Contributions",
                            className="gs-header gs-table-header padded"),
                    dcc.Graph(
                        id="graph-2",
                        figure={
                            'data': [
                                go.Pie(labels=reg_geo_kpi_label, values=reg_geo_kpi_values)
                            ],
                            'layout': go.Layout(
                                autosize = False,
                                title = "",
                                font = {
                                  "family": "Raleway",
                                  "size": 10
                                },
                                height = 200,
                                width = 340,
                                hovermode = "closest",
                                legend = {
                                  "x": -0.0277108433735,
                                  "y": -0.142606516291,
                                  "orientation": "h"
                                },
                                margin = {
                                  "r": 20,
                                  "t": 20,
                                  "b": 20,
                                  "l": 50
                                },
                                showlegend = True,
                                xaxis = {
                                  "autorange": True,
                                  "linecolor": "rgb(0, 0, 0)",
                                  "linewidth": 1,
                                  "range": [2008, 2018],
                                  "showgrid": False,
                                  "showline": True,
                                  "title": "",
                                  "type": "linear"
                                },
                                yaxis = {
                                  "autorange": False,
                                  "gridcolor": "rgba(127, 127, 127, 0.2)",
                                  "mirror": False,
                                  "nticks": 4,
                                  "range": [0, 30000],
                                  "showgrid": True,
                                  "showline": True,
                                  "ticklen": 10,
                                  "ticks": "outside",
                                  "title": "$",
                                  "type": "linear",
                                  "zeroline": False,
                                  "zerolinewidth": 4
                                }
                            )
                        },
                        config={
                            'displayModeBar': False
                        }
                    )
                ], className="six columns"),

            ], className="row "),

            # Row 5

            html.Div([
                html.Div([
                    html.H6('Price & Performance (%)',
                            className="gs-header gs-table-header padded"),
                    html.Table(make_dash_table(df_price_perf))
                ], className="six columns"),

                html.Div([
                    html.H6("Risk Potential",
                            className="gs-header gs-table-header padded"),
                    dcc.Graph(
                        id='graph-3',
                        figure = {
                            'data': [
                                go.Scatter(
                                    x = ["0", "0.18", "0.18", "0"],
                                    y = ["0.2", "0.2", "0.4", "0.2"],
                                    fill = "tozerox",
                                    fillcolor = "rgba(31, 119, 180, 0.2)",
                                    hoverinfo = "none",
                                    line = {"width": 0},
                                    mode = "lines",
                                    name = "B",
                                    showlegend = False
                                ),
                                go.Scatter(
                                    x = ["0.2", "0.38", "0.38", "0.2", "0.2"],
                                    y = ["0.2", "0.2", "0.6", "0.4", "0.2"],
                                    fill = "tozerox",
                                    fillcolor = "rgba(31, 119, 180, 0.4)",
                                    hoverinfo = "none",
                                    line = {"width": 0},
                                    mode = "lines",
                                    name = "D",
                                    showlegend = False
                                ),
                                go.Scatter(
                                    x = ["0.4", "0.58", "0.58", "0.4", "0.4"],
                                    y = ["0.2", "0.2", "0.8", "0.6", "0.2"],
                                    fill = "tozerox",
                                    fillcolor = "rgba(31, 119, 180, 0.6)",
                                    hoverinfo = "none",
                                    line = {"width": 0},
                                    mode = "lines",
                                    name = "F",
                                    showlegend = False
                                ),
                                go.Scatter(
                                    x = ["0.6", "0.78", "0.78", "0.6", "0.6"],
                                    y = ["0.2", "0.2", "1", "0.8", "0.2"],
                                    fill = "tozerox",
                                    fillcolor = "rgb(31, 119, 180)",
                                    hoverinfo = "none",
                                    line = {"width": 0},
                                    mode = "lines",
                                    name = "H",
                                    showlegend = False
                                ),
                                go.Scatter(
                                    x = ["0.8", "0.98", "0.98", "0.8", "0.8"],
                                    y = ["0.2", "0.2", "1.2", "1", "0.2"],
                                    fill = "tozerox",
                                    fillcolor = "rgba(31, 119, 180, 0.8)",
                                    hoverinfo = "none",
                                    line = {"width": 0},
                                    mode = "lines",
                                    name = "J",
                                    showlegend = False
                                ),
                            ],
                            'layout': go.Layout(
                                title = "",
                                annotations = [
                                    {
                                      "x": 0.69,
                                      "y": 0.6,
                                      "font": {
                                        "color": "rgb(31, 119, 180)",
                                        "family": "Raleway",
                                        "size": 30
                                      },
                                      "showarrow": False,
                                      "text": "<b>4</b>",
                                      "xref": "x",
                                      "yref": "y"
                                    },
                                    {
                                      "x": 0.0631034482759,
                                      "y": -0.04,
                                      "align": "left",
                                      "font": {
                                        "color": "rgb(44, 160, 44)",
                                        "family": "Raleway",
                                        "size": 10
                                      },
                                      "showarrow": False,
                                      "text": "<b>Less risk<br>Less reward</b>",
                                      "xref": "x",
                                      "yref": "y"
                                    },
                                    {
                                      "x": 0.92125,
                                      "y": -0.04,
                                      "align": "right",
                                      "font": {
                                        "color": "rgb(214, 39, 40)",
                                        "family": "Raleway",
                                        "size": 10
                                      },
                                      "showarrow": False,
                                      "text": "<b>More risk<br>More reward</b>",
                                      "xref": "x",
                                      "yref": "y"
                                    }
                                  ],
                                  autosize = False,
                                  height = 200,
                                  width = 340,
                                  hovermode = "closest",
                                  margin = {
                                    "r": 10,
                                    "t": 20,
                                    "b": 80,
                                    "l": 10
                                  },
                                  shapes = [
                                    {
                                      "fillcolor": "rgb(255, 255, 255)",
                                      "line": {
                                        "color": "rgb(31, 119, 180)",
                                        "width": 4
                                      },
                                      "opacity": 1,
                                      "type": "circle",
                                      "x0": 0.621,
                                      "x1": 0.764,
                                      "xref": "x",
                                      "y0": 0.135238095238,
                                      "y1": 0.98619047619,
                                      "yref": "y"
                                    }
                                  ],
                                  showlegend = True,
                                  xaxis = {
                                    "autorange": False,
                                    "fixedrange": True,
                                    "range": [-0.05, 1.05],
                                    "showgrid": False,
                                    "showticklabels": False,
                                    "title": "<br>",
                                    "type": "linear",
                                    "zeroline": False
                                  },
                                  yaxis = {
                                    "autorange": False,
                                    "fixedrange": True,
                                    "range": [-0.3, 1.6],
                                    "showgrid": False,
                                    "showticklabels": False,
                                    "title": "<br>",
                                    "type": "linear",
                                    "zeroline": False
                                }
                            )
                        },
                        config={
                            'displayModeBar': False
                        }
                    )
                ], className="six columns"),

            ], className="row ")

        ], className="subpage")

    ], className="page")

performance = html.Div([  # page 2

        print_button(),

        html.Div([

            # Header
            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Row ``
            html.Div([

                html.Div([
                    html.H6("Performance",
                            className="gs-header gs-table-header padded"),
                    dcc.Markdown(dedent('''
                    # 21 %                     26                              33
                    On Time Completion      Request to Vetted               New Request
                    
                    
                    '''))],className="twelve columns"),
                ], className="row "),


            # Row 2

            html.Div([

                html.Div([
                    html.H6(["Average annual returns--updated monthly as of 02/28/2018"], className="gs-header gs-table-header tiny-header"),
                    html.Table(make_dash_table(df_avg_returns), className="tiny-header")
                ], className=" twelve columns"),

            ], className="row "),

            # Row 3

            html.Div([

                html.Div([
                    html.H6(["Recent investment returns"], className="gs-header gs-table-header tiny-header"),
                    html.Table(make_dash_table(df_recent_returns), className="tiny-header")
                ], className=" twelve columns"),

            ], className="row "),

        ], className="subpage")

    ], className="page")

allProjects = html.Div([ # page 3

        print_button(),

        html.Div([

            # Header

            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Row 1

            html.Div([

                html.Div([
                    html.H6(["Portfolio"],
                            className="gs-header gs-table-header padded")
                ], className="twelve columns"),

            ], className="row "),

            # Row 2

            html.Div([

                html.Div([
                    html.Strong(["Stock style"]),
                    dcc.Graph(
                        id='graph-5',
                        figure={
                            'data': [
                                go.Scatter(
                                    x = ["1"],
                                    y = ["1"],
                                    hoverinfo = "none",
                                    marker = {
                                        "opacity": 0
                                    },
                                    mode = "markers",
                                    name = "B",
                                )
                            ],
                            'layout': go.Layout(
                                title = "",
                                annotations = [
                                {
                                  "x": 0.990130093458,
                                  "y": 1.00181709504,
                                  "align": "left",
                                  "font": {
                                    "family": "Raleway",
                                    "size": 9
                                  },
                                  "showarrow": False,
                                  "text": "<b>Market<br>Cap</b>",
                                  "xref": "x",
                                  "yref": "y"
                                },
                                {
                                  "x": 1.00001816013,
                                  "y": 1.35907755794e-16,
                                  "font": {
                                    "family": "Raleway",
                                    "size": 9
                                  },
                                  "showarrow": False,
                                  "text": "<b>Style</b>",
                                  "xref": "x",
                                  "yanchor": "top",
                                  "yref": "y"
                                }
                              ],
                              autosize = False,
                              width = 200,
                              height = 150,
                              hovermode = "closest",
                              margin = {
                                "r": 30,
                                "t": 20,
                                "b": 20,
                                "l": 30
                              },
                              shapes = [
                                {
                                  "fillcolor": "rgb(51, 102, 255)",
                                  "line": {
                                    "color": "rgb(0, 0, 0)",
                                    "width": 2
                                  },
                                  "opacity": 0.3,
                                  "type": "rect",
                                  "x0": 0,
                                  "x1": 0.33,
                                  "xref": "paper",
                                  "y0": 0,
                                  "y1": 0.33,
                                  "yref": "paper"
                                },
                                {
                                  "fillcolor": "rgb(51, 102, 255)",
                                  "line": {
                                    "color": "rgb(0, 0, 0)",
                                    "dash": "solid",
                                    "width": 2
                                  },
                                  "opacity": 0.3,
                                  "type": "rect",
                                  "x0": 0.33,
                                  "x1": 0.66,
                                  "xref": "paper",
                                  "y0": 0,
                                  "y1": 0.33,
                                  "yref": "paper"
                                },
                                {
                                  "fillcolor": "rgb(51, 102, 255)",
                                  "line": {
                                    "color": "rgb(0, 0, 0)",
                                    "width": 2
                                  },
                                  "opacity": 0.3,
                                  "type": "rect",
                                  "x0": 0.66,
                                  "x1": 0.99,
                                  "xref": "paper",
                                  "y0": 0,
                                  "y1": 0.33,
                                  "yref": "paper"
                                },
                                {
                                  "fillcolor": "rgb(51, 102, 255)",
                                  "line": {
                                    "color": "rgb(0, 0, 0)",
                                    "width": 2
                                  },
                                  "opacity": 0.3,
                                  "type": "rect",
                                  "x0": 0,
                                  "x1": 0.33,
                                  "xref": "paper",
                                  "y0": 0.33,
                                  "y1": 0.66,
                                  "yref": "paper"
                                },
                                {
                                  "fillcolor": "rgb(51, 102, 255)",
                                  "line": {
                                    "color": "rgb(0, 0, 0)",
                                    "width": 2
                                  },
                                  "opacity": 0.3,
                                  "type": "rect",
                                  "x0": 0.33,
                                  "x1": 0.66,
                                  "xref": "paper",
                                  "y0": 0.33,
                                  "y1": 0.66,
                                  "yref": "paper"
                                },
                                {
                                  "fillcolor": "rgb(51, 102, 255)",
                                  "line": {
                                    "color": "rgb(0, 0, 0)",
                                    "width": 2
                                  },
                                  "opacity": 0.3,
                                  "type": "rect",
                                  "x0": 0.66,
                                  "x1": 0.99,
                                  "xref": "paper",
                                  "y0": 0.33,
                                  "y1": 0.66,
                                  "yref": "paper"
                                },
                                {
                                  "fillcolor": "rgb(51, 102, 255)",
                                  "line": {
                                    "color": "rgb(0, 0, 0)",
                                    "width": 2
                                  },
                                  "opacity": 0.3,
                                  "type": "rect",
                                  "x0": 0,
                                  "x1": 0.33,
                                  "xref": "paper",
                                  "y0": 0.66,
                                  "y1": 0.99,
                                  "yref": "paper"
                                },
                                {
                                  "fillcolor": "rgb(255, 127, 14)",
                                  "line": {
                                    "color": "rgb(0, 0, 0)",
                                    "width": 1
                                  },
                                  "opacity": 0.9,
                                  "type": "rect",
                                  "x0": 0.33,
                                  "x1": 0.66,
                                  "xref": "paper",
                                  "y0": 0.66,
                                  "y1": 0.99,
                                  "yref": "paper"
                                },
                                {
                                  "fillcolor": "rgb(51, 102, 255)",
                                  "line": {
                                    "color": "rgb(0, 0, 0)",
                                    "width": 2
                                  },
                                  "opacity": 0.3,
                                  "type": "rect",
                                  "x0": 0.66,
                                  "x1": 0.99,
                                  "xref": "paper",
                                  "y0": 0.66,
                                  "y1": 0.99,
                                  "yref": "paper"
                                }
                              ],
                              xaxis = {
                                "autorange": True,
                                "range": [0.989694747864, 1.00064057995],
                                "showgrid": False,
                                "showline": False,
                                "showticklabels": False,
                                "title": "<br>",
                                "type": "linear",
                                "zeroline": False
                              },
                              yaxis = {
                                "autorange": True,
                                "range": [-0.0358637178721, 1.06395696354],
                                "showgrid": False,
                                "showline": False,
                                "showticklabels": False,
                                "title": "<br>",
                                "type": "linear",
                                "zeroline": False
                              }
                            )
                        },
                        config={
                            'displayModeBar': False
                        }
                    )

                ], className="four columns"),

                html.Div([
                    html.P("Vanguard 500 Index Fund seeks to track the performance of\
                     a benchmark index that meaures the investment return of large-capitalization stocks."),
                    html.P("Learn more about this portfolio's investment strategy and policy.")
                ], className="eight columns middle-aligned"),

            ], className="row "),

            # Row 3

            html.Br([]),

            html.Div([

                html.Div([
                    html.H6(["Equity characteristics as of 01/31/2018"], className="gs-header gs-table-header tiny-header"),
                    html.Table(make_dash_table(df_equity_char), className="tiny-header")
                ], className=" twelve columns"),

            ], className="row "),

            # Row 4

            html.Div([

                html.Div([
                    html.H6(["Equity sector diversification"], className="gs-header gs-table-header tiny-header"),
                    html.Table(make_dash_table(df_equity_diver), className="tiny-header")
                ], className=" twelve columns"),

            ], className="row "),

        ], className="subpage")

    ], className="page")

noPage = html.Div([  # 404

    html.P(["404 Page not found"])

    ], className="no-page")


# Describe the layout, or the UI, of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update page
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/' or pathname == '/overview':
        return overview
    elif pathname == '/performance':
        return performance
    elif pathname == '/all-projects':
        return allProjects
    elif pathname == '/full-view':
        return overview,performance,allProjects
    else:
        return noPage


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                #"https://codepen.io/bcd/pen/KQrXdb.css",
                "https://codepen.io/tangerine2003/pen/aaJWaa.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://codepen.io/bcd/pen/YaXojL.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})


if __name__ == '__main__':
    app.run_server(debug=True)