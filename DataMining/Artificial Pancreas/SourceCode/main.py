import pandas as pd
import numpy as np
from datetime import datetime


CGMData     = "CGMData.csv";
InsulinData = "InsulinData.csv";

overnightStartTime = datetime.strptime('00:00:00','%H:%M:%S')
overnightEndTime   = datetime.strptime('05:59:59', '%H:%M:%S')

dayStartTime = datetime.strptime('06:00:00','%H:%M:%S')
dayEndTime   = datetime.strptime('23:59:59', '%H:%M:%S')


def extractCGMDataFeature(CGMDataFile):
    readCGMData = pd.read_csv(CGMDataFile, low_memory=False)
    print(readCGMData.shape)
    return readCGMData


def clearCGMData(df):
    headers = ['Date','Time','Sensor Glucose (mg/dL)']
    df = df[headers]
    df1= pd.DataFrame(df[df['Sensor Glucose (mg/dL)'].notna()]).iloc[::-1]
    df1['timestamp'] = df1.Date.str.cat(df1.Time,sep=" ").astype('datetime64[s]')
    df1['timestamp'] = pd.to_datetime(df1['timestamp'], format='%Y-%m-%d %I-%p' )
    df1['scount']=df1.groupby(by='Date')['Date'].transform('count')
    print(df1.shape)
    df2=df1.loc[df1.scount >=231 ]
    print(df2.shape)
    return df2
    

def calculateAutoModeTimeStamp(file):
    datain = pd.read_csv(file, low_memory=False)
    df = pd.DataFrame(datain[datain['Alarm'].notna()]).iloc[::-1]
    df['timestamp'] = df['Date'] + ' ' + df['Time']
    df['timestamp'] = df['timestamp'].astype('datetime64[ns]')
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %I-%p' )
    amts = df.loc[(df['Alarm'] =='AUTO MODE ACTIVE PLGM OFF')]
    return amts.timestamp.min()




def totalNumberOfDays(df):
    startDate = df.iloc[0]['timestamp']
    endDate = df.iloc[-1]['timestamp']
    tndf= df.loc[(df['timestamp'] >= startDate) & (df['timestamp'] <=endDate) ]
    noOfDays = len(pd.unique(tndf['Date'])) 
    return noOfDays



def metricsToBeExtracted(df):
    emdf = pd.DataFrame(df[['Date','Time','timestamp','Sensor Glucose (mg/dL)','scount']])
    emdf['hyperglycemia (CGM > 180 mg/dL)'] = np.where(emdf['Sensor Glucose (mg/dL)']>180, 1, np.nan)
    emdf['hyperglycemia critical (CGM > 250 mg/dL)'] = np.where(emdf['Sensor Glucose (mg/dL)']>250,  1, np.nan)
    emdf['range (CGM >= 70 mg/dL and CGM <= 180 mg/dL)'] = np.where(((emdf['Sensor Glucose (mg/dL)']>=70) & (emdf['Sensor Glucose (mg/dL)']<=180)),  1, np.nan)
    emdf['range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL)'] = np.where(((emdf['Sensor Glucose (mg/dL)']>=70) & (emdf['Sensor Glucose (mg/dL)']<=150)),  1, np.nan)
    emdf['hypoglycemia level 1 (CGM < 70 mg/dL)'] = np.where(emdf['Sensor Glucose (mg/dL)']<70,  1, np.nan)
    emdf['hypoglycemia level 2 (CGM < 54 mg/dL)'] = np.where(emdf['Sensor Glucose (mg/dL)']<54,  1, np.nan)
    return emdf


def evaluatePercentage(filteredDF, start, end, count, totalDays, mode, status):
    pindex=['Date','Time','timestamp','Sensor Glucose (mg/dL)', 'scount',
       'hyperglycemia (CGM > 180 mg/dL)',
       'hyperglycemia critical (CGM > 250 mg/dL)',
       'range (CGM >= 70 mg/dL and CGM <= 180 mg/dL)',
       'range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL)',
       'hypoglycemia level 1 (CGM < 70 mg/dL)',
       'hypoglycemia level 2 (CGM < 54 mg/dL)']
    df= filteredDF[filteredDF['timestamp'].dt.time.between(start.time(), end.time())]
    df1= df.resample('D', on='timestamp').count()
    df1[status + ' Percentage time in hyperglycemia (CGM > 180 mg/dL)'] = df1['hyperglycemia (CGM > 180 mg/dL)'].div(count)*100
    df1[status + ' percentage of time in hyperglycemia critical (CGM > 250 mg/dL)'] = df1['hyperglycemia critical (CGM > 250 mg/dL)'].div(count)*100
    df1[status + ' percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL)'] = df1['range (CGM >= 70 mg/dL and CGM <= 180 mg/dL)'].div(count)*100
    df1[status + ' percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL)'] = df1['range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL)'].div(count)*100
    df1[status + ' percentage time in hypoglycemia level 1 (CGM < 70 mg/dL)'] = df1['hypoglycemia level 1 (CGM < 70 mg/dL)'].div(count)*100
    df1[status + ' percentage time in hypoglycemia level 2 (CGM < 54 mg/dL)']  = df1['hypoglycemia level 2 (CGM < 54 mg/dL)'].div(count)*100
    df2=df1.drop(columns=pindex)
    df2=df2.reset_index()
    df2=df2.select_dtypes(pd.np.number).mean().rename(mode)
    result=pd.DataFrame(df2)
    return result.T


def writeDataToCSV(manualMode_overnight, manualMode_dayTime, manualMode_days,autoMode_overnight, autoMode_dayTime, autoMode_days):
    manualModeResult= manualMode_overnight.join(manualMode_dayTime).join(manualMode_days)
    manualModeResult.to_csv('Results.csv', mode='a', header=False, sep=',', index=False)
    autoModeResult= autoMode_overnight.join(autoMode_dayTime).join(autoMode_days)
    autoModeResult.to_csv('Results.csv', mode='a', header=False, sep=',', index=False)



readCGMDataFile = extractCGMDataFeature(CGMData);
filteredCGMData = clearCGMData(readCGMDataFile);

automodeStartTime      = calculateAutoModeTimeStamp(InsulinData);
automode_totalNoOfDays = totalNumberOfDays(filteredCGMData);

manualModeData = filteredCGMData.loc[(filteredCGMData['timestamp'] < automodeStartTime)]
autoModeData   = filteredCGMData.loc[(filteredCGMData['timestamp'] >= automodeStartTime)]
manualmode_totalNoOfDays = totalNumberOfDays(manualModeData);

manualModeMatrix = metricsToBeExtracted(manualModeData);
manualModeDays   = totalNumberOfDays(manualModeMatrix);

autoModeMatrix   = metricsToBeExtracted(autoModeData);
autoModeDays     = totalNumberOfDays(autoModeMatrix);

manualMode_overnight = evaluatePercentage(manualModeMatrix, overnightStartTime, overnightEndTime, 288, manualModeDays, 'Manual Mode','Overnight');
manualMode_dayTime   = evaluatePercentage(manualModeMatrix, dayStartTime, dayEndTime, 288, manualModeDays, 'Manual Mode','Daytime');
manualMode_days      = evaluatePercentage(manualModeMatrix, overnightStartTime, dayEndTime, 288, manualModeDays, 'Manual Mode','Whole Day');

autoMode_overnight   = evaluatePercentage(autoModeMatrix, overnightStartTime, overnightEndTime, 288, autoModeDays, 'Auto Mode', 'Overnight');
autoMode_dayTime     = evaluatePercentage(autoModeMatrix, dayStartTime, dayEndTime, 288, autoModeDays, 'Auto Mode', 'Daytime');
autoMode_days        = evaluatePercentage(autoModeMatrix, overnightStartTime, dayEndTime, 288, autoModeDays, 'Auto Mode','Whole Day');

writeDataToCSV(manualMode_overnight, manualMode_dayTime, manualMode_days,autoMode_overnight, autoMode_dayTime, autoMode_days);




