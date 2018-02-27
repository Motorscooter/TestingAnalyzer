# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 08:13:57 2018

@author: scott.downard
"""
import os
from scipy.signal import filtfilt
import struct
import numpy as np

##finalDict outputs a dictionary that hold the Metadata from the impax file.
def finalDict(directory):
    startdict = {}
    new_float_data = []
    new_data = []
    time = []
    with open(directory,'rb') as fup:
        
        textfilestr = fup.read()
        textfilestr = textfilestr.decode('latin-1') #Decode text from binary file
        
        vs = textfilestr.find('VERTSCALE')     #Vertical scaling factor
        vo = textfilestr.find('VERTOFFSET')    #Vertical offset from 0
        vu = textfilestr.find('VERTUNITS')     #Vertical units
        hs = textfilestr.find('HORZSCALE')     #horizontal scaling factor
        ho = textfilestr.find('HORZOFFSET')    #horizontal offset from 0
        hu = textfilestr.find('HORZUNITS')     #horizontal units
        hups = textfilestr.find('HUNITPERSEC') #number of horizontal units per second
        rl = textfilestr.find('RECLEN')        #Number of datapoints in file
        xdc = textfilestr.find('XDCRSENS')     #Used to find grab the correct number of points in datapoint line
        if 'CLOCK_RATE' in textfilestr:            
            cr = textfilestr.find('CLOCK_RATE')    #Sample rate
            ss = textfilestr.find('SUBSAMP_SKIP')  #Used to grab correct number of points in Sample Rate
        else:
            cr = textfilestr.find('DDR_RATE')
            ss = textfilestr.find('EXTMASTER')

        

    
        startdict['VertScale'] = float(textfilestr[vs+10:vo - 1])
        startdict['VertOffset'] = float(textfilestr[vo+11:vu - 1])
        startdict['VertUnits'] = textfilestr[vu+10:hs - 1]
        startdict['HorzScale'] = float(textfilestr[hs+10:hups - 1])
        startdict['HorzUnitsPerSec'] = float(textfilestr[hups+12:ho - 1])
        startdict['HorzOffset'] = float(textfilestr[ho+11:hu - 1])
        startdict['HorzUnits'] = (textfilestr[hu+10:rl - 1])
        startdict['NumofPoints'] = int(textfilestr[rl+7:xdc-1])
        if 'CLOCK_RATE' in textfilestr:
            startdict['Sample Rate'] = float(textfilestr[cr+11:ss-1])
        else:
            startdict['Sample Rate'] = float(textfilestr[cr+9:ss-1])
    fup.close()
    with open(directory, 'rb') as fup:
        datacount = startdict['NumofPoints']
#        data = fup.read(datacount)
#        startdict['Data'] = data
        
        size = fup.read()
        data = struct.unpack('h'*datacount,size[len(size)-(datacount*2):])
        list_data = list(data)
        for i in list_data:
            new_float_data.append(float(i))
        for i in new_float_data:
            new_data.append(i *  startdict['VertScale'] + startdict['VertOffset'])
        startdict['Data'] = new_data
        timecount = startdict['HorzOffset']
        
        for i in range(0,startdict['NumofPoints']):
            time.append(timecount)
            timecount += startdict['HorzScale']
        startdict['Time'] = time
    fup.close()
    return startdict

#fileRead the impax file determine whether its an acceleration or displacement 
#file. Calls finalDict() function to place into data into dictionary.
def fileReadlin(directory):
    filelist = []
    totaldata_dic = {}
    for root, dirs, files in os.walk(directory):
        
        for filenames in files:
            files.sort()
            filename , file_extension = os.path.splitext(filenames)

            if filename == 'H0HEAD000000ACX0' or filename == 'H0HEAD000000DSX0':
                filedir = os.path.join(root,filenames)
                if int(file_extension.strip('.')) in filelist:
                    
                    if filename == 'H0HEAD000000ACX0':
                        totaldata_dic[int(file_extension.strip('.'))]['Acceleration'] = finalDict(filedir)
                    elif filename == 'H0HEAD000000DSX0':
                        totaldata_dic[int(file_extension.strip('.'))]['Displacement'] = finalDict(filedir)
                else:
                    
                    filelist.append(int(file_extension.strip('.')))                
                    totaldata_dic[int(file_extension.strip('.'))] = {} 
                    
                    if filename == 'H0HEAD000000ACX0':
                        totaldata_dic[int(file_extension.strip('.'))]['Acceleration'] = finalDict(filedir)
                    elif filename == 'H0HEAD000000DSX0':
                        totaldata_dic[int(file_extension.strip('.'))]['Displacement'] = finalDict(filedir)
    return totaldata_dic

def fileReadpres(directory):
    filelist = []
    totaldata_dic = {}
    for root, dirs, files in os.walk(directory):
        
        for filenames in files:
            files.sort()
            filename , file_extension = os.path.splitext(filenames)

            if "PR" in filename:
                filedir = os.path.join(root,filenames)
                if int(file_extension.strip('.')) in filelist:
                    filelist.append(max(filelist)+1)
                    index = max(filelist) + 1
                    totaldata_dic[index]['Pressure'] = finalDict(filedir)
                else:
                    
                    filelist.append(int(file_extension.strip('.')))
                    filelist.sort()
                    totaldata_dic[int(file_extension.strip('.'))] = {} 
                    totaldata_dic[int(file_extension.strip('.'))]['Pressure'] = finalDict(filedir)
    return totaldata_dic

def fileReadinfl(directory):
    filelist = []
    totaldata_dic = {}
    for root, dirs, files in os.walk(directory):
        
        for filenames in files:
            files.sort()
            filename , file_extension = os.path.splitext(filenames)

            if "TNK" in filename:
                filename, temp, tank = filename.split('_')
                filedir = os.path.join(root,filenames)
                filelist.append(filename)
                totaldata_dic[filename]['Tank'] = finalDict(filedir)

    return totaldata_dic      
#Filter processing based on SAE J211 filtering.
def filterProcessing(data_frame,CFC,sample_rate):    
    #calculate sample rate
        #Filter RAW data using J211 SAE Filtering
    sample_rate = int(sample_rate)
    T = 1/sample_rate
    wd = 2 * np.pi * CFC * 1.25*5.0/3.0
    x = wd * (T)/2
    wa = np.sin(x)/np.cos(x)
    
    a0 = wa**2.0/(1.0+np.sqrt(2.0)*wa+(wa**2.0))
    a1 = 2.0*a0
    a2 = a0
    b0 = 1
    b1 = (-2.0*((wa**2.0)-1.0))/(1.0+np.sqrt(2.0)*wa+(wa**2.0))
    b2 = (-1.0+np.sqrt(2.0)*wa-(wa**2.0))/(1.0+np.sqrt(2.0)*wa+(wa**2.0))
    b  = [a0,a1,a2]
    a = [b0,-1*b1,-1*b2]

#    CFC = 5/3*CFC
#    wn = CFC/sample_rate * 2
#    b,a = butter(2,wn,'low')
    y = filtfilt(b,a,data_frame)
    return y
def truntozero (data):
    idx1 = (np.abs(data-0)).argmin()
    del data[0:idx1]  
    return data

def tableCalc(accel,disp,time):
    maxAccel = []
    maxDisp = []
    contTime = []
    contact_index = []
    
    for accellist in accel:
        accellist = accellist.tolist()
        maxAccel.append(min(accellist))
        max_index = accellist.index(min(accellist))
        
        count = 0
        
        for i in reversed(accellist[0:max_index]):
            if i < -2.00:
                if round(i,1) == -2.00:
                    contact_index.append(accellist.index(i))                   
                    break
        
    for displist in disp:
        maxDisp.append(max(displist))
    count = 0
    for timelist in time:
        i = contact_index[count]
        contTime.append(timelist[i])
        count += 1

    return(maxAccel,maxDisp,contTime) 
