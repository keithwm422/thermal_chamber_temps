#!/usr/bin/python

import time
import pprint
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from datetime import datetime, timedelta
from pip import main


print(os.getcwd())
print(os.path.dirname(__file__))
data_path=os.path.dirname(__file__)
file_name="testing_cleanup.csv"
name_to_read=os.path.join(data_path,file_name)
il=[1,2,3,4]
names=[]
tempnames=[]
for i in il:
      names.append("addr"+str(i))
      tempnames.append("temp"+str(i))
print(names)
print(tempnames)
my_list = ["apple", "banana", "cherry"]
my_dict = {my_list[i]: i for i in range(len(my_list))}

dtype1 = {i: str for i in names}
dtype2 = {j: float for j in tempnames}
print(dtype1)
print(dtype2)
dtype1.update(dtype2)
print(dtype1)
# USed to cleanup below
#temp_df=pd.read_csv(name_to_read)
#temp_df = temp_df.drop(temp_df[temp_df['temp1'] == 'DA'].index)
#temp_df = temp_df.drop(temp_df[temp_df['temp2'] == 'DA'].index)
#temp_df = temp_df.drop(temp_df[temp_df['temp3'] == 'DA'].index)
#temp_df = temp_df.drop(temp_df[temp_df['temp4'] == 'DA'].index)
#temp_df.dropna(inplace=True)
#temp_df.to_csv("testing_cleanup.csv",index=False)
temp_df=pd.read_csv(name_to_read)

print(temp_df.head())
print(type(temp_df.addr1.values[0]))
#print("Read in {} rows and with {} variables".format(temp_df.shape[0], temp_df.shape[1]))
print("  => First Timestamp: {}".format(temp_df.iloc[0].time))
print("  => Last Timestamp : {}".format(temp_df.iloc[-1].time))
#times_zeroed = pd.to_datetime(temp_df['time'])
#print(type(times_zeroed[0]))
times_zeroed=temp_df['time'].values - temp_df['time'].values[0]
temp_df['RealTimes']=times_zeroed
#calc the pumpdown time
print(type(temp_df.temp1.values[0]))

print(temp_df.addr1.unique)
min_pos=temp_df['temp1'].idxmin()

print("Time at min {} and temp change {} are ".format(times_zeroed[min_pos]/60, temp_df['temp1'].values[0]-temp_df['temp1'].min()))
# Now make a plot
fig = plt.figure(figsize=(14, 10), dpi=200)
axs=fig.add_subplot(111)
#gs = fig.add_gridspec(1, 1)
#axs = gs.subplots(sharex=True, sharey=False)
#axs = gs.subplots()
#axs[0].scatter(times, pressure, marker='.')
#axs[0].set_ylabel("Pressure (Torr)")
#axs[0].set_ylim([1, 759])

labelling=["cold plate","thermal braid","Heatsink", "dummy load"]
#temp1 is 0 which is cold plate, temp2 is D0 ois thermal braid
axs.scatter(temp_df.RealTimes, temp_df.temp1, marker='.', s=3, label=labelling[0]) #this is a temp by the inflections.
axs.scatter(temp_df.RealTimes, temp_df.temp2, marker='*', color='k', s=3,label = labelling[1]) #this is a temp by the inflections.
axs.scatter(temp_df.RealTimes, temp_df.temp3, marker='+', color='r', s=3,label = labelling[2]) #this is a temp by the inflections.
axs.scatter(temp_df.RealTimes, temp_df.temp4, marker='o', color='m', s=3,label = labelling[3]) #this is a temp by the inflections.
turn_on_dummies=10
cold_plating=2600
power_on=3950
higher_power=8400
ending=17200
axs.axvline(x=turn_on_dummies-5,ymin=0, ymax=1, ls=':', color='Brown')
axs.text(turn_on_dummies, -7, "Pretesting", color='Brown', rotation=90, fontsize=8)
axs.axvline(x=cold_plating-5,ymin=0, ymax=1, ls=':', color='Brown')
axs.text(cold_plating, -7, "TVAC start", color='Brown', rotation=90, fontsize=8)
axs.axvline(x=power_on-5,ymin=0, ymax=1, ls=':', color='Brown')
axs.text(power_on, -7, "DCT HSK ON", color='Brown', rotation=90, fontsize=8)
axs.axvspan(power_on, higher_power, alpha=0.1, color='royalblue',label="Power On default")
axs.axvspan(higher_power, ending, alpha=0.1, color='cyan', label="Worst Case")
#axs.axvspan(hot_case_start,hot_case_end , alpha=0.1, color='firebrick', label="hot case")
#axs.axvspan(kickflip_start,kickflip_end , alpha=0.3, hatch="XXX", color='darkorange', label="flipped hot case")

#axs[1].axvline(x=discharge_magnet,ymin=0, ymax=1, ls=':',color='Brown')
#axs[1].axvline(x=cold_wall_fill_start,ymin=0, ymax=1, color='black',label="cold wall fill start")
#axs[1].axvline(x=cold_wall_fill_end,ymin=0, ymax=1, color='black',label="cold wall fill start")

#axs.scatter(temp_df[temp_df.addr=="DA"].RealTimes, temp_df[temp_df.addr=="D1"].temp, marker='*',color='k',s=3,label="Copper Plate") #this is a temp by the inflections.
#axs.scatter(temp_df[temp_df.addr=="D0"].RealTimes, temp_df[temp_df.addr=="62"].temp, marker='+',color='r',s=3,label="Wedgelock") #this is a temp by the inflections.
#axs.scatter(temp_df[temp_df.addr=="10"].RealTimes, temp_df[temp_df.addr=="22"].temp, marker='o',s=3,color='m',label="TURFIO Heatsink back") #this is a temp by the inflections.

#dataframe[dataframe['Percentage'] > 70] 
#axs.scatter(times, magnetflows_array[:,0], marker='.',s=3) #this is a dictionary in each element of the array
#axs.scatter(times, Xadc_array[:,0], marker='.',s=3) #these are xadc for FPGA so array of voltages and temps somewhere
#axs.scatter(times, df['payload.fSFCStatus.fATX_V33'], marker='.',s=3) #this one is always 0
#axs.scatter(times, df['payload.fSFCStatus.fMB_V33SB'], marker='.',s=3) #this one is always 3.2 ish
#axs.scatter(times, df['payload.fSFCStatus.fMB_V33'], marker='.',s=3) #this one is always 2.56
plt.xlabel("Time(s)")
plt.ylabel("Temp (C)")
plt.ylim([-10,80])
plt.grid()
handles, labels = axs.get_legend_handles_labels()
#lgd = axs.legend(handles, labels)
lgd=fig.legend(handles, labels, loc='upper center', ncol=5, fontsize=8)
#for legend_handle in lgd.legendHandles:
    ###legend_handle.set_sizes([20])
#labels[6]._legmarker.set_markersize(6)
#lgd=fig.legend(handles, labels, loc='upper center', ncol=5, fontsize=8)
# as many of these as axs[1].scatter above


#lgd.legendHandles[-14].set_sizes([60])
#lgd.legendHandles[-13].set_sizes([60])
#lgd.legendHandles[-12].set_sizes([60])
#lgd.legendHandles[-11].set_sizes([60])
#lgd.legendHandles[-10].set_sizes([60])
#lgd.legendHandles[-9].set_sizes([60])
#lgd.legendHandles[-8].set_sizes([60])
#lgd.legendHandles[-7].set_sizes([60])
lgd.legendHandles[-6].set_sizes([60])
lgd.legendHandles[-5].set_sizes([60])
lgd.legendHandles[-4].set_sizes([60])
lgd.legendHandles[-3].set_sizes([60])
#lgd.legendHandles[-2].set_sizes([60])
#lgd.legendHandles[-1].set_sizes([60])#

#plt.savefig("plot_timeline_south.pdf", bbox_inches='tight')

#plt.savefig("plot_timeline_south.png")

plt.show()
# now in hours
# do conversions...

#Vertical lines
#axs[0].axvline(x=power_on_DAQ,ymin=0, ymax=1, color='red',label="power on DAQ")
#axs[0].text(power_on_DAQ, 10, "Power on DAQ", color='red',rotation=90, fontsize=8)
#axs[0].axvline(x=discharge_magnet,ymin=0, ymax=1, color='Brown',label="discharge magnet")
#axs[0].text(discharge_magnet, 10, "Discharge magnet", color='Brown', rotation=90, fontsize=8)
#axs[1].axvline(x=power_on_DAQ,ymin=0, ymax=1, ls=':', color='red')
#axs[1].axvline(x=discharge_magnet,ymin=0, ymax=1, ls=':',color='Brown')
#axs[1].axvline(x=cold_wall_fill_start,ymin=0, ymax=1, color='black',label="cold wall fill start")
#axs[1].axvline(x=cold_wall_fill_end,ymin=0, ymax=1, color='black',label="cold wall fill start")

# hatches for timespans
#axs.axvspan(cold_wall_fill_start, cold_wall_fill_end, alpha=0.1, color='royalblue',label="cold wall fill")
#axs.axvspan(cold_case_start, cold_case_end, alpha=0.1, color='cyan', label="cold case")
#axs.axvspan(hot_case_start,hot_case_end , alpha=0.1, color='firebrick', label="hot case")
#axs.axvspan(kickflip_start,kickflip_end , alpha=0.3, hatch="XXX", color='darkorange', label="flipped hot case")
#axs.axvspan(drain_cold_wall_begin,drain_cold_wall_end , alpha=0.1, color='royalblue', label="draining cold wall")
#axs.axvspan(slight_warmup_start,slight_warmup_end , alpha=0.3, color='red', label="slight warm up")

#size for markers visibility
s0=3
#temp data goes here

#across foam
#axs.scatter(NASA_TCs[1]['Times'], NASA_TCs[1]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[1]) # In South is on foam inside gondola
#axs.scatter(NASA_TCs[8]['Times'], NASA_TCs[8]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[8]) # SoLo is on foam outside gondola
#axs.scatter(NASA_TCs[0]['Times'], NASA_TCs[0]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[0]) # InEast is on foam inside foam
#axs.scatter(NASA_TCs[6]['Times'], NASA_TCs[6]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[6]) # EastLo is on foam inside gondola
#axs.set_ylim([-80, 30])
#axs.set_xlim([times.values[0],times.values[-1]])


#NASA TCs
#iter=0
#while iter<len(NASA_TCs):
#    #print(len(NASA_TCs[iter]['Times'].values))
#    #print(len(NASA_TCs[iter]['Value'].values))
#    #print(NASA_names[iter]['Times'].values))
#    axs.scatter(NASA_TCs[iter]['Times'], NASA_TCs[iter]['Value'], marker='.',s=s0,label=NASA_names.ID.values[iter]) # 
#    iter+=1
#
#axs.set_ylim([-79, 49])
#axs.set_xlim([times.values[0],times.values[-1]])

# south here : seq=1
#axs.scatter(times, mainhsk_temps_array[:,7], marker='.',s=s0,label=mainhsk_names.Location.values[7]) # TOF top South
#axs.scatter(times, mainhsk_temps_array[:,5], marker='.',s=s0,label=mainhsk_names.Location.values[5]) # TOF btm south
#axs.scatter(times, mainhsk_temps_array[:,3], marker='.',s=s0,label=mainhsk_names.Location.values[3]) # gondola btm south
#axs.scatter(times, mainhsk_temps_array[:,8], marker='.',s=s0,label=mainhsk_names.Location.values[8]) # gondola mid South
#axs.scatter(NASA_TCs[13]['Times'], NASA_TCs[13]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[13]) # SoFr is on the gondola I believe
#axs.scatter(NASA_TCs[1]['Times'], NASA_TCs[1]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[1]) # In South is on foam inside gondola
#axs.scatter(NASA_TCs[7]['Times'], NASA_TCs[7]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[7]) # SoUp is on foam outside gondola
#axs.scatter(NASA_TCs[8]['Times'], NASA_TCs[8]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[8]) # SoUp is on foam outside gondola
#axs.set_ylim([-50, 33])
#axs.set_xlim([times.values[0],times.values[-1]])


#RICH east or west side
#axs.scatter(times, mainhsk_temps_array[:,13], marker='.',s=s0,label=mainhsk_names.Location.values[13]) # Mid east RICH heatsink
#axs.scatter(times, mainhsk_temps_array[:,17], marker='.',s=s0,label=mainhsk_names.Location.values[17]) # RICH cover E
#axs.scatter(NASA_TCs[0]['Times'], NASA_TCs[0]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[0]) # InEast is on foam inside foam
#axs.scatter(NASA_TCs[5]['Times'], NASA_TCs[5]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[5]) # EastUp is on foam inside gondola
#axs.scatter(NASA_TCs[6]['Times'], NASA_TCs[6]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[6]) # EastUp is on foam inside gondola
#axs.scatter(times, mainhsk_temps_array[:,14], marker='.',s=s0,label=mainhsk_names.Location.values[14]) # Mid West RICH heatsink
#axs.scatter(times, mainhsk_temps_array[:,19], marker='.',s=s0,label=mainhsk_names.Location.values[19]) # RICH cover E
#axs.scatter(NASA_TCs[9]['Times'], NASA_TCs[9]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[9]) # WestUp is on foam inside gondola
#axs.scatter(NASA_TCs[10]['Times'], NASA_TCs[10]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[10]) # WestLo is on foam inside gondola
#axs.set_ylim([-60, 60])
#axs.set_xlim([times.values[0],times.values[-1]])

#North side across foam
#correct/calibrate the North top TOF sensor
#begin_pumping=datetime(2022,2,7,14,55,0,0)
#times_calibrate=pd.to_datetime(times.values)
#times_range=np.asarray(begin_pumping-times_calibrate).astype('timedelta64[s]')
#times_range = times_range / np.timedelta64(1, 's')
#times_to_consider=np.where(times_range>0)
#TOF_diffs=mainhsk_temps_array[times_to_consider,21]-mainhsk_temps_array[times_to_consider,7]
#average_offset=np.mean(TOF_diffs[0])
#median_offset=np.median(TOF_diffs[0])
#axs.scatter(times, mainhsk_temps_array[:,20], marker='.',s=s0,label=mainhsk_names.Location.values[20]) # Gondola btm north
#axs.scatter(times, mainhsk_temps_array[:,16], marker='.',s=s0,label=mainhsk_names.Location.values[16]) # TOF btm N
#axs.scatter(times, mainhsk_temps_array[:,21]-average_offset, marker='.',s=s0,label=mainhsk_names.Location.values[21]) # TOF top N
#axs.scatter(NASA_TCs[3]['Times'], NASA_TCs[3]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[3]) # NoUp is on foam inside gondola
#axs.scatter(NASA_TCs[4]['Times'], NASA_TCs[4]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[4]) # NoLo is on foam inside gondola
#axs.set_ylim([-80, 30])
#axs.set_xlim([times.values[0],times.values[-1]])



#misc 1 interesting areas
#axs[1].scatter(times, mainhsk_temps_array[:,2], marker='.',s=s0,label=mainhsk_names.Location.values[2]) # DCT HV box
#axs[1].scatter(times, mainhsk_temps_array[:,6], marker='.',s=s0,label=mainhsk_names.Location.values[6]) # SFC backplate
#axs[1].scatter(times, mainhsk_temps_array[:,15], marker='.',s=s0,label=mainhsk_names.Location.values[15]) # Gas panel
#axs[1].scatter(times, mainhsk_temps_array[:,3], marker='.',s=s0,label=mainhsk_names.Location.values[3]) # gondola btm South
#axs[1].scatter(times, dctboxtemp, marker='.',s=s0,label="DCT box internal temp") # dctbox temp
#axs[1].set_ylim([-50, 38])


#RICH
#axs.axvline(x=DAQ_Run,ymin=0, ymax=1, color='red',label="DAQ Run")
#axs.axvline(x=DAQ_Run_2,ymin=0, ymax=1, color='black',label="DAQ Run 2 end")
#axs.scatter(times, mainhsk_temps_array[:,23], marker='.',s=s0,label=mainhsk_names.Location.values[23]) # rich focal plane NW
#axs.scatter(times, mainhsk_temps_array[:,0], marker='.',s=s0,label=mainhsk_names.Location.values[0]) # rich focal plane SW
#axs.scatter(times, mainhsk_temps_array[:,18], marker='.',s=s0,label=mainhsk_names.Location.values[18]) # rich cover N
#axs.scatter(times, mainhsk_temps_array[:,9], marker='.',s=s0,label=mainhsk_names.Location.values[9]) # rich cover S
#axs.scatter(times, mainhsk_temps_array[:,19], marker='.',s=s0,label=mainhsk_names.Location.values[19]) # rich cover W
#axs.scatter(times, mainhsk_temps_array[:,17], marker='.',s=s0,label=mainhsk_names.Location.values[17]) # rich cover E
#axs.set_ylim([-20, 39])

#TOF Fees only
#axs.scatter(times, mainhsk_temps_array[:,12], marker='.',s=s0,label=mainhsk_names.Location.values[12]) 
#axs.scatter(times, mainhsk_temps_array[:,22], marker='.',s=s0,label=mainhsk_names.Location.values[22]) 
#axs.scatter(times, mainhsk_temps_array[:,24], marker='.',s=s0,label=mainhsk_names.Location.values[24]) 
#axs.scatter(times, mainhsk_temps_array[:,25], marker='.',s=s0,label=mainhsk_names.Location.values[25]) 

#Gondola Bottom
#axs.scatter(times, mainhsk_temps_array[:,3], marker='.',s=s0,label=mainhsk_names.Location.values[3]) 
#axs.scatter(times, mainhsk_temps_array[:,4], marker='.',s=s0,label=mainhsk_names.Location.values[4]) 
#axs.scatter(times, mainhsk_temps_array[:,20], marker='.',s=s0,label=mainhsk_names.Location.values[20]) 
#axs.scatter(times, mainhsk_temps_array[:,2], marker='.',s=s0,label=mainhsk_names.Location.values[2])

#bore paddle stuff
#axs.scatter(times, mainhsk_temps_array[:,10], marker='.',s=s0,label=mainhsk_names.Location.values[10]) 
#axs.scatter(times, mainhsk_temps_array[:,11], marker='.',s=s0,label=mainhsk_names.Location.values[11]) 

#DCT
#axs.axvline(x=heater_start,ymin=0, ymax=1,ls='-', color='red',label="heaters start")
#axs.axvline(x=heater_max,ymin=0, ymax=1,ls=':', color='black',label="heaters highest")
#axs.scatter(times, mainhsk_temps_array[:,15], marker='.',s=s0,label=mainhsk_names.Location.values[15]) #gas panel
#axs.scatter(times, mainhsk_temps_array[:,1], marker='.',s=s0,label=mainhsk_names.Location.values[1])  # DCTV top
#dct box temp
#axs.scatter(times,df['payload.dctBoxTemp'], marker='2',s=s0,label="DCT HSK box uC") # In South is on foam inside gondola
#axs.set_ylim([-30, 50])
# for DCT thermistors
#iter=0
#while iter<len(DCT_temps[0]): #,label=mainhsk_names.Location.values[1]
#    axs[1].scatter(times, DCT_temps_array[:,iter], marker='.',s=s0)  # DCTV top
#    iter+=1
#
#axs[1].set_ylim([-20, 39])

#axs.set_ylabel("Temps (C)")

#plt.xticks(rotation=45)
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d - %H:%M'))
#plt.gcf().autofmt_xdate()
#axs[0].grid()
#axs.grid()
#handles, labels = axs.get_legend_handles_labels()
#lgd = axs[1].legend(handles, labels)
#for legend_handle in lgd.legendHandles:
#    legend_handle.set_sizes([20])
#labels[6]._legmarker.set_markersize(6)
#lgd=fig.legend(handles, labels, loc='upper center', ncol=5, fontsize=8)
# as many of these as axs[1].scatter above


#lgd.legendHandles[-14].set_sizes([60])
#lgd.legendHandles[-13].set_sizes([60])
#lgd.legendHandles[-12].set_sizes([60])
#lgd.legendHandles[-11].set_sizes([60])
#lgd.legendHandles[-10].set_sizes([60])
#lgd.legendHandles[-9].set_sizes([60])
#lgd.legendHandles[-8].set_sizes([60])
#lgd.legendHandles[-7].set_sizes([60])
#lgd.legendHandles[-6].set_sizes([60])
#lgd.legendHandles[-5].set_sizes([60])
#lgd.legendHandles[-4].set_sizes([60])
#lgd.legendHandles[-3].set_sizes([60])
#lgd.legendHandles[-2].set_sizes([60])
#lgd.legendHandles[-1].set_sizes([60])#

#plt.savefig("plot_timeline_south.pdf", bbox_inches='tight')

#plt.savefig("plot_timeline_south.png")

#plt.show()
