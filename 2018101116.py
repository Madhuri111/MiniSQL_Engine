#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import re
from collections import OrderedDict
import csv
import sqlparse
import operator


# In[2]:


filename="metadata.txt"
store_data={}
totaldata={}
columndata={}
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
def table(tab):
    for i in range(len(tab)):
        try:
            store_data[tab[i]]
        except :
            print('table not found')
            sys.exit()
    tabs=[tab[i] for i in range(len(tab)) if tab[i] not in tab[:i]]
    if(len(tabs)!=len(tab)):
        print("Please enter correct command , tables are not unique")
        sys.exit()
    if(len(tabs)==0):
        print("Please enter correct command , tables are missing")
        sys.exit()
    arr1=[store_data[tab[0]][totaldata[tab[0]][i]] for i in range(len(totaldata[tab[0]]))]
    arr=[[row[i] for row in arr1] for i in range(len(arr1[0]))]
    #print(arr)
    for i in range(1,len(tab)):
        fin=[]
        arr1=[store_data[tab[i]][totaldata[tab[i]][ii]] for ii in range(len(totaldata[tab[i]]))]
        temp=[[row[i] for row in arr1] for i in range(len(arr1[0]))]
        #print(temp)
        for ii in range(len(arr)):
            for jj in range(len(temp)):
                temps=[0 for me in range(len(arr[0])+len(temp[0]))]
                for kk in range(len(arr[0])):
                    temps[kk]=arr[ii][kk]
                for kk in range(len(temp[0])):
                    temps[kk+len(arr[0])]=temp[jj][kk]
                fin.append(temps)
        arr=fin.copy()
    return arr
def columns(arr):
    #print(arr)
    tem=[]
    for i in arr:
        tem.extend(totaldata[i])
    return tem
with open("metadata.txt", "r") as f:
    contents = f.read().splitlines()
        #print(contents)

    tablename=""  #data in column
    attribute=[]
    createtable=False  #if new table
    for line in contents:
        lines=line.lower()
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
            columndata[lines]=tablename
#print(totaldata)
#print(columndata)
def extract_data():

    for table in totaldata:
        store_data[table]={}
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
extract_data()
#    print("Metadata.txt file not found")


# In[3]:


def int_me(arr,a,cols):
    try :
        int(a)
        return int(a)
    except :
        for i in range(len(cols)):
            if(cols[i]==a):
                return arr[i]
        print('column not exist')
        sys.exit()
def me(st1,op,st2,arr,colss):
    if(op=='='):
        if(operator.eq(int_me(arr,st1,colss),int_me(arr,st2,colss))):
            return True
    if(op=='<='):
        if(operator.le(int_me(arr,st1,colss),int_me(arr,st2,colss))):
            return True
    if(op=='>='):
        if(operator.ge(int_me(arr,st1,colss),int_me(arr,st2,colss))):
            return True
    if(op=='>'):
        if(operator.gt(int_me(arr,st1,colss),int_me(arr,st2,colss))):
            return True
    if(op=='<'):
        if(operator.lt(int_me(arr,st1,colss),int_me(arr,st2,colss))):
            return True
def where(arr,colss,com):
    if('where' not in com):
        return [arr,colss],com
    com.pop(0)
    l=[]
    #print('in where',com)
    if('and' in com):
        st11=com[0]
        com.pop(0)
        op1=com[0]
        com.pop(0)
        st12=com[0]
        com.pop(0)
        com.pop(0)
        st21=com[0]
        com.pop(0)
        op2=com[0]
        com.pop(0)
        st22=com[0]
        com.pop(0)
        for i in range(len(arr)):
            if(me(st11,op1,st12,arr[i],colss) and me(st21,op2,st22,arr[i],colss)):
                l.append(arr[i])
    elif('or' in com):
        st11=com[0]
        com.pop(0)
        op1=com[0]
        com.pop(0)
        st12=com[0]
        com.pop(0)
        com.pop(0)
        st21=com[0]
        com.pop(0)
        op2=com[0]
        com.pop(0)
        st22=com[0]
        com.pop(0)
        for i in range(len(arr)):
            if(me(st11,op1,st12,arr[i],colss) or me(st21,op2,st22,arr[i],colss)):
                l.append(arr[i])
    else:
        st11=com[0]
        com.pop(0)
        op1=com[0]
        com.pop(0)
        st12=com[0]
        com.pop(0)
        for i in range(len(arr)):
            if(me(st11,op1,st12,arr[i],colss) or me(st11,op1,st12,arr[i],colss)):
                l.append(arr[i])
    return [l,colss],com


# In[4]:


def func(a,b):
    #print(a,b)
    if(b.lower()=='min'):
        return min(a)
    elif(b.lower()=='max'):
        return max(a)
    elif(b.lower()=='sum'):
        return sum(a)
    elif(b.lower()=='count'):
        return len(a)
    elif(b.lower()=='avg'):
        return sum(a)/len(a)
def group_lilly(arr,colss,com,cols):
    if('group' not in com):
        return [arr,colss],com,False
    if(com[0]!='group'):
        print('something gone wrong --> something is in between group and where')
        sys.exit()
    com.pop(0)
    if(len(com)==0 or com[0]!='by'):
        print('not found group by')
        sys.exit()
    com.pop(0)
    nn=len(cols)
    flag_here=0
    temp_here=[]
    for i in range(len(com)):
        if(com[0]=='order'):
            break
        temp_here.extend(com[0].split(','))
        com.pop(0)    
    temp_here=[x for x in temp_here if x]
    temp_here.reverse()
    #print(temp_here)
    for i in range(len(cols)):
        if('(' not in cols[i] and cols[i] not in temp_here):
            print(cols[i],temp_here)
            print('not all columns are grouped correctly')
            sys.exit()
    cols.extend(temp_here)
    lilly=0
    cols22=cols.copy()
    #print('-hi',cols22)
    tab1=[[row[i] for row in arr] for i in range(len(arr[0]))]
    tab2=[]
    lil_cols=[]
    cols2=[]
    for i in range(len(cols)):
        if('(' not in cols[i]):
            cols2.append(cols[i])
            flag=0
            for j in range(len(colss)):
                if(colss[j]==cols[i]):
                    flag=1
                    tab2.append(tab1[j])
                    lil_cols.append(cols[i])
            if(flag==0):
                print(cols[i])
                print('column not found for grouping')
                sys.exit()
    n=len(tab2)
    #print(cols)
    for i in range(len(cols)):
        if('(' in cols[i]):
            cols2.append(cols[i])
            for j in range(len(cols[i])):
                if(cols[i][j]=='('):
                    temp=cols[i][j+1:-1]
                    lil_cols.append(cols[i][:j])
                    cols[i]=temp
                    break
            for j in range(len(colss)):
                if(colss[j]==temp):
                    flag=1
                    tab2.append(tab1[j])
            if(flag==0):
                print('column not found for grouping')
                sys.exit()
    #print('temp-verify',tab2,colss,cols,n)
    arr=[[row[i] for row in tab2] for i in range(len(tab2[0]))]
    #print(arr)
    for j in range(n,len(cols)):
        arr=sorted(arr,key=lambda x:x[j])
    final=[]
    #print(cols)
    #print(len(arr[0]))
    while(len(arr)!=0):
        temp=arr[0]
        me_here=[]
        mohit=[0 for i in range(len(cols))]
        mohit[:n]=arr[0][:n]
        l=[[]for i in range(len(cols))]
        for i in range(len(arr)):
            if(temp[:n]==arr[i][:n]):
                for j in range(n,len(cols)):
                    l[j].append(arr[i][j])
                me_here.append(arr[i])
        for i in range(len(me_here)):
            for j in range(len(arr)):
                if(me_here[i]==arr[j]):
                    arr.pop(j)
                    break
        for i in range(n,len(cols)):
            mohit[i]=func(l[i],lil_cols[i])
        final.append(mohit)
    for i in range(n,len(cols)):
        temperory=''
        for j in range(len(cols2[i])):
            if(cols2[i][j]=='('):
                temperory=cols2[i][j+1:-1]
        lil_cols[i]=lil_cols[i]+'('+temperory+')'
    #print(cols2)
    #print(final)
    arr=[[row[i] for row in final] for i in range(len(final[0]))]
    final=[]
    #print(nn)
    #print('hi',lil_cols,cols22)
    for i in range(len(cols22[:nn])):
        for j in range(len(lil_cols)):
            if(lil_cols[j]==cols22[i]):
                final.append(arr[j])
                break
    arr=[[row[i] for row in final] for i in range(len(final[0]))]
    #print(arr)
    return [arr,cols22[:nn]],com,True


# In[5]:


def order(arr,cols,com):
    if('order' not in com):
        return [arr,cols],com
    if(com[0]!='order'):
        print('something is wrong not found order by next to group by')
        sys.exit()
    com.pop(0)
    if(com[0]!='by'):
        print('not found order by')
        sys.exit()
    com.pop(0)
    oder=1
    req=[]
    for i in range(len(com)):
        req.extend(com[0].split(','))
        com.pop(0)
    req=[x for x in req if x]
    req.reverse()
    #print(req)
    for j in range(len(req)):
        tempoo=0
        if(req[j]=='desc'):
            oder=-1
            continue
        if(req[j]=='asc'):
            oder=1
            continue
        for i in range(len(cols)):
            if(cols[i]==req[j]):
                arr.sort(key=lambda x:oder*x[i])
                tempoo=1
                break
        oder=1
        if(tempoo==0):
            print('column not found for ordering')
            sys.exit()
    #arr=sorted(arr,key = lambda x : oder*x[req])
    return [arr,cols],com


# In[6]:


def aggregates(req,arrs,cols,flag_group):
    if(flag_group==True):
        #print('hi')
        return [arrs,cols]
    arr=[[row[i] for row in arrs] for i in range(len(arrs[0]))]
    temp=0
    here=[]
    for i in range(len(req)):
        cl=req[i]
        s1=re.match('^(sum)\(.*\)', cl)
        ma1=re.match('^(max)\(.*\)', cl)
        mi1=re.match('^(min)\(.*\)', cl)
        a1=re.match('^(avg)\(.*\)', cl)
        b1=re.match('^(count)\(.*\)', cl)
        if s1:
            sum_flag=True
            cl=cl.replace('sum','')
            cl=cl.strip()
            cl=cl.rstrip("()")
            cl=cl.lstrip("()")
            for j in range(len(cols)):
                if(cols[j]==cl):
                    here.append(func(arr[j],'sum'))
        elif ma1:
            max_flag=True
            cl=cl.replace('max','')
            cl=cl.strip()
            cl=cl.rstrip("()")
            cl=cl.lstrip("()")
            for j in range(len(cols)):
                if(cols[j]==cl):
                    here.append(func(arr[j],'max'))
        elif mi1:
            min_flag=True
            cl=cl.replace('min','')
            cl=cl.strip()
            cl=cl.rstrip("()")
            cl=cl.lstrip("()")
            for j in range(len(cols)):
                if(cols[j]==cl):
                    here.append(func(arr[j],'min'))
        elif a1:
            avg_flag=True
            cl=cl.replace('avg','')
            cl=cl.strip()
            cl=cl.rstrip("()")
            cl=cl.lstrip("()")
            for j in range(len(cols)):
                if(cols[j]==cl):
                    here.append(func(arr[j],'avg'))
        elif b1:
            count_flag=True
            cl=cl.replace('count','')
            cl=cl.strip()
            cl=cl.rstrip("()")
            cl=cl.lstrip("()")
            for j in range(len(cols)):
                if(cols[j]==cl):
                    #print('hello')
                    #print(func(arr[j],'count'))
                    here.append(func(arr[j],'count'))
        else :
            #print('hello2')
            for j in range(len(cols)):
                if(cols[j]==cl):
                    temp=temp+1 
                    here.append(arr[j])
    if(temp==len(req)):
        arr=[[row[i] for row in here] for i in range(len(here[0]))]
    else :
        arr=[here]
    if(temp!=len(req) and temp!=0):
        print('group by not found and aggregates + columns found error or some column is missing error')
        sys.exit()
    return [arr,req]


# In[7]:


def select(arr,colss,req):
    #print('aryya=',arr)
    arrs=[[row[i] for row in arr] for i in range(len(arr[0]))]
    arr=arrs.copy()
    tab=[]
    #print(arr,colss,req)
    for i in req :
        here=0
        for j in range(len(colss)) :
            if(i==colss[j]):
                here=1
                tab.append(arr[j])
                break
        if(here==0):
            print(i,'--column not present')
            sys.exit()
    arrs=[[row[i] for row in tab] for i in range(len(tab[0]))]
    return [arrs,req]


# In[8]:


def print_me(arr,comm):
    brr=arr[1].copy()
    for i in range(len(brr)):
        cl=brr[i]
        s1=re.match('^(sum)\(.*\)', cl)
        ma1=re.match('^(max)\(.*\)', cl)
        mi1=re.match('^(min)\(.*\)', cl)
        a1=re.match('^(avg)\(.*\)', cl)
        b1=re.match('^(count)\(.*\)', cl)
        if s1:
            sum_flag=True
            cl=cl.replace('sum','')
            cl=cl.strip()
            cl=cl.rstrip("()")
            cl=cl.lstrip("()")
        elif ma1:
            max_flag=True
            cl=cl.replace('max','')
            cl=cl.strip()
            cl=cl.rstrip("()")
            cl=cl.lstrip("()")
        elif mi1:
            min_flag=True
            cl=cl.replace('min','')
            cl=cl.strip()
            cl=cl.rstrip("()")
            cl=cl.lstrip("()")
        elif a1:
            avg_flag=True
            cl=cl.replace('avg','')
            cl=cl.strip()
            cl=cl.rstrip("()")
            cl=cl.lstrip("()")
        elif b1:
            count_flag=True
            cl=cl.replace('count','')
            cl=cl.strip()
            cl=cl.rstrip("()")
            cl=cl.lstrip("()")
        brr[i]=cl
    if(comm):
        print('command not properly executed')
        sys.exit()
    for i in range(len(brr)):
        try :
            columndata[brr[i]]
        except:
            print('not all columns found in data')
            sys.exit()
    print(columndata[brr[0]],'.',arr[1][0],sep='',end='')
    if(len(arr[0])==0 or len(arr[0][0])==0):
        print('\n','empty table')
        sys.exit()
    for i in range(1,len(arr[1])):
        print(',',columndata[brr[i]],'.',arr[1][i],sep='',end='')
    print()
    for i in range(len(arr[0])):
        print(arr[0][i][0],end='',sep='')
        for j in range(1,len(arr[0][i])):
            print(',',arr[0][i][j],sep='',end='')
        print()
    return True


# In[9]:


#print((store_data))
def main():
    flag=0
    flag_group=False
    flag_distinct=0
#reoved the count if case count<=1 something 
    com=sys.argv[1]
#com=com[1:-1]
    com=com.lower()
    command=com.lower()
    command=command.strip()
    if(command==''):
        print("command missing")
        sys.exit()
    semicolon=com[-1]
    com=com[:-1]
    com=com.split()
    #print(com)
    #command=command.lower()
    s1="select"
    s2="from"
    if(semicolon!=';'):
        print("Please enter correct command , Semicolon is missing")
        sys.exit()
    if(re.search(s1,command) and re.search(s2,command)):  #checking if select,from is there in command
        flag=1
    if flag==0:
        print("Please enter valid command")
        sys.exit()
    elif flag==1:
        if(com[0].lower()=='select'):
            com.pop(0)
        else :
            print('select is not 1st word')
            sys.exit()
#print(com)

    cols=[]
    flag=0
    for i in range(len(com)):
        if(com[0]=='from'):
            flag=1
            com.pop(0)
            break
        cols.extend(com[0].split(','))
        com.pop(0)
    cols=[x for x in cols if x]
    if(len(cols)==0):
        print("Please enter correct command , co columns present")
        sys.exit()
#print(cols)
    if(cols[0]=='distinct'):
        flag_distinct=1
        cols.pop(0)
    cond=['where','group','order']
    tabs=[]
    for i in range(len(com)):
        if(com[0] in cond):
            break
        tabs.extend(com[0].split(','))
        com.pop(0)
    tabs=[x for x in tabs if x]
#print('tabs=',tabs)
    finale=[table(tabs.copy()),columns(tabs.copy())]
#print('lilly--',finale,len(finale[0]))
    if(cols[0]=='*'):
    #print(cols)
        temp=cols[1:]
        cols=finale[1].copy()
        cols.extend(temp)
#print('-',cols,'-')
    finale,com=where(finale[0],finale[1],com)
    if(len(finale[0])==0):
        print_me(finale,'')
    finale,com,flag_group=group_lilly(finale[0],finale[1],com,cols.copy())
#print(finale)
    finale,com=order(finale[0],finale[1],com)
#print(finale)
    finale=aggregates(cols,finale[0],finale[1],flag_group)
#print('for select',finale)
#finale=select(finale[0],finale[1],cols)
    if(flag_distinct==1):
        finale[0]=[ele for ind, ele in enumerate(finale[0]) if ele not in finale[0][:ind]]
#print(finale)
    print_me(finale,com)
#print(len(finale[0]))
    #print(cols)
#print(finale,cols)


# In[10]:


#print(store_data['table4'])
if __name__ == '__main__':
    main()

