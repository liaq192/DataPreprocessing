
# coding: utf-8

# In[26]:

3#Imports
import csv;
import os;
from itertools import groupby;
from datetime import datetime ,timedelta;
import datetime;
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce


# In[27]:

#Helper Functions
def dateFormatting(inp_date) : 
    #print( '[Str] Date :' + inp_date);
    date_time  = inp_date.split(' ');
    date = date_time[0].split('-');
# 13 --> 2013  ( fun(13) = 0013 --> fun(2013) = 2013 );
    date[0] = '20' + date[0];  
    time = date_time[1].split(':');
    newDate = datetime.datetime(*map(int, (date + time)))
    #print('[Date] Date :' + str(newDate));
    return newDate;

def keyForSorting(row) :
    inTime = row[2];
    return str((inTime.date())) + ':' + str(inTime.hour);



# In[28]:

#File Data Loading


base_path='C:\\Uni\\Research\\Data';
filename='Parking_Info_2013.csv';
path_to_file = os.path.join(base_path, filename);
print('File Path :' + path_to_file);

inputData = [];

counter = 0;
with open(path_to_file, encoding="utf-8",  newline='') as f:
    reader = csv.reader(f)
    next(f)
    for row in reader:
        dat = row[:2];
        dat.append(dateFormatting(row[2]));
        dat.append(dateFormatting(row[3]));
        
        inputData.append(dat );
        #print(row);
#         inTime =;
#         outTime = ;
        #print(str(inTime) + ' ' + str(inTime.hour) + '  ' + str(inTime.weekday()) , str(outTime)  + ' ' + str(outTime.hour)+ '  ' + str(outTime.weekday()) );
        # As data is sorted at Incoming Date , we can use 
        counter += 1;
#         if (counter >= 1000) :
#             break;
            
    #print(inputData);
    print('Total Rows :' + str(counter) );
  


# In[29]:

groups = [];
uniqueKeys = [];
for key , group in groupby(inputData ,keyForSorting ):
    groups.append(list(group))    # Store group iterator as a list
    uniqueKeys.append(key);
#         print (uniqueKeys[-1]);
#         print ('[Hr] : ' +  key + '  [Incoming] : ' + str(len(groups[-1])));
    #for thing in group:
#print(str(groups));
#     [print(X) for X in groups];
   
  


# In[30]:

# Grouping For Outgoing Cars


outTimeSortedData = sorted(inputData , key= lambda X : X[3]);
#     [print(str(X[3]) +' : ' + str(X[2]) )  for X in outTimeSortedData];
 
outTimeGroups = [];
outTimeUniqueKeys = [];

for key , group in groupby(outTimeSortedData ,lambda X : str( str(X[3].date()) + ':' + str(X[3].hour)) ):
    outTimeGroups.append(list(group))    # Store group iterator as a list
    outTimeUniqueKeys.append(key);
#         print (outTimeUniqueKeys[-1]);
#         print ('[Hr] : ' +  key + '  [Outgoing] : ' + str(len(outTimeGroups[-1])));


#     [print(str(inKey) +' '+ str(len(inCars)) +' '+ str(outKey) +' '+ str(len(outCars))) for inKey , inCars , outKey , outCars in uniquekeys , groups , outTimeUniquekeys , outTimeGroups]
#     for i in range(0,len(uniquekeys)):
#         print(  str(uniqueKeys[i]) + ' ' + str(len(groups[i])) + ' ' + str(outTimeUniqueKeys[i]) + ' ' + str(len(outTimeGroups[i])) + ' '  );


# In[31]:

#Data Checking : If incount == OutCount
# Idealy it should be equal 
inCount = 0;
outCount  = 0;

for eachGroup in groups:
    inCount = inCount + len(eachGroup) ;

for eachGroup in  outTimeGroups:
    outCount = outCount + len(eachGroup);
    
print ( 'Total InComing Cars :' + str(inCount) + '   : OutCount : ' + str(outCount) );


#Incount == OutCount


# In[32]:



# Sanity Checks for the Data 


print ("Incoming Groups : " + str(len(uniqueKeys))+ "  Outgoing Groups : " + str(len(outTimeUniqueKeys)));

# Comparing In vs Out and making pairs according to Time.     
inCount = 0;
outCount  = 0;
inTemp = uniqueKeys[0].split(':');
inTempTime = datetime.datetime.strptime( inTemp[0] , '%Y-%m-%d') + timedelta(hours= int(inTemp[1]) );
outTemp = outTimeUniqueKeys[0].split(':');
outTempTime = datetime.datetime.strptime( outTemp[0] , '%Y-%m-%d') + timedelta(hours= int(outTemp[1]));

inTemp = uniqueKeys[-1].split(':');
inTempEndTime = datetime.datetime.strptime( inTemp[0] , '%Y-%m-%d') + timedelta(hours= int(inTemp[1]) );
outTemp = outTimeUniqueKeys[-1].split(':');
outTempEndTime = datetime.datetime.strptime( outTemp[0] , '%Y-%m-%d') + timedelta(hours= int(outTemp[1]));

print('InTime : ' + str(inTempTime)  + '  OutTime : ' + str(outTempTime) + '    InEndTime : ' + str(inTempEndTime) + '   OutTempEndTime  : '+str(outTempEndTime) );


startTime = datetime.datetime.now();
endTime = datetime.datetime.now();

if inTempTime < outTempTime :
    startTime = inTempTime;
else :
    startTime = outTempTime;

if outTempEndTime > inTempEndTime :
    endTime  = outTempEndTime;
else :
    endTime = inTempEndTime;

print('[  ' + str(startTime) +' --> ' + str(endTime)   + '  ]');

inCounter = 0;
outCounter = 0;
slots = [];

inCurrent =  uniqueKeys[inCounter].split(':');
inCurrentKey = datetime.datetime.strptime( inCurrent[0] , '%Y-%m-%d') + timedelta(hours= int(inCurrent[1]) );

outCurrent =  outTimeUniqueKeys[outCounter].split(':');
outCurrentKey = datetime.datetime.strptime( outCurrent[0] , '%Y-%m-%d') + timedelta(hours= int(outCurrent[1]) );

while (startTime <= endTime):
    timeStamp = [ startTime , 0 , 0  ]


    while (inCurrentKey < startTime ):
        inCounter += 1;
        if inCounter >= len(uniqueKeys) : break;
        inCurrent =  uniqueKeys[inCounter].split(':');
        inCurrentKey = datetime.datetime.strptime( inCurrent[0] , '%Y-%m-%d') + timedelta(hours= int(inCurrent[1]) );    

    if (inCurrentKey == startTime):
        timeStamp[1] = len(groups[inCounter]);
        inCount += len(groups[inCounter]);



    while (outCurrentKey < startTime ):
        outCounter += 1;
        if outCounter >= len(outTimeUniqueKeys) : break;
        outCurrent =  outTimeUniqueKeys[outCounter].split(':');
        outCurrentKey = datetime.datetime.strptime( outCurrent[0] , '%Y-%m-%d') + timedelta(hours= int(outCurrent[1]) );    

    if (outCurrentKey == startTime):
        timeStamp[2] = len(outTimeGroups[outCounter]);
        outCount += len(outTimeGroups[outCounter]);

    slots.append(  timeStamp  );    
    startTime = startTime + timedelta(hours = 1);


    
print ( 'Total InComing Cars :' + str(inCount) + '   : OutCount : ' + str(outCount) );

# Already Parked Cars : 26  ** Not already parked 
# Rather these are the cars parked left after 1st hr . 
# as our logic starts from X[1] therefore need to address X[0] = 26 manually. 

parkedCars = 26;
# For the initial case 
# Assuming that parking is empty at start;
slots[0].append(26);



for i in range (1,len(slots)) : 
    parkedCars = (slots[i])[1] - (slots[i])[2] + parkedCars ;
    slots[i].append( parkedCars );
[print(slot) for slot in slots ];


# Data Varified till the parking : Its correct and has right Counts. 

# Plotting this Data raw. 





plot_date =[];
inComing = [];
outGoing = [];



# print(slots[0].)
for i in range(0 , len(slots)):
    plot_date.append((slots[i][0]).strftime('%d-%m-%Y HH'));
    inComing.append(slots[i][1]);
    outGoing.append(slots[i][2]);



# plt.plot(plot_date, inComing, plot_date ,outGoing , label='Raw Data Graph');

# # Add a legend
# plt.legend('Incoming' , 'OutGoing');
# plt.xlabel('Date');
# plt.ylabel('Cars');

# # Show the plot
# plt.show()



# Now adding the Weekday and Hours. 
data_V3 = slots[:];

        
        


# In[33]:


for i in range( 0 , len(slots)): #
    temp = data_V3[i];
#     print(str(temp[:1]))
    temp2 = (temp[:1]);
    temp2.append(temp[0].hour) ;
#     print(str(temp2));
    temp2.append(temp[0].weekday());
    temp2 = temp2 + temp[1:];
    data_V3[i] = temp2;
#     print('Slot[' + str(i) + '] : ' + str(temp2));
    
# Weekday and Time Added. 


# In[34]:



# Sorting based on Time and Plotting Graph based on  

# Plotting 24 HR based Graphs. 


# Avg 24 hrs all Data Graph. 

# Sorting based on HRS. 


hrwiseData = data_V3[:]

hrWiseSortedData = sorted(hrwiseData , key = lambda X : X[1]);
# print (str(type(hrWiseSortedData)) + '  Len :' + str(len(hrWiseSortedData)));
#[print(eachRow) for eachRow in hrWiseSortedData]; 
    
hrGroups = [];
hrGroupKeys = [];


for hr , hrGroup in groupby( hrWiseSortedData ,  lambda X : X[1]) : 
    hrGroups.append(list(hrGroup));
#     print(hrGroups[-1]);
    hrGroupKeys.append(hr);
# hrGroupslist = list()

# print (type(hrGroups));
# print(str(list(hrGroups)));
# [print(hr) for hr in list(hrGroups)];
# [print(str(list(hr))) for hr in list(hrGroups)]; 

# for i in range(0 , len(hrGroupKeys)):
#     print ('HrGroup :' + str(hrGroupKeys[i]) + '  :  ' + str( list(hrGroups[i]))  );



# Row Format
# Slot[7] : [datetime.datetime(2013, 1, 2, 16, 0), 16, 2, 33, 30, 43]
gHrs = [];
hrWiseAverageData = [];
for i in range(0 , len(hrGroupKeys)):
    eachHr = [hrGroupKeys[i] , 0 , 0];
    gHrs.append(hrGroupKeys[i]);
    inComingCars = 0;
    inComingCars = [rec[3] for rec in hrGroups[i]];
    outGoingCars = [rec[4] for rec in hrGroups[i]];
    
    eachHr[1] = reduce(lambda x , y : x+y , inComingCars);
    eachHr[2] = reduce(lambda x , y : x+y ,outGoingCars);
    hrWiseAverageData.append(eachHr);
#     print ( 'HR : ' + str(eachHr[0]) +'\t\t   Incoming : ' + str(eachHr[1]) + '\t\t\t   OutGoingCars Total : ' + str(eachHr[2]));

# Data Ready For Each Hr Total Data Graph. 



# Plotting Boiler plate

# Get current size
fig_size = plt.rcParams["figure.figsize"]
 
# Prints: [8.0, 6.0]
print ("Current size:", fig_size)
 
# Set figure width to 12 and height to 9
fig_size[0] = 12
fig_size[1] = 9
plt.rcParams["figure.figsize"] = fig_size

# plt.plot(gHrs, [eachHr[1] for eachHr in hrWiseAverageData], gHrs ,[eachHr[2] for eachHr in hrWiseAverageData] , label='24 Hrs Average In Out');

# # # Add a legend
# plt.legend('Incoming' , 'OutGoing');
# plt.xlabel('Date');
# plt.ylabel('Cars');

# Plot the data

# ------------ Working Graph Data


fig = plt.figure()
curPlot = plt.subplot(111);

incomingplot, = curPlot.plot(gHrs, [eachHr[1] for eachHr in hrWiseAverageData],  label='Incoming')
outgoingplot, = curPlot.plot(gHrs , [eachHr[2] for eachHr in hrWiseAverageData], label='Outgoing')

# Add a legend
plt.legend([incomingplot , outgoingplot] , ['Incoming Cars' , 'OutGoing Cars']);
plt.xlabel('Hours');
plt.ylabel('Cars');

# Show the plot
plt.title('24 Hrs Average Cars Traffic');
plt.grid(True);
# plt.axis([6,22 , 0 , 13000]);
plt.xlim(xmin=6  , xmax = 22);

# plt.axis('equal');
# plt.show()

fig.savefig('24 Hrs Average Cars Traffic.png')
#fig.close();

# plt.show()

# ------------------------------



# Testing new Graph Data . 

# fig = plt.figure()
# fig.savefig('plot.png');


# # y = [2,4,6,8,10,12,14,16,18,20]
# # x = np.arange(10)
# fig = plt.figure('24 Hrs Average of Complete Data')
# ax = plt.subplot(111)
# ax.plot(x, y, label='$y = numbers')
# plt.title('Legend inside')
# ax.legend()
# #plt.show()
 
# fig.savefig('plot.png')



# Now plot other Graphs . 







# In[35]:


# Now Ploting all the Graphs for each Weekday ( Hr Wise);


def HrwiseGraph( hrwiseData  , day) :

    
#     hrwiseData = data[:];


#     hrwiseData = data_V3[:]
#     hrwiseDataMondays = [x for x in hrwiseData if x[2] == 0] 
#     print(str(len(hrwiseDataMondays)) + ' : ' + str(len(hrwiseData)) );
    # hrwiseData = hrwiseDataMondays;
    # print(str(len(hrwiseDataMondays)) + ' : ' + str(len(hrwiseData)) );


    hrWiseSortedData = sorted(hrwiseData , key = lambda X : X[1]);
    # print (str(type(hrWiseSortedData)) + '  Len :' + str(len(hrWiseSortedData)));
    #[print(eachRow) for eachRow in hrWiseSortedData]; 

    hrGroups = [];
    hrGroupKeys = [];


    for hr , hrGroup in groupby( hrWiseSortedData ,  lambda X : X[1]) : 
        hrGroups.append(list(hrGroup));
    #     print(hrGroups[-1]);
        hrGroupKeys.append(hr);
    # hrGroupslist = list()

    # Row Format
    # Slot[7] : [datetime.datetime(2013, 1, 2, 16, 0), 16, 2, 33, 30, 43]
    gHrs = [];
    hrWiseAverageData = [];
    for i in range(0 , len(hrGroupKeys)):
        eachHr = [hrGroupKeys[i] , 0 , 0];
        gHrs.append(hrGroupKeys[i]);
        inComingCars = 0;
        inComingCars = [rec[3] for rec in hrGroups[i]];
        outGoingCars = [rec[4] for rec in hrGroups[i]];

        eachHr[1] = reduce(lambda x , y : x+y , inComingCars);
        eachHr[2] = reduce(lambda x , y : x+y ,outGoingCars);
        hrWiseAverageData.append(eachHr);
    #     print ( 'HR : ' + str(eachHr[0]) +'\t\t   Incoming : ' + str(eachHr[1]) + '\t\t\t   OutGoingCars Total : ' + str(eachHr[2]));


    fig = plt.figure('24 Hrs Average of Complete - [ Day '+str(day) + ' ]')
    curPlot = plt.subplot();
    incomingplot, = curPlot.plot(gHrs, [eachHr[1] for eachHr in hrWiseAverageData],  label='Incoming')
    outgoingplot, = curPlot.plot(gHrs , [eachHr[2] for eachHr in hrWiseAverageData], label='Outgoing')

    # Add a legend
    plt.legend([incomingplot , outgoingplot] , ['Incoming Cars' , 'OutGoing Cars']);
    plt.xlabel('Hours');
    plt.ylabel('Cars');

    # Show the plot
    plt.title('24 Hrs Average Cars Traffic - [ Day '+str(day) + ' ]');
    plt.grid(True);
    # plt.axis([6,22 , 0 , 13000]);
    plt.xlim(xmin=6  , xmax = 22);

    # plt.axis('equal');
    # plt.show()

    # # Get current size
    # fig_size = plt.rcParams["figure.figsize"]

    # # Prints: [8.0, 6.0]
    # print ("Current size:", fig_size)

    # # Set figure width to 12 and height to 9
    # fig_size[0] = 12
    # fig_size[1] = 9
    # plt.rcParams["figure.figsize"] = fig_size
    

    fig.savefig('24 Hrs Average Cars Traffic-' + str(day) + '.png' )
    fig.close();
    #plt.show()



# Pre-Processing Data for each Graph
# Each Weekday Hour Wise Graphs. 


hrwiseData = data_V3[:]
# hrwiseDataMondays = [x for x in hrwiseData if x[2] == 0] 
# HrwiseGraph(hrwiseDataMondays);
# hrwiseDataMondays = [x for x in hrwiseData if x[2] == 1] 
# HrwiseGraph(hrwiseDataMondays);
# hrwiseDataMondays = [x for x in hrwiseData if x[2] == 2] 
# HrwiseGraph(hrwiseDataMondays);
# hrwiseDataMondays = [x for x in hrwiseData if x[2] == 3] 
# HrwiseGraph(hrwiseDataMondays);
# hrwiseDataMondays = [x for x in hrwiseData if x[2] == 4] 
# HrwiseGraph(hrwiseDataMondays);
# hrwiseDataMondays = [x for x in hrwiseData if x[2] == 5] 
# HrwiseGraph(hrwiseDataMondays);
# hrwiseDataMondays = [x for x in hrwiseData if x[2] == 6] 
# HrwiseGraph(hrwiseDataMondays);


# OverAll Average Month Wise
HrwiseGraph(data_V3 , 'Complete Data ');
# Day wise
[HrwiseGraph([x for x in hrwiseData if x[2] == day] , day) for day in range(0,7)];




# In[37]:

# Pre-Processing Data for Month Wise 24 hr graphs. 



# hrwiseDataMonthly = [x for x in hrwiseData if x[0].month == 1] 
# HrwiseGraph(hrwiseDataMonthly);


# for i in range(1,12):
#     for 
# Make the Range Generic.
[HrwiseGraph( [x for x in hrwiseData if x[0].month == hrwiseDataMonthly] , hrwiseDataMonthly) for hrwiseDataMonthly in range(1,10)]




# In[38]:

#Sorting Data on Day Grain.

groups = [];
uniqueKeys = [];
for key , group in groupby(inputData ,lambda X : str( str(X[3].date()) ) ):
    groups.append(list(group))    # Store group iterator as a list
    uniqueKeys.append(key);


outTimeSortedData = sorted(inputData , key= lambda X : X[3]);
#     [print(str(X[3]) +' : ' + str(X[2]) )  for X in outTimeSortedData];
 
outTimeGroups = [];
outTimeUniqueKeys = [];

for key , group in groupby(outTimeSortedData ,lambda X : str( str(X[3].date()) ) ):
    outTimeGroups.append(list(group))    # Store group iterator as a list
    outTimeUniqueKeys.append(key);    
    
    


# In[39]:


print ("Incoming Groups : " + str(len(uniqueKeys))+ "  Outgoing Groups : " + str(len(outTimeUniqueKeys)));

# Comparing In vs Out and making pairs according to Time.     
inCount = 0;
outCount  = 0;
inTempTime = datetime.datetime.strptime( uniqueKeys[0] , '%Y-%m-%d')  ;
outTempTime = datetime.datetime.strptime( outTimeUniqueKeys[0] , '%Y-%m-%d') ;

inTempEndTime = datetime.datetime.strptime( uniqueKeys[-1] , '%Y-%m-%d')  ;
outTempEndTime = datetime.datetime.strptime( outTimeUniqueKeys[-1] , '%Y-%m-%d') ;

print('InTime : ' + str(inTempTime)  + '  OutTime : ' + str(outTempTime) + '    InEndTime : ' + str(inTempEndTime) + '   OutTempEndTime  : '+str(outTempEndTime) );


startTime = datetime.datetime.now();
endTime = datetime.datetime.now();

if inTempTime < outTempTime :
    startTime = inTempTime;
else :
    startTime = outTempTime;

if outTempEndTime > inTempEndTime :
    endTime  = outTempEndTime;
else :
    endTime = inTempEndTime;

print('[  ' + str(startTime) +' --> ' + str(endTime)   + '  ]');

inCounter = 0;
outCounter = 0;
slots = [];

inCurrent =  uniqueKeys[inCounter].split(':');
inCurrentKey = datetime.datetime.strptime( uniqueKeys[inCounter] , '%Y-%m-%d')  ;

outCurrentKey = datetime.datetime.strptime(outTimeUniqueKeys[outCounter] , '%Y-%m-%d') ;


while (startTime <= endTime):
    timeStamp = [ startTime , 0 , 0  ]


    while (inCurrentKey < startTime ):
        inCounter += 1;
        if inCounter >= len(uniqueKeys) : break;
        inCurrentKey = datetime.datetime.strptime( uniqueKeys[inCounter] , '%Y-%m-%d')  ;    

    if (inCurrentKey == startTime):
        timeStamp[1] = len(groups[inCounter]);
        inCount += len(groups[inCounter]);



    while (outCurrentKey < startTime ):
        outCounter += 1;
        if outCounter >= len(outTimeUniqueKeys) : break;
        outCurrentKey = datetime.datetime.strptime( outTimeUniqueKeys[outCounter] , '%Y-%m-%d');    

    if (outCurrentKey == startTime):
        timeStamp[2] = len(outTimeGroups[outCounter]);
        outCount += len(outTimeGroups[outCounter]);

    slots.append(  timeStamp  );    
    startTime = startTime + timedelta(days = 1);


    
print ( 'Total InComing Cars :' + str(inCount) + '   : OutCount : ' + str(outCount) );


# Already Parked Cars : 26

parkedCars = 0;
# For the initial case 
# Assuming that parking is empty at start;
slots[0].append(0);



for i in range (1,len(slots)) : 
    parkedCars = (slots[i])[1] - (slots[i])[2] + parkedCars ;
    slots[i].append( parkedCars );

# [print(slot) for slot in slots ];





# In[40]:

def DaywiseGraph(dayWiseData , month) : 
    daywiseSortedData = sorted(dayWiseData , key = lambda X : X[0].day);
    hrGroups = [];
    hrGroupKeys = [];


    for hr , hrGroup in groupby( daywiseSortedData ,  lambda X : X[0].day) : 
        hrGroups.append(list(hrGroup));
    #     print(hrGroups[-1]);
        hrGroupKeys.append(hr);
    # hrGroupslist = list()

    # Row Format
    # Slot[7] : [datetime.datetime(2013, 1, 2, 16, 0), 16, 2, 33, 30, 43]
    gHrs = [];
    hrWiseAverageData = [];
    for i in range(0 , len(hrGroupKeys)):
        eachHr = [hrGroupKeys[i] , 0 , 0];
        gHrs.append(hrGroupKeys[i]);
        inComingCars = 0;
        inComingCars = [rec[1] for rec in hrGroups[i]];
        outGoingCars = [rec[2] for rec in hrGroups[i]];

        eachHr[1] = reduce(lambda x , y : x+y , inComingCars);
        eachHr[2] = reduce(lambda x , y : x+y ,outGoingCars);
        hrWiseAverageData.append(eachHr);
        
#     Day Wise Average Stats for Data    
    fig = plt.figure('Day Wise Average of ' + str(month))
    curPlot = plt.subplot();
    incomingplot, = curPlot.plot(gHrs, [eachHr[1] for eachHr in hrWiseAverageData],  label='Incoming')
    outgoingplot, = curPlot.plot(gHrs , [eachHr[2] for eachHr in hrWiseAverageData], label='Outgoing')

    # Add a legend
    plt.legend([incomingplot , outgoingplot] , ['Incoming Cars' , 'OutGoing Cars']);
    plt.xlabel('Days');
    plt.ylabel('Cars');

    # Show the plot
    plt.title('Day Wise Average of Complete Data');
    plt.grid(True);
    # plt.axis([6,22 , 0 , 13000]);
#     plt.xlim(xmin=6  , xmax = 22);

    # plt.axis('equal');
    # plt.show()

    # # Get current size
    # fig_size = plt.rcParams["figure.figsize"]

    # # Prints: [8.0, 6.0]
    # print ("Current size:", fig_size)

    # # Set figure width to 12 and height to 9
    # fig_size[0] = 12
    # fig_size[1] = 9
    # plt.rcParams["figure.figsize"] = fig_size

    fig.savefig('Day Wise Average of -' + str(month) + '.png' )
    #fig.close();
    #plt.show()

data_V4 = slots[:];
DaywiseGraph(data_V4 , 'Complete Data');

[DaywiseGraph(  [x for x in data_V4 if x[0].month == month]  , month ) for month in range(1,10)];


# Data Displayed daywise for each month + alldata. 






# In[41]:

#Day Wise Data For each Month.

# Grouping Data based on Weeks

weekwiseSorted = sorted(data_V4 ,   key= lambda X : X[0].isocalendar()[1] )
#     [print(str(X[3]) +' : ' + str(X[2]) )  for X in outTimeSortedData];
 
outTimeGroups = [];
outTimeUniqueKeys = [];

for key , group in groupby(weekwiseSorted ,lambda X :  X[0].isocalendar()[1]  ) :
    outTimeGroups.append(list(group))    # Store group iterator as a list
    outTimeUniqueKeys.append(key);    

# [print(x) for x in outTimeGroups ];  

weekwiseSortedData = [];
for i in range(0 , len(outTimeUniqueKeys)) :
    temp = [outTimeUniqueKeys[i] , 0 , 0];
#     eachHr[1] = reduce(lambda x , y : x+y , inComingCars);
#     temp[1] = reduce( lambda X,Y : print(X) , outTimeGroups[i]);
    temp = reduce( lambda X,Y :   [X[0] ,(X[1] + Y[1]) , (X[2] + Y[2]) ]  , outTimeGroups[i]);
    weekwiseSortedData.append(temp);
#     print(outTimeGroups[i]);
# [print(x) for x in weekwiseSortedData];    

def weekWiseGraphs(weekwiseSortedData , month) :
    #     Day Wise Average Stats for Data    
    fig = plt.figure('Monthly Wise Average of ' + str(month))
    subPlot = plt.subplot(); 
    incomingplot, = subPlot.plot([eachHr[0].isocalendar()[1] for eachHr in weekwiseSortedData], [eachHr[1] for eachHr in weekwiseSortedData],  label='Incoming')
    outgoingplot, = subPlot.plot([eachHr[0].isocalendar()[1] for eachHr in weekwiseSortedData] , [eachHr[2] for eachHr in weekwiseSortedData], label='Outgoing')

    # Add a legend
    plt.legend([incomingplot , outgoingplot] , ['Incoming Cars' , 'OutGoing Cars']);
    plt.xlabel('Week');
    plt.ylabel('Cars');

    # Show the plot
    plt.title('Monthly Average of ' + str(month));
    plt.grid(True);
    fig.savefig('Monthly Average of ' + str(month) + '.png' )
    #fig.close();
    #plt.show();
# All Data Graph.    
weekWiseGraphs(weekwiseSortedData , 'Complete Data');  
#Graph Month Wise
# a = [ X for X in weekwiseSortedData if (X[0].month == 1)]
# print(a);
# print()
#[weekWiseGraphs([ X for X in weekwiseSortedData if (X[0].month == mon)]  , mon) for mon in range(1,10)];
# [print( [ X for X in weekwiseSortedData if (X[0].month == month)] ) for month in range(1-3)];


# In[25]:

# Month Wise Traffic Data and Graph. 

# Grouping Data based on Weeks

monthwiseSorted = sorted(data_V4 ,   key= lambda X : X[0].month )
#     [print(str(X[3]) +' : ' + str(X[2]) )  for X in outTimeSortedData];
 
outTimeGroups = [];
outTimeUniqueKeys = [];

for key , group in groupby(monthwiseSorted ,lambda X :  X[0].month  ) :
    outTimeGroups.append(list(group))    # Store group iterator as a list
    outTimeUniqueKeys.append(key);    

# [print(x) for x in outTimeGroups ];  

monthwiseSortedData = [];
for i in range(0 , len(outTimeUniqueKeys)) :
    temp = [outTimeUniqueKeys[i] , 0 , 0];
#     eachHr[1] = reduce(lambda x , y : x+y , inComingCars);
#     temp[1] = reduce( lambda X,Y : print(X) , outTimeGroups[i]);
    temp = reduce( lambda X,Y :   [X[0] ,(X[1] + Y[1]) , (X[2] + Y[2]) ]  , outTimeGroups[i]);
    monthwiseSortedData.append(temp);
#     print(outTimeGroups[i]);
[print(x) for x in monthwiseSortedData];    

def monthWiseGraphs(weekwiseSortedData ) :
    #     Day Wise Average Stats for Data    
    fig = plt.figure('MonthWise Average of Complete Data')
    subPlot = plt.subplot();
    incomingplot, = subPlot.plot([eachHr[0].month for eachHr in weekwiseSortedData], [eachHr[1] for eachHr in weekwiseSortedData],  label='Incoming')
    outgoingplot, = subPlot.plot([eachHr[0].month for eachHr in weekwiseSortedData] , [eachHr[2] for eachHr in weekwiseSortedData], label='Outgoing')

    # Add a legend
    plt.legend([incomingplot , outgoingplot] , ['Incoming Cars' , 'OutGoing Cars']);
    plt.xlabel('Month');
    plt.ylabel('Cars');

    # Show the plot
    plt.title('MonthWise Average of Complete Data');
    plt.grid(True);
    
    fig.savefig('MonthWise Average of Complete Data.png' )
    #fig.close();
    
    #fig = plt.figure();
    #fig1 = plt.gcf();
#     fig1.savefig('plot.jpg', bbox_inches='tight');
#     fig1.savefig('plot.jpg');
monthWiseGraphs(monthwiseSortedData);    


# In[ ]:




# In[ ]:



