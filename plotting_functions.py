# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 11:44:38 2022

@author: moelg
"""

#%%
#Plot hr for each day:
def day_plot(pt_id='rs432'):
    array=patient_dict[pt_id].SAT[1:]
    fig,axs = plt.subplots(1,len(array),
                           figsize=(15,3),sharey='row',dpi=75)
    for no,days in enumerate(array):
        array_minutesFromMidnight = [x.hour*60+x.minute for x in days[:,0]]
        axs[no].axvspan(60*23,1440,color='black',alpha=.4)
        axs[no].axvspan(0,7*60,color='black',alpha=.4)
        axs[no].scatter(x=array_minutesFromMidnight,y=days[:,2],marker='+',alpha=.5)
        axs[no].set_xlim(0,1440)
        axs[no].set_xticks([0,360,720,1080,1439])
        axs[no].set_xticklabels(['00:00','06:00','12:00','18:00','23:59'])
        axs[no].hlines(30,0,1440,color='red',ls='--')
        axs[no].hlines(40,0,1440,color='orange',ls=':')
        axs[no].hlines(110,0,1440,color='orange',ls=':')
        axs[no].hlines(130,0,1440,color='red',ls='--')

day_plot()


#%%    
#Plot values during the night(2300 - 0600):
def night_values_plot(pt_id='rs432'):
    all_vals = np.concatenate(patient_dict[pt_id].PR)
  
    night_mask = (all_vals[:,3] > 1380) | (all_vals[:,3] < 360) 
    masked_time = np.array([x[0] for x in all_vals])[night_mask]
    masked_vals = np.array([x[2] for x in all_vals])[night_mask]

    
    plt.scatter(x=masked_time,
         y=masked_vals,marker='+')
night_values_plot()



#%%
#To do a presentation on average and mean values for time of day:
all_values_sorted_timeofday = all_values[all_values[:,3].argsort()]
minute_indices = np.unique(all_values_sorted_timeofday[:,3],return_index=True)
minute_groups = np.split(all_values_sorted_timeofday,minute_indices[1])[1:]
minute_groups_naremoved = [x[:,2][~np.isnan(x[:,2].astype(float))] for x in minute_groups]

per_minute_median = [np.nanmedian(x[:,2].astype(float)) for x in minute_groups]
iqr_low = [np.nanpercentile(x[:,2].astype(float),25) for x in minute_groups]
iqr_high = [np.nanpercentile(x[:,2].astype(float),75) for x in minute_groups]

per_minute_mean = [np.nanmean(x[:,2].astype(float)) for x in minute_groups]
ci_low  = [stats.bayes_mvs(x,alpha=.95)[0][1][0] for x in minute_groups_naremoved]
ci_high = [stats.bayes_mvs(x,alpha=.95)[0][1][1] for x in minute_groups_naremoved]

plt.plot(per_minute_median,c='orange')
plt.fill_between(range(0,1440), iqr_low, iqr_high,color='orange',alpha=.3)
plt.show()

plt.plot(per_minute_mean)
plt.fill_between(range(0,1440), ci_low, ci_high,color='blue',alpha=.3)

#%%
from helper_functions import random_patient,moving_average

pr_temp = random_patient(patient_dict).SAT

fig,axs = plt.subplots(1,len(pr_temp))
axs = axs.ravel()
for no,i in enumerate(pr_temp):
  axs[no].scatter(i[:,0],moving_average(i[:,2],n=60))
  axs[no].hlines(92,axs[no].get_xlim()[0],axs[no].get_xlim()[1],color='yellow',ls='--')
  axs[no].hlines(88,axs[no].get_xlim()[0],axs[no].get_xlim()[1],color='orange',ls='-.')
  axs[no].hlines(85,axs[no].get_xlim()[0],axs[no].get_xlim()[1],color='orange',ls='--')
  axs[no].hlines(80,axs[no].get_xlim()[0],axs[no].get_xlim()[1],color='red')
#        axs[no].hlines(40,0,1440,color='orange',ls=':')
#        axs[no].hlines(110,0,1440,color='orange',ls=':')
#        axs[no].hlines(130,0,1440,color='red',ls='--')
#plt.fill_betweenx([20],
#                  hr[1][1]['time'][true],
#                  hr[1][1]['time'][true],color='r')

plt.show()
