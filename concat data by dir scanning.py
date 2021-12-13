import os
import pandas as pd
import openpyxl

#Configure the dirPath for file scanning, and configure the exportfile_name by needs.
#If it is for merging excels, configure excelsheet_name.
#Exported format is stored by default as pickle, you can specify to '.xlsx' or '.csv'.
dirPath= r"C:\DevTest"
exportfile_name = r"batch data"   
exportformat=".pickle"
excelsheet_name = "Sheet1"
#----------------------------------------------------------------

def mergeExcelBatchFiles(dirPath, sheetname, rowheader=0,columnrange=None):
    df_list=[]
    for parentDir, dirnames, filenames in os.walk(dirPath,sheetname):
        print("\nCurrent importing dir: ", str(parentDir),)
        for filename in filenames:
            ext = os.path.splitext(filename)[-1].lower()
            if ext in ('.xlsx','.xlsm','.xls'):
                try:
                    df=pd.read_excel(os.path.join(parentDir,filename),sheet_name=sheetname,header=rowheader,usecols=columnrange)
                    df_list.append(df)
                except:
                    print("Excel import failed: ", os.path.join(parentDir,filename))               
    return pd.concat(df_list)

def mergeCsvBatchFiles(dirPath, rowheader=0, columnrange=None, seperator=';'):
    df_list=[]
    for parentDir, dirnames, filenames in os.walk(dirPath):
        print("\nCurrent importing dir: ", str(parentDir),)
        for filename in filenames:
            ext = os.path.splitext(filename)[-1].lower()
            if ext == '.csv':
                try:
                    df=pd.read_csv(os.path.join(parentDir,filename),header=rowheader,usecols=columnrange,sep=seperator)
                    df_list.append(df)
                except:
                    print("Csv import failed: ", os.path.join(parentDir,filename))               
    return pd.concat(df_list)

def exportmergedFiles(pd_batch, dirPath, exportmode='.pickle',filename=r"batch data"):
    if exportmode == '.csv':
        pd_batch.to_csv(os.path.join(dirPath,filename)+exportmode)
    elif exportmode == '.xlsx':
        pd_batch.to_excel(os.path.join(dirPath,filename)+exportmode, sheetname='Sheet1')
    else:
        pd_batch.to_pickle(os.path.join(dirPath,filename)+'.pickle')
    print("\nExport Completed To: ", os.path.join(dirPath,filename)+exportmode)
            

if __name__=="__main__":

    df_batchexcel=mergeExcelBatchFiles(dirPath, excelsheet_name, rowheader=0)
    df_batchcsv=mergeCsvBatchFiles(dirPath, rowheader=0)
    
    exportmergedFiles(df_batchexcel, dirPath, filename=exportfile_name, exportmode=exportformat)
    exportmergedFiles(df_batchcsv, dirPath, filename=r"batch data from csv")
    
    #Test-review
    df_review=pd.read_pickle(os.path.join(dirPath,"batch data from csv")+ exportformat )
    print(df_review.head( round(len(df_review)*0.2) ))

