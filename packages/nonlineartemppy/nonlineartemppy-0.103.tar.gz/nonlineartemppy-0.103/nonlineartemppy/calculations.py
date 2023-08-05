import numpy as np
import warnings

def degree_days(data, threshold):
    '''Calculates degree days with specific thresholds
    
    Keyword arguments
    data - pandas DataFrame with tmax and tmin in columns
    threshold - specific thresholds to integrate over'''
    
    
    retdat = data
    retdat = retdat.sort_values('date', ascending=True)
    retdat['tavg'] = (retdat.tmax + retdat.tmin)/2
    #nc = len(retdat.columns)
    

    for i in range(0, (len(threshold))):
        col = ("dday" + str(threshold[i]) + "C")

        b = threshold[i]

        retdat[col] = np.where(b <= retdat['tmin'], retdat['tavg']- b, 0)
        retdat[col]

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            temp = np.arccos((2*b - retdat['tmax']- retdat['tmin'])/(retdat['tmax'] - retdat['tmin']))

        retdat[col] = np.where((retdat.tmin < b) & (b < retdat.tmax), 
                               ((retdat.tavg -b)*temp + (retdat.tmax - retdat.tmin)*np.sin(temp)/2)/np.pi, 
                               retdat[col])
        retdat[col] = retdat[col].round(5)
    return(retdat)

def degree_time(data, threshold):
    '''Calculates time in each degree with specific thresholds
    
    Keyword arguments
    data - pandas DataFrame with tmax and tmin in columns
    threshold - specific thresholds to integrate over'''
    
    
    retdat = data
    retdat = retdat.sort_values('date', ascending=True)

    for i in range(0, (len(threshold))):
        col = ("tdegree" + str(threshold[i]) + "C")
        b = threshold[i]
        retdat[col] = 0

        n = len(retdat.tmin)
        t0 = np.repeat((threshold[i] - 0.5), n)
        t1 = np.repeat((threshold[i] + 0.5), n)

        t0[t0 < retdat.tmin] = retdat.tmin[t0 < retdat.tmin]
        t1[t1 > retdat.tmax] = retdat.tmax[t1 > retdat.tmax]

        with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    retdat[col] = (2/np.pi) * (np.arcsin((t1 - retdat.tmin)/(retdat.tmax - retdat.tmin)) - 
                                 np.arcsin((t0 - retdat.tmin)/(retdat.tmax - retdat.tmin)))
        retdat[col] = np.where(np.isnan(retdat[col]), 0, retdat[col])
        retdat[col] = np.where(retdat[col] < 0, 0, retdat[col])

        retdat[col] = retdat[col].round(5)
    return(retdat)




