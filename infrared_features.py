import numpy as np
import heartpy as hp
import scipy

def get_ir_results(df, ir_results,ppnum,freq):

    '''
    df = 1-dim timeseries
    ir_results = list with feature names
    label = 
    freq = sample frequency
    '''
    
    new = np.zeros(df.shape)
    new = hp.filtersignal(df, [.3,2], sample_rate =freq, order = 2,filtertype='bandpass')

    smoothed_pos = hp.filtersignal(new, 0.3, sample_rate =freq, order =2,filtertype='highpass')
    smoothed_pos = hp.filtersignal(smoothed_pos, 2.5, sample_rate =freq, order = 2,filtertype='lowpass')

    scaled = hp.scale_data(new)

    rr_list = scipy.signal.find_peaks(scaled)[0]
    
    scaled[rr_list ]=scaled[rr_list ]-50
     
    upper_std = np.mean(rr_list[1:]) + (1*np.std(rr_list[1:]))
    lower_std = np.mean(rr_list[1:]) - (1*np.std(rr_list[1:]))
    for item in range(len(rr_list)):
        if rr_list[item] > upper_std or rr_list[item] < lower_std:
            np.delete(rr_list, item)
            
    rr_diff = np.abs(np.diff(rr_list))

    med = np.median(rr_list)
    mad = np.median(np.abs(rr_list - med))  
    ibi = np.mean(df)        
    sdnn=np.std(df)
    sdsd = np.std(rr_diff)
    
    hrv=np.mean(rr_diff)
    nn20=rr_diff[np.where(rr_diff >20)]
    nn50=rr_diff[np.where(rr_diff >50)]
        
    try:
        pnn20=float(len(nn20)) / float(len(rr_diff))
    except:
        pnn20=np.nan
    try:
        pnn50=float(len(nn50)) / float(len(rr_diff))
    except:
        pnn50=np.nan
        
    ir_results = ir_results.append({'ibi_ir':ibi,
                                    'mad_ir':mad,
                                    'sdnn_ir':sdnn,
                                    'sdsd_ir':sdsd,
                                    'hrv_ir':hrv,
                                    'pnn20_ir':pnn20,
                                    'pnn50_ir':pnn50,
                                    'ppnum':ppnum,
                                    'label':label}, 
        ignore_index=True)
