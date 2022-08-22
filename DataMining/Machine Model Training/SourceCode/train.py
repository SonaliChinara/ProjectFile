#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import scipy
#import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sklearn as skl
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, f1_score,accuracy_score
import pickle
#import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.covariance import OAS


trainCGMData = "CGMData.csv";
trainInsulinData = "InsulinData.csv";
testCGM_patient2 = "CGM_patient2.csv";
testInsulin_patient2 = "Insulin_patient2.csv";
testCGM_patient3 = "CGM_patient3.csv";
testInsulin_patient3 = "Insulin_patient3.csv";


# In[2]:


def extractCGMData(CGMData):
    try:
        custom_date_parser = lambda x: datetime.strptime(x,  format='%m/%d/%Y %H:%M:%S')
        df = pd.read_csv(CGMData, low_memory=False,  usecols=['Date','Time','Sensor Glucose (mg/dL)'])
        df['timestamp'] = df.Date.str.cat(df.Time,sep=" ").astype('datetime64[s]')
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%m/%d/%Y %H:%M:%S' )
        df=pd.DataFrame(df[df['Sensor Glucose (mg/dL)'].notna()]).iloc[::-1]
        df.rename(columns={'Sensor Glucose (mg/dL)':'cgmdata'}, inplace=True)
        df1=df.drop(columns=['Date','Time'])
        df1=df.iloc[::-1].reset_index(drop=True)
        return df1
    except NameError as e:
        print ('extractCGMDataFromCSV function is not defined!'+ str(e))
    except TypeError as e:
        print ("extractCGMDataFromCSV function is supposed to accept one argument. Yours does not!" + str(e))
    except KeyError:
        print ("extractCGMDataFromCSV function key error " + str(e)) 


# In[3]:


def getMealDataTimeStamp(insulinData):
    try:
        index=['Index', 'Date', 'Time','timestamp','BWZ Carb Input (grams)']
        datain = pd.read_csv(insulinData, low_memory=False)
        print('InsulinData before removing NaN values:', datain.shape)
        df = pd.DataFrame(datain[datain['BWZ Carb Input (grams)'].notna()]).iloc[::-1]
        df['timestamp'] = df.Date.str.cat(df.Time,sep=" ").astype('datetime64[s]')
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%m/%d/%Y %H:%M:%S' )
        df1 = pd.DataFrame(df[index])
        df1=df1.reset_index(drop=True)
        df1.rename(columns={'BWZ Carb Input (grams)':'mealData'}, inplace=True)
        #print(df1.shape)
        zeroMeal = df1.loc[df1.mealData < 1 ]
        print('MealData with zero readings:',zeroMeal.shape)
        mealDF=df1.loc[df1.mealData >=1 ]
        print('MealData after removing zero values  readings:',mealDF.shape)
        mealDF=mealDF.reset_index(drop=True)
        mealDF['Time_diff'] = pd.to_datetime(mealDF['timestamp'].astype(str)).diff()
        mealDF['Time_diff'] = mealDF['Time_diff'].shift(-1).fillna(pd.Timedelta(hours=2))
        mealDF['Time_diff'] = (mealDF['Time_diff'].dt.total_seconds()/3600).round(2)
        end=mealDF.iloc[-1]['timestamp']
        mealDF['next_mtime'] = pd.to_datetime(mealDF['timestamp'].astype(str)).shift(-1).fillna(end)
        mealDF=mealDF.drop(columns=['Index','Date','Time'])
        mealDF=mealDF.reset_index(drop=True)
        #print (mealDF.tail(20))
        return mealDF
    except NameError as e:
        print ('extractCGMDataFromCSV function is not defined!'+ str(e))
    except TypeError as e:
        print ("extractCGMDataFromCSV function is supposed to accept one argument. Yours does not!" + str(e))
    except KeyError:
        print ("extractCGMDataFromCSV function key error " + str(e))  


# In[4]:


def filterMealDataWithin2hours(df):
    try:
        removedf = df.loc[df.Time_diff < 2.00,:]
        print('MealData cases to be ignored betweentp>tmandtp<tm+2hrs  readings:',removedf.shape)
        meal_df=df.loc[df.Time_diff >= 2.00,:]
        meal_df=meal_df.reset_index(drop=True)
        print('Valid MealData Metrics for feature extraction readings:',meal_df.shape)
        return meal_df
    except NameError as e:
        print ('extractCGMDataFromCSV function is not defined!'+ str(e))
    except TypeError as e:
        print ("extractCGMDataFromCSV function is supposed to accept one argument. Yours does not!" + str(e))
    except KeyError:
        print ("extractCGMDataFromCSV function key error " + str(e))    


# In[5]:


def getFilteredtMealData(df, start, end, threshold):
    try:
        lst=[]
        for i in df:
            x = df.loc[(df['Date_time'] >= (i - pd.Timedelta(minutes=30))) & (df['Date_time'] < (i + pd.Timedelta(hours=2)))]
            y = x['Sensor Glucose (mg/dL)'].tolist()
            if len(y)>=threshold:
                ay= x['Sensor Glucose (mg/dL)'].apply(lambda row: row.fillna(int(row.mean())), axis=1).head(30).tolist()
            #print(mean)
            #ay=x['Sensor Glucose (mg/dL)'].fillna(mean)
            lst.append(ay)
            return lst
    except NameError as e:
        print ('extractCGMDataFromCSV function is not defined!'+ str(e))
    except TypeError as e:
        print ("extractCGMDataFromCSV function is supposed to accept one argument. Yours does not!" + str(e))
    except KeyError:
        print ("extractCGMDataFromCSV function key error " + str(e)) 


# In[6]:


def getfilteredDate(df0,a):
    print(a)
    #b= datetime.strptime(a.time(),'%H:%M:%S')
    #print(df0.head(5))
    mealStartTime = pd.to_datetime(a.time())
    print(mealStartTime)
    #df2=df0.index.get_loc(mealStartTime, method='nearest')
    ans=df.loc[mealStartTime]
    print(ans)
    return mealStartTime


# In[7]:


def extractMealData(insulinDF,cgmDf, threshold,limit):
    meal_df = pd.DataFrame(columns=range(30))
    #cgmDf = pd.DataFrame()
    arr = np.empty([1, limit], dtype=float)
    n=0
    custom_date_parser = lambda x: datetime.strptime(x,  format='%m/%d/%Y %H:%M:%S')
    for i in range(len(insulinDF) - 1):
        start = insulinDF.iloc[i]['timestamp']
        cgmDf = cgmDf.loc[((cgmDf['timestamp']) >= start)]
        #print(cgmDf)
        starttime=cgmDf.timestamp.iloc[0]
        #print(starttime)
        mealInstance = cgmDf.loc[((cgmDf['timestamp']) >= (starttime-timedelta(hours=0.5))) & ((cgmDf['timestamp']) <= (starttime+timedelta(hours=2)))]
        #print(mealInstance)
        #df1= df0[df0['timestamp'].dt.time.between((mealStartTime-timedelta(hours=0.5)).time(), (mealStartTime+timedelta(hours=2)).time())]
        temp = mealInstance['cgmdata'].head(30)
        count = mealInstance['cgmdata'].count()
        
        if count >=threshold :
            temp= mealInstance['cgmdata'].T
            reindex_Temp = temp.reset_index(drop=True)
            meal_df= meal_df.append(reindex_Temp)
    #meal_df.to_csv('insideextract.csv')
    meal_df=meal_df.apply(lambda row: row.fillna(int(row.mean())), axis=1)
   
    return meal_df


# In[8]:


import math
def extractNoMealData(insulinDF,cgmDf, threshold,limit):
    try:
        nomeal_df = pd.DataFrame(columns=range(24))
        n=0
        for i in range(len(insulinDF) - 1):
            start = insulinDF.iloc[i]['timestamp']
            if i == (len(insulinDF) - 1):
                end = cgmDf.timestamp.iloc[-1]
                print('finalrecord')
                print(end)
            else:
                end = insulinDF.iloc[i]['next_mtime']
            #print(end)
            cgmDf1 = cgmDf.loc[((cgmDf['timestamp']) >= (start))]
    #         if (start <= cgmDf['timestamp'].iloc[0]):
    #             print('Not enough time range to consider it as mealdata')
    #             continue;
    #         else:
            timediffCount = insulinDF.iloc[i]['Time_diff']
            counts= math.floor(timediffCount/2)-1
            if counts > 0:
                starttime=cgmDf1.timestamp.iloc[0]
                starttime=starttime+timedelta(hours=2)
                for j in range(counts):
                    noMealInstance = cgmDf1.loc[((cgmDf['timestamp']) >= (starttime)) & ((cgmDf1['timestamp']) <= (starttime+timedelta(hours=2)))]
                    #print(starttime)           
                    endtime= cgmDf1.timestamp.iloc[0]
                    endtime2=cgmDf1.timestamp.iloc[-1]
                    #print(endtime,endtime2)
                    temp = noMealInstance['cgmdata']
                    count = noMealInstance['cgmdata'].count()
                    if count >=threshold :
                        temp= noMealInstance['cgmdata'].T
                        reindex_Temp = temp.reset_index(drop=True)
                        nomeal_df= nomeal_df.append(reindex_Temp.head(24))
                starttime=starttime+timedelta(hours=2)
        nomeal_df=nomeal_df.apply(lambda row: row.fillna(int(row.median())), axis=1)
        return nomeal_df
    except NameError as e:
        print ('extractCGMDataFromCSV function is not defined!'+ str(e))
    except TypeError as e:
        print ("extractCGMDataFromCSV function is supposed to accept one argument. Yours does not!" + str(e))
    except KeyError:
        print ("extractCGMDataFromCSV function key error " + str(e)) 
    except IndexError:
        print ("extractCGMDataFromCSV function IndexError error " + str(e))    


# In[9]:


def D(xlist,ylist):
    yprime=np.diff(ylist)/np.diff(xlist)
    xprime=[]
    for i in range(len(yprime)):
        xtemp=(xlist[i+1]+xlist[i])/2
        xprime=np.append(xprime, xtemp)
    return xprime, yprime

def DobuleD(xprime,yprime):
    return D(xprime,yprime)

#def fft(x):
    


# In[10]:


def feature_extrction(meal_data_matrix):
    dg_norm = pd.DataFrame([], dtype=float)
    time_diff = pd.DataFrame([], dtype=float)
    feature = pd.DataFrame([], dtype=float)
    cgm_mean = pd.DataFrame([], dtype=float)
    #count = len(meal_data_matrix)
    #output_diffrence = pd.DataFrame([], dtype=float)
    #double_differentiaon = pd.DataFrame([], dtype=float)
    for i in range(len(meal_data_matrix)):
        cgm_max = meal_data_matrix.iloc[i].max()
        cgm_meal = meal_data_matrix.iloc[i][6]
        temp = (cgm_max - cgm_meal) / cgm_meal
       # output_diffrence =  D(meal_data_matrix.iloc[i], [i for i in range(0,30)])
        #double_differentiaon= 
        # max_loc = meal_data_matrix.loc(meal_data_matrix.iloc[i].max)
        time_diff = np.append(time_diff, (i - 6))
        dg_norm = np.append(dg_norm, temp)
    #print(dg_norm)
    #print(time_diff)
    time_diff = pd.Series(time_diff)
    dg_norm = pd.Series(dg_norm)
    cgm_mean = pd.Series(meal_data_matrix.mean(axis=1))
    #print(cgm_mean)
    # feature = np.concatenate(([dg_norm], [time_diff], [cgm_mean]), axis=1)
    # feature = pd.concat([dg_norm, time_diff, cgm_mean], axis=1).reset_index()
    feature = pd.concat([dg_norm, time_diff], axis=1)
    return feature


# In[11]:


print('Extracting train dataset from CGMData.csv and InsulinData.csv')
trainInsdf = getMealDataTimeStamp(trainInsulinData);       
trainfilteted_df = filterMealDataWithin2hours(trainInsdf);
trainCGMdf = extractCGMData(trainCGMData);
trainMeal_df= extractMealData(trainfilteted_df,trainCGMdf, 24, 30);
trainNoMeal_df= extractNoMealData(trainfilteted_df,trainCGMdf, 20, 24); 
print(trainMeal_df.shape)
print(trainNoMeal_df.shape)


# In[12]:


print('Extracting test dataset from CGMData.csv and InsulinData.csv')
testInsdf = getMealDataTimeStamp(testInsulin_patient2);       
testfilteted_df = filterMealDataWithin2hours(testInsdf);
testCGMdf = extractCGMData(testCGM_patient2);
testMeal_df= extractMealData(testfilteted_df,testCGMdf, 24, 30);
testNoMeal_df= extractNoMealData(testfilteted_df,testCGMdf, 20, 24);
#print(testMeal_df.shape)
#print(testNoMeal_df.shape)


# In[13]:


train_meal_matrix= feature_extrction(trainMeal_df)
#print(train_meal_matrix.columns)
train_nomeal_matrix= feature_extrction(trainNoMeal_df)
#print(train_nomeal_matrix.columns)


# In[14]:


from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
def training_data(df):
    x_train, x_test, y_train, y_test = train_test_split(df.drop('class_label', axis=1), df.class_label, test_size=0.2,
                                                        random_state=13)
    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(x_train, y_train)
    predictions = clf.predict(x_test)
    print(predictions)
    print(classification_report(y_test, predictions))
    filename = 'model.sav'
    pickle.dump(clf, open(filename, 'wb'))
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.score(x_test, y_test)
    print(result)
    return predictions


# In[15]:


test_meal_matrix= feature_extrction(testMeal_df)
test_nomeal_matrix= feature_extrction(testNoMeal_df)
test_meal_matrix['class_label'] = '1'
test_nomeal_matrix['class_label'] = '0'
test_features = [test_meal_matrix, test_nomeal_matrix]
test_feature_df = pd.concat(test_features)
result = training_data(test_feature_df)
print(result)


# In[16]:


train_meal_matrix= feature_extrction(trainMeal_df)
train_nomeal_matrix= feature_extrction(trainNoMeal_df)
train_meal_matrix['class_label'] = '1'
train_nomeal_matrix['class_label'] = '0'
train_features = [train_meal_matrix, train_nomeal_matrix]
train_feature_df = pd.concat(train_features)
result = training_data(train_feature_df)

print(result)

