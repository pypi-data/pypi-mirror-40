cy_Oracle
=========

cy_Oracle is a simple Python module that improves the handling of
Oracle object types compared to cx_Oracle.
cy_Oracle supports a central declaration of a mapping between
Python classes and Oracle object types. This mapping can be
used in DML (SELECT, UPDATE, INSERT) as well as with PL/SQL
functions and procedures. Details are described in the online help
for the function "addTypemap".

>>> import cy_Oracle
>>> help(cy_Oracle.OracleDB.addTypemap)

The entry point for the client is the class cy_Oracle.OracleDB.
Here you define the connection parameter to the Oracle database
(User, Password, URL). 

>>> import cy_Oracle
>>> help(cy_Oracle.OracleDB) for details.

The class cy_Oracle.Connection derives from cx_Oracle.Connection.
It does not add any new methods, but override the method "cursor()".
Here we return an object of the class cy_Oracle.Cursor. 

>>> import cy_Oracle
>>> help(cy_Oracle.Connection.cursor) for details.

The class cy_Oracle.Cursor derives from cx_Oracle.Cursor.
Here we setup the input and output handlers to map between
Oracle object types and Python classes. 

>>> import cy_Oracle
>>> help(cy_Oracle.Cursor) for details.

Example 1
---------

This 'Hello World' example for the module cy_Oracle will 
list the names and the creation date of objects in the 
database schema "book"::

  1    from cy_Oracle import OracleDB
  2    # setup the DB connection
  3    myDB = OracleDB(user='book', password='book', databaseURL='bookdb')
  4    # connect to DB
  5    con = myDB.connect()
  6    # select some data from the view 'USER_OBJECTS'
  7    cur = con.cursor()
  8    cur.execute('SELECT object_name, created from user_objects')
  9    # loop the result
  10   for row in cur:
  11           print ('%s --> %s' % (row.object_name, row.created))
  12   # close down
  13   cur.close()	
  14   con.close()

In this example, cy_Oracle works just as cx_Oracle - the only difference
is line 11. Here, cy_Oracle gives you an object with names of the selected
columns as attributes whereas in cx_Oracle you will just get a collection.

The example needs a TNS-entry (here: bookdb) to locate the host of the 
database server. As an alternative, it is possible to include the host,
the port an the service name into the connection::

  3    myDB = OracleDB(databaseURL='user/password@dbhost:dbport/servicename')


Example 2
---------

Oracle object types are mostly used in complex database application
that are build from a mixture of SQL and PL/SQL. So, this "simple" 
example using object types is one that is not very useful. It will
list all columns of all tables an views in the database schema "book"::

  1   from cy_Oracle import OracleDB
  2   from cy_Oracle import Attribute
  3
  4   # class to receive the result - one object of type T_COL_INFO.
  5   class ColInfo(object):
  6           def __init__(self):
  7                   self.name=None
  8                   self.oracleDataType=None
  9                   self.oracleDataLenght=None
  10         
  11         def __str__(self):
  12                 return 'name=%s type=%s(%d)' % \
  13                         (self.name,self.oracleDataType,self.oracleDataLenght)
  14
  15  myDB = OracleDB(user='book', password='book', databaseURL='orcl')
  16  con = myDB.connect()
  17  cur = con.cursor()
  18  # Create a new object type in the database
  19  cur.execute(""" create or replace type T_COL_INFO as object(
  20                   NAME	      varchar2(85 char)
  21                  ,DATA_TYPE      varchar2(106 char)
  22                  ,DATA_LENGTH    number
  23                  ,COMMENTS       varchar2(4000 char))
  24              """)
  25  # create a view containing objects of the type T_COL_INFO
  26  cur.execute(""" create or replace view V_COL_INFO as
  27                    select 
  28                       c.TABLE_NAME as TABLE_NAME  
  29                      ,T_COL_INFO(c.COLUMN_NAME,c.DATA_TYPE,c.DATA_LENGTH,m.COMMENTS) 
  30                       as COL_INFO
  31                    from USER_TAB_COLUMNS c ,USER_COL_COMMENTS m
  32                    where c.COLUMN_NAME = m.COLUMN_NAME and c.TABLE_NAME = m.TABLE_NAME
  33              """)
  34  # Create a type-mapping between T_COL_INFO and the Python object ColInfo
  35  myDB.addTypemap(oracleTypename='T_COL_INFO',pythonClass=ColInfo,attrDict={
  36          'name' 			: Attribute('NAME'),
  37          'oracleDataType'	        : Attribute('DATA_TYPE'),
  38          'oracleDataLenght'	: Attribute('DATA_LENGTH'),
  39          })
  40  # select some objects from the database
  41  for row in cur.execute("""  select TABLE_NAME,COL_INFO from V_COL_INFO order by 1 """):
  42   print 'Table::%s "%s"::%s' % \
  43   (row.table_name,row.col_info.__class__.__name__,row.col_info)
  43  cur.close()	
  44  con.close()

First of all, we need a Python class to receive the data from the 
Oracle object type. In line 5, we create the class "ColInfo". To
use the class with cy_Oracle, it needs a constructor without 
parameters an "object" somewhere in its base classes.

Now, we need an Oracle object type. We are using the DDL-statement in
line 19 to create the type T_COL_INFO. It stores information about one colunm
of a table or a view in the database.

Next, we want to be able to receive objects of the type T_COL_INFO from the database.
In this example, we are creating the database view V_COL_INFO that contains this object 
in one of its columns - see line 26.

The interesting part of this example the code in line 35. In cx_Oracle, a SELECT
from the view V_COL_INFO would return an object of the Python class cx_Oracle.Object.
This is a generic class, used for all Oracle object types with the following
advantages and disadvantages:

* it is generic and contains all attributes of the Oracle object
* all instances become inaccessable when closing the database connection  
* you can not derive your own Python class from cx_Oracle.Object

With the method "addTypemap" we tell cy_Oracle that:

* we want an object of the Python class "ColInfo" each time a Oracle object
  of the object type "T_COL_INFO" shows up 
* we want an Oracle object of the object type "T_COL_INFO" each time a Python
  object of the class "ColInfo" shows up
* we tell cy_Oracle how the attributes of the two types are mapped. 


The output from the example depends on the objects in your database schema, but
it should be something like this::

        Table::BOOK "ColInfo"::name=BK_ISBN type=NUMBER(22)
        Table::BOOK "ColInfo"::name=BK_BOOK type=T_BOOK(1)

It shows, that:

* we got an object of the Python class "ColInfo" for each entry in view
  "V_COL_INFO".
* We can add or override methods in "ColInfo" as usual  

Example 3
---------

Oracle object types can be build as a composition using other object types.
The following example shows how cy_Oracle handles compositions and collections
of objects.

We are extending the example 2 to get one Python object for each table in our
schema containing:

* the name of the table
* the remaining free space in the table
* a collection of "ColInfo" (see Example 2) objects describing each of the columns.  

The exmple also shows that cy_Oracle is able to deal with composit Object
object types::

 1  """ Example using Oracle Object Types
 2  
 3  This example shows how to map composit
 4  Oracle object types as well collections
 5  to Python objects using cy_Oracle.
 6  """
 7  from cy_Oracle import OracleDB
 8  from cy_Oracle import Attribute
 9  from cy_Oracle import Collection
 10  
 11  # class to receive the result - one object of type T_COL_INFO.
 12  class ColInfo(object):
 13  	def __init__(self):
 14  		self.name=None
 15  		self.oracleDataType=None
 16  		self.oracleDataLenght=None
 17  	def __str__(self):
 18  		return 'name=%s type=%s(%d)' % \
 19  			(self.name,self.oracleDataType,self.oracleDataLenght)
 20  
 21  # Class the receive the result - one object of type T_TAB_INFO
 22  class TabInfo(object):
 23  	def __init__(self):
 24  		self.name=None
 25  		self.pctFree=None
 26  		self.colInfo=None
 27  	def __str__(self):
 28  		result = 'name=%s free=%d(%%)' % (self.name,self.pctFree)
 29  		for col in self.colInfo:
 30  			result = '%s\n    %s' % (result,col)
 31  		return result
 32  
 33  myDB = OracleDB(user='book', password='book', databaseURL='bookdb')
 34  con = myDB.connect()
 35  cur = con.cursor()
 36  
 37  # to be able to run this program more then once we must drop the existing types
 38  try:
 39  	cur.execute(""" drop type T_TAB_INFO """)
 40  except:
 41  	pass
 42  try:
 43  	cur.execute(""" drop type T_COL_INFO_NT """)
 44  except:
 45  	pass
 46  
 47  # Create a object type in the database
 48  cur.execute(""" create or replace type T_COL_INFO as object(
 49  		 NAME		varchar2(85 char)
 50  		,DATA_TYPE      varchar2(106 char)
 51  		,DATA_LENGTH	number
 52  		,COMMENTS       varchar2(4000 char))
 53  	    """)
 54  # Create a collection type in the database
 55  cur.execute(""" create or replace type T_COL_INFO_NT as table of T_COL_INFO """)
 56  # Create the type that describes one table 
 57  cur.execute(""" create or replace type T_TAB_INFO as object(
 58  		 NAME varchar2(30 char),
 59  		 PCT_FREE number,
 60  		 COL_INFO T_COL_INFO_NT)
 61  	    """)
 62  # create a view containing objects of the type T_COL_INFO
 63  cur.execute(""" create or replace view V_TAB_INFO as 
 64                  select T_TAB_INFO(
 65                     t.TABLE_NAME 
 66                    ,t.PCT_FREE
 67                    ,cast(MULTISET( 
 68  	                SELECT T_COL_INFO(c.COLUMN_NAME,c.DATA_TYPE,c.DATA_LENGTH
 69  			,m.COMMENTS) from 
 70  	                USER_TAB_COLUMNS c,USER_COL_COMMENTS m
 71  	                where c.TABLE_NAME=t.TABLE_NAME and c.TABLE_NAME=m.TABLE_NAME)
 72                     as T_COL_INFO_NT )
 73                  ) as TAB_INFO
 74                  from user_tables t
 75              """)
 76  
 77  # Create a type-mapping between T_COL_INFO and the Python object ColInfo
 78  myDB.addTypemap(oracleTypename='T_COL_INFO',pythonClass=ColInfo,attrDict={
 79  	'name' 			: Attribute('NAME'),
 80  	'oracleDataType'	: Attribute('DATA_TYPE'),
 81  	'oracleDataLenght'	: Attribute('DATA_LENGTH'),
 82  	})
 83  # Create a type-mapping between T_TAB_INFO and the Python object ColInfo
 84  myDB.addTypemap(oracleTypename='T_TAB_INFO',pythonClass=TabInfo,attrDict={
 85  	'name' 			: Attribute('NAME'),
 86  	'pctFree'		: Attribute('PCT_FREE'),
 87  	'colInfo'		: Collection('COL_INFO','T_COL_INFO_NT')
 88  	})
 89  
 90  # select some objects from the database
 91  for row in cur.execute("""  select TAB_INFO  from V_TAB_INFO """):
 92  	print '\n%s' %  (row.tab_info)
 93  cur.close()	
 94  con.close()


The output from the example depends on the objects in your database schema, but
it should be something like this::

        name=BOOK free=10(%)
            name=BK_BOOK type=T_BOOK(1)
            name=BK_ISBN type=NUMBER(22)
            name=BK_BOOK type=T_BOOK(1)
            name=BK_ISBN type=NUMBER(22)
        ...
        ...

