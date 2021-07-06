## ----------app_dash.py----------##
# main file of app web of scoring model and
# dashboard in Dash 
# ----------------------------------------
# Created: 18/06/2021 by R. Barbeiro
## ---------------------------------------##

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Dashboard_functions import *

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table   


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# comment the next line to run it locally
server = app.server

# load data
df, main_features, nn = load_data('data/')

app.layout = html.Div([
    html.Div([
        html.H1('Dashboard of credit default risk scoring'),
        html.Img(src="/assets/logo_societe.PNG")
    ], className="banner"),

    #htlm.Div: python htlm component for a <div> HTML5 element 
    #here we create 1 line with 2 coloumns (2 divs inside 1)
    html.Div([
        html.H4('Select customer\'s ID for model\'s prediction'),
        #dcc.Input(id="id_input", value=100001, type="number", placeholder="Insert Customer's ID"),
        html.Label([      
            "Select customer's ID",
            dcc.Dropdown(id='ID', clearable=False, style={'width':'25%'},
                         value=None, options=[{'label': i, 'value': i} for i in df.index])
        ]),
#         html.Button(children='Submit', id='submit_button', n_clicks=0)
    ], style={'margin-left': '1vw'}),
        
    html.Div([
        html.H4('Predicted default risk analysis', style={'textAlign':'center'}), #style={'margin-left':'10px'} 
        # 1st column
        html.Div([
            dcc.Graph(id='left_graph'),
            html.Div(id='textarea', style={'width': '80%'}), 
            html.Div(id='div_out_local', children=[])
        ], style={'display': 'inline-block','vertical-align': 'top', 'width': '50%'}),
        # 2nd column
        html.Div([
            dcc.Graph(id='right_graph'),
            html.Label(['Change independet variable:'], style={'font-weight':'bold'}),
            dcc.RadioItems(id='indep_variables',
                           options=[{'label': 'Credit', 'value': 'AMT_CREDIT'},
                                    {'label': 'Annuity', 'value': 'AMT_ANNUITY'}, 
                                    {'label': 'Employed time', 'value': 'DAYS_EMPLOYED'},
                                    {'label': 'Age', 'value': 'DAYS_BIRTH'},
                                    {'label': 'External score 3', 'value': 'EXT_SOURCE_3'}],
                           value='AMT_CREDIT', labelStyle={'display': 'inline-block'}), 

            html.Button('Explanation of global predictions', id='global_button', style={'margin-top':'1vw'}),
            html.Img(id = 'out_img_global', src = '', style={'vertical-align': 'top', 'width': '90%'})
        ], style={'display': 'inline-block','vertical-align': 'top', 'width': '50%'}),        
        ], style={'margin-left': '1vw'}),
    
    html.Div(id='div_comparison', children=[])
    
    
])  # close main Div layout

           
## ------ left div callbacks -------##  

# update left_graph and text upon submit
@app.callback(
    [Output('left_graph', 'figure'), Output('textarea', 'children')],
    [Input('ID', 'value')]
#     [State('ID', 'value')]
)

def update_left_graph(ID):    
    if ID is None:
        target=df['RISK_label'].value_counts()
        fig = px.pie(values=target.values, names=target.index, title='Customers distribution by default risk', hole=.4, color_discrete_sequence=['#00CC96','#EF553B'])
        note = 'NB: A threshold of 50% probability of default was chosen to classify clients as high or low risk type (high risk > 50%; low risk <= 50%).' 
        return fig, note 
    else:
        proba = df.loc[ID, 'TARGET']  
        #Gauge Chart
        fig = go.Figure(go.Indicator(domain = {'x': [0, 1], 'y': [0, 1]}, 
                             value = proba, 
                             mode = "gauge+number",
                             title = {'text': "Default probability (%)"},
                             gauge = {'bar': {'color': "black"}, 
                                      'axis': {'range': [0, 100]},
                                      'steps' : [{'range': [0, 50], 'color': '#00CC96'}, {'range': [50, 100], 'color': '#EF553B'}]})
               )
        
        risk = df.loc[ID, 'RISK_label']
        if risk == 'high': note = 'Customer {} has high default risk. Loan not granted.'.format(ID)   
        else: note = 'Customer {} has low default risk. Loan granted.'.format(ID)
        return fig, note
    
# update left 2nd-division upon selected ID  
@app.callback(
    Output('div_out_local','children'),
    [Input('ID', 'value')],
    [State('div_out_local','children')]
)
def update_div(ID, children):
    if ID is None:
        raise PreventUpdate
    else:
        new_child = html.Div(
            style={'margin-top':'1vw'},
            children=[
            html.Button('Explanation of customer\'s prediction', id='local_button'),
            html.Img(id = 'out_img_local', src = '', style={'vertical-align': 'top', 'width':'90%'}),
            html.Div(id = 'out_error'),
            html.Button('Comparison to other customers', id='comparison_button', style={'margin-top':'1vw'})]
        )
        
        return new_child
      
@app.callback(
    [Output('out_img_local', 'src'), Output('out_error', 'children')],
    [Input('local_button', 'n_clicks')],
    [State('ID', 'value')]
)
def update_output_shap(n_clicks, ID):
    if n_clicks is None:
        raise PreventUpdate
    else:
#         customer_idx =  df.loc[df['SK_ID_CURR']==ID].index #should be value index, not ID
#         shap.plots._waterfall.waterfall_legacy(explainer.expected_value[customer_idx], shap_values[1], df.iloc[:,1:-2].values.reshape(-1), 
#                                                feature_names=df.iloc[:,1:-2].columns,
#                                                show=False)
        if ID==100001: return "/assets/shap_ID100001.png", 'Contribution of main factors. The arrows indicate their contribution (positive in red, and negative in blue) to move the prediction from the model basis (average model output over the training dataset).'
        elif ID==100005: return "/assets/shap_ID100005.png", 'Contribution of main factors. The arrows indicate their contribution (positive in red, and negative in blue) to move the prediction from the model basis (average model output over the training dataset).'
        else: return '','Shap plot not available for this customer.'
          

#update div comparison upon comparison_button
@app.callback(
    [Output('div_comparison','children'), Output('bar_plot','figure'), Output('radar_plot','figure')],
    [Input('comparison_button', 'n_clicks')],  
    [State('ID', 'value')]
)
def update_div(n_clicks, ID):    
    if n_clicks is None:
        raise PreventUpdate
    else:
        new_child = html.Div(
            style={'margin-top':'1vw', 'margin-left':'1vw'},
            children=[
            html.H4('Comparison of main contributing features', style={'textAlign':'center'}),
            html.Label('Select features to plot'),
            dcc.Dropdown(id='dd_features', options=[{'label': i, 'value': i} for i in main_features.Features.unique()],
                         value=['EXT_SOURCE_3', 'EXT_SOURCE_2', 'ANNUITY_CREDIT_RATIO'], multi=True, style={'width': '50%'}),
            html.Div([dcc.Graph(id='bar_plot')], 
                     style={'display': 'inline-block','vertical-align': 'top', 'width': '50%'}),
            html.Div([dcc.Graph(id='radar_plot')], style={'display': 'inline-block','vertical-align': 'top', 'width': '50%'}),
            html.Div([dash_table.DataTable(id='desc_table', 
                                           columns=[{'name':c, 'id':c} for c in main_features.columns], 
                                           data=main_features.to_dict('records'), style_as_list_view=True,
                                           style_cell={'padding': '5px', 'textAlign': 'left','fontSize':14}, 
                                           style_header={'fontWeight': 'bold'})
                     ], style={'width':'50%'})]
        ) 
        
        features=['EXT_SOURCE_3', 'EXT_SOURCE_2', 'ANNUITY_CREDIT_RATIO']
        df_neighbors = neighbors(df, nn, ID)
        df_medians = medians(df, ID, df_neighbors, features)
        fig_bar = px.bar(df_medians, x='vars', y='median', color='Group', log_y=True, labels={'median':'Feature value (log scale)'}, barmode="group",
                         color_discrete_sequence=['#636EFA','#AB63FA', '#EF553B',"#00CC96"], 
                         title='Feature values for customer {} and feature medians by group'.format(ID))
        fig_radar = plot_radar(df, ID, df_neighbors, features, title='Normalized feature values for customer {} and feature means by group'.format(ID))
        
        return new_child, fig_bar, fig_radar  

# update bar et radar plots with selected features
@app.callback(
    [Output('bar_plot', 'figure'), Output('radar_plot', 'figure')],
    [Input('dd_features', 'value'), Input('ID', 'value')]
)
def update_bar_plot(features, ID):
    df_neighbors = neighbors(df, nn, ID)
    df_medians = medians(df, ID, df_neighbors, features)
    fig_bar = px.bar(df_medians, x='vars', y='median', color='Group', log_y=True, labels={'median':'Feature value (log scale)'}, barmode="group",
                         color_discrete_sequence=['#636EFA','#AB63FA', '#EF553B',"#00CC96"], 
                         title='Feature values for customer {} and feature medians by group'.format(ID))
    fig_radar = plot_radar(df, ID, df_neighbors, features, title='Normalized feature values for customer {} and feature means by group'.format(ID))
    return fig_bar, fig_radar   
                


## ------ Right div callbacks -------##        
@app.callback(
    Output('out_img_global', 'src'),
    [Input('global_button', 'n_clicks')]
)
def update_output_shap(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:       
#         fig = shap.summary_plot(shap_values[0:1000,:], df.iloc[0:1000,1:-2].values, feature_names=df.iloc[:,1:-2].columns, max_display=10, show=False)
        url = '/assets/shap_summary_plot.png'
        return url
    
@app.callback(
    Output('right_graph', 'figure'),
    [Input('indep_variables', 'value')]
)
def update_right_graph(indep_variable):
    if indep_variable=='AMT_CREDIT':
        fig_right = px.scatter(df, x='AMT_CREDIT', y='TARGET', color='RISK_label',  
                               hover_name='SK_ID_CURR', hover_data=['SK_ID_CURR'],
                               labels={'AMT_CREDIT': 'Credit amount (local currency)', 'TARGET': 'Default probability (%)'},
                               color_discrete_sequence=["#00CC96", '#EF553B'], 
                               title='Default probability vs. credit amount by risk type')
        return fig_right
    else:
        fig_right = px.scatter(df, x=indep_variable, y='TARGET', color='RISK_label', 
                               hover_name='SK_ID_CURR', hover_data=['SK_ID_CURR'],
                               labels={indep_variable: indep_variable, 'TARGET': 'Default probability (%)'},
                               color_discrete_sequence=["#00CC96", '#EF553B'],
                               title='Default probability vs. {} by risk type'.format(indep_variable))
    return fig_right



if __name__ == '__main__':
    app.run_server(debug=False)