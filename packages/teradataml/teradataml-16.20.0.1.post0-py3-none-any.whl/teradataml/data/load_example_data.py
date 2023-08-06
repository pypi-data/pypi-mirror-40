"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: mounika.kotha@teradata.com
Secondary Owner:

This file implements the functionality of loading data to a table.
"""

import csv
import json
import os
import datetime
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.context.context import *
from teradataml.dataframe.copy_to import copy_to_sql
import pandas as pd
import numpy as np
from teradataml import *
from teradataml.options import display
from teradataml.common.utils import UtilFuncs
from collections import defaultdict
from teradataml.common.sqlbundle import SQLBundle
import teradataml.context.context as tdmlctx
from collections import OrderedDict

json_data = {}
col_types_dict = {}
curr_dir = os.path.dirname(os.path.abspath(__file__))

def load_example_data(function_name, table_name):
    """
    This function loads the data to the specified table. This is only used for
    trying examples for the analytic functions, to load the required data.
    
    PARAMETERS:
        function_name (Required) - The argument contains name to load data.
        table_name (Required) - Specifies the name of the table to be created in the database.
               Type : String/List of Strings
    EXAMPLES:
        load_example_data("pack", "ville_temperature")
        load_example_data("attribution", ["attribution_sample_table1", "attribution_sample_table2" , 
                                  "conversion_event_table", "optional_event_table", "model1_table", "model2_table"])
              
    RETURNS:
        None.
        
    RAISES:
        None.
        
    
    """
    example_filename = os.path.join(curr_dir, "{}_example.json".format(function_name.lower()))
    global json_data
    
    #Read json file to get table columns and datatypes
    with open(format(example_filename)) as json_input:
        json_data = json.load(json_input, object_pairs_hook = OrderedDict)

    if isinstance(table_name, list) :
        for table in table_name:
            try:
                __create_table_insert_data(table)
            except TeradataMlException as err:
                if err.code == MessageCodes.TABLE_ALREADY_EXISTS:
                    # TODO - Use the improved way of logging messages when the right tools for it are built in
                    print("WARNING: Skipped loading table {} since it already exists in the database.".format(table))
                else:
                    raise
    else:
        try:
            __create_table_insert_data(table_name)
        except TeradataMlException as err:
            if err.code == MessageCodes.TABLE_ALREADY_EXISTS:
                # TODO - Use the improved way of logging messages when the right tools for it are built in
                print("WARNING: Skipped loading table {} since it already exists in the database.".format(table_name))
            else:
                raise

    json_input.close()

def __create_table_insert_data(tablename):
    """
    Function creates table and inserts data from csv into the table.
    
     PARAMETERS:
         table_name ((Required) - Specifies the name of the table to be created in the database.
            Type : String
     
    EXAMPLES:
         __create_table_insert_data("ville_temperature")
         
     RETURNS:
         None.
        
     RAISES:
         TeradataMlException - If table already exists in database.
     """
    csv_file = os.path.join(curr_dir, "{}.csv".format(tablename))
    col_types_dict  = json_data[tablename]    
    td_number_of_columns = '?,' * len(col_types_dict)
    column_dtypes = ''
    date_time = {}
    
    '''
    Create column datatype string required to create a table.
    EXAMPLE:
        id integer,model varchar(30)
    '''
    for column in col_types_dict.keys():
        # Create a dictionary with column names as list of values which has 
        # datatype as date and timestamp.
        # EXAMPLE : date_time_columns = {'date':['orderdate']}
        if col_types_dict[column] == "date":
            date_time.setdefault("date", []).append(column)
        elif col_types_dict[column] == "timestamp":
            date_time.setdefault("timestamp", []).append(column)
        column_dtypes ="{0}{1} {2},\n" .format(column_dtypes, column, col_types_dict[column])
    
    #Deriving global connection using context.get_context()
    con = get_context()    
    table_exists = con.dialect.has_table(con, tablename)
    if table_exists:
        raise TeradataMlException(Messages.get_message(MessageCodes.TABLE_ALREADY_EXISTS, tablename),
                                              MessageCodes.TABLE_ALREADY_EXISTS)   
    else:
        UtilFuncs._create_table_using_columns(tablename,column_dtypes[:-2])
        __insert_into_table_from_csv(tablename, td_number_of_columns[:-1], csv_file, date_time)
        

def __insert_into_table_from_csv(tablename, column_markers, file, date_time_columns):
        """
        Builds and executes a prepared statement with parameter markers for a table. 
        
        PARAMETERS:
            tablename - table name to insert data.
            column_markers - the parameter markers for the prepared statement
            file - csv file which comtains data to load into table
            date_time_columns - dictionary which contains date and time columns
            list
            
        EXAMPLES:
            date_time_columns = {'date':['orderdate']}
            preparedstmt = __insert_into_table_from_csv(
                            'mytab', '?, ?','file.csv', date_time_columns )

        RETURNS:
             

        RAISES:
            Database error if an error occurred while executing the DDL statement.
        
        """
        insert_stmt = SQLBundle._build_insert_into_table_records(tablename, column_markers)
        
        if tdmlctx.td_connection is not None:
            cursor = None
            try:
                conn = tdmlctx.td_connection.connection
                cursor = conn.cursor()        
                
                with open (file, 'r') as f:
                    reader = csv.reader(f)
                    #Read headers of csv file
                    headers = next(reader) 
                    
                    for row in reader :
                        '''
                        The data in the row is converted from string to date or 
                        timestamp format, which is required to insert data into
                        table for date or timestamp columns.
                        '''
                        for key,value in date_time_columns.items():
                            if key == 'date':
                                for val in value:
                                    if val in headers:
                                        row[headers.index(val)] = datetime.datetime.strptime(
                                                row[headers.index(val)], '%Y-%m-%d')
                            elif key == 'timestamp':
                                for val in value:
                                    if val in headers:
                                        row[headers.index(val)] = datetime.datetime.strptime(
                                                row[headers.index(val)], '%Y-%m-%d %H:%M:%S')                                
                        cursor.execute (insert_stmt, row)
                        conn.commit()
            except:
                raise
            finally:
                if cursor:
                    cursor.close()
        else:
            raise TeradataMlException(Messages.get_message(MessageCodes.CONNECTION_FAILURE), MessageCodes.CONNECTION_FAILURE)
    
