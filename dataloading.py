# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 13:29:02 2022

@author: moelg
"""

def matlab_to_python_timestamp_conversion(no):
    from datetime import datetime, timedelta
    return (datetime.fromordinal(int(no)) + timedelta(days=no%1)  - timedelta(days = 366))

def array_splitter(array,level=2):
    import numpy as np
    a = array#[array[:, level].argsort()] # if data is already sorted, we dont need this function
    col_no = a[:, level]
    
    _, indices = np.unique(col_no, return_index=True)
    result = np.split(a, indices)[1:]
    return np.array(result)


def vitals_loader(variable = 'hr',limit=50,split=1,only='rs'):
    """
    

    Parameters
    ----------
    variable : TYPE, optional
        DESCRIPTION. Has no function yet. The default is 'hr'.
    limit : Int, optional
        DESCRIPTION. Limits the number of files to import. The default is 50.
    split : Integer, optional
        DESCRIPTION. Level to split arrays on.
        The default is 1=day. But can be expanded in the future. For instance; before or after complication.
    only : String, optional
        DESCRIPTION: If only a specific study population is desired, the textstring to do regex on can be specified here.
        The default is 

    Returns
    -------
    patient_dict : TYPE
        DESCRIPTION.

    """
    import os
    import re
    import scipy.io as scio
    import numpy as np
    from patient_class import patient


    pr_path  = 'O:\Sund\Public\WARD\data\dataOut\Preprocessed_PulseRate'
    rr_path  = 'O:\Sund\Public\WARD\data\dataOut\Preprocessed_RespirationRate'
    sat_path = 'O:\Sund\Public\WARD\data\dataOut\Preprocessed_Saturation'
    files = os.listdir(path=pr_path) #just to use a folder containing patient files
    selected_files = [file for file in files if only in file]
    patient_dict = {}
    
    for no,file in enumerate(selected_files[:limit]):
      p_type = re.sub(r'[^a-zA-Z]', '', str(file)[:-3])
      patient_dict[file[:-4]] = patient(p_type=p_type)
      
      pr_data = scio.loadmat(pr_path + "\\" + file)
      rr_data = scio.loadmat(rr_path + "\\" + file)
      sat_data = scio.loadmat(sat_path + "\\" + file)
      for data_file in [pr_data,rr_data,sat_data]:
          var = list(data_file.keys())[4]
          array = data_file[var]
          timestamp = np.array([matlab_to_python_timestamp_conversion(x) for x in array[:,0]])
          day = [x.day for x in timestamp]
          minute = np.round([x.hour *60 + x.minute +x.second/60 for x in timestamp],decimals=0)
          var_data = np.array(data_file[var][:,1])
          extrapolated = np.array(data_file[var][:,2])
          values_tuples = zip(timestamp,day,var_data,minute,extrapolated)
          values = list(map(list, values_tuples))
          if var.upper()   == 'PR' :    patient_dict[file[:-4]].PR  = array_splitter(np.array(values),level=split)
          elif var.upper() == 'RR' :    patient_dict[file[:-4]].RR  = array_splitter(np.array(values),level=split)
          elif var.upper() == 'SAT':    patient_dict[file[:-4]].SAT = array_splitter(np.array(values),level=split)
          
          #patient_dict[file[:-4]] = patient(var=timestamp)
      
      #timestamp = np.array([matlab_to_python_timestamp_conversion(x) for x in pr_data['PR'][:,0]])
      #day = [x.day for x in timestamp]
      #minute = np.round([x.hour *60 + x.minute +x.second/60 for x in timestamp],decimals=0)
      #pr = np.array(pr_data['PR'][:,1])
      #extrapolated = np.array(pr_data['PR'][:,2])
    
      #values_tuples = zip(timestamp,day,pr,minute,extrapolated)
      #values = list(map(list, values_tuples))
      #print (array_splitter(values,level=split))
      #patient_dict[file[:-4]] = patient(hr=array_splitter(np.array(values),level=split)) # splits patient values pr. 24h period
      #patient_dict[file[:-4]] = patient(PR=np.array(values),p_type=p_type)
      print ((no+1)/limit*100,'%')
    print ('Done')
    return (patient_dict)

#%timeit vitals_loader(limit=10)

#%%
def SAE_loader(dict_in):
    #Loads csv file to use for looking for complications.
    import pandas as pd
    sae_csv = 'O:\Sund\Public\WARD\Jesper_temp\surgery.csv'
    df = pd.read_csv(sae_csv,index_col='id_nmbr')
    
    df[outcomes_datetimes] = df[outcomes_datetimes].apply(pd.to_datetime, format='%Y-%m-%d %H:%M')
    df[dt_list] = df[dt_list].apply(pd.to_datetime, format='%Y-%m-%d %H:%M')
    
    #Add 12 hours to discharge time, since they are discharged at the daytime.
    df['disch_pr_adm'] = df['disch_pr_adm'] + pd.Timedelta('12 hours')

    #If no dicharge_date, patient is probably dead:
    df.loc[df['disch_pr_adm'].isnull(),'disch_pr_adm'] = df.loc[df['disch_pr_adm'].isnull(),'sixmo_death_date']
    
    #1.1: As data is structured in different rows, use forwardfill to help calculations:
    df[dt_list] = df.groupby('id_nmbr')[dt_list].apply(lambda x: x.ffill().bfill())

    #1.2.1: Remove outcomes happening before PACU discharge set-up and after 30 days.
    df['end_30doutcomes_date'] = df['arr_gnr_wrd'] + pd.Timedelta('30 days')
    mask0 = df[outcomes_datetimes].apply(lambda d: (d >= df['arr_gnr_wrd'])&(d <= df['end_30doutcomes_date']))
    df[outcomes_datetimes] = df[outcomes_datetimes][mask0]
    #1.2.2: Remove outcomes happening before equipment set-up:
    mask1 = df[outcomes_datetimes].apply(lambda d: (d >= df['strt_mntrng']))
    df[outcomes_datetimes] = df[outcomes_datetimes][mask1]

    #1.3:
    #Outcomes have a 1 if it is counted as a SAE.
    #Where key in dictionary = 1, then get value(datetime):
    mask2  = df[list(sae_y_n_to_date_lookup_dictionary.keys())].eq(1).rename(columns=sae_y_n_to_date_lookup_dictionary)
    sae_df = df[list(sae_y_n_to_date_lookup_dictionary.values())].where(mask2)
    sae_df = sae_df.join(df[outcomes_no_sae])
    
    patient_id_col = df.groupby(level=0).first().prjct_id
    
    
    for key in dict_in.keys():
        index_for_sae = patient_id_col[patient_id_col==str(key).upper()].index
        first_SAE = sae_df.loc[index_for_sae].min().min()
        dict_in[key].first_SAE = first_SAE
        dict_in[key].SAE_during_mon = (first_SAE<dict_in[key].PR[:,0].max()) & (first_SAE>dict_in[key].PR[:,0].min())


#SAE_loader(patient_dict)
#%%