#Author: Hanlian Lyu, 2021-12-10
#This script serves for Batch deletion of files by pattern, iterating through all subfolders and files under dirPath.
#Package needs: pandas, openpyxl
import os
import pandas as pd
import fnmatch

##To Configure: Batchfiles' root path, and Filterfile must be excel.
dirPath=r"C:\DevTest"
dirFilterfile=r"C:\Temp\table_data.xlsx"
filterFile_sheet_name="FilterList"

def prepPattern(filterPath,excelsheet_name):
    try:
        df_ref = pd.read_excel(filterPath, sheet_name=excelsheet_name)
    except:
        print("File format should be excel, or sheet_name is not correct")
    ref_list=df_ref.iloc[:,0].tolist()
    return ref_list

def removeFilesByMatchingPattern(dirPath, pattern):
    #pattern: list
    #dirPath: str
    listOfFilesWithError = []
    for parentDir, dirnames, filenames in os.walk(dirPath):
        for filename in filenames:
            for patternelement in pattern:
                if patternelement in filename:
                    try:
                        os.remove(os.path.join(parentDir, filename))
                    except:
                        #print("Error while deleting file : ", os.path.join(parentDir, filename))
                        listOfFilesWithError.append(os.path.join(parentDir, filename))
        print("Currently proceeding on :", str(parentDir),"\n")
    return listOfFilesWithError

def removeFilesByMatchingPattern_naive(dirPath, pattern):
    #pattern: str, e.g. "TEST-*.xml"
    #dirPath: str
    listOfFilesWithError = []
    for parentDir, dirnames, filenames in os.walk(dirPath):
        for filename in fnmatch.filter(filenames,pattern):
            try:
                os.remove(os.path.join(parentDir, filename))
            except:
                #print("Error while deleting file : ", os.path.join(parentDir, filename))
                listOfFilesWithError.append(os.path.join(parentDir, filename))
        print("Currently proceeding on :", str(parentDir),"\n")
    return listOfFilesWithError

if __name__ == '__main__':
    print("Is dirFilter and excelfile existed :",str(os.path.exists(dirFilterfile)) )
    ref_list= prepPattern(dirFilterfile, filterFile_sheet_name)
    listOfErrors = removeFilesByMatchingPattern(dirPath, ref_list)
    if len(listOfErrors)>1:
        print('Files that can not be deleted : ')
        for filePath in listOfErrors:
            print(filePath)
    else:
        print("Batch deletion completed with no exception :) ")