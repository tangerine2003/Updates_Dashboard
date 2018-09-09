8# coding: utf-8

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

df_status_update = pd.DataFrame([["AR Solution", "     QA     ", "Beta testing within MIA first week in Sept"],
                    ["Branch Procurement", "     QA     ", "Began piloting the tool in MIA. Ran into a permission issue that the CHQ team has to look into before using it"]], 
                    columns=['Project name', 'Project Status', 'Project Notes'])

# Employee KPI
time_kpi_x = ["Chris Clifton", "Tyler Cox", "Luis Fernandez", "Dustin Snyder"]
time_kpi_y_percent = ["113", "122", "106", "116"]
time_kpi_y_hours = ["143", "139", "134", "146"]

# Regional/Geo Contributions KPI
reg_geo_kpi_label = ['Regional / Geography', 'Branch / District']
reg_geo_kpi_values = [81, 19]

# Alignment
align_name = ['Expeditors', 'Americas', 'Southeast', 'SAV', 'CHS', 'MCO', 'MIA','SJU']
align_value = [9,0,72,9,7,0,3,0]

# Resource Breakdown Percentage
#break_name = ['Project','Special', 'Support', 'Ticket']
#break_value = [78,10,8,4]

# data frames
df_topten = pd.read_csv('Top 10 Projects.csv',header=0)

#variables
on_time_completion = '''# 30%'''
request_to_vetted = '''# 20 '''
new_request = '''# 33'''
completed_request = '''# 20'''

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
             html.Img(src='https://i.imgur.com/cbkzBeV.jpg', height='45.1', width='154.5')
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

        dcc.Link('All Projects (Active & Ready to Start)   ', href='/all-projects', className="tab"),

        dcc.Link('All Projects (Vetting & On Hold)   ', href='/all-project-vet-hld', className="tab")

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
                    html.Table(make_dash_table(df_status_update),className="tiny-header")
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
                
                #Regional / Geo Contributions
                html.Div([
                    html.H6("Regional / Geography Contributions",
                            className="gs-header gs-table-header padded"),
                    html.P("Regional and Geo Contributions KPI should be greater than 70% each month"),
                    dcc.Graph(
                        id="graph-2",
                        figure={
                            'data': [
                                go.Pie(
                                    labels=reg_geo_kpi_label, 
                                    values=reg_geo_kpi_values,
                                    textposition='auto',
                                    marker = {
                                        "colors": ["rgb(132, 186, 91)",
                                                "rgb(114, 147, 203)"]}
                                    )
                            ],
                            'layout': go.Layout(
                                autosize = False,
                                font = {
                                  "family": "Raleway",
                                  "size": 10
                                },
                                height = 200,
                                width = 340,
                                hovermode = "percent",
                                margin = {
                                  "r": 0,
                                  "t": 20,
                                  "b": 10,
                                  "l": 10
                                },
                                showlegend = True
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
                    html.H6('Resource Breakdown Percentage',
                            className="gs-header gs-text-header padded"),

                    html.P("Breakdown of the resource areas where the most time was spent"),
                    dcc.Graph(
                        id = "graph-3",
                        figure={
                            'data' : [
                                go.Bar(
                                    y=['Resources'],
                                    x=[78],
                                    textposition='auto',
                                    orientation='h',
                                    name = "Project"
                                    ),
                                    go.Bar(
                                    y=['Resources'],
                                    x=[10],
                                    textposition='auto',
                                    orientation='h',
                                    name = "Special"
                                    ),
                                    go.Bar(
                                    y=['Resources'],
                                    x=[8],
                                    textposition='auto',
                                    orientation='h',
                                    name = "Support"
                                    ),
                                    go.Bar(
                                    y=['Resources'],
                                    x=[4],
                                    textposition='auto',
                                    orientation='h',
                                    name = "Ticket"
                                    ),],
                            'layout' : go.Layout(
                                autosize = False,
                                barmode='stack',
                                font = {
                                  "family": "Raleway",
                                  "size": 10
                                },
                                showlegend= True,
                                height = 200,
                                width = 340,
                                hovermode = "closest",
                                margin = {
                                  "r": 0,
                                  "t": 20,
                                  "b": 15,
                                  "l": 50
                                })
                        }

                    )
                ], className="six columns"),



                html.Div([
                    html.H6("Alignment",
                            className="gs-header gs-table-header padded"),
                    dcc.Graph(
                        id='graph-4',
                        figure = {
                            'data': [
                                go.Pie(
                                    labels= align_name,
                                    values= align_value,
                                    hole=.5,
                                    textposition='auto'
                                )                              
                            ],
                            'layout': go.Layout(
                                autosize = False,
                                font = {
                                  "family": "Raleway",
                                  "size": 10
                                },
                                height = 325,
                                width = 340,
                                hovermode = "percent",
                                margin = {
                                "r": 10,
                                "t": 20,
                                "b": 100,
                                "l": 15
                                },
                                  showlegend = True
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

            # Row 1
            html.Div([
                # On Time Completion
                html.Div([
                    html.H6('On Time Completion',
                            className="gs-header gs-text-header padded"),

                    html.Br([]),

                    dcc.Markdown(on_time_completion),], className="three columns"),
                # Request to vetted days
                html.Div([
                    html.H6('Request to Vetted',
                            className="gs-header gs-text-header padded"),
                    html.Br([]),
                    dcc.Markdown(request_to_vetted),
                    dcc.Markdown('''##### Days '''),], className="three columns"),
                # New Request
                html.Div([
                    html.H6('New Request',
                            className="gs-header gs-text-header padded"),
                    html.Br([]),
                    dcc.Markdown(new_request),], className="three columns"),
                # Completed Request
                html.Div([
                    html.H6('Completed Request',
                            className="gs-header gs-text-header padded"),
                    html.Br([]),
                    dcc.Markdown(completed_request),], className="three columns"),                

            ], className="row "),

            # Row 2
            html.Div([
                html.Div([
                    html.H6('Impact Area', className="gs-header gs-text-header padded"),
                    dcc.Graph(
                        id = "impact-area-1",
                        figure={
                            'data' : [

                            ],
                            'layout' : go.Layout(

                            )
                        }

                    )
                ],className="six columns"),

                html.Div([

                    html.H6('Solution Type', className="gs-header gs-text-header padded"),
                    dcc.Graph(  
                        id = "solution-type-1",
                        figure={
                            'data' : [
                                go.Bar(

                                )
                            ],
                            'layout' : go.Layout(

                            )
                        }
                    )
                ],className="six columns")

            ],className="row"),
            
            # Top 10 Projects
            html.Div([              
                html.H6("Top 10 Projects for the past month", className="gs-header gs-table-header padded"),
                html.Table(make_dash_table(df_topten))
            ], className="row "),

        ], className="row ")

    ], className="page")

allProjects = html.Div([ # page 3

        print_button(),

        html.Div([

            # Header

            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Active Projects
            html.Div([
                html.Div([
                    html.H6(["Active Projects"],
                            className="gs-header gs-table-header padded"),
                    html.Table(make_dash_table(df_topten))
                ], className="twelve columns"),
            ], className="row "),

            # Ready to Start
            html.Div([
                html.Div([
                    html.H6(["Ready to Start"],
                            className="gs-header gs-table-header padded"),
                    html.Table(make_dash_table(df_topten))
                ], className="twelve columns"),
            ], className="row "),

        ], className="subpage")

    ], className="page")

allProjects_vet_hld = html.Div([ # page 4

        print_button(),

        html.Div([

            # Header
            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # In Vetting
            html.Div([
                html.Div([
                    html.H6(["In Vetting"],
                            className="gs-header gs-table-header padded"),
                    html.Table(make_dash_table(df_topten))
                ], className="twelve columns"),
            ], className="row "),

            # On Hold
            html.Div([
                html.Div([
                    html.H6(["On Hold"],
                            className="gs-header gs-table-header padded"),
                    html.Table(make_dash_table(df_topten))
                ], className="twelve columns"),
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
    elif pathname == '/all-project-vet-hld':
        return allProjects_vet_hld
    elif pathname == '/full-view':
        return overview,performance,allProjects,allProjects_vet_hld
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