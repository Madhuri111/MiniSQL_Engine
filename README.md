# MiniSQL_Engine

Supposed to develop a mini sql engine which will run a subset of SQL queries using command line interface
Language used : Python

table1.csv and table2.csv contains data 



Dataset:
        CSV files with data (all integers and unique columns)
        "Metadata.txt" file which represents structure for each table

Queries:
        Project =>
                1)select * from table1;
                2)select col1,col2 from table2;
        Aggregate Functions =>
                1)select max(col1) from table1;
                likewise for sum,average,min,count,
        Distinct =>
                1) select distinct col1,col2 from table1;
        Where =>
                1)Select col1,col2 from table1,table2 where col1 = 10 AND col2 = 20;
                Likewise operators include "< , >, <=, >=, =".
        Group By =>
                 Select col1, COUNT(col2) from table_name group by col1
                 Also,In the group by queries, Sum/Average/Max/Min/Count can be used as
aggregate functions.
        Order By =>
                Select col1,col2 from table_name order by col1 ASC|DESC.
                Also,queries can have multiple columns in it

Input file format:-
        roll_number.sh "SQL Query"
Output format:-
        <Table1.column1,Table1.column2,... TableN.columnM>
                Row1
                Row2
                .......
                RowN
        
