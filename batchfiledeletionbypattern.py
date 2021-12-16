#Author: Hanlian Lyu, 2021-12-10
#This script serves for Batch deletion of files by pattern, iterating through all subfolders and files under dirPath.
#Package needs: pandas, openpyxl
import os
import pandas as pd
import fnmatch
import openpyxl

##To Configure: Batchfiles' root path, and Filterfile must be excel.
#dirPath = r"\\nasweucvot2001p.got.volvocars.net\C_9413_APP_NASsympathy01\data_srec_secret"
dirPath=r"C:\DevTest"
dirFilterfile = r"\\nasweucvot2001p.got.volvocars.net\C_9413_APP_NASsympathy01\temp\table_data.xlsx"
filterExcel_sheet_name = "CHINA CarID"

def prepLookup(filterPath,excelsheet_name="Sheet1"):
    try:
        df_ref = pd.read_excel(filterPath, sheet_name=excelsheet_name)
    except:
        print("File format should be excel, or sheet_name is not correct")
    ref_list=df_ref.iloc[:,0].tolist()
    return ref_list

def removeFilesbyMatchLookup(dirPath, lookuplist):
    for parentDir, dirnames, filenames in os.walk(dirPath):
        print("Current Dir is: ", str(parentDir))
        [[matchFilenamebyLookup(lookupelement, filename, parentDir) for lookupelement in lookuplist] for filename in filenames]

def matchFilenamebyLookup(lookupelement, filename, path):
    if lookupelement in filename:
        os.remove(os.path.join(path,filename))
        

def removeFilesbyPattern(dirPath, pattern):
    #pattern: str, e.g. "TEST-*.xml" etc.
        # '*' matches everything; '?' matches any single character,
        # '[seq]' matches any character in seq; '[!seq]' matches any character not in seq.
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
    print("Is dirFilter and file existed :",str(os.path.exists(dirFilterfile)) )
    ref_list= prepLookup(dirFilterfile, excelsheet_name=filterExcel_sheet_name)
    removeFilesbyMatchLookup(dirPath, ref_list)
    print("Batch deletion completed :)") 


    #ref_pattern = "Test_*.sydata"
    #listOfErrors = removeFilesbyPattern(dirPath, ref_pattern)