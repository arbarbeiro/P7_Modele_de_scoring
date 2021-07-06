## ----------Dashboard functions----------##
# This file contains some of the required functions 
# for the dashboard app called by app_dash.py.
# The rest are contained in app_dash.py.
# ----------------------------------------
# Created: 18/06/2021 by R. Barbeiro
## ---------------------------------------##

import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go


def load_data(path):
    df = pd.read_csv(path+'df_test_predicted_imputed.csv')
    df.index = df.SK_ID_CURR
    df['TARGET'] = df.TARGET*100
    main_features = pd.read_csv(path+'main_features.csv') #index_col=0
    nn = pickle.load(open(path+'nneighbors_model.sav', 'rb'))
    
    return df, main_features, nn

def neighbors(df, nn, ID):
    '''Calculates 20-N-neighbors of the customer, based on all features'''
    nearest_idx = nn.kneighbors(X=np.array(df.loc[ID].iloc[1:-2]).reshape(1, -1),n_neighbors=20,return_distance=False).ravel()
    df_neighbors = df.iloc[nearest_idx] 
    return df_neighbors
    

def medians(df, ID, df_neighbors, features): 
    '''Calculates medians by group along with customer values for
    selected features, to be ploted in a comparative bar plot'''

    low=pd.DataFrame(df.loc[df['RISK_label']=='low'][features].median())
    low['low']='Low risk'
    low.columns = ['median', 'Group']

    high=pd.DataFrame(df.loc[df['RISK_label']=='high'][features].median())
    high['high']='High risk'
    high.columns = ['median', 'Group']
  
    customer = pd.DataFrame(df.loc[ID]).loc[features]
    customer['Group']='Customer'
    customer.columns = ['median', 'Group']
   
    neighbors=pd.DataFrame(df_neighbors.median()).loc[features].rename({0:'median'},axis=1)
    neighbors['Group']='20-N-neighbors'

    df_medians = customer.append(neighbors).append(high).append(low)
    df_medians['vars'] = df_medians.index

    return df_medians


def plot_radar(df, ID, df_neighbors, features, title):
    '''Plot radar chart of normalized means of selected features 
    (relative to their maxs) for each comparative group and their
    values for the cutomer being compared'''
    
    X_means_extra=df.groupby('RISK_label').mean()[features]
    X_means_extra = X_means_extra.append(pd.DataFrame(df[features].loc[ID]).T).rename({ID: 'customer'}, axis=0)  
    X_means_extra = X_means_extra.append(pd.DataFrame(df_neighbors[features].mean()).T).rename({0: 'neighbors'}, axis=0)
    X_means_norm_extra = MinMaxScaler().fit_transform(X_means_extra)
    X_means_norm_extra =pd.DataFrame(X_means_norm_extra, columns=features).set_axis([X_means_extra.index.values], axis=0)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=X_means_norm_extra.loc['customer'].values[0],
        theta=features,
        fill='toself',
        fillcolor='rgba(99,110,250,0.2)',
        name='Customer'
    ))

    fig.add_trace(go.Scatterpolar(
        r=X_means_norm_extra.loc['neighbors'].values[0],
        theta=features,
        marker= { 'color' : 'rgb(171,99,250)'},
        fillcolor='rgba(171, 99, 250,0.2)',
        fill='toself',
        name='20-N-neighbors'
    ))

    fig.add_trace(go.Scatterpolar(
        r=X_means_norm_extra.loc['high'].values[0],
        theta=features,
        marker= { 'color' : 'rgb(239,85,59)'},
        fillcolor='rgba(239,85,59,0.2)',
        fill='toself',
        name='High risk'
    ))
    fig.add_trace(go.Scatterpolar(
        r=X_means_norm_extra.loc['low'].values[0],
        theta=features,
        fill='toself',
        marker= { 'color' : 'rgb(0,204,150)'},
        fillcolor='rgba(0,204,150,0.2)',
        name='Low risk'
    ))

    fig.update_layout(title=title,
        polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 1]
        )),
      showlegend=True
    )
    
    return fig


## ---functions for shap graphs--- ##

# import shap
# from scipy.special import expit
# import matplotlib.pyplot as plt


#  def global_shap_values(df):
#     model = pickle.load(open('data/lgbm_model.sav', 'rb'))
#     explainer = shap.TreeExplainer(model, model_output='raw')
#     shap_values = explainer.shap_values(df.iloc[:,1:-2])[1] #only for target positive class
    
#     shap.summary_plot(shap_values, 
#                   df.iloc[:,1:-2].values, # data (np.array)
#                   feature_names=df.iloc[:,1:-2].columns, 
#                   max_display=10, 
#                   show=False, 
#                  ) 

#     #save fig to open as static figure in dash, since shap objects not supported, or need to convert to javascript  
#     plt.gcf().set_size_inches((10,5))
#     plt.title('Impact of feature values in terms of SHAP')
#     plt.savefig('assets/shap_summary_plot.png', bbox_inches ='tight', dpi=300)
#     src='assets/shap_summary_plot.png'
    
#     return explainer, src


# def local_shap_values(ID, explainer):
#     #compute shap values for a customer  
#     shap_values_ID = explainer.shap_values(X=np.array(df.loc[ID].iloc[1:-2]).reshape(1, -1))[1]
#     #Convert to probability space instead of log-odds 
#     shap_values_trans, expected_value_trans = shap_transform_scale(shap_values_ID, 
#                                                                    expected_value=explainer.expected_value[1], 
#                                                                    model_prediction=df.loc[ID]['TARGET']/100)

#     shap.plots._waterfall.waterfall_legacy(expected_value_transformed, shap_values_trans,
#                                            df.iloc[:,1:-2].values.reshape(-1),
#                                            feature_names=df.iloc[:,1:-2].columns,
#                                            max_display=10, show=False)

#     plt.gcf().set_size_inches((10,5))
#     plt.savefig('assets/local_shap_plot.png', bbox_inches ='tight', dpi=300)
#     src= 'assets/local_shap_plot.png'
#
#     return src


# def shap_transform_scale(shap_values, expected_value, model_prediction):
#     #applying the logit function to the base value - to have probab instead of log-odds   
#     expected_value_transformed = expit(expected_value)
#     # distance in log-odds space
#     original_explanation_distance = np.sum(shap_values)
#     #distance in probability space
#     distance_to_explain = model_prediction - expected_value_transformed
#     #distance_coefficient (ratio between both distances) to then convert
#     distance_coefficient = original_explanation_distance / distance_to_explain
#     #Transforming the original shapley values to probab space
#     shap_values_transformed = shap_values / distance_coefficient
    
#     return shap_values_transformed, expected_value_transformed 
