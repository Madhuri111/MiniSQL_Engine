# MiniSQL_Engine

Supposed to develop a mini sql engine which will run a subset of SQL queries using command line interface
Language used : Python

table1.csv and table2.csv contains data 

Implemented Queries like :-
  1)Select col1, col2 from table_name;    <!-- //Projecting Columns -->
  2)Select max(col1) from table_name;     <!--  //Aggregate Functions -->
  3)Select distinct col1, col2 from table_name;  <!--  //Distinct -->
  4)Select col1,col2 from table1,table2 where col1 = 10 AND col2 = 20; <!--  //Where -->
  5)Select col1, COUNT(col2) from table_name group by col1. <!--  //GROUP BY -->
  6)Select col1,col2 from table_name order by col1 ASC|DESC.  <!--  //ORDER BY -->
