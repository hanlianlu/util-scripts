import os
import pandas as pd
import openpyxl

#Configure the dirPath and corresponding excel sheets.
dirPath= r"C:\DevTest"
filesheet_name = "Sheet1"

def mergeExcelBatchFiles(dirPath, excelsheet_name, rowheader=0,columnrange=None):
    df_list=[]
    for parentDir, dirnames, filenames in os.walk(dirPath,excelsheet_name):
        print("\nCurrent importing dir: ", str(parentDir),)
        for filename in filenames:
            ext = os.path.splitext(filename)[-1].lower()
            if ext in ('.xlsx','.xlsm','.xls'):
                try:
                    df=pd.read_excel(os.path.join(parentDir,filename),sheet_name=excelsheet_name,header=rowheader,usecols=columnrange)
                    df_list.append(df)
                except:
                    print("Excel import failed: ", os.path.join(parentDir,filename))               
    return pd.concat(df_list)

def exportmergedFiles(pd_batch, dirPath, filename=r"batch data.csv"):
    pd_batch.to_csv(os.path.join(dirPath,filename))
    print("\nExport Completed To: ", os.path.join(dirPath,filename))
            
if __name__=="__main__":

    df_batch=mergeExcelBatchFiles(dirPath, filesheet_name, rowheader=2)
    exportmergedFiles(df_batch,dirPath)

