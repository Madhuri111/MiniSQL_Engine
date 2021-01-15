import sys
import re
import csv
import sqlparse

filename="metadata.txt"

totaldata={}

def execute(command):


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



    count=len(sys.argv)
    #    print(sys.argv[1])
    flag=0
    #    print(sys.argv[1][-1])
    if(count <=1 ):
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
        else:
            print("Please enter valid command")
        execute(command)




if __name__ == '__main__':
    main()



   
"""
    for tname in totaldata:
        with open(tname+'.csv','r') as csvfile:
            csvreader=csv.reader(csvfile)

            for record in csvreader:
                ind=0
                for att in totaldata[tname]:
                    totaldata[tname][att].append(record(ind))
                    ind+=1
"""

