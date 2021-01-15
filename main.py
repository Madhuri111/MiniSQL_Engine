import sys
import csv
import sqlparse

filename="metadata.txt"

totaldata={}





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
    
    for tname in totaldata:
        with open(tname+'.csv','r') as csvfile:
            csvreader=csv.reader(csvfile)

            for record in csvreader:
                ind=0
                for att in totaldata[tname]:
                    totaldata[tname][att].append(record(ind))
                    ind+=1




    print(totaldata)

    count=len(sys.argv)
    #    print(sys.argv[1])
    #    print(sys.argv[1][-1])
    if(count <=1 ):
        print("please enter command in command line")
    if(count>=2):
        command=sys.argv[1]
        semicolon=command[-1]
        if(semicolon!=';'):
            print("Please enter correct command , Semicolon is missing")
    #        else:
    #           read_data(filename)



   # myq=sqlparse.parse(com[:1])[0].tokens


if __name__ == '__main__':
    main()
