# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 09:37:14 2022

@author: moelg
"""

dt_list = ['strt_mntrng','end_mntrng','disch_pr_adm','sixmo_death_date','anaest_start','op_start','last_sutur','ansth_end','pota_arrival','arr_gnr_wrd']

outcomes_datetimes =['delirium_date','syncope_date','stroke_date','tia_date','resp_failr_date','imv_date','imv_date_rslvd','pneum_date','atelectasis_date','date_pneumothorax','pleuraleff_date','pulm_embolism_date',
                     'heart_failure_date','dvt_time','non_cardiac_arrest_date','outcomes_tpn_elev_time','outcomes_mi_date','out_afli_date','afla_date','outcomes_other_svt_time','date_vt','date_scnd_av_blck',
                     'date_thr_av_blck','outcomes_uti_datetime','sepsis_date','outcomes_sept_shock_time','date_ssi','outcomes_drain_time','outcomes_major_bleed_time','riffle_date','outcomes_hypoglycemia_time',
                     'outcomes_diabeticketo_time','date_bwl_obstrct','outcomes_fracture_time','outcomes_opioid_intox_time','outcomes_reop_timedate','date_other_sae','sixmo_death_date'
                     # 'sixmo_admission_date','sixmo_icuadmission_date'
                     ]

#Create pairs of outcome dates and sae y/n values as dictionary
sae_y_n_to_date_lookup_dictionary = {
'delirium_sae'				      : 'delirium_date',
'syncope_sae'				        : 'syncope_date',
'tia_sae' 		  	         	: 'tia_date',
'pneum_sae'   	  	     		: 'pneum_date',
'atelectasis_sae'		      	: 'atelectasis_date',
'pneumothorax_sae'		    	: 'date_pneumothorax',
'pleuraleff_sae'			      : 'pleuraleff_date',
'heart_failure_sae'			    : 'heart_failure_date',
'outcomes_tpn_elev_sae'     : 'outcomes_tpn_elev_time',
'dvt_sae'			            	: 'dvt_time',
'out_afli_sae'			       	: 'out_afli_date',
'afla_sae'			          	: 'afla_date',
'outcomes_other_svt_sae'    : 'outcomes_other_svt_time',
'scnd_av_blck_sae'		    	: 'date_scnd_av_blck',
'thr_av_blck_sae'		      	: 'date_thr_av_blck',
'outcomes_uti_sae'		    	: 'outcomes_uti_datetime',
'sepsis_sae'				        : 'sepsis_date',
'ssi_sae'				            : 'date_ssi',
'riffle_sae' 				        : 'riffle_date',
'outcome_hypoglycemia_sae'  : 'outcomes_hypoglycemia_time',
'bwl_obstrct_sae'			      : 'date_bwl_obstrct',
'outcomes_opioid_intox_sae'	: 'outcomes_opioid_intox_time'
}
#outcome dates with no sae indication:
outcomes_no_sae = ['stroke_date','resp_failr_date','imv_date','pulm_embolism_date','non_cardiac_arrest_date','outcomes_mi_date','date_vt','outcomes_sept_shock_time','outcomes_major_bleed_time',
                   'outcomes_diabeticketo_time','outcomes_fracture_time','outcomes_reop_timedate','outcomes_drain_time','date_other_sae','sixmo_death_date']