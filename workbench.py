# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
#%%
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from dataloading import *
from definitions import ME_definitions
from helper_functions import *
from patient_class import *

patient_dict = vitals_loader(limit=400,only='rs') #start by loading a subset of surgical patients

#%%
#Mean for a patient
#np.nanmean(np.concatenate(patient_dict['rs432'].hr)[:,2])

#Mean and CI for all patients:
all_values = np.concatenate([x.PR for x in patient_dict.values()]) #make an array with all Pulse-Rate values in. For testing purposes
all_values = all_values[all_values[:,2] < 220] # how many values are > 220
all_values_nanremoved = all_values[~np.isnan(all_values[:,2].astype(float))][:,2] #create array with nan removed.
all_values_nanremoved = all_values_nanremoved[all_values_nanremoved < 230]
stats.bayes_mvs(all_values_nanremoved,alpha=.95) #create 95% Confidence interval of values.


#%%
#Simple cumulative number of values outside threshold, number of values and cumulative number/24h
def outside_thresh(random_patient=True,variable='SAT',thresh=91,lower_than=True):
    """
    Calculates the number of values outside threshold for the selected patient. Returns number per 24 hours.

    Parameters
    ----------
    random_patient : TYPE, optional
        DESCRIPTION. The default is True.
    variable : TYPE, optional
        DESCRIPTION. The default is 'SAT'.
    thresh : TYPE, optional
        DESCRIPTION. The default is 91.
    lower_than : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
       value=number of values outside threshold
       number_of_values = The total number of values evaluated
       minutes per 24 hours

    """
    
    if random_patient: data=random_patient() #use function to grab a random patient to calculate on
    else: data = patient_dict[patient] #Else give a patient id in the form 'rs002' for instance.
    
    if variable == 'SAT': data = data.SAT #function only done for SAT thresholds.
    
    number_of_values = len(data)    
    
    if lower_than: value = sum(np.array([x[2] for x in data])<thresh)
    
    return value,number_of_values,(value/(number_of_values/1440))

outside_thresh()



#%%
import pandas as pd
df_ME = pd.DataFrame(columns = ['id','me','value'])
for no,patient in enumerate(list(patient_dict.keys())): #Creates a pandas dataframe with patients as index, and all microevents of said patient.
    print(no/len(list(patient_dict.keys())))
    for i in ME_definitions:
      result = MicroeventCalculator(data_in=patient_dict[patient],value=i[0],threshold_low=i[1],threshold_high=i[2],duration=2)
      for res in result[2]:
        df_ME.loc[len(df_ME)] = [patient,str(i),res]

#%%
df_ME.groupby(['id','me']).count() #Gives average number of microevents for each patient.
df_ME.groupby(['id','me']).mean()  # Gives average length of each microevent

MEs = df_ME.me.unique()
fig,axs = plt.subplots(len(MEs),1,dpi=150,figsize=(15,20),sharex=True)
import seaborn as sns
for no,i in enumerate(MEs):
    data = df_ME[df_ME.me == i].value
    q_dur = data.quantile(.95)
    sns.histplot(data,ax=axs[no],
                kde=True) #Styling
    axs[no].set_title(i)
    dur = float(str.split(i,',')[3][:-1])
    print (i,dur,data.median(),q_dur)
    axs[no].vlines(dur,0,axs[no].get_ylim()[1],color='orange')
    axs[no].vlines(q_dur,0,axs[no].get_ylim()[1],color='orange',ls='-.')
    axs[no].set_xlim(0,200)
    #axs[no].set_xscale('log')

#%%
for no,pt in enumerate(df_ME.id):
    print (no/len(df_ME))
    value = patient_dict[pt].SAE_during_mon
    df_ME.loc[df_ME.id==pt,'sae_during'] = value
    
#%%
from sklearn import metrics

youdens_index_vals = {}
#create ROC curves
fig,axs = plt.subplots(3,4,
                         figsize=(20,20),
                         #constrained_layout=True,
                         dpi=150
                         )
axs = axs.ravel()
for no,MicroEvent in enumerate(df_ME.me.unique()):
    temp_df_drop_na = df_ME.loc[df_ME.me==MicroEvent,['value','sae_during']].dropna()
    fpr, tpr, val  = metrics.roc_curve(temp_df_drop_na['sae_during'].astype(bool),  temp_df_drop_na['value'])
    auc = metrics.roc_auc_score(temp_df_drop_na['sae_during'].astype(bool),  temp_df_drop_na['value'])
    prc = metrics.average_precision_score(temp_df_drop_na['sae_during'].astype(bool),  temp_df_drop_na['value'])
    print (auc,prc)
    #auc_corr = metrics.balanced_accuracy_score(temp_df_drop_na['sae'],  temp_df_drop_na[col])
    idx = np.argmax(tpr - fpr)
    idmin = np.argmin(tpr - fpr)
    youdens_index_vals[MicroEvent] = [val[idx],val[idmin]]
 
    if auc > 0.5: axs[no].vlines(fpr[idx],0,tpr[idx],ls=":",label="Youden's index="+str(round(val[idx],2)))
    else: axs[no].vlines(fpr[idmin],0,tpr[idmin],ls=":",label="Youden's index="+str(round(val[idx],2)))
    
    axs[no].plot(fpr,tpr,label="AUC="+str(round(auc,3)))
    axs[no].set_ylabel('True Positive Rate')
    axs[no].set_xlabel('False Positive Rate')
    axs[no].plot([[0,0],[1,1]],ls='-.',c='r')
    axs[no].legend(loc=4)
    axs[no].set_title(MicroEvent)
    axs[no].axis('square')

    #%%
def Time_Outside_circ_iqr():
  list_of_ptt = []
  for pt_id in patient_dict.keys():
    array=patient_dict[pt_id].PR
    indices = np.sort(np.unique(array[:,1],return_index=True)[1])
    split_array = np.split(array,indices)[1:]
    for day_array in split_array:
      day_of_month = np.unique(day_array[:,1])[0]
      list_outside= []
      for no,i in enumerate (day_array):
        if np.isnan(i[2]): None
        else:
          list_outside.append((i[2]<iqr_low[no])|(i[2]>iqr_high[no]))
      list_of_ptt.append([pt_id,day_of_month,
                      len(list_outside),
                      np.sum(list_outside),
                      np.sum(list_outside)/len(list_outside)*100])
  #print ("Values with valid measurements:",len(list_outside)
  #     ,"\nValues outside circadian IQR:",np.sum(list_outside),
  #     "\nPercentage of values outside IQR:",np.sum(list_outside)/len(list_outside)*100)
  return list_of_ptt
Time_Outside_circ_iqr()

import pandas as pd

df = pd.DataFrame(Time_Outside_circ_iqr())
