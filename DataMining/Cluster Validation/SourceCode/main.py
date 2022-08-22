import pandas as pd
import numpy as np
import scipy
from datetime import datetime, timedelta
import sklearn as skl
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, f1_score,accuracy_score
import math
from sklearn import metrics
from sklearn.metrics import mean_squared_error 
from sklearn.cluster import KMeans,DBSCAN
from scipy.stats import entropy


def features(data):
    if len(data.columns) ==30:
        start=6
    else:
        start=0
    for index in range(len(data)):
        if index==0:
            x = rowDataFeatures(data.iloc[index][0:], start)
            result = np.array(x)
        else:
            y = rowDataFeatures(data.iloc[index][0:], start)
            result = np.vstack((result, y))
    data = pd.DataFrame(result)
    return data 
    
    

def extractFeaturefromMealData(insulinData):
    dateTimeIndex = ['Date', 'Time','timestamp','BWZ Carb Input (grams)']
    input = pd.read_csv(insulinData, low_memory=False)      
    df_input = pd.DataFrame(input[input['BWZ Carb Input (grams)'].notna()]).iloc[::-1]
    df_input['timestamp'] = df_input.Date.str.cat(df_input.Time,sep=" ").astype('datetime64[s]')
    df_input['timestamp'] = pd.to_datetime(df_input['timestamp'], format='%m/%d/%Y %H:%M:%S' )
    df = pd.DataFrame(df_input[dateTimeIndex])
    df=df.reset_index(drop=True)
    df.rename(columns={'BWZ Carb Input (grams)':'mealData'}, inplace=True)
    zeroMeal = df.loc[df.mealData < 1 ]
    mealData = df.loc[df.mealData >=1 ]
    mealData = mealData.reset_index(drop=True)
    mealData['Time_diff'] = pd.to_datetime(mealData['timestamp'].astype(str)).diff()
    mealData['Time_diff'] = mealData['Time_diff'].shift(-1).fillna(pd.Timedelta(hours=2))
    mealData['Time_diff'] = (mealData['Time_diff'].dt.total_seconds()/3600).round(2)
    endTime = mealData.iloc[-1]['timestamp']
    mealData['next_mtime'] = pd.to_datetime(mealData['timestamp'].astype(str)).shift(-1).fillna(endTime)
    mealData = mealData.drop(columns=['Date','Time'])
    mealData = mealData.reset_index(drop=True)
    return mealData
    
def extractCGMData(CGMData):
    dateFormat = lambda x: datetime.strptime(x,  format='%m/%d/%Y %H:%M:%S')
    CGMInput = pd.read_csv(CGMData, low_memory=False,  usecols=['Date','Time','Sensor Glucose (mg/dL)'])
    CGMInput['timestamp'] = CGMInput.Date.str.cat(CGMInput.Time,sep=" ").astype('datetime64[s]')
    CGMInput['timestamp'] = pd.to_datetime(CGMInput['timestamp'], format='%m/%d/%Y %H:%M:%S' )
    
    CGMInput=pd.DataFrame(CGMInput[CGMInput['Sensor Glucose (mg/dL)'].notna()]).iloc[::-1]
    CGMInput.rename(columns={'Sensor Glucose (mg/dL)':'cgmdata'}, inplace=True)
    
    df_CGM = CGMInput.drop(columns=['Date','Time'])
    df_CGM = df_CGM.reset_index(drop=True)
    return df_CGM 
    
def rowDataFeatures(data, N):
    if N == 6:
        minCGM = data[6]
        minDT = 6
    else:
        minCGM = data[0]
        minDT = 0
    maxCGM = data.max()
    maxDT = data.idxmax() 
    timeDiff = abs(maxDT - N) * 5
    diff_cgm = maxCGM - minCGM
    nom = diff_cgm / minCGM
    diff = (maxCGM - data[maxDT + 1])  if maxDT < len(data) - 1 else (maxCGM - data[maxDT - 1])
    ddf = (maxCGM - data[maxDT + 1]) ** 2 if maxDT < len(data) - 1 else (maxCGM - data[maxDT - 1]) ** 2
    mealData = np.array(data)
    x = np.fft.fft(mealData)
    dataAbs = np.abs(x)
    absDiff = np.unique(dataAbs)[-2] - np.unique(dataAbs)[-3]
    diff= np.diff(mealData)
    f = np.array([timeDiff, diff_cgm, nom, ddf, absDiff])
    return f  




def filterMealData(insulin_Feature):
    filterData = insulin_Feature.loc[insulin_Feature.Time_diff < 2.00,:]
    df_meal = insulin_Feature.loc[insulin_Feature.Time_diff >= 2.00,:]
    df_meal = df_meal.reset_index(drop=True)
    return df_meal
   

def mealDetails(insulin,CGM, threshold,limit):
    mealData = pd.DataFrame(columns=range(limit))
    updatedInsulinValue = pd.DataFrame()

    for index in range(len(insulin) - 1):
        startTimeDetails = insulin.iloc[index]['timestamp']
        cgmTemp = CGM.loc[((CGM['timestamp']) >= startTimeDetails)]
        startTime=cgmTemp.timestamp.iloc[0]
        mealFrequency = CGM.loc[((CGM['timestamp']) >= (startTime-timedelta(hours=0.5))) & ((CGM['timestamp']) <= (startTime+timedelta(hours=2)))]
        temp = mealFrequency['cgmdata'].head(limit)
        count = mealFrequency['cgmdata'].count()
        if count >=threshold :
            updatedInsulinValue=updatedInsulinValue.append(insulin.iloc[index])
            temp= mealFrequency['cgmdata'].T
            resetValue = temp.reset_index(drop=True)
            mealData = mealData.append(resetValue)
        mealData = mealData.apply(lambda row: row.fillna(int(row.mean())), axis=1)
    updatedInsulinValue = updatedInsulinValue.reset_index(drop=True)
    return mealData, updatedInsulinValue



def extractGroundTruth(insulinData):
    minValue = insulinData['mealData'].min()
    maxValue = insulinData['mealData'].max()
    binSize = math.floor((maxValue-minValue)/20)
    bins=[] 
    cluster=[]
    for index in range(binSize):
        if index==0:
            bins=[minValue-1]
        else:
            bins.append(bins[index-1]+20)
        cluster.append(index)
    bins.append(maxValue)
    insulinData['mealData_bin']=pd.cut(x = insulinData['mealData'],bins = bins, labels = cluster)
    insulinData = insulinData.reset_index()
    sortValue = insulinData.sort_values(by='mealData_bin')
    return sortValue 



def kmeans(X, n_clusters):
    i = StandardScaler()
    X = i.fit_transform(X)
    cluster = KMeans(n_clusters = n_clusters)
    cluster.fit(X)
    res = cluster.predict(X)
    return res


def purityScore(y_true, y_pred):
    contingencyMatrix = metrics.cluster.contingencyMatrix(y_true, y_pred)
    return np.sum(np.amax(contingencyMatrix, axis=0)) / np.sum(contingencyMatrix)

def purityMatrix(matrix):
    purity = np.amax(matrix,axis=1).sum()/matrix.sum()
    return purity

def squaredError(y_true, y_pred):
    MSE = mean_squared_error(y_true, y_pred)
    counts = np.count_nonzero(y_true)
    return MSE*counts


def calculateEntropy(matrix):
    x = []
    entropyValue = []
    for p in range(len(matrix)):
        x.insert(p,sum(matrix[p]))
        entropyValue.insert(p,0)
        y = []
        for q in range(len(matrix[p])):
            if x[p]!=0:         
                val = matrix[p][q]/x[p]
                if val!=0:
                    y.insert(q,val)
        entropyValue[p]=entropy(y,base=2)
    total = sum(x)
    totalEntropy=0
    for p in range(len(entropyValue)):
        totalEntropy = ((x[p]/total)*entropyValue[p])+totalEntropy
    return totalEntropy


def calculateDBSCAN(matrix, eps, min_samples):
    z = StandardScaler()
    X = z.fit_transform(matrix)
    val = DBSCAN(eps=eps, min_samples = min_samples).fit(X)
    y_pred = val.fit_predict(X)
    return y_pred




#Extrating features from InsulinData.csv and CGMData.csv
insulin_Feature = extractFeaturefromMealData("InsulinData.csv");  
filteredInsulinData = filterMealData(insulin_Feature);

groundtruthInsulin = extractGroundTruth(filteredInsulinData)
CGM_Feature = extractCGMData("CGMData.csv");
df_Meal, df_insulin = mealDetails(groundtruthInsulin,CGM_Feature, 24, 30);


clusters = df_insulin.mealData_bin.nunique()
y_true = df_insulin["mealData_bin"].to_numpy()

meal_feature= features(df_Meal)
if clusters <= 1:
    clusters=1
    
kmeansVal               = kmeans(meal_feature,clusters)
kmeans_cf               = confusion_matrix(y_true, kmeansVal)
km_meanSquaredErrorVal  = squaredError(y_true, kmeansVal) 
km_entropyVal           = calculateEntropy(kmeans_cf)
km_purityVal            = purityMatrix(kmeans_cf)


DBSCAN_Value            = calculateDBSCAN(meal_feature,1.5,16)
DBSCAN_cf               = confusion_matrix(y_true,DBSCAN_Value)
DBSCAN_meanSquaredErr   = squaredError(y_true, DBSCAN_Value)
DBSCAN_entropy          = calculateEntropy(DBSCAN_cf)
DBSCAN_purity           = purityMatrix(DBSCAN_cf)


result = [km_meanSquaredErrorVal,DBSCAN_meanSquaredErr,km_entropyVal,DBSCAN_entropy,km_purityVal,DBSCAN_purity]
print(result)
df_result = pd.DataFrame([result])
df_result.to_csv('Result.csv', index = False, header=False)
print(":::::::::::: -Data Written To CSV File- ::::::::::::::::::::")


