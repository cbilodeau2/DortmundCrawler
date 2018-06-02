# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 20:46:08 2018

@author: Gaurav
"""

#WebCrawler for Dortmund Data Bank

import requests
from bs4 import BeautifulSoup
import scipy as sci
import win32com.client
import os
import sys

#This Function gets the constant value of Temperature or Pressure from above
#the table
def GetConstantValue(useful_header):
    useful_value=useful_header.find_previous("table")
    col=useful_value.find_all("td")
    constvalue=col[0].get_text()
    constvalue=float(constvalue)
    return constvalue

#This function captures the useful headers in the webpage that point to 
#Data Tables
def GetUsefulHeaders(soup):
    headers=soup.find_all("h4")
    useful_headers=[]
    for header in headers:
        text=header.get_text()
        if(text=="Data Table"):
            useful_headers.append(header)
    return useful_headers

#This function captures useful tables from the useful headers and stores the 
#tables as numpy arrays which are themselves stored in a list

def GetUsefulTables(useful_headers):
    number_of_tables=len(useful_headers)
    list_of_arrays=[]
    constvalues=sci.zeros(number_of_tables)
    stats=sci.zeros(number_of_tables)
    for i in range(number_of_tables):
        useful_header=useful_headers[i]
        useful_table=useful_header.find_next("table")
        rows=useful_table.find_all("tr")
        number_of_cols=len(rows[-1].find_all("td"))
        if(number_of_cols<3):
            continue
        constvalues[i]=GetConstantValue(useful_header)
        stats[i]=GetTableStat(useful_header)
        arr=sci.zeros((len(rows),3))
        
        row_counter=0
        for row in rows:
            cols=row.find_all("td")
            for cell in range(len(cols)):
                arr[row_counter,cell]=cols[cell].get_text()
            row_counter+=1
        
        arr=sci.delete(arr,(0),axis=0)
        if(arr[0,1]==0.):
            arr=sci.delete(arr,(0),axis=0)
        if(arr[-1,1]==1.):
            arr=sci.delete(arr,(-1),axis=0)
        list_of_arrays.append(arr)
    
    final_constvalues=constvalues[constvalues!=0]
    final_stats=stats[constvalues!=0]
    return [list_of_arrays,final_constvalues,final_stats]
  

#This function is used to print the VLEData to an Excel file (which is created)
#using the win32com library
def PrintToExcel(list_of_tables,compound1,compound2,switch):
    app=win32com.client.Dispatch("Excel.Application")
    app.Visible=False
    wb=app.Workbooks.Add()
    cwdir=os.getcwd()
    filename=f"{compound1}-{compound2}_VLEData.xlsx"
    path=cwdir+"\\"+filename
    wb.SaveAs(path)
    sh=wb.Sheets("Sheet1")
    
    offset=0
    for table in list_of_tables:
        one_table=table
        [rows,cols]=one_table.shape
        one_table=one_table.tolist()
        for i in range(rows):
            for j in range(cols):
                sh.Cells(i+1+offset,j+1).Value=one_table[i][j]
                if(switch==0):
                    sh.Cells(i+1+offset,1).Interior.ColorIndex=19
                if(switch==1):
                    sh.Cells(i+1+offset,1).Interior.ColorIndex=20
        offset+=rows+1    
    
    wb.Save()
    wb.Close()
    app.Quit()

#This function returns 0 if the table is PXY, else it returns 1 for TXY
def GetTableStat(useful_header):
    useful_value=useful_header.find_previous("table")
    col=useful_value.find_all("td")
    check=col[1].get_text()
    if(check=="K"):
        return 0
    else:
        return 1
    
#The main function that accepts compound names, calls all the relevant functions
#and returns/prints the final tables
def Crawl(compound1,compound2):
    comp1=f"{compound1}"
    comp2=f"{compound2}"
    page=requests.get(f"http://www.ddbst.com/en/EED/VLE/VLE%20{comp1}%3B{comp2}.php")
    if(page.status_code==200):
        switch=0
    else:
        switch=1
        page=requests.get(f"http://www.ddbst.com/en/EED/VLE/VLE%20{comp2}%3B{comp1}.php")
    soup=BeautifulSoup(page.text,"html.parser")

    useful_headers=GetUsefulHeaders(soup)
    [tables,constantvalues,stats]=GetUsefulTables(useful_headers)
    
    PrintToExcel(tables,comp1,comp2,switch)
    return [tables,constantvalues,stats,switch]


if __name__=="__main__":
    if(len(sys.argv)==3):
        compound1=f"{sys.argv[1]}"
        compound2=f"{sys.argv[2]}"
    if(len(sys.argv)==4):
        compound1=f"{sys.argv[1]} {sys.argv[2]}"
        compound2=f"{sys.argv[3]}"
    if(len(sys.argv)==5):
        compound1=f"{sys.argv[1]} {sys.argv[2]}"
        compound2=f"{sys.argv[3]} {sys.argv[4]}"
        
    Crawl(f"{compound1}",f"{compound2}")