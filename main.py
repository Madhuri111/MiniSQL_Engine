import sys
import re
from collections import OrderedDict
import csv
import sqlparse

filename="metadata.txt"
store_data=OrderedDict()
totaldata=OrderedDict()


def call_csv(table):
    table=table+'.csv'
    rows=[]
    try:
        file1=open(table,'r').readlines()
    except:
        print("File not found")

    for liness in file1:
        rows.append(liness.rstrip("\r\n"))

    return rows


def execute(command):
    


def extract_data():

    for table in totaldata:
        store_data[table]=OrderedDict()
        for vals in totaldata[table]:
            store_data[table][vals]=[]

    
    for table in totaldata:
        table_rows=[]
        table_rows=call_csv(table)
        for row in table_rows:
            row=row.split(',')
            i=len(row)
            for var in range(i):
                add_value=int(row[var].strip('""'))
                mine=totaldata[table][var]
                store_data[table][mine].append(add_value)
                


def main():
    try:
        with open("metadata.txt", "r") as f:
            contents = f.read().splitlines()
        print(contents)
        
        tablename=""  #data in column
        attribute=[]
        createtable=False  #if new table
        for lines in contents:
            if(lines=="<begin_table>"):
                tablename=''
                createtable=True
            elif (createtable==True):
                createtable=False
                tablename=lines
                #also , empty the attribute for next table vlaues
                attribute=[]
            elif(lines=="<end_table>"):
                totaldata[tablename]=attribute
            else:
                attribute.append(lines)

        print(totaldata)
    except:
        print("Metadata.txt file not found")


    
    extract_data()
        
    #print(store_data)

    count=len(sys.argv)
    flag=0
    if(count<=1):
        print("please enter command in command line")
    if(count>=2):
        com=sys.argv[1]
        command=com[:-1].strip()
        command=command.lower()
        semicolon=com[-1]
        s1="select"
        s2="from"
        if(semicolon!=';'):
            print("Please enter correct command , Semicolon is missing")
        if(re.search(s1,command) and re.search(s2,command)):  #checking if select,from is there in command
            flag=1
        elif flag==0:
            print("Please enter valid command")
        elif re.match(r'^(?i)(select\ ).+(?i)(\ from\ ).+[;]$', line):
            print("You have an error in your SQL syntax")
        else:
            execute(com)




if __name__ == '__main__':
    main()



   
