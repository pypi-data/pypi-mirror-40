# -*- coding: utf-8 -*-
"""

Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: ellen.teradata@teradata.com
Secondary Owner:

This file implements the teradataml dataframe.
A teradataml dataframe maps virtually to teradata tables and views.
"""
import sys
import inspect
import sqlalchemy
import teradatasqlalchemy
import numbers
import decimal
import teradataml.context.context as tdmlctx
import pandas as pd

from sqlalchemy import Table, Column
from teradataml.dataframe.sql import _MetaExpression
from teradataml.dataframe.sql_interfaces import ColumnExpression

from teradataml.common.utils import UtilFuncs
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.sqlbundle import SQLBundle

from teradataml.common.constants import SQLConstants, AEDConstants
from teradataml.common.constants import SourceType, PythonTypes, TeradataConstants, TeradataTypes
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils
from teradataml.dataframe.indexer import _LocationIndexer
from teradataml.common.aed_utils import AedUtils
from sqlalchemy.exc import UnsupportedCompilationError
from teradataml.options.display import display
from teradataml.common.wrapper_utils import AnalyticsWrapperUtils
from teradataml.dataframe.copy_to import copy_to_sql
from teradatasqlalchemy.dialect import preparer, dialect as td_dialect

#TODO use logger when available on master branch
#logger = teradatapylog.getLogger()

in_schema = UtilFuncs._in_schema

class DataFrame():
    """
    The teradataml DataFrame enables data manipulation, exploration, and analysis
    on tables, views, and queries on Teradata Vantage.
    """

    def __init__(self, table_name=None, index=True, index_label=None, query=None):
        """
        Constructor for TerdataML DataFrame.

        PARAMETERS:
            table_name - The table name or view name in Teradata referenced by this DataFrame.
            index - True if using index column for sorting, otherwise False.
            index_label - Column/s used for sorting.
            query - SQL query for this Dataframe. Used by class method from_query.

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            df = DataFrame("mytab")
            df = DataFrame("myview")
            df = DataFrame("myview", False)
            df = DataFrame("mytab", True, "Col1, Col2")

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL

        """
        self._table_name = None
        self._query = None
        self._metadata = None
        self._column_names_and_types = None
        self._td_column_names_and_types = None
        self._nodeid = None
        self._metaexpr = None
        self._index = index
        self._index_label = index_label
        self._aed_utils = AedUtils()
        self._source_type = None
        self._orderby = None
        self._undropped_index = None
        # This attribute added to add setter for columns property,
        # it is required when setting columns from groupby
        self._columns = None
        try:
            if table_name is not None:
                self._table_name = UtilFuncs._quote_table_names(table_name)
                self._source_type = SourceType.TABLE
                self._nodeid = self._aed_utils._aed_table(self._table_name)
                self._metadata = df_utils._get_metadata_from_table(self._table_name)
                if self._index_label is None:
                    try:
                        self._index_label = df_utils._get_primary_index_from_table(self._table_name)
                    except Exception as err:
                        # DataFrames generated from views (top node), _index_label is None when PI fetch fails.
                        self._index_label = None

            elif query is not None:
                self._query = query
                self._source_type = SourceType.QUERY
                temp_table_name = UtilFuncs._generate_temp_table_name(use_default_database=True, quote=False)
                self._table_name = UtilFuncs._quote_table_names(temp_table_name)
                UtilFuncs._create_view(self._table_name, self._query)
                self._metadata = df_utils._get_metadata_from_table(self._table_name)
                self._nodeid = self._aed_utils._aed_query(self._query, temp_table_name)

            else:
                if inspect.stack()[1][3] not in ['_from_node', '__init__']:
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_CREATE_FAIL), MessageCodes.TDMLDF_CREATE_FAIL)

            if self._metadata is not None:
                self._column_names_and_types = UtilFuncs._describe_column(self._metadata)
                self._td_column_names_and_types = UtilFuncs._describe_column(self._metadata, to_type = "TD")

                if table_name or query:
                    self._metaexpr = self._get_metaexpr()

            self._loc = _LocationIndexer(self)
            self._iloc = _LocationIndexer(self, integer_indexing=True)

        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_CREATE_FAIL), MessageCodes.TDMLDF_CREATE_FAIL) from err

    @classmethod
    def from_table(cls, table_name, index=True, index_label=None):
        """
        Class method for creating a DataFrame from a table or a view.

        PARAMETERS:
            table_name (required)- The table name in Teradata referenced by this DataFrame.
            index (optional) - True if using index column for sorting otherwise False. Default is True.
            index_label (optional) - Column/s used for sorting.

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            df = DataFrame.from_table("mytab")
            df = DataFrame.from_table("myview")
            df = DataFrame.from_table("myview", False)
            df = DataFrame.from_table("mytab", True, "Col1, Col2")

        RETURNS:
            DataFrame

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL

        """
        return cls(table_name, index, index_label)

    @classmethod
    def from_query(cls, query, index=True, index_label=None):
        """
        Class method for creating a DataFrame from a table or view.

        PARAMETERS:
            query - The Teradata SQL query referenced by this DataFrame.
            index - True if using index column for sorting otherwise False.
            index_label - Column/s used for sorting.

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            df = DataFrame.from_query("select col1, col2, from mytab")
            df = DataFrame.from_query("select col1, col2, from myview", False)
            df = DataFrame.from_query("select * from mytab", True, "Col1, Col2")

        RETURNS:
            DataFrame

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL

        """
        return cls(index=index, index_label=index_label, query=query)

    @classmethod
    def _from_node(cls, nodeid, metaexpr, index_label=None, undropped_index=None):
        """
        Private class method for creating a DataFrame from a nodeid and parent metadata.

        PARAMETERS:
            nodeid - Node ID for the DataFrame.
            metaexpr - Parent metadata (_MetaExpression Object).
            index_label - List specifying index column(s) for the DataFrame.
            undropped_index - List specifying index column(s) to be retained as columns for printing.

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            df = DataFrame._from_node(1234, metaexpr)
            df = DataFrame._from_node(1234, metaexpr, ['col1'], ['col2'])

        RETURNS:
            DataFrame

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL

        """
        df = cls()
        df._nodeid = nodeid
        df._source_type = SourceType.TABLE
        df._get_metadata_from_metaexpr(metaexpr)

        if isinstance(index_label, str):
            index_label = [index_label]

        if index_label is not None and all(elem in [col.name for col in metaexpr.c] for elem in index_label):
            df._index_label = index_label
        elif index_label is not None and all(UtilFuncs._teradata_quote_arg(elem, "\"")
                                             in [col.name for col in metaexpr.c] for elem in index_label):
            df._index_label = index_label

        if isinstance(undropped_index, str):
            undropped_index = [undropped_index]

        if undropped_index is not None and all(elem in [col.name for col in metaexpr.c] for elem in undropped_index):
            df._undropped_index = undropped_index

        return df

    def _get_metadata_from_metaexpr(self, metaexpr):
        """
        Private method for setting _metaexpr and retrieving column names and types
        if _metadata is None.

        PARAMETERS:
            metaexpr - Parent meta data (_MetaExpression object).

        RETURNS:
            Python type.

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL

        """
        self._metaexpr = metaexpr
        #if there is no metadata from HELP COLUMN then use the metadata from metaexpr
        if self._metadata is None:
            self._column_names_and_types = []
            self._td_column_names_and_types = []
            for col in metaexpr.c:
                if isinstance(col.type, sqlalchemy.sql.sqltypes.NullType):
                    tdtype = TeradataTypes.TD_NULL_TYPE
                else:
                    tdtype = "{}".format(col.type)

                self._column_names_and_types.append((col.name, UtilFuncs._teradata_type_to_python_type(col.type)))
                self._td_column_names_and_types.append((col.name, tdtype))

    def _get_metaexpr(self):
        """
        Private method that returns a TableExpression object for this dataframe.

        RETURNS:
            TableExpression object

        EXAMPLES:
            table_meta = self._get_metaexpr()

            # you can access the columns with the 'c' attribute
            table_meta.c

        """
        eng = tdmlctx.get_context()
        meta = sqlalchemy.MetaData(eng)
        names = self._table_name.split(".")
        db_schema = None
        #Remove quotes because sqlalchemy.Table() does not like the quotes.
        if len(names) > 1:
            db_schema = names[0][1:-1]
            db_table_name = names[1][1:-1]
        else:
            db_table_name = names[0][1:-1]

        t = sqlalchemy.Table(db_table_name, meta, schema=db_schema, autoload=True, autoload_with=eng)
        return _MetaExpression(t, column_order = self.columns)


    def __getattr__(self, name):
        """
        Returns an attribute of the DataFrame

        PARAMETERS:
          name: the name of the attribute

        RETURNS:
          Return the value of the named attribute of object (if found).

        EXAMPLES:
          df = DataFrame('table')

          # you can access a column from the DataFrame
          df.c1

        RAISES:
          Attribute Error when the named attribute is not found
        """

        # look in the underlying _MetaExpression for columns
        for col in self._metaexpr.c:
            if col.name == name:
                return col

        raise AttributeError("'DataFrame' object has no attribute %s" % name)

    def __getitem__(self, key):
        """
        Return a column from the DataFrame or filter the DataFrame using an expression
        The following operators are supported:
          comparison: ==, !=, <, <=, >, >=
          boolean: & (and), | (or), ~ (not), ^ (xor)

        Operands can be python literals and instances of ColumnExpressions from the DataFrame

        EXAMPLES:
          df = DataFrame('table')

          # filter the DataFrame df
          df[df.c1 > df.c2]

          df[df.c1 >= 1]

          df[df.c1 == 'string']

          df[1 != df.c2]

          df[~(1 < df.c2)]

          df[(df.c1 > 0) & (df.c2 > df.c1)]

          # retrieve column c1 from df
          df['c1']

        PARAMETERS:
          key: A column name as a string or filter expression (ColumnExpression)

        RETURNS:
          DataFrame or ColumnExpression instance

        RAISES:
          KeyError
        """

        try:
            # get the ColumnExpression from the _MetaExpression
            if isinstance(key, str):
                return self.__getattr__(key)

            # apply the filter expression
            if isinstance(key, ColumnExpression):

                if self._metaexpr is None:
                    msg = Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR)
                    raise TeradataMlException(msg, MessageCodes.TDMLDF_INFO_ERROR)

                clause_exp = key.compile()
                new_nodeid = self._aed_utils._aed_filter(self._nodeid, clause_exp)

                return DataFrame._from_node(new_nodeid, self._metaexpr, self._index_label)

        except TeradataMlException:
            raise

        except Exception as err:
            errcode = MessageCodes.TDMLDF_INFO_ERROR
            msg = Messages.get_message(errcode)
            raise TeradataMlException(msg, errcode) from err

        raise KeyError('Unable to find key: %s' % str(key))

    def keys(self):
        """
        RETURNS:
            a list containing the column names

        EXAMPLES:
            df.keys()

        """
        if self._column_names_and_types is not None:
            return [i[0] for i in self._column_names_and_types]
        else:
            return []

    @property
    def columns(self):
        """
        RETURNS:
            a list containing the column names

        EXAMPLES:
            df.columns

        """
        return self.keys()

    @property
    def loc(self):
        """
        Access a group of rows and columns by label(s) or a boolean array.

        VALID INPUTS:

            - A single label, e.g. ``5`` or ``'a'``, (note that ``5`` is
            interpreted as a label of the index, it is not interpreted as an
            integer position along the index).

            - A list or array of column or index labels, e.g. ``['a', 'b', 'c']``.

            - A slice object with labels, e.g. ``'a':'f'``.
            Note that unlike the usual python slices where the stop index is not included, both the
                start and the stop are included

            - A conditional expression for row access.

            - A boolean array of the same length as the column axis for column access.

        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES
        --------
            >>> df = DataFrame('sales')
            >>> df
                        Feb   Jan   Mar   Apr    datetime
            accounts
            Blue Inc     90.0    50    95   101  2017-04-01
            Alpha Co    210.0   200   215   250  2017-04-01
            Jones LLC   200.0   150   140   180  2017-04-01
            Yellow Inc   90.0  None  None  None  2017-04-01
            Orange Inc  210.0  None  None   250  2017-04-01
            Red Inc     200.0   150   140  None  2017-04-01

            Retrieve row using a single label.
            >>> df.loc['Blue Inc']
                    Feb Jan Mar  Apr    datetime
            accounts
            Blue Inc  90.0  50  95  101  2017-04-01

            List of labels. Note using ``[[]]``
            >>> df.loc[['Blue Inc', 'Jones LLC']]
                        Feb  Jan  Mar  Apr    datetime
            accounts
            Blue Inc    90.0   50   95  101  2017-04-01
            Jones LLC  200.0  150  140  180  2017-04-01

            Single label for row and column (index)
            >>> df.loc['Yellow Inc', 'accounts']
            Empty DataFrame
            Columns: []
            Index: [Yellow Inc]

            Single label for row and column
            >>> df.loc['Yellow Inc', 'Feb']
                Feb
            0  90.0

            Single label for row and column access using a tuple
            >>> df.loc[('Yellow Inc', 'Feb')]
                Feb
            0  90.0

            Slice with labels for row and single label for column. As mentioned
            above, note that both the start and stop of the slice are included.
            >>> df.loc['Jones LLC':'Red Inc', 'accounts']
            Empty DataFrame
            Columns: []
            Index: [Orange Inc, Jones LLC, Red Inc]

            Slice with labels for row and single label for column. As mentioned
            above, note that both the start and stop of the slice are included.
            >>> df.loc['Jones LLC':'Red Inc', 'Jan']
                Jan
            0  None
            1   150
            2   150

            Slice with labels for row and labels for column. As mentioned
            above, note that both the start and stop of the slice are included.
            >>> df.loc['Jones LLC':'Red Inc', 'accounts':'Apr']
                        Mar   Jan    Feb   Apr
            accounts
            Orange Inc  None  None  210.0   250
            Red Inc      140   150  200.0  None
            Jones LLC    140   150  200.0   180

            Empty slice for row and labels for column.
            >>> df.loc[:, :]
                        Feb   Jan   Mar    datetime   Apr
            accounts
            Jones LLC   200.0   150   140  2017-04-01   180
            Blue Inc     90.0    50    95  2017-04-01   101
            Yellow Inc   90.0  None  None  2017-04-01  None
            Orange Inc  210.0  None  None  2017-04-01   250
            Alpha Co    210.0   200   215  2017-04-01   250
            Red Inc     200.0   150   140  2017-04-01  None

            Conditional expression
            >>> df.loc[df['Feb'] > 90]
                        Feb   Jan   Mar   Apr    datetime
            accounts
            Jones LLC   200.0   150   140   180  2017-04-01
            Red Inc     200.0   150   140  None  2017-04-01
            Alpha Co    210.0   200   215   250  2017-04-01
            Orange Inc  210.0  None  None   250  2017-04-01

            Conditional expression with column labels specified
            >>> df.loc[df['Feb'] > 90, ['accounts', 'Jan']]
                        Jan
            accounts
            Jones LLC    150
            Red Inc      150
            Alpha Co     200
            Orange Inc  None

            Conditional expression with multiple column labels specified
            >>> df.loc[df['accounts'] == 'Jones LLC', ['accounts', 'Jan', 'Feb']]
                    Jan    Feb
            accounts
            Jones LLC  150  200.0

            Conditional expression and slice with column labels specified
            >>> df.loc[df['accounts'] == 'Jones LLC', 'accounts':'Mar']
                    Mar  Jan    Feb
            accounts
            Jones LLC  140  150  200.0

            Conditional expression and boolean array for column access
            >>> df.loc[df['Feb'] > 90, [True, True, False, False, True, True]]
                        datetime   Apr    Feb
            accounts
            Jones LLC   2017-04-01   180  200.0
            Orange Inc  2017-04-01   250  210.0
            Alpha Co    2017-04-01   250  210.0
            Red Inc     2017-04-01  None  200.0
        """
        return self._loc

    @property
    def iloc(self):
        """
        Access a group of rows and columns by integer values or a boolean array.
        VALID INPUTS:
            - A single integer values, e.g. 5.

            - A list or array of integer values, e.g. ``[1, 2, 3]``.

            - A slice object with integer values, e.g. ``1:6``.
              Note: The stop value is excluded.

            - A boolean array of the same length as the column axis for column access,

            Note: For integer indexing on row access, the integer index values are
            applied to a sorted teradataml DataFrame on the index column or the first column if
            there is no index column.

        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES
        --------
            >>> df = DataFrame('sales')
            >>> df
                        Feb   Jan   Mar   Apr    datetime
            accounts
            Blue Inc     90.0    50    95   101  2017-04-01
            Alpha Co    210.0   200   215   250  2017-04-01
            Jones LLC   200.0   150   140   180  2017-04-01
            Yellow Inc   90.0  None  None  None  2017-04-01
            Orange Inc  210.0  None  None   250  2017-04-01
            Red Inc     200.0   150   140  None  2017-04-01

            Retrieve row using a single integer.
            >>> df.iloc[1]
                    Feb Jan Mar  Apr    datetime
            accounts
            Blue Inc  90.0  50  95  101  2017-04-01

            List of integers. Note using ``[[]]``
            >>> df.iloc[[1, 2]]
                        Feb  Jan  Mar  Apr    datetime
            accounts
            Blue Inc    90.0   50   95  101  2017-04-01
            Jones LLC  200.0  150  140  180  2017-04-01

            Single integer for row and column
            >>> df.iloc[5, 0]
            Empty DataFrame
            Columns: []
            Index: [Yellow Inc]

            Single integer for row and column
            >>> df.iloc[5, 1]
                Feb
            0  90.0

            Single integer for row and column access using a tuple
            >>> df.iloc[(5, 1)]
                Feb
            0  90.0

            Slice for row and single integer for column access. As mentioned
            above, note the stop for the slice is excluded.
            >>> df.iloc[2:5, 0]
            Empty DataFrame
            Columns: []
            Index: [Orange Inc, Jones LLC, Red Inc]

            Slice for row and a single integer for column access. As mentioned
            above, note the stop for the slice is excluded.
            >>> df.iloc[2:5, 2]
                Jan
            0  None
            1   150
            2   150

            Slice for row and column access. As mentioned
            above, note the stop for the slice is excluded.
            >>> df.iloc[2:5, 0:5]
                        Mar   Jan    Feb   Apr
            accounts
            Orange Inc  None  None  210.0   250
            Red Inc      140   150  200.0  None
            Jones LLC    140   150  200.0   180

            Empty slice for row and column access.
            >>> df.iloc[:, :]
                        Feb   Jan   Mar    datetime   Apr
            accounts
            Jones LLC   200.0   150   140  2017-04-01   180
            Blue Inc     90.0    50    95  2017-04-01   101
            Yellow Inc   90.0  None  None  2017-04-01  None
            Orange Inc  210.0  None  None  2017-04-01   250
            Alpha Co    210.0   200   215  2017-04-01   250
            Red Inc     200.0   150   140  2017-04-01  None

            List of integers and boolean array for column access
            >>> df.iloc[[0, 2, 3, 4], [True, True, False, False, True, True]]
                        datetime   Apr    Feb
            accounts
            Jones LLC   2017-04-01   180  200.0
            Orange Inc  2017-04-01   250  210.0
            Alpha Co    2017-04-01   250  210.0
            Red Inc     2017-04-01  None  200.0
        """
        return self._iloc

    @columns.setter
    def columns(self, columns):
        """
        Assigns self._columns for the passed columns

        PARAMETERS:
            columns

        EXAMPLES:
            df.columns

        """
        self._columns = columns

    @property
    def dtypes(self):
        """
        Returns a MetaData containing the column names and types.

        PARAMETERS:

        RETURNS:
            MetaData containing the column names and Python types

        RAISES:

        EXAMPLES:
            >>> print(df.dtypes)
            InfoKey     str
            InfoData    str
        """
        return MetaData(self._column_names_and_types)

    def info(self, verbose=True, buf=None, max_cols=None, null_counts=None):
        """
        Print a summary of the DataFrame.

        PARAMETERS:
        verbose(optional) - Print full summary if True. Print
            short summary if False.
        buf(optional) - The writable buffer to send the output to.
            By default, the output is sent to sys.stdout.
        max_cols(optional) - The maximum number of columns allowed for
            printing the full summary.
        null_counts(optional) - Whether to show the non-null counts.
            Display the counts if True, otherwise do not display the counts.

        RETURNS:

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> df.info()
            <class 'teradataml.dataframe.dataframe.DataFrame'>
            Data columns (total 6 columns):
            accounts      str
            Feb         float
            Jan           int
            Mar           int
            Apr           int
            datetime      str
            dtypes: float(1), int(3), str(2)

            >>> df.info(null_counts=True)
            <class 'teradataml.dataframe.dataframe.DataFrame'>
            Data columns (total 6 columns):
            accounts    3 non-null str
            Feb         3 non-null float
            Jan         3 non-null int
            Mar         3 non-null int
            Apr         3 non-null int
            datetime    3 non-null str
            dtypes: float(1), int(3), str(2)

            >>> df.info(verbose=False)
            <class 'teradataml.dataframe.dataframe.DataFrame'>
            Data columns (total 6 columns):
            dtypes: float(1), int(3), str(2)
        """
        try:
            output_buf = sys.stdout
            if buf is not None:
                output_buf = buf

            num_columns = len(self._column_names_and_types)
            suffix = ""
            if num_columns > 1:
                suffix = "s"

            col_names = [i[0] for i in self._column_names_and_types]
            col_types = [i[1] for i in self._column_names_and_types]

            #print the class name for self.
            print(str(type(self)), file=output_buf)
            #print the total number of columns
            print("Data columns (total {0} column{1}):".format(num_columns, suffix), file=output_buf)

            #if max_cols and the number of columns exceeds max_cols, do not print the column names and types
            if max_cols is not None and len(col_names) > max_cols:
                verbose = False

            #if verbose, print the column names and types.
            if verbose:
                #if null_counts, print the number of non-null values for each column if this is not an empty dataframe.
                if null_counts is not None and null_counts and self._table_name is not None:
                    null_count_str = UtilFuncs._get_non_null_counts(col_names, self._table_name)
                    zipped = zip(col_names, col_types, null_count_str)
                    column_names_and_types = list(zipped)
                    null_count = True
                #else just print the column names and types
                else:
                    column_names_and_types = self._column_names_and_types
                    null_count = False
                print("{}".format(df_utils._get_pprint_dtypes(column_names_and_types, null_count)), file=output_buf)

            #print the dtypes and count of each dtypes
            unique_types = list(set(col_types))
            for i in range(0, len(unique_types)):
                unique_types[i] = "{0}({1})".format(unique_types[i], col_types.count(unique_types[i]))
            print("dtypes: {}".format(", ".join(unique_types)), file=output_buf)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def head(self, n=display.max_rows):
        """
        Print the first n rows of the sorted teradataml DataFrame.
        Note: The DataFrame is sorted on the index column or the first column if
        there is no index column. The column type must support sorting.
        Unsupported types: ['BLOB', 'CLOB', 'ARRAY', 'VARRAY']

        PARAMETERS:
            n: Optional argument.
               Specifies the number of rows to select.
               Default is 10.
               Type: int

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>>df
               masters   gpa     stats programming admitted
            id
            15     yes  4.00  advanced    advanced        1
            7      yes  2.33    novice      novice        1
            22     yes  3.46    novice    beginner        0
            17      no  3.83  advanced    advanced        1
            13      no  4.00  advanced      novice        1
            38     yes  2.65  advanced    beginner        1
            26     yes  3.57  advanced    advanced        1
            5       no  3.44    novice      novice        0
            34     yes  3.85  advanced    beginner        0
            40     yes  3.95    novice    beginner        0
            
            >>>df.head()
               masters   gpa     stats programming admitted
            id
            3       no  3.70    novice    beginner        1
            5       no  3.44    novice      novice        0
            6      yes  3.50  beginner    advanced        1
            7      yes  2.33    novice      novice        1
            9       no  3.82  advanced    advanced        1
            10      no  3.71  advanced    advanced        1
            8       no  3.60  beginner    advanced        1
            4      yes  3.50  beginner      novice        1
            2      yes  3.76  beginner    beginner        0
            1      yes  3.95  beginner    beginner        0
            
            >>>df.head(15)
               masters   gpa     stats programming admitted
            id
            3       no  3.70    novice    beginner        1
            5       no  3.44    novice      novice        0
            6      yes  3.50  beginner    advanced        1
            7      yes  2.33    novice      novice        1
            9       no  3.82  advanced    advanced        1
            10      no  3.71  advanced    advanced        1
            11      no  3.13  advanced    advanced        1
            12      no  3.65    novice      novice        1
            13      no  4.00  advanced      novice        1
            14     yes  3.45  advanced    advanced        0
            15     yes  4.00  advanced    advanced        1
            8       no  3.60  beginner    advanced        1
            4      yes  3.50  beginner      novice        1
            2      yes  3.76  beginner    beginner        0
            1      yes  3.95  beginner    beginner        0
            
            >>>df.head(5)
               masters   gpa     stats programming admitted
            id
            3       no  3.70    novice    beginner        1
            5       no  3.44    novice      novice        0
            4      yes  3.50  beginner      novice        1
            2      yes  3.76  beginner    beginner        0
            1      yes  3.95  beginner    beginner        0
        """
        try:
            if not isinstance(n, numbers.Integral) or n <= 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_POSITIVE_INT).format("n"), MessageCodes.TDMLDF_POSITIVE_INT)
            if self._metaexpr is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR)
            sort_col = self._get_sort_col()
            return df_utils._get_sorted_nrow(self, n, sort_col[0], asc=True)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def tail(self, n=display.max_rows):
        """
        Print the last n rows of the sorted teradataml DataFrame.
        Note: The Dataframe is sorted on the index column or the first column if
        there is no index column. The column type must support sorting.
        Unsupported types: ['BLOB', 'CLOB', 'ARRAY', 'VARRAY']

        PARAMETERS:
            n: Optional argument.
               Specifies the number of rows to select.
               Default is 10.
               Type: int

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>>df
               masters   gpa     stats programming admitted
            id
            15     yes  4.00  advanced    advanced        1
            7      yes  2.33    novice      novice        1
            22     yes  3.46    novice    beginner        0
            17      no  3.83  advanced    advanced        1
            13      no  4.00  advanced      novice        1
            38     yes  2.65  advanced    beginner        1
            26     yes  3.57  advanced    advanced        1
            5       no  3.44    novice      novice        0
            34     yes  3.85  advanced    beginner        0
            40     yes  3.95    novice    beginner        0

            >>>df.tail()
               masters   gpa     stats programming admitted
            id
            38     yes  2.65  advanced    beginner        1
            36      no  3.00  advanced      novice        0
            35      no  3.68    novice    beginner        1
            34     yes  3.85  advanced    beginner        0
            32     yes  3.46  advanced    beginner        0
            31     yes  3.50  advanced    beginner        1
            33      no  3.55    novice      novice        1
            37      no  3.52    novice      novice        1
            39     yes  3.75  advanced    beginner        0
            40     yes  3.95    novice    beginner        0

            >>>df.tail(3)
               masters   gpa     stats programming admitted
            id
            38     yes  2.65  advanced    beginner        1
            39     yes  3.75  advanced    beginner        0
            40     yes  3.95    novice    beginner        0

            >>>df.tail(15)
               masters   gpa     stats programming admitted
            id
            38     yes  2.65  advanced    beginner        1
            36      no  3.00  advanced      novice        0
            35      no  3.68    novice    beginner        1
            34     yes  3.85  advanced    beginner        0
            32     yes  3.46  advanced    beginner        0
            31     yes  3.50  advanced    beginner        1
            30     yes  3.79  advanced      novice        0
            29     yes  4.00    novice    beginner        0
            28      no  3.93  advanced    advanced        1
            27     yes  3.96  advanced    advanced        0
            26     yes  3.57  advanced    advanced        1
            33      no  3.55    novice      novice        1
            37      no  3.52    novice      novice        1
            39     yes  3.75  advanced    beginner        0
            40     yes  3.95    novice    beginner        0
        """
        try:
            if not isinstance(n, numbers.Integral) or n <= 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_POSITIVE_INT).format("n"), MessageCodes.TDMLDF_POSITIVE_INT)
            if self._metaexpr is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR)

            sort_col = self._get_sort_col()
            return df_utils._get_sorted_nrow(self, n, sort_col[0], asc=False)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def _get_axis(self, axis):
        """
        Private method to retrieve axis value, 0 for index or 1 for columns

        PARAMETERS:
            axis - 0 or 'index' for index labels
                   1 or 'columns' for column labels

        RETURNS:
            0 or 1

        RAISE:
            TeradataMlException

        EXAMPLES:
            a = self._get_axis(0)
            a = self._get_axis(1)
            a = self._get_axis('index')
            a = self._get_axis('columns')
        """
        if isinstance(axis, str):
            if axis == "index":
                return 0
            elif axis == "columns":
                return 1
            else:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INVALID_DROP_AXIS), MessageCodes.TDMLDF_INVALID_DROP_AXIS)
        elif isinstance(axis, numbers.Integral):
            if axis in [0, 1]:
                return axis
            else:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INVALID_DROP_AXIS), MessageCodes.TDMLDF_INVALID_DROP_AXIS)
        else:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INVALID_DROP_AXIS), MessageCodes.TDMLDF_INVALID_DROP_AXIS)

    def _get_sort_col(self):
        """
        Private method to retrieve sort column.
        If _index_labels is not None, return first column and type in _index_labels.
        Otherwise return first column and type in _metadata.

        PARAMETERS:

        RETURNS:
            A tuple containing the column name and type in _index_labels or first column in _metadata.

        RAISE:

        EXAMPLES:
            sort_col = self._get_sort_col()
        """
        unsupported_types = ['BLOB', 'CLOB', 'ARRAY', 'VARRAY']
        
        if self._index_label is not None:
            if isinstance(self._index_label, list):
                col_name = self._index_label[0]
            else:
                col_name = self._index_label
        else: #Use the first column from metadata
            col_name = self.columns[0]

        col_type = PythonTypes.PY_NULL_TYPE
        for name, py_type in self._column_names_and_types:
            if col_name == name:
                col_type = py_type

        if col_type == PythonTypes.PY_NULL_TYPE:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR)

        sort_col_sqlalchemy_type = (self._metaexpr.t.c[col_name].type)  
        # convert types to string from sqlalchemy type for the columns entered for sort
        sort_col_type = repr(sort_col_sqlalchemy_type).split("(")[0]
        if sort_col_type in unsupported_types:
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, sort_col_type, "ANY, except following {}".format(unsupported_types)), MessageCodes.UNSUPPORTED_DATATYPE)

        return (col_name, col_type)

    def drop(self, labels=None, axis=0, columns=None):
        """
        Drop specified labels from rows or columns.

        Remove rows or columns by specifying label names and corresponding
        axis, or by specifying the index or column names directly.

        PARAMETERS:
            labels (optional) - Single label or list-like. Can be Index or column labels to drop depending on axis.
            axis (optional)- 0 or 'index' for index labels
                   1 or 'columns' for column labels
                   The default is 0
            columns (optional)- Single label or list-like. This is an alternative to specifying axis=1 with labels.
                      Cannot specify both labels and columns.

        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES:
            >>> df = DataFrame('admissions_train')
            >>> df
               masters   gpa     stats programming admitted
            id
            5       no  3.44    novice      novice        0
            7      yes  2.33    novice      novice        1
            22     yes  3.46    novice    beginner        0
            17      no  3.83  advanced    advanced        1
            13      no  4.00  advanced      novice        1
            19     yes  1.98  advanced    advanced        0
            36      no  3.00  advanced      novice        0
            15     yes  4.00  advanced    advanced        1
            34     yes  3.85  advanced    beginner        0
            40     yes  3.95    novice    beginner        0

            Drop columns

            >>> df.drop(['stats', 'admitted'], axis=1)
               programming masters   gpa
            id
            5       novice      no  3.44
            34    beginner     yes  3.85
            13      novice      no  4.00
            40    beginner     yes  3.95
            22    beginner     yes  3.46
            19    advanced     yes  1.98
            36      novice      no  3.00
            15    advanced     yes  4.00
            7       novice     yes  2.33
            17    advanced      no  3.83

            >>> df.drop(columns=['stats', 'admitted'])
               programming masters   gpa
            id
            5       novice      no  3.44
            34    beginner     yes  3.85
            13      novice      no  4.00
            19    advanced     yes  1.98
            15    advanced     yes  4.00
            40    beginner     yes  3.95
            7       novice     yes  2.33
            22    beginner     yes  3.46
            36      novice      no  3.00
            17    advanced      no  3.83

            Drop a row by index
            >>> df.drop([34, 13], axis=0)
               masters   gpa     stats programming admitted
            id
            5       no  3.44    novice      novice        0
            7      yes  2.33    novice      novice        1
            22     yes  3.46    novice    beginner        0
            19     yes  1.98  advanced    advanced        0
            15     yes  4.00  advanced    advanced        1
            17      no  3.83  advanced    advanced        1
            32     yes  3.46  advanced    beginner        0
            11      no  3.13  advanced    advanced        1
            36      no  3.00  advanced      novice        0
            40     yes  3.95    novice    beginner        0
        """
        try:
            column_labels = None
            index_labels = None
            if labels is not None and columns is not None:
                #Cannot specify both 'labels' and 'columns'
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)
            elif labels is None and columns is None:
                #Need to specify at least one of 'labels' or 'columns'
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)

            if labels is not None:
                if self._get_axis(axis) == 0:
                    index_labels = labels
                else:
                    column_labels = labels
            else: #columns is not None
                column_labels = columns

            if index_labels is not None:
                sort_col = self._get_sort_col()
                df_utils._validate_sort_col_type(sort_col[1], index_labels)

                if isinstance(index_labels, list):
                    if len(index_labels) == 0:
                        raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)

                    if sort_col[1] == PythonTypes.PY_STRING_TYPE:
                        index_labels = ["'{}'".format(x) for x in index_labels]
                    index_expr = ",".join(map(str, (index_labels)))
                else:
                    if sort_col[1] == PythonTypes.PY_STRING_TYPE:
                        index_expr = "'{}'".format(index_labels)
                    else:
                        index_expr = index_labels

                filter_expr = "{0} not in ({1})".format(sort_col[0], index_expr)
                new_nodeid= self._aed_utils._aed_filter(self._nodeid, filter_expr)
                return DataFrame._from_node(new_nodeid, self._metaexpr, self._index_label)
            else: #column labels
                select_cols = []
                cols = [x.name for x in self._metaexpr.columns]
                if isinstance(column_labels, list):
                    if len(column_labels) == 0:
                        raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)

                    if not all(isinstance(n, str) for n in column_labels):
                        raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES), MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES)
                    drop_cols = [x for x in column_labels]
                elif isinstance(column_labels, (tuple, dict)):
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)
                else:
                    if not isinstance(column_labels, str):
                        raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES), MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES)
                    drop_cols = [column_labels]

                for drop_name in drop_cols:
                    if drop_name not in cols:
                        msg = Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL).format(drop_name, cols)
                        raise TeradataMlException(msg, MessageCodes.TDMLDF_DROP_INVALID_COL)

                for colname in cols:
                    if colname not in drop_cols:
                        select_cols.append(colname)
                if len(select_cols) > 0:
                    return self.select(select_cols)
                else: # no columns selected
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ALL_COLS), MessageCodes.TDMLDF_DROP_ALL_COLS)

        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def dropna(self, how='any', thresh=None, subset=None):
        """
        Removes rows with null values.

        PARAMETERS:
            how (optional) - Specifies how rows are removed.
                    Values can be either 'any' or 'all'. The default is 'any'.
                    'any' removes rows with at least one null value.
                    'all' removes rows with all null values.
            thresh (optional) - Specifies the minimum number of non null values in
                                a row to include. thresh=n, where n is an integer.
            subset (optional) Specifies list of column names to include, in array-like format.

        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES:
            >>> df = DataFrame('sales')
            >>> df
                          Feb   Jan   Mar   Apr    datetime
            accounts
            Jones LLC   200.0   150   140   180  2017-04-01
            Yellow Inc   90.0  None  None  None  2017-04-01
            Orange Inc  210.0  None  None   250  2017-04-01
            Blue Inc     90.0    50    95   101  2017-04-01
            Alpha Co    210.0   200   215   250  2017-04-01
            Red Inc     200.0   150   140  None  2017-04-01

            Drop the rows where at least one element is null.
            >>> df.dropna()
                         Feb  Jan  Mar  Apr    datetime
            accounts
            Blue Inc    90.0   50   95  101  2017-04-01
            Jones LLC  200.0  150  140  180  2017-04-01
            Alpha Co   210.0  200  215  250  2017-04-01

            Drop the rows where all elements are nulls for columns 'Jan' and 'Mar'.
            >>> df.dropna(how='all', subset=['Jan','Mar'])
                         Feb  Jan  Mar   Apr    datetime
            accounts
            Alpha Co   210.0  200  215   250  2017-04-01
            Jones LLC  200.0  150  140   180  2017-04-01
            Red Inc    200.0  150  140  None  2017-04-01
            Blue Inc    90.0   50   95   101  2017-04-01

            Keep only the rows with at least 4 non null values.
            >>> df.dropna(thresh=4)
                          Feb   Jan   Mar   Apr    datetime
            accounts
            Jones LLC   200.0   150   140   180  2017-04-01
            Blue Inc     90.0    50    95   101  2017-04-01
            Orange Inc  210.0  None  None   250  2017-04-01
            Alpha Co    210.0   200   215   250  2017-04-01
            Red Inc     200.0   150   140  None  2017-04-01

            Keep only the rows with at least 5 non null values.
            >>> df.dropna(thresh=5)
                         Feb  Jan  Mar   Apr    datetime
            accounts
            Alpha Co   210.0  200  215   250  2017-04-01
            Jones LLC  200.0  150  140   180  2017-04-01
            Blue Inc    90.0   50   95   101  2017-04-01
            Red Inc    200.0  150  140  None  2017-04-01
        """
        try:
            col_names = [item.lower() for item in self.keys()]

            if not isinstance(how, str) or how not in ['any', 'all']:
                msg = Messages.get_message(MessageCodes.INVALID_ARG_VALUE, how, "how", "'any' or 'all'")
                raise TeradataMlException(msg, MessageCodes.INVALID_ARG_VALUE)

            #if there is a thresh value, the thresh value must be a positive number greater than 0
            if thresh is not None and (not isinstance(thresh, numbers.Integral) or thresh <= 0):
                msg = Messages.get_message(MessageCodes.TDMLDF_POSITIVE_INT).format('thresh')
                raise TeradataMlException(msg, MessageCodes.TDMLDF_POSITIVE_INT)

            #if there is a subset value, the subset value must be a list containing at least one element.
            if subset is not None and (not isinstance(subset, list) or len(subset) == 0):
                msg = Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "subset", "list of column names")
                raise TeradataMlException(msg, MessageCodes.UNSUPPORTED_DATATYPE)

            if subset is not None:
                if not all(isinstance(n, str) for n in subset):
                    msg = Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "subset", "list of column names")
                    raise TeradataMlException(msg, MessageCodes.UNSUPPORTED_DATATYPE)
                for n in subset:
                    if n.lower() not in col_names:
                        msg = Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL).format(n, self.keys())
                        raise TeradataMlException(msg, MessageCodes.TDMLDF_DROP_INVALID_COL)
                col_filters = subset
            else:
                col_filters = col_names

            col_filters_decode = ["decode(\"{}\", null, 0, 1)".format(col_name) for col_name in col_filters]
            fmt_filter = " + ".join(col_filters_decode)

            if thresh is not None:
                filter_expr = "{0} >= {1}".format(fmt_filter, thresh)
            elif how == 'any':
                filter_expr = "{0} = {1}".format(fmt_filter, len(col_filters))
            else: #how == 'all'
                filter_expr = "{0} > 0".format(fmt_filter)

            new_nodeid= self._aed_utils._aed_filter(self._nodeid, filter_expr)
            return DataFrame._from_node(new_nodeid, self._metaexpr, self._index_label)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def sort(self, columns, ascending=True):
        """
        Get Sorted data by one or more columns in either ascending or descending order for a Dataframe.

        PARAMETERS:
            columns:
                Required Argument.
                Column names as a string or a list of strings.
            ascending:
                Optional Argument.
                Order ASC or DESC to be applied for each column.
                Default value: True

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> df = DataFrame("kmeanssample")
            >>> df.sort("id")
            >>> df.sort(["id"])
            >>> df.sort(["point1","point2"])
            >>> df.sort(["point1","point2"], ascending=[True,False]) -- here 'True' means ASCENDING & 'False' means DESCENDING for respective columns

        """
        try:
            columns_expr=""
            orderexpr=""
            type_expr=[]
            invalid_types = []
            unsupported_types = ['BLOB', 'CLOB', 'ARRAY', 'VARRAY']

            if (isinstance(columns, str)):
                columns=[columns]
            if isinstance(ascending, bool):
                ascending=[ascending] * len(columns)
            # validating columns and validating each argument value for columns of passed lists
            if not ((isinstance(columns, list) or (isinstance(columns, str)))
                    and all(isinstance(col, str) for col in columns)):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "columns", ["list","str"]), MessageCodes.UNSUPPORTED_DATATYPE)
            # validating order types which has to be a list
            if not ((isinstance(ascending, list) or (isinstance(ascending, bool)))
                    and all(isinstance(asc, bool) for asc in ascending)):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "ascending", ["list","bool"]), MessageCodes.UNSUPPORTED_DATATYPE)
            # validating lengths of passed arguments which are passed i.e. length of columns
            # must be same as ascending
            if ascending and len(columns) != len(ascending):
                raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_LENGTH_ARGS), MessageCodes.INVALID_LENGTH_ARGS)
            # getting all the columns and data types for given metaexpr
            col_names, col_types = df_utils._get_column_names_and_types_from_metaexpr(self._metaexpr)
            # checking each element in passed columns to be valid column in dataframe
            for col in columns:
                if not df_utils._check_column_exists(col, col_names):
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDF_UNKNOWN_COLUMN, ": {}".format(col)), MessageCodes.TDF_UNKNOWN_COLUMN)
                else:
                    type_expr.append(self._metaexpr.t.c[col].type)
            # convert types to string from sqlalchemy type for the columns entered for sort
            columns_types = [repr(type_expr[i]).split("(")[0] for i in range(len(type_expr))]
            # checking each element in passed columns_types to be valid a data type for sort
            # and create a list of invalid_types
            for col_type in columns_types:
                if col_type in unsupported_types:
                    invalid_types.append(col_type)
            if len(invalid_types) > 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, invalid_types, "ANY, except following {}".format(unsupported_types)), MessageCodes.UNSUPPORTED_DATATYPE)

            columns_expr = UtilFuncs._teradata_quote_arg(columns, "\"")
            columns_expr = columns_expr.split(",")
            if (len(ascending) != 0):
                val=['ASC' if i==True else 'DESC' for i in ascending]
                for c,v in zip(columns_expr,val):
                    orderexpr='{}{} {}, '.format(orderexpr,c,v)
                orderexpr=orderexpr[:-2]
            else:
                orderexpr=", ".join(columns_expr)
            # We are just updating orderby clause in exisitng teradataml dataframe
            # and returning new teradataml dataframe.
            sort_df = self._from_node(self._nodeid, self._metaexpr, self._index_label)
            sort_df._orderby = orderexpr
            # Assigning self attributes to newly created dataframe.
            sort_df._table_name = self._table_name
            sort_df._index = self._index
            sort_df._index_label = self._index_label
            return sort_df
        except TeradataMlException:
            raise

    def filter(self, items = None, like = None, regex = None, axis = 1, **kw):
      """
        Filter rows or columns of dataframe according to labels in the specified index.
        The filter is applied to the columns of the index when axis is set to 'rows'.

        Must use one of the parameters 'items', 'like', and 'regex' only.

        PARAMETERS:

        axis (optional): int or string axis name. The default value is 1.
          Specifies the axis to filter on.
          1 denotes column axis (default). Alternatively, 'columns' can be specified.
          0 denotes row axis. Alternatively, 'rows' can be specified.

        items (optional): list-like
          List of values that the info axis should be restricted to
          When axis is 1, items is a list of column names
          When axis is 0, items is a list of literal values

        like (optional): string
          (optional)
          When axis is 1, substring pattern for matching column names
          When axis is 0, substring pattern for checking index values with REGEXP_SUBSTR

        regex (optional): string (regular expression)
          When axis is 1, regex pattern for re.search(regex, column_name)
          When axis is 0, regex pattern for checking index values with REGEXP_SUBSTR

        **kw: optional keyword arguments

          varchar_size: integer (default: DEFAULT_VAR_SIZE = 1024)
            An integer to specify the size of varchar-casted index.
            Used when axis = 0/'rows' and index must be char-like in "like" and "regex" filtering

          match_arg: string
            argument to pass if axis is 0/'rows' and regex is used

            Valid values for match_arg are:
              - 'i' = case-insensitive matching.
              - 'c' = case sensitive matching.
              - 'n' = the period character (match any character) can match the newline character.
              - 'm' = index value is treated as multiple lines instead of as a single line. With this option, the
                      '^' and '$' characters apply to each line in source_string instead of the entire index value.
              - 'l' = if index value exceeds the current maximum allowed size (currently 16 MB), a NULL is returned
                      instead of an error.
                      This is useful for long-running queries where you do not want long strings
                      causing an error that would make the query fail.
              - 'x' = ignore whitespace.

            The 'match_arg' argument may contain more than one character.
            If a character in 'match_arg' is not valid, then that character is ignored.

        See Teradata® Database SQL Functions, Operators, Expressions, and Predicates, Release 16.20
        for more information on specifying arguments for REGEXP_SUBSTR.

        NOTES:
          - Using 'regex' or 'like' with axis equal to 0 will attempt to cast the values in the index to a VARCHAR.
            Note that conversion between BYTE data and other types is not supported.
            Also, LOBs are not allowed to be compared.

          - When using 'like' or 'regex', datatypes are casted into VARCHAR.
            This may alter the format of the value in the column(s)
            and thus whether there is a match or not. The size of the VARCHAR may also
            play a role since the casted value is truncated if the size is not big enough.
            See varchar_size under **kw: optional keyword arguments.

        RETURNS:
          teradataml DataFrame

        RAISES:
          ValueError if more than one parameter: 'items', 'like', or 'regex' is used.
          TeradataMlException if invalid argument values are given.

        EXAMPLES:

        df = DataFrame('t1')

        # retrieve columns x, y, and z in df
        df.filter(items = ['x', 'y', 'z'])

        # retrieve rows where index matches 'x', 'y', or 'z'
        df.filter(items = ['x', 'y', 'z'], axis = 0)

        # retrieve columns with a matching substring
        df.filter(like = 'x')

        # retrieve rows where index values have 'y' as a subtring
        df.filter(like = 'y', axis = 'rows')

        # give a regular expression to match column names
        df.filter(regex = '^A.+')

        # give a regular expression to match values in index
        df.filter(regex = '^A.+', axis = 0)

        # case-insensitive, ignore white space when matching index values
        df.filter(regex = '^A.+', axis = 0, match_args = 'ix')

        # case-insensitive/ ignore white space/ match up to 32 characters
        df.filter(regex = '^A.+', axis = 0, match_args = 'ix', varchar_size = 32)

      """

      # check that DataFrame has a valid axis

      if axis not in (0, 1, 'columns', 'rows'):
        raise ValueError("axis must be 0 ('rows') or 1 ('columns')")

      if self._index_label is None and axis in (0, 'rows'):
        raise AttributeError('DataFrame must have index_label set to a valid column')

      axis = 1 if axis == 'columns' or axis == 1 else 0
      errcode = MessageCodes.UNSUPPORTED_DATATYPE

      # validate items, like, regex type and value
      op = ''

      if items is not None:
          op += 'items'
          valid_value = (type(items) is list) and\
                       len(set(map(lambda x: type(x), items))) == 1

      if like is not None:
          op += 'like'
          valid_value = type(like) is str

      if regex is not None:
          op += 'regex'
          valid_value = type(regex) is str


      if op not in('items', 'like', 'regex'):
          raise ValueError('Must use exactly one of the parameters items, like, and regex.')

      if not valid_value:
          msg = 'The "items" parameter must be list of strings or tuples of column labels/index values. ' +\
                'The "regex" parameter and "like" parameter must be strings.'
          raise TeradataMlException(msg, errcode)

      # validate multi index labels for items
      if op == 'items' and axis == 0:

        num_col_indexes = len(self._index_label)
        if num_col_indexes > 1 and not all(map(lambda entry: len(entry) == num_col_indexes, items)):
          raise ValueError('tuple length in items must match length of multi index: %d' % num_col_indexes)



      # validate the optional keyword args
      if kw is not None and 'match_arg' in kw:
          if not isinstance(kw['match_arg'], str):
            msg = Messages.get_message(errcode, type(kw['match_arg']), 'match_arg', 'string')
            raise TeradataMlException(msg, errcode)

      if kw is not None and 'varchar_size' in kw:
          if not isinstance(kw['varchar_size'], int):
              msg = Messages.get_message(errcode, type(kw['varchar_size']), 'varchar_size', 'int')
              raise TeradataMlException(msg, errcode)

      # generate the sql expression
      expression = self._metaexpr._filter(axis, op, self._index_label,
                                          items = items,
                                          like = like,
                                          regex = regex,
                                          **kw)

      if axis == 1 and isinstance(expression, list):
          return self.select(expression)

      elif axis == 0 and isinstance(expression, ColumnExpression):
          return self.__getitem__(expression)

      else:
          errcode = MessageCodes.TDMLDF_INFO_ERROR
          msg = Messages.get_message(errcode)
          raise TeradataMlException(msg, errcode)

    def describe(self, percentiles=[.25, .5, .75], include=None):
        """
        Generates statistics for numeric columns. Computes the count, mean, std, min, percentiles, and max for numeric columns.

        PARAMETERS:
            percentiles (optional) - A list of values between 0 and 1.
                                     The default is [.25, .5, .75], which
                                     returns the 25th, 50th, and 75th percentiles.
            include (optional) -     Values can be either None or "all".
                                     If the value is "all", then both numeric and non-numeric columns are included.
                                     Computes count, mean, std, min, percentiles, and max for numeric columns.
                                     Computes count and unique for non-numeric columns
                                     If the value is None, only numeric columns are used for collecting statics.
                                     The default is None.


        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES:
            >>> df = DataFrame('sales')
            >>> print(df)
                          Feb   Jan   Mar   Apr    datetime
            accounts
            Blue Inc     90.0    50    95   101  2017-04-01
            Alpha Co    210.0   200   215   250  2017-04-01
            Jones LLC   200.0   150   140   180  2017-04-01
            Yellow Inc   90.0  None  None  None  2017-04-01
            Red Inc     200.0   150   140  None  2017-04-01
            Orange Inc  210.0  None  None   250  2017-04-01

            # Computes count, mean, std, min, percentiles, and max for numeric columns.
            >>> df.describe()
                      Apr      Feb     Mar     Jan
            func
            count       4        6       4       4
            mean   195.25  166.667   147.5   137.5
            std    70.971   59.554  49.749  62.915
            min       101       90      95      50
            25%    160.25    117.5  128.75     125
            50%       215      200     140     150
            75%       250    207.5  158.75   162.5
            max       250      210     215     200

            # Computes count, mean, std, min, percentiles, and max for numeric columns with 30th and 60th percentiles.
            >>> df.describe(percentiles=[.3, .6])
                      Apr      Feb     Mar     Jan
            func
            count       4        6       4       4
            mean   195.25  166.667   147.5   137.5
            std    70.971   59.554  49.749  62.915
            min       101       90      95      50
            30%     172.1      145   135.5     140
            60%       236      200     140     150
            max       250      210     215     200

            # Computes count, mean, std, min, percentiles, and max for numeric columns group by "datetime" and "Feb".
            >>> df1 = df.groupby(["datetime", "Feb"])
            >>> df1.describe()
                                     Apr   Mar   Jan
              datetime   Feb func
            2017-04-01  90.0  25%     101    95    50
                              50%     101    95    50
                              75%     101    95    50
                              count     1     1     1
                              max     101    95    50
                              mean    101    95    50
                              min     101    95    50
                              std    None  None  None
                       200.0  25%     180   140   150
                              50%     180   140   150
                              75%     180   140   150
                              count     1     1     1
                              max     180   140   150
                              mean    180   140   150
                              min     180   140   150
                              std    None  None  None
                       210.0  25%     250   215   200
                              50%     250   215   200
                              75%     250   215   200
                              count     2     1     1
                              max     250   215   200
                              mean    250   215   200
                              min     250   215   200
                              std       0  None  None
            2018-10-15 200.0  25%    None   140   150
                              50%    None   140   150
                              75%    None   140   150
                              count     0     1     1
                              max    None   140   150
                              mean   None   140   150
                              min    None   140   150
                              std    None  None  None

            # Computes count, mean, std, min, percentiles, and max for numeric columns and
            # computes count and unique for non-numeric columns
            >>> df.describe(include="all")
                       Mar      Feb datetime     Jan accounts     Apr
            func
            count        4        6        6       4        6       4
            unique    None     None        2    None        6    None
            mean     147.5  166.667     None   137.5     None  195.25
            std     49.749   59.554     None  62.915     None  70.971
            min         95       90     None      50     None     101
            25%     128.75    117.5     None     125     None  160.25
            50%        140      200     None     150     None     215
            75%     158.75    207.5     None   162.5     None     250
            max        215      210     None     200     None     250
        """
        function_label = "func"
        try:
            # percentiles must be a list of values between 0 and 1.
            if not isinstance(percentiles, list) or not all(p > 0 and p < 1 for p in percentiles):
                raise TeradataMlException(
                    Messages.get_message(MessageCodes.INVALID_ARG_VALUE, percentiles, "percentiles", "percentiles must be a list of values between 0 and 1"),
                    MessageCodes.INVALID_ARG_VALUE)
            # include must be either None or "all".
            if include is not None and include.lower() != "all":
                raise TeradataMlException(
                    Messages.get_message(MessageCodes.INVALID_ARG_VALUE, include, "include", "include must be either None or 'all'"),
                    MessageCodes.INVALID_ARG_VALUE)

            groupby_column_list = None
            if isinstance(self, DataFrameGroupBy):
                groupby_column_list = self.groupby_column_list

            if self._table_name is None:
                self._table_name = df_utils._execute_node_return_db_object_name(self._nodeid)

            # Construct the aggregate query.
            agg_query = df_utils._construct_describe_query(self._table_name, self._metaexpr, percentiles, function_label, groupby_column_list, include)
            if groupby_column_list is not None:
                sort_cols = [i for i in groupby_column_list]
                sort_cols.append(function_label)
                df = DataFrame.from_query(agg_query, index_label=sort_cols)
                df2 = df.sort(sort_cols)
                df2._metaexpr._n_rows = 100
                return df2
            else:
                return DataFrame.from_query(agg_query, index_label=function_label)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err


    def min(self):
        """
        Returns column-wise minimum value of the dataframe.

        PARAMETERS:
            None

        RETURNS :
            teradataml DataFrame object with min()
            operation performed.

        RAISES :
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If min() operation fails to
                                         generate dataframe.

                Possible Value:
                Unable to perform 'min()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the min() operation
                doesn't support all the columns in the dataframe.

                Possible Value :
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'min' operation.

        EXAMPLES :
            >> table_name = "employee_info"
            >> df1 = DataFrame(table_name)
            >> df1
                            first_name marks   dob joined_date
                employee_no
                100               abcd  None  None        None
                101              abcde  None  None  1902-05-12
                112               None  None  None  2018-05-12

            >> df2 = df1.min()
            >> df2
                  min_employee_no min_first_name min_marks min_dob min_joined_date
                0             100           abcd      None    None      1902-05-12

            >> df3 = df1.select(['employee_no', 'first_name', 'joined_date'])
            >> df4 = df3.min()
            >> df4
                  min_employee_no min_first_name min_joined_date
                0             100           abcd      1902-05-12
        """

        return self._get_dataframe_aggregate(operation = 'min')

    def max(self):
        """
        Returns column-wise maximum value of the dataframe.

        PARAMETERS:
            None

        RETURNS :
            teradataml DataFrame object with max()
            operation performed.

        RAISES :
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If max() operation fails to
                                         generate dataframe.

                Possible Value:
                Unable to perform 'max()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the max() operation
                doesn't support all the columns in the dataframe.

                Possible Value :
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'max' operation.

        EXAMPLES :
            >> table_name = "employee_info"
            >> df1 = DataFrame(table_name)
            >> df1
                            first_name marks   dob joined_date
                employee_no
                100               abcd  None  None        None
                101              abcde  None  None  1902-05-12
                112               None  None  None  2018-05-12

            >> df2 = df1.max()
                  max_employee_no max_first_name max_marks max_dob max_joined_date
                0             112          abcde      None    None      2018-05-12

            >> df3 = df1.select(['employee_no', 'first_name', 'joined_date'])
            >> df4 = df3.max()
            >> df4
                  max_employee_no max_first_name max_joined_date
                0             112          abcde      2018-05-12
        """

        return self._get_dataframe_aggregate(operation = 'max')

    def mean(self):
        """
        Returns column-wise mean value of the dataframe.

        PARAMETERS:
            None

        RETURNS :
            teradataml DataFrame object with mean()
            operation performed.

        RAISES :
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If mean() operation fails to
                                         generate dataframe.

                Possible Value:
                Unable to perform 'mean()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the mean() operation
                doesn't support all the columns in the dataframe.

                Possible Value :
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'mean' operation.

        EXAMPLES :
            >> table_name = "employee_info"
            >> df1 = DataFrame(table_name)
            >> df1
                            first_name marks   dob joined_date
                employee_no
                100               abcd  None  None        None
                101              abcde  None  None  1902-05-12
                112               None  None  None  2018-05-12

            >> df2 = df1.select(['employee_no', 'marks', 'first_name'])
            >> df2.mean()
                   mean_employee_no mean_marks
                0        104.333333       None
        """

        return self._get_dataframe_aggregate(operation='mean')

    def sum(self):
        """
        Returns column-wise sum value of the dataframe.

        PARAMETERS:
            None

        RETURNS :
            teradataml DataFrame object with sum()
            operation performed.

        RAISES :
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If sum() operation fails to
                                         generate dataframe.

                Possible Value:
                Unable to perform 'sum()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the sum() operation
                doesn't support all the columns in the dataframe.

                Possible Value :
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'sum' operation.

        EXAMPLES :
            >> table_name = "employee_info"
            >> df1 = DataFrame(table_name)
            >> df1
                            first_name marks   dob joined_date
                employee_no
                100               abcd  None  None        None
                101              abcde  None  None  1902-05-12
                112               None  None  None  2018-05-12

            >> df1.sum()
                  sum_employee_no sum_marks
                0             313      None

        Note :  teradataml doesn't support sum operation on
                character-like columns.

        """

        return self._get_dataframe_aggregate(operation='sum')

    def count(self):
        """
        Returns column-wise count of the dataframe.

        PARAMETERS:
            None

        RETURNS :
            teradataml DataFrame object with count()
            operation performed.

        RAISES :
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If count() operation fails to
                                         generate dataframe.

                Possible Value:
                Unable to perform 'count()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the count() operation
                doesn't support all the columns in the dataframe.

                Possible Value :
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'count' operation.

        EXAMPLES :
            >> table_name = "employee_info"
            >> df1 = DataFrame(table_name)
            >> df1
                            first_name marks   dob joined_date
                employee_no
                100               abcd  None  None        None
                101              abcde  None  None  1902-05-12
                112               None  None  None  2018-05-12

            >> df2 = df1.select(['employee_no', 'first_name', 'marks'])
            >> df2.count()
                  count_employee_no count_first_name count_marks
                0                 3                2           0
        """

        return self._get_dataframe_aggregate(operation = 'count')

    def std(self):
        """
        Returns column-wise sample standard deviation value of the
        dataframe.

        PARAMETERS:
            None

        RETURNS :
            teradataml DataFrame object with std()
            operation performed.

        RAISES :
            1. TDMLDF_AGGREGATE_FAILED - If std() operation fails to
                                         generate dataframe.

                Possible Value:
                Unable to perform 'std()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the std() operation
                doesn't support all the columns in the dataframe.

                Possible Value :
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'std' operation.

        EXAMPLES :
            >> table_name = "employee_info"
            >> df1 = DataFrame(table_name)
            >> df1
                            first_name marks   dob joined_date
                employee_no
                100               abcd  None  None        None
                101              abcde  None  None  1902-05-12
                112               None  None  None  2018-05-12

            >> df2 = df1.select(['employee_no', 'first_name', 'marks', 'dob'])
            >> df2.std()
                   std_employee_no std_marks std_dob
                0         6.658328      None    None
        """

        return self._get_dataframe_aggregate(operation = 'std')

    def agg(self, func = None):
        """
        PARAMETERS:
            func -  (Required) Specifies the function(s) to apply
                    on DataFrame columns.

                    Valid values for func are:
                    'count', 'sum', 'min', 'max', 'mean', 'std', 'percentile', 'unique'

                    Acceptable formats for function(s) are
                    string, dictionary or list of strings/functions.

                    Accepted combinations are:
                    1. String function name
                    2. List of string functions
                    3. Dictionary containing column name as key and
                       aggregate function name (string or list of
                       strings) as value

        RETURNS :
            teradataml DataFrame object with operations
            mentioned in parameter 'func' performed on specified
            columns.

        RAISES :
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If operations on given columns
                    fail to generate dataframe.

                Possible Value:
                Unable to perform 'agg()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the provided
                aggregate operations do not support specified columns.

                Possible Value :
                No results. Below is/are the error message(s):
                All selected columns [(col1 - VARCHAR)] is/are
                unsupported for 'sum' operation.

            3. TDMLDF_INVALID_AGGREGATE_OPERATION - If the aggregate
                operation(s) received in parameter 'func' is/are
                invalid.

                Possible Value :
                Invalid aggregate operation(s): minimum, counter.
                Valid aggregate operation(s): count, max, mean, min,
                std, sum.

            4. TDMLDF_AGGREGATE_INVALID_COLUMN - If any of the columns
                specified in 'func' is not present in the dataframe.

                Possible Value :
                Invalid column(s) given in parameter func: col1.
                Valid column(s) : A, B, C, D.

            5. MISSING_ARGS - If the argument 'func' is missing.

                Possible Value :
                Following required arguments are missing: func.

            6. UNSUPPORTED_DATATYPE - If the argument 'func' is not of
                valid datatype.

                Possible Value :
                Invalid type(s) passed to argument 'func', should be:"\
                             "['str', 'list', 'dict'].

        EXAMPLES :
            >> table_name = "employee_info"
            >> df = DataFrame(table_name)
            >> df
                            first_name marks   dob joined_date
                employee_no
                100               abcd  None  None        None
                101              abcde  None  None  1902-05-12
                112               None  None  None  2018-05-12

            # Dictionary of column names to string function/list of string functions as parameter
            >> df.agg({'employee_no' : ['min', 'sum'], 'first_name' : ['min', 'mean']})
                  min_employee_no sum_employee_no min_first_name
                0             100             313           abcd

            # List of string functions as parameter
            >> df.agg(['min', 'sum'])
                  min_employee_no sum_employee_no min_first_name min_marks sum_marks min_dob min_joined_date
                0             100             313           abcd      None      None    None      1902-05-12

            # A string function as parameter
            >> df.agg('mean')
                   mean_employee_no mean_marks mean_dob mean_joined_date
                0        104.333333       None     None       1960-05-11

            >> df1 = df.select(['employee_no', 'first_name', 'joined_date'])
            >> df1.agg(['mean', 'unique'])
                   mean_employee_no unique_employee_no unique_first_name mean_joined_date unique_joined_date
                0        104.333333                  3                 2       1960-05-11                  2

            >> df.agg('percentile')
                  percentile_employee_no percentile_marks
                0                    101             None

            # Using another table 'df_sales' (having repeated values) to demonstrate operations
            # 'unique' and 'percentile'.
            >> df = DataFrame('df_sales')
            >> df
                              Feb   Jan   Mar   Apr    datetime
                accounts
                Yellow Inc   90.0  None  None  None  2017-04-01
                Alpha Co    210.0   200   215   250  2017-04-01
                Jones LLC   200.0   150   140   180  2017-04-01
                Orange Inc  210.0  None  None   250  2017-04-01
                Blue Inc     90.0    50    95   101  2017-04-01
                Red Inc     200.0   150   140  None  2017-04-01

            >> df.agg('percentile')
                   percentile_Feb percentile_Jan percentile_Mar percentile_Apr
                0           200.0            150            140            215

            >> df.agg('unique')
                  unique_accounts unique_Feb unique_Jan unique_Mar unique_Apr unique_datetime
                0               6          3          3          3          3               1
        """

        if func is None:
            raise TeradataMlException(Messages.get_message(MessageCodes.MISSING_ARGS, "func"),
                                      MessageCodes.MISSING_ARGS)

        if not isinstance(func, str) and not isinstance(func, list) and not isinstance(func, dict):
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE,
                                'func', ['str', 'list', 'dict']), MessageCodes.UNSUPPORTED_DATATYPE)

        return self._get_dataframe_aggregate(func)

    def _get_dataframe_aggregate(self, operation):
        """
        Returns the DataFrame given the aggregate operation or list of
        operations or dictionary of column names -> operations.

        PARAMETERS:
            operation - (Required) Specifies the function(s) to be
                    applied on teradataml DataFrame columns.
                    Acceptable formats for function(s) are string,
                    dictionary or list of strings/functions.
                    Accepted combinations are:
                    1. String function name
                    2. List of string functions
                    3. Dictionary containing column name as key and
                       aggregate function name (string or list of
                       strings) as value

        RETURNS :
            teradataml DataFrame object with required
            operations mentioned in 'operation' parameter performed.

        RAISES :
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If operations on given columns
                    fail to generate dataframe.

                Possible Value:
                Unable to perform 'agg()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the provided
                aggregate operations do not support specified columns.

                Possible Value :
                No results. Below is/are the error message(s):
                All selected columns [(col1 - VARCHAR)] is/are
                unsupported for 'sum' operation.

            3. TDMLDF_INVALID_AGGREGATE_OPERATION - If the aggregate
                operation(s) received in parameter 'operation' is/are
                invalid.

                Possible Value :
                Invalid aggregate operation(s): minimum, counter.
                Valid aggregate operation(s): count, max, mean, min,
                std, sum.

            4. TDMLDF_AGGREGATE_INVALID_COLUMN - If any of the columns
                specified in the parameter 'operation' is not present
                in the dataframe.

                Possible Value :
                Invalid column(s) given in parameter func: col1.
                Valid column(s) : A, B, C, D.

        EXAMPLES :
            df = _get_dataframe_aggregate(operation = 'mean')
            or
            df = _get_dataframe_aggregate(operation = ['mean', 'min'])
            or
            df = _get_dataframe_aggregate(operation = {'col1' :
                                    ['mean', 'min'], 'col2' : 'count'})
        """

        try:
            col_names, col_types = df_utils._get_column_names_and_types_from_metaexpr(self._metaexpr)
            # Remove columns from metaexpr before passing to stated aggr func if dataframe
            # is of DataFrameGroupBy type so that no duplicate columns shown in result
            groupby_col_names = []
            groupby_col_types = []
            if isinstance(self, DataFrameGroupBy):
                new_colindex = []
                for col in col_names:
                    if (col in self.groupby_column_list):
                        colindex = col_names.index(col)
                        new_colindex.append(colindex)
                for index in sorted(new_colindex, reverse=True):
                    groupby_col_names.append(col_names[index])
                    groupby_col_types.append(col_types[index])
                    del col_names[index]
                    del col_types[index]

            aggregate_expression, new_column_names, new_column_types = \
                        df_utils._construct_sql_expression_for_aggregations(col_names, col_types,
                                                                            operation)

            if isinstance(operation, dict) or isinstance(operation, list):
                operation = 'agg'

            aggregate_node_id = self._aed_utils._aed_aggregate(self._nodeid, aggregate_expression,
                                                               operation)
            new_column_names = groupby_col_names + new_column_names
            new_column_types = groupby_col_types + new_column_types

            new_metaexpr = UtilFuncs._get_metaexpr_using_columns(aggregate_node_id,
                                                                 zip(new_column_names,
                                                                     new_column_types))
            return DataFrame._from_node(aggregate_node_id, new_metaexpr, self._index_label)

        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(
                MessageCodes.TDMLDF_AGGREGATE_FAILED, str(err.exception)).format(operation),
                                      MessageCodes.TDMLDF_AGGREGATE_FAILED) from err

    def __repr__(self):
        """
        Returns the string representation for a teradataml DataFrame instance.
        The string contains:
            1. Column names of the dataframe.
            2. At most the first no_of_rows rows of the dataframe.
            3. A default index for row numbers.

        NOTES:
          - This makes an explicit call to get rows from the database.
          - To change number of rows to be printed set the max_rows option in options.display.display
          - Default value of max_rows is 10

        EXAMPLES:
            df = DataFrame.from_table("table1")
            print(df)

            df = DataFrame.from_query("select col1, col2, col3 from table1")
            print(df)
        """
        try:

            # Generate/Execute AED nodes
            if self._table_name is None:
                self._table_name = df_utils._execute_node_return_db_object_name(self._nodeid, self._metaexpr)

            query = repr(self._metaexpr) + ' FROM ' + self._table_name

            if self._orderby is not None:
                query += ' ORDER BY ' + self._orderby

            context = tdmlctx.get_context()
            if self._index_label:
                pandas_df = pd.read_sql_query(query, context, index_col = self._index_label)
            else:
                pandas_df = pd.read_sql_query(query, context)

            if self._undropped_index is not None:
                for col in self._undropped_index:
                    pandas_df.insert(0, col, pandas_df.index.get_level_values(col).tolist(), allow_duplicates = True)

            return pandas_df.to_string()

        except TeradataMlException:
            raise

        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR) + str(err),
                                      MessageCodes.TDMLDF_INFO_ERROR) from err

    def select(self, select_expression):
        """
        Select required columns from DataFrame using an expression.
        Returns a new teradataml DataFrame with selected columns only.
        PARAMETERS:

            select_expression - String or List representing columns to select.
            Data Types Accepted: String/List
            Required: Yes

            The following formats (only) are supported for select_expression:

            A] Single Column String: df.select("col1")
            B] Single Column List: df.select(["col1"])
            C] Multi-Column List: df.select(['col1', 'col2', 'col3'])
            D] Multi-Column List of List: df.select([["col1", "col2", "col3"]])

            Column Names ("col1", "col2"..) are Strings representing database table Columns.
            All Standard Teradata Data-Types for columns supported: INTEGER, VARCHAR(5), FLOAT.

            Note: Multi-Column selection of the same column such as df.select(['col1', 'col1']) is not supported.

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException (TDMLDF_SELECT_INVALID_COLUMN, TDMLDF_SELECT_INVALID_FORMAT,
                                 TDMLDF_SELECT_DF_FAIL, TDMLDF_SELECT_EXPR_UNSPECIFIED,
                                 TDMLDF_SELECT_NONE_OR_EMPTY)

        EXAMPLES:
            >>> df
               masters   gpa     stats programming admitted
            id
            5       no  3.44    novice      novice        0
            7      yes  2.33    novice      novice        1
            22     yes  3.46    novice    beginner        0
            17      no  3.83  advanced    advanced        1
            13      no  4.00  advanced      novice        1
            19     yes  1.98  advanced    advanced        0
            36      no  3.00  advanced      novice        0
            15     yes  4.00  advanced    advanced        1
            34     yes  3.85  advanced    beginner        0
            40     yes  3.95    novice    beginner        0

            A] Single String Column
            >>> df.select("id")
            Empty DataFrame
            Columns: []
            Index: [22, 34, 13, 19, 15, 38, 26, 5, 36, 17]

            B] Single Column List
            >>> df.select(["id"])
            Empty DataFrame
            Columns: []
            Index: [15, 26, 5, 40, 22, 17, 34, 13, 7, 38]

            C] Multi-Column List
            >>> df.select(["id", "masters", "gpa"])
               masters   gpa
            id
            5       no  3.44
            36      no  3.00
            15     yes  4.00
            17      no  3.83
            13      no  4.00
            40     yes  3.95
            7      yes  2.33
            22     yes  3.46
            34     yes  3.85
            19     yes  1.98

            D] Multi-Column List of List
            >>> df.select([['id', 'masters', 'gpa']])
               masters   gpa
            id
            5       no  3.44
            34     yes  3.85
            13      no  4.00
            40     yes  3.95
            22     yes  3.46
            19     yes  1.98
            36      no  3.00
            15     yes  4.00
            7      yes  2.33
            17      no  3.83
        """
        try:
            if self._metaexpr is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR)

            # If invalid, appropriate exception raised; Processing ahead only for valid expressions
            select_exp_col_list = self.__validate_select_expression(select_expression)

            # Constructing New Column names & Types for selected columns ONLY using Parent _metaexpr
            col_names_types = df_utils._get_required_columns_types_from_metaexpr(self._metaexpr, select_exp_col_list)

            meta = sqlalchemy.MetaData()
            aed_utils = AedUtils()

            column_expression = ','.join(select_exp_col_list)
            sel_nodeid = aed_utils._aed_select(self._nodeid, column_expression)

            # Constructing new Metadata (_metaexpr) without DB; using dummy select_nodeid
            cols = (Column(col_name, col_type) for col_name, col_type in col_names_types.items())
            t = Table(sel_nodeid, meta, *cols)
            new_metaexpr = _MetaExpression(t)

            return DataFrame._from_node(sel_nodeid, new_metaexpr, self._index_label)

        except TeradataMlException:
            raise

        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_DF_FAIL, str(err.exception)),
                                      MessageCodes.TDMLDF_SELECT_DF_FAIL) from err

    def __validate_select_expression(self, select_expression):
        """
        This is an internal function used to validate the select expression for the Select API.
        When the select expression is valid, a list of valid columns to be selected is returned.
        Appropriate TeradataMlException is raised when validation fails.

        PARAMETERS:
            select_expression - The expression to be validated.
            Type: Single String or List of Strings or List of List (single-level)
            Required: Yes

        RETURNS:
            List of column name strings, when valid select_expression is passed.

        RAISES:
            TeradataMlException, when parameter validation fails.

        EXAMPLES:
            self.__validate_select_expression(select_expression = 'col1')
            self.__validate_select_expression(select_expression = ["col1"])
            self.__validate_select_expression(select_expression = [['col1', 'col2', 'col3']])
        """
        tdp = preparer(td_dialect)

        if select_expression is None:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_EXPR_UNSPECIFIED),
                                      MessageCodes.TDMLDF_SELECT_EXPR_UNSPECIFIED)

        else:
            # _extract_select_string returns column list only if valid; else raises appropriate exception
            select_exp_col_list = df_utils._extract_select_string(select_expression)
            df_column_list = [tdp.quote("{0}".format(column.name)) for column in self._metaexpr.c]

            # TODO: Remove this check when same column multiple selection enabled
            if len(select_exp_col_list) > len(df_column_list):
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_INVALID_COLUMN, ', '.join(df_column_list)),
                                          MessageCodes.TDMLDF_SELECT_INVALID_COLUMN)

            all_cols_exist =  all(col in df_column_list for col in select_exp_col_list)

            if not all_cols_exist:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_INVALID_COLUMN, ', '.join(df_column_list)),
                                          MessageCodes.TDMLDF_SELECT_INVALID_COLUMN)

            return select_exp_col_list

    def to_pandas(self, index_column = None, num_rows = 99999):
        """
        Returns a Pandas DataFrame for the corresponding teradataml DataFrame Object.

        Optionally, when an index_column parameter is provided, the specified column is used
        as the Pandas index; otherwise the teradataml DataFrame object's index attribute is used
        as the Pandas index if it exists; otherwise the Teradata database table is checked for a Primary Index.
        In case none of the above exist, a default integer index is used.

        PARAMETERS:

            index_column (optional) - String or List (of strings) representing column(s) to be used as Pandas index.
                Data Types: String or List of strings.
                Default: Integer index

            num_rows (optional) - The number of rows to retrieve from DataFrame while creating Pandas Dataframe.
                Data Type: Integer
                Default: 99999

        RETURNS:
            Pandas DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:

            Teradata supports the following formats:

            A] No parameter(s): df.to_pandas()
            B] Single index_column parameter: df.to_pandas(index_column = "col1")
            C] Multiple index_column (list) parameters: df.to_pandas(index_column = ['col1', 'col2'])
            D] Only num_rows parameter specified:  df.to_pandas(num_rows = 100)
            E] Both index_column & num_rows specified: df.to_pandas(index_column = 'col1', num_rows = 100)

            Column names ("col1", "col2"..) are strings representing database table Columns.
            It supports all standard Teradata data types for columns: INTEGER, VARCHAR(5), FLOAT etc.
            df is a Teradata DataFrame object: df = DataFrame.from_table('df_admissions_train')

                >>> df = DataFrame.from_table('df_admissions_train')
                >>> df
                  id masters gpa  stats    programming admitted
                0 26 yes     3.57 advanced advanced    1
                1 34 yes     3.85 advanced beginner    0
                2 40 yes     3.95 novice   beginner    0
                3 14 yes     3.45 advanced advanced    0
                4 29 yes     4.0  novice   beginner    0
                5 6  yes     3.5  beginner advanced    1
                6 36 no      3.0  advanced novice      0
                7 32 yes     3.46 advanced beginner    0
                8 5  no      3.44 novice   novice      0

                >>> pandas_df = df.to_pandas()
                >>> pandas_df
                     id   masters gpa   stats     programming  admitted
                0    5.0      no  3.44    novice      novice       0.0
                1    8.0      no  3.60  beginner    advanced       1.0
                2   30.0     yes  3.79  advanced      novice       0.0
                3   25.0      no  3.96  advanced    advanced       1.0
                4   20.0     yes  3.90  advanced    advanced       1.0
                5   27.0     yes  3.96  advanced    advanced       0.0
                ...

                >>> pandas_df = df.to_pandas(index_column = 'id')
                >>> pandas_df
                     masters   gpa     stats programming  admitted
                id
                5.0       no  3.44    novice      novice       0.0
                3.0       no  3.70    novice    beginner       1.0
                1.0      yes  3.95  beginner    beginner       0.0
                20.0     yes  3.90  advanced    advanced       1.0
                8.0       no  3.60  beginner    advanced       1.0
                ...

                >>> pandas_df = df.to_pandas(index_column = ['id', 'gpa'])
                >>> pandas_df
                            masters     stats programming  admitted
                id   gpa
                5.0  3.44      no    novice      novice       0.0
                3.0  3.70      no    novice    beginner       1.0
                1.0  3.95     yes  beginner    beginner       0.0
                20.0 3.90     yes  advanced    advanced       1.0
                8.0  3.60      no  beginner    advanced       1.0
                ...

                >>> pandas_df = df.to_pandas(index_column = 'id', num_rows = 3)
                    OR
                    pandas_df = df.to_pandas('id', 3)

                >>> pandas_df
                     masters   gpa     stats programming  admitted
                id
                5.0       no  3.44    novice      novice       0.0
                3.0       no  3.70    novice    beginner       1.0
                1.0      yes  3.95  beginner    beginner       0.0

        """
        try:
            pandas_df = None

            df_utils._validate_to_pandas_parameters(self, index_column, num_rows)

            if self._table_name is None:
                # Un-executed - Generate/Execute Nodes & Set Table Name
                if self._nodeid:
                    self._table_name = df_utils._execute_node_return_db_object_name(self._nodeid, self._metaexpr)
                else:
                    raise TeradataMlException(Messages.get_message(MessageCodes.TO_PANDAS_FAILED),
                                              MessageCodes.TO_PANDAS_FAILED)

            pandas_df = df_utils._get_pandas_dataframe(self._table_name, index_column,
                                                       self._index_label, num_rows, self._orderby)
            if pandas_df is not None:
                return pandas_df
            else:
                raise TeradataMlException(Messages.get_message(MessageCodes.EMPTY_DF_RETRIEVED),
                                              MessageCodes.EMPTY_DF_RETRIEVED)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TO_PANDAS_FAILED) + str(err),
                                      MessageCodes.TO_PANDAS_FAILED) from err

    def __validate_to_pandas_parameters(self, index_column, num_rows):
        """
        Validates the to_pandas API parameters.

        PARAMETERS:
            index_column - User Specified String/List specifying columns to use as Pandas Index.
            num_rows - Integer specifying number of rows to use to create Pandas Dataframe;

        EXAMPLES:
             __validate_to_pandas_parameters(index_column, num_rows)

        RETURNS:
            None

        RAISES:
            TeradataMlException (TDMLDF_INFO_ERROR, UNSUPPORTED_DATATYPE,
                                 INVALID_ARG_VALUE, DF_LABEL_MISMATCH)
        """

        if self._metaexpr is not None:
            df_column_list = [col.name for col in self._metaexpr.c]
        else:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR),
                                      MessageCodes.TDMLDF_INFO_ERROR)

        if index_column is not None:
            # Check Format validity for index_column
            if not (isinstance(index_column, str) or isinstance(index_column, list)):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "index_column",
                                                               "string or list of strings"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

            self.__check_column_in_dataframe(index_column, 'index_column')

        # Check if TDML DF has appropriate index_label set when required
        df_index_label = self._index_label

        if df_index_label is not None:
            if isinstance(df_index_label, str):
                if df_index_label.lower() not in df_column_list:
                    raise TeradataMlException(Messages.get_message(MessageCodes.DF_LABEL_MISMATCH), MessageCodes.DF_LABEL_MISMATCH)
            elif isinstance(df_index_label, list):
                for index_label in df_index_label:
                    if index_label.lower() not in df_column_list:
                        raise TeradataMlException(Messages.get_message(MessageCodes.DF_LABEL_MISMATCH), MessageCodes.DF_LABEL_MISMATCH)

        # Check Format validity for num_rows
        if num_rows is not None:
            if not isinstance(num_rows, int):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "num_rows", "int"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)
            elif num_rows <= 0:
                awuObj = AnalyticsWrapperUtils()
                arg_name = awuObj._deparse_arg_name(num_rows)
                raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,num_rows, arg_name,
                                                               "integer value greater than zero"),
                                          MessageCodes.INVALID_ARG_VALUE)

    def __check_column_in_dataframe(self, column_names, error_message_arg = 'Dataframe column name'):
        """
        Internal Utility function to check if given column(s) (String or list of strings)
        exists in the Dataframe columns or not.

        PARAMETERS:
            column_names - String or List of strings specifying column names to be checked.

            error_message_arg (optional) - Specifies column name/argument to be used in the
                exception message of the format: "Invalid value passed for argument: error_message_arg"
                Default: 'Dataframe column name'

        RETURNS:
            True, when all columns specified are valid (exist in DataFrame)
            TeradataMlException, otherwise.

        RAISES:
            TeradataMlException (INVALID_ARG_VALUE)

        EXAMPLES:
            __check_column_in_dataframe('column_name')
            __check_column_in_dataframe(['column_name1', 'column_name2'])
            __check_column_in_dataframe('column_name', error_message_arg = 'index_column')

        """
        if self._metaexpr is not None:
            df_column_list = [col.name for col in self._metaexpr.c]

        if isinstance(column_names, list):
            for column in column_names:
                #if not isinstance(column, str) or (column.lower() not in df_column_list):
                if not isinstance(column, str) or not df_utils._check_column_exists(column.lower(), df_column_list):
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_COLUMN_NOT_FOUND,column,""),
                                          MessageCodes.TDMLDF_COLUMN_NOT_FOUND)

        elif isinstance(column_names, str):
            #if column_names.lower() not in df_column_list:
            if not df_utils._check_column_exists(column_names.lower(), df_column_list):
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_COLUMN_NOT_FOUND, column_names, ""),
                                          MessageCodes.TDMLDF_COLUMN_NOT_FOUND)
        return True

    def join(self, other, on, how="left", lsuffix=None, rsuffix=None):
        """
        Joins two different Teradata DataFrames together.
        Supported join operations are:
            Inner join: Returns only matching rows, non matching rows eliminated
            Left outer join: Returns all matching rows plus non matching rows from the left table
            Right outer join: Returns all matching rows plus non matching rows from the right table
            Full outer join: Returns all rows from both tables, including non matching rows

        PARAMETERS:
           other   - Required argument. Specifies right teradataml dataframe on which joins to be perform.
           on      - Required argument. Specifies list of conditions that indicate the columns to be join keys.
                     Examples:
                         1. ["a","b"] indicates df1.a = df2.a and df1.b = df2.b.
                         2. ["a = b", "c = d"] indicates df1.a = df2.b and df1.c = df2.d.
           how     - Optional argument. Specifies the type of join to perform. Supports inner, left, right and outer joins.
                     Default value is "left".
           lsuffix - Optional argument. Specifies suffix to be added to the left table columns.
                     Default value is "None".
           rsuffix - Optional argument. Specifies suffix to be added to the right table columns.
                     Default value is "None".

        RAISES:
          TeradataMlException

        RETURNS:
           teradataml DataFrame

        EXAMPLES:
           df1 = DataFrame("table1")
           df2 = DataFrame("table2")
           df1.join(other = df2, on = ["a","c=d"], how = "left", lsuffix = "t1", rsuffix = "t2")
           df1.join(other = df2, on = ["a","c"], how = "right", lsuffix = "t1", rsuffix = "t2")
           df1.join(other = df2, on = ["a=b","c"], how = "inner", lsuffix = "t1", rsuffix = "t2")
           df1.join(other = df2, on = ["a=c","c=b"], how = "full", lsuffix = "t1", rsuffix = "t2")
        """
        if not isinstance(other, DataFrame):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "other", "TeradataML DataFrame"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        if not isinstance(how, str):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "how", "str"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        if how.lower() not in TeradataConstants.TERADATA_JOINS.value:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.INVALID_ARG_VALUE, how, "how", TeradataConstants.TERADATA_JOINS.value),
                MessageCodes.INVALID_ARG_VALUE)

        for column in self.columns:
            if column in other.columns:
                if lsuffix is None or rsuffix is None:
                    raise TeradataMlException(
                        Messages.get_message(MessageCodes.TDMLDF_REQUIRED_TABLE_ALIAS),MessageCodes.TDMLDF_REQUIRED_TABLE_ALIAS)

        if lsuffix is None:
            lsuffix = "df1"

        if rsuffix is None:
            rsuffix = "df2"

        if isinstance(lsuffix,str) is False or isinstance(rsuffix,str) is False:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "'lsuffix' or 'rsuffix'", "'str'"),
                MessageCodes.UNSUPPORTED_DATATYPE)
        # Both suffix shuold not be equal to perform join
        if lsuffix == rsuffix:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.TDMLDF_INVALID_TABLE_ALIAS, "'lsuffix' and 'rsuffix'"),
                MessageCodes.TDMLDF_INVALID_TABLE_ALIAS)


        df1_join_columns = []
        df2_join_columns = []

        if isinstance(on, str):
            on = [on]

        if not isinstance(on, list):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "on", "'str' or 'list'"),
                MessageCodes.TDMLDF_UNKNOWN_TYPE)

        # Forming join condition
        for condition in on:
            if isinstance(condition, str):
                if "=" in condition:
                    columns = [column.strip() for column in condition.split(sep="=") if len(column) > 0]
                    df1_join_columns.append(self.__add_alias_to_column(columns[0], self.columns,lsuffix, "left"))
                    df2_join_columns.append(self.__add_alias_to_column(columns[1], other.columns, rsuffix, "right"))

                else:
                    df1_join_columns.append(self.__add_alias_to_column(condition, self.columns, lsuffix, "left"))
                    df2_join_columns.append(self.__add_alias_to_column(condition, other.columns,  rsuffix, "right"))
            else:
                raise TeradataMlException(
                    Messages.get_message(MessageCodes.TDMLDF_INVALID_JOIN_CONDITION, condition),
                    MessageCodes.TDMLDF_INVALID_JOIN_CONDITION)

        condition = '{0} = {1}'
        join_condition = ' and '.join([condition.format(df1_join_column, df2_join_column)
                                       for df1_join_column, df2_join_column in zip(df1_join_columns, df2_join_columns)])

        df1_columns_types = df_utils._get_required_columns_types_from_metaexpr(self._metaexpr)
        df2_columns_types = df_utils._get_required_columns_types_from_metaexpr(other._metaexpr)

        select_columns = []
        new_metaexpr_columns_types = {}

        for column in self.columns:
            if df_utils._check_column_exists(column, other.columns):
                df1_column_with_suffix = self.__check_and_return_new_column_name(lsuffix, column, other.columns, "right")
                select_columns.append("{0} as {1}".format(self.__add_suffix(column,lsuffix),df1_column_with_suffix))

                df2_column_with_suffix = self.__check_and_return_new_column_name(rsuffix, column, self.columns, "left")
                select_columns.append("{0} as {1}".format(self.__add_suffix(column, rsuffix),df2_column_with_suffix))

                # As we are creating new column name, adding it to new metadata dict for new dataframe from join
                self.__add_column_type_item_to_dict(new_metaexpr_columns_types,
                                               UtilFuncs._teradata_unquote_arg(df1_column_with_suffix, "\""), column, df1_columns_types)
                self.__add_column_type_item_to_dict(new_metaexpr_columns_types,
                                                    UtilFuncs._teradata_unquote_arg(df2_column_with_suffix, "\""), column, df2_columns_types)
            else:
                # As column not present in right dataframe, directly adding column to new metadata dict.
                self.__add_column_type_item_to_dict(new_metaexpr_columns_types,
                                                    column, column, df1_columns_types)
                select_columns.append(UtilFuncs._teradata_quote_arg(column, "\""))

        for column in other.columns:
            if not df_utils._check_column_exists(column, self.columns):
                # As column not present in left dataframe, directly adding column to new metadata dict.
                self.__add_column_type_item_to_dict(new_metaexpr_columns_types,
                                                    column, column, df2_columns_types)
                select_columns.append(UtilFuncs._teradata_quote_arg(column, "\""))

        join_node_id = self._aed_utils._aed_join(self._nodeid, other._nodeid, ", ".join(select_columns),
                                                 how, join_condition, lsuffix, rsuffix)

        # Forming metadata expression
        meta = sqlalchemy.MetaData()

        # Creting sqlalchemy table expression
        t = Table(join_node_id, meta,
                  *(Column(col_name, col_type) for col_name, col_type in new_metaexpr_columns_types.items()))

        return DataFrame._from_node(join_node_id, _MetaExpression(t), self._index_label)

    def __add_alias_to_column(self, column, df_columns, alias, df_side):
        """
        This function check column exists in list of columns, if exists add suffix to column and
        adds to join columns list.

        PARAMETERS:
            column  - Column name.
            self_columns - List of left dataframe columns.
            other_columns - List of right dataframe columns.
            alias - alias to be added to column.
            df_side - Position of data frame in join (left or right).

        EXAMPLES:
            df1 = DataFrame("table1")
            df2 = DataFrame("table2")
            __add_alias_to_column("a", df1.columns, df2.columns, "t1", "left")

        RAISES:
            TDMLDF_COLUMN_NOT_FOUND
        """
        if df_utils._check_column_exists(column, df_columns):
            return  self.__add_suffix(column, alias)
        else:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.TDMLDF_COLUMN_NOT_FOUND, column, df_side),
                MessageCodes.TDMLDF_COLUMN_NOT_FOUND)

    def __add_suffix(self, column, alias):
        """
        Adds alias to column

        PARAMETERS:
            column  - Column name.
            alias - alias to be appended to column.

        EXAMPLES:
            __add_suffix("a", "t1")

        RAISES:
            None
        """
        return "{0}.{1}".format(UtilFuncs._teradata_quote_arg(alias, "\""),
                                UtilFuncs._teradata_quote_arg(column, "\""))

    def __check_and_return_new_column_name(self, suffix, column, col_list, df_side):
        """
         Check new column name alias with column exists in col_list or not, if exists throws exception else
         returns new column name.

         PARAMETERS:
             suffix  - alias to be added to column.
             column - column name.
             col_list - list of columns to check in which new column is exists or not.
             df_side - Side of the dataframe.

         EXAMPLES:
             df = DataFrame("t1")
             __check_and_return_new_column_name("df1", "column_name", df.columns, "right")

         RAISES:
             None
         """
        df1_column_with_suffix = "{0}_{1}".format(suffix,
                                                  UtilFuncs._teradata_unquote_arg(column, "\""))
        if df_utils._check_column_exists(df1_column_with_suffix, col_list):
            if df_side == "right":
                suffix_side = "lsuffix"
            else:
                suffix_side = "rsuffix"
            raise TeradataMlException(
                Messages.get_message(MessageCodes.TDMLDF_COLUMN_ALREADY_EXISTS, df1_column_with_suffix, df_side,
                                     suffix_side),
                MessageCodes.TDMLDF_COLUMN_ALREADY_EXISTS)
        return UtilFuncs._teradata_quote_arg(df1_column_with_suffix, "\"")

    def __add_column_type_item_to_dict(self, new_metadata_dict, new_column,column, column_types):
        """
        Add a column as key and datatype as a value to dictionary

        PARAMETERS:
            new_metadata_dict  - Dictionary to which new item to be added.
            new_column - key fo new item.
            column - column to which datatype to be get.
            column_types - datatypes of the columns.
        EXAMPLES:
            __add_to_column_types_dict( metadata_dict, "col1","integer")

        RAISES:
            None
        """
        try:
            new_metadata_dict[new_column] = column_types[column]
        except KeyError:
            try:
                new_metadata_dict[new_column] = column_types[UtilFuncs._teradata_quote_arg(column, "\"")]
            except KeyError:
                new_metadata_dict[new_column] = column_types[UtilFuncs._teradata_unquote_arg(column, "\"")]

    def to_sql(self, table_name, if_exists='fail', primary_index=None, temporary=False, schema_name=None):
        """
        Writes records stored in a teradataml DataFrame to a Teradata database.

        PARAMETERS:

            table_name (required): Specifies the name of the table to be created in the database.
                Type : String

            schema_name (optional): Specifies the name of the SQL schema in the database to write to.
                Type: String
                Default: None (Use default database schema).

            if_exists (optional): Specifies the action to take when table already exists in the database.
                Type : String; possible values: {'fail', 'replace', 'append'}
                    - fail: If table exists, do nothing.
                    - replace: If table exists, drop it, recreate it, and insert data.
                    - append: If table exists, insert data. Create if does not exist.
                Default : append

            primary_index (optional): Creates Teradata Table(s) with Primary index column when specified.
                Type : String or List of strings
                    Example:
                        primary_index = 'my_primary_index'
                        primary_index = ['my_primary_index1', 'my_primary_index2', 'my_primary_index3']
                Default : None
                For teradataml DataFrames, when None, no Primary Index Teradata tables are created.

            temporary (optional): Creates Teradata SQL tables as permanent or volatile.
                Type : Boolean (True or False)
                Default : False
                When True, volatile tables are created.
                When False, permanent tables are created.

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:

            from teradataml.dataframe.dataframe import DataFrame
            from teradataml.dataframe.copy_to import copy_to_sql

            df = DataFrame('test_table_name')
            df2 = df1.select(['col_name1', 'col_name2'])

            df2.to_sql('my_table_name2')

            OR

            df2.to_sql(table_name = 'my_table_name2', if_exists='append',
                       primary_index = 'my_primary_index', temporary=False, schema_name='my_schema_name')

            OR

            copy_to_sql(df2, 'my_table_name2')

            OR

            copy_to_sql(df = df2, table_name = 'my_table_name2', schema_name = 'default_schema',
                    temporary = False, primary_index = None, if_exists = 'append')
        """

        if primary_index is None and self._index_label is not None:
            primary_index = self._index_label

        return copy_to_sql(df = self, table_name = table_name, schema_name = schema_name,
                    index = False, index_label = None, temporary = temporary,
                    primary_index = primary_index, if_exists = if_exists)

    def assign(self, drop_columns = False, **kwargs):
        """
        Assign new columns to a teradataml DataFrame

        PARAMETERS:

             drop_columns (optional):  bool If True, drop columns that are not specified in assign. The default is False.
             kwargs: keyword, value pairs
                 - keywords are the column names.
                 - values can be column arithmetic expressions and int/float/string literals.

        RETURNS:

             teradataml DataFrame
             A new DataFrame with the new columns in addition to
             all the existing columns if drop_columns is equal to False.
             Otherwise, if drop_columns = True, a new DataFrame with only columns in kwargs.

        NOTES:

             - The values in kwargs cannot be callable (functions).

             - The original DataFrame is not modified.

             - Since ``kwargs`` is a dictionary, the order of your
               arguments may not be preserved. To make things predicatable,
               the columns are inserted in alphabetical order, at the end of
               your DataFrame. Assigning multiple columns within the same
               ``assign`` is possible, but you cannot reference other columns
               created within the same ``assign`` call.

             - The maximum number of columns in a DataFrame is 2048.

        RAISES:

             - ValueError when a value that is callable is given in kwargs
             - TeradataMlException when there is an internal error in DataFrame or invalid argument type

        EXAMPLES:

        df = DataFrame(...)
        c1 = df.c1
        c2 = df.c2

        df.assign(new_column = c1 + c2)
        df.assign(new_column = c1 * c2)
        df.assign(new_column = c1 / c2)
        df.assign(new_column = c1 - c2)
        df.assign(new_column = c1 % c2)

        df.assign(c1 = c2, c2 = c1)
        df.assign(c3 = c1 + 1, c4 = c2 + 1)

        df.assign(c1 = 1)
        df.assign(c3 = 'string')

        # + op is overidden for string columns
        df.assign(concatenated = string_col + 'string')

        # setting drop_columns to True will only return assigned expressions
        res = df.assign(drop_columns = True, c1 = 1)
        assert len(res.columns) == 1

        """
        # handle invalid inputs and empty input
        if not isinstance(drop_columns, bool):

            err_msg_code = MessageCodes.UNSUPPORTED_DATATYPE
            err = Messages.get_message(err_msg_code, "drop_columns", "bool")
            raise TeradataMlException(err, err_msg_code)

        if len(kwargs) == 0:
            return self

        elif len(kwargs) >= TeradataConstants['TABLE_COLUMN_LIMIT'].value:
            errcode = MessageCodes.TD_MAX_COL_MESSAGE
            raise TeradataMlException(Messages.get_message(errcode), errcode)

        allowed_types = (type(None), int, float, str, decimal.Decimal, ColumnExpression)

        for key, val in kwargs.items():

            is_allowed = lambda x: isinstance(*x) and type(x[0]) != bool
            value_type_allowed = map(is_allowed, ((val, t) for t in allowed_types))

            if callable(val):
                err = 'Unsupported callable value for key: {}'.format(key)
                raise ValueError(err)

            elif not any(list(value_type_allowed)):
                err = 'Unsupported values of type {t} for key {k}'.format(k = key, t = type(val))
                raise ValueError(err)

        if self._metaexpr is None:
            msg = Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR)
            raise TeradataMlException(msg, MessageCodes.TDMLDF_INFO_ERROR)

        try:

            # apply the assign expression
            (new_meta, result) = self._metaexpr._assign(drop_columns, **kwargs)

            # join the expressions in result
            assign_expression = ', '.join(list(map(lambda x: x[1], result)))
            new_nodeid = self._aed_utils._aed_assign(self._nodeid,
                                                     assign_expression,
                                                     AEDConstants.AED_ASSIGN_DROP_EXISITING_COLUMNS.value)
            return DataFrame._from_node(new_nodeid, new_meta, self._index_label)

        except Exception as err:
            errcode = MessageCodes.TDMLDF_INFO_ERROR
            msg = Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR)
            raise TeradataMlException(msg, errcode) from err

    def get(self, key):
        """
        Retrieve required columns from DataFrame using column name(s) as key.
        Returns a new teradataml DataFrame with requested columns only.

        PARAMETERS:

            key:
                Required Argument.
                Specifies column(s) to retrieve from the teradataml DataFrame.
                Data Types Accepted: String or List of strings.

            teradataml supports the following formats (only) for the "get" method:

            1] Single Column String: df.get("col1")
            2] Single Column List: df.get(["col1"])
            3] Multi-Column List: df.get(['col1', 'col2', 'col3'])
            4] Multi-Column List of List: df.get([["col1", "col2", "col3"]])

            Note: Multi-Column retrieval of the same column such as df.get(['col1', 'col1']) is not supported.

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> df
              id masters gpa  stats    programming admitted
            0 26 yes     3.57 advanced advanced    1
            1 34 yes     3.85 advanced beginner    0
            2 40 yes     3.95 novice   beginner    0
            3 14 yes     3.45 advanced advanced    0
            4 29 yes     4.0  novice   beginner    0
            5 6  yes     3.5  beginner advanced    1
            6 36 no      3.0  advanced novice      0
            7 32 yes     3.46 advanced beginner    0
            8 5  no      3.44 novice   novice      0

            1] Single String Column
            >>> df.get("id")
              id
            0 26
            1 34
            2 40
            3 14
            4 29

            2] Single Column List
            >>> df.get(["id"])
              id
            0 26
            1 34
            2 40
            3 14
            4 29

            3] Multi-Column List
            >>> df.get(["id", "masters", "gpa"])
              id masters gpa
            0 26 yes     3.57
            1 34 yes     3.85
            2 40 yes     3.95
            3 14 yes     3.45
            4 29 yes     4.0

            4] Multi-Column List of List
            >>> df.get([['id', 'masters', 'gpa']])
              id masters gpa
            0 26 yes     3.57
            1 34 yes     3.85
            2 40 yes     3.95
            3 14 yes     3.45
            4 29 yes     4.0
        """
        return self.select(key)

    def set_index(self, keys, drop = True, append = False):
        """
        Assigns one or more existing columns as the new index to a teradataml DataFrame.

        PARAMETERS:

            keys (required): Specifies the column name or a list of column names to use as the DataFrame index.
                Type : String or List

            drop (optional): Specifies whether or not to delete columns requested to be used as the new index.
                             When drop is True, columns are set as index and not displayed as columns.
                             When drop is False, columns are set as index; but also displayed as columns.
                Type : Boolean (True or False)
                Default: True

            append (optional): Specifies whether or not to append requested columns to the existing index.
                               When append is False, replaces existing index.
                               When append is True, retains both existing & currently appended index.
                Type : Boolean (True or False)
                Default : False

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:

            >>> df1 = DataFrame.from_table('df_admissions_train')
            >>> df1
              id masters gpa  stats    programming admitted
            0 26 yes     3.57 advanced advanced    1
            1 34 yes     3.85 advanced beginner    0
            2 40 yes     3.95 novice   beginner    0
            3 14 yes     3.45 advanced advanced    0
            4 29 yes     4.0  novice   beginner    0
            5 6  yes     3.5  beginner advanced    1
            6 36 no      3.0  advanced novice      0
            7 32 yes     3.46 advanced beginner    0
            8 5  no      3.44 novice   novice      0

            >>> df2 = df1.set_index('id')
            >>> df2
                masters gpa  stats    programming admitted
            id
            26  yes     3.57 advanced advanced    1
            34  yes     3.85 advanced beginner    0
            40  yes     3.95 novice   beginner    0
            14  yes     3.45 advanced advanced    0
            29  yes     4.0  novice   beginner    0
            6   yes     3.5  beginner advanced    1
            36  no      3.0  advanced novice      0
            32  yes     3.46 advanced beginner    0
            5   no      3.44 novice   novice      0

            >>> df3 = df1.set_index(['id', 'masters'])
            >>> df3
                        gpa  stats    programming admitted
            id  masters
            26  yes     3.57 advanced advanced    1
            34  yes     3.85 advanced beginner    0
            40  yes     3.95 novice   beginner    0
            14  yes     3.45 advanced advanced    0
            29  yes     4.0  novice   beginner    0
            6   yes     3.5  beginner advanced    1
            36  no      3.0  advanced novice      0
            32  yes     3.46 advanced beginner    0
            5   no      3.44 novice   novice      0

            >>> df4 = df3.set_index('gpa', drop = False, append = True)
            >>> df4
                             gpa   stats   programming admitted
            id  masters gpa
            26  yes     3.57 3.57  advanced advanced    1
            34  yes     3.85 3.85  advanced beginner    0
            40  yes     3.95 3.95  novice   beginner    0
            14  yes     3.45 3.45  advanced advanced    0
            29  yes     4.0  4.0   novice   beginner    0
            6   yes     3.5  3.5   beginner advanced    1
            36  no      3.0  3.0   advanced novice      0
            32  yes     3.46 3.46  advanced beginner    0
            5   no      3.44 3.44  novice   novice      0

            >>> df5 = df3.set_index('gpa', drop = True, append = True)
            >>> df5
                              stats   programming admitted
            id  masters gpa
            26  yes     3.57 advanced advanced    1
            34  yes     3.85 advanced beginner    0
            40  yes     3.95 novice   beginner    0
            14  yes     3.45 advanced advanced    0
            29  yes     4.0  novice   beginner    0
            6   yes     3.5  beginner advanced    1
            36  no      3.0  advanced novice      0
            32  yes     3.46 advanced beginner    0
            5   no      3.44 novice   novice      0

            >>> df6 = df1.set_index('id', drop = False)
            >>> df6
                id masters  gpa  stats    programming admitted
            id
            26  26  yes     3.57 advanced advanced    1
            34  34  yes     3.85 advanced beginner    0
            40  40  yes     3.95 novice   beginner    0
            14  14  yes     3.45 advanced advanced    0
            29  29  yes     4.0  novice   beginner    0
            6   6   yes     3.5  beginner advanced    1
            36  36  no      3.0  advanced novice      0
            32  32  yes     3.46 advanced beginner    0
            5   5   no      3.44 novice   novice      0

        """
        try:
            if drop not in (True, False):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "drop", "Boolean (True/False)"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

            if append not in (True, False):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "append", "Boolean (True/False)"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

            if not (isinstance(keys, str) or isinstance(keys, list)):
                raise TeradataMlException(
                    Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "keys", "String or List of strings"),
                    MessageCodes.UNSUPPORTED_DATATYPE)

            # Check & proceed only if keys (requested index_column) is a valid DataFrame column
            df_utils._check_column_in_dataframe(self, keys)

            new_index_list = self._index_label if self._index_label is not None else []

            # Creating a list with requested index labels bases on append
            if append:
                if isinstance(keys, str):
                    new_index_list.append(keys)
                elif isinstance(keys, list):
                    new_index_list.extend(keys)
            else:
                if isinstance(keys, str):
                    new_index_list = [keys]
                elif isinstance(keys, list):
                    new_index_list = keys

            # Takes care of appending already existing index
            new_index_list = list(set(new_index_list))

            # In case requested index is same as existing index, return same DF
            if new_index_list == self._index_label:
                return self

            # Creating list of undropped columns for printing
            undropped_columns = []
            if not drop:
                if isinstance(keys, str):
                    undropped_columns = [keys]
                elif isinstance(keys, list):
                    undropped_columns = keys

            if len(undropped_columns) == 0:
                undropped_columns = None

            # Assigning self attributes to newly created dataframe.
            new_df = DataFrame._from_node(self._nodeid, self._metaexpr, new_index_list, undropped_columns)
            new_df._table_name = self._table_name
            new_df._index = self._index
            return new_df

        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR),
                                      MessageCodes.TDMLDF_INFO_ERROR) from err

    def groupby(self, columns_expr):
        """
        DESCRIPTION:
            Apply GroupBy to one or more columns of a teradataml Dataframe
            The result will always behaves like calling groupby with as_index = False in pandas

        PARAMETERS:
            columns_expr:
                Required Argument.
                Specifies the Column name(s) to be given as list/string

        NOTES:
            Users can still apply teradataml DataFrame methods (filters/sort/etc) on top of the result.

        RETURNS:
            teradataml DataFrameGroupBy Object

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> df = DataFrame("kmeanssample")
            >>> df1 = df.groupby(["id","point1"])
            >>> df1.min()

        """
        try:
            column_list=[]
            unsupported_types = ['BLOB', 'CLOB', 'PERIOD_DATE', 'PERIOD_TIME', 'PERIOD_TIMESTAMP', 'ARRAY', 'VARRAY', 'XML', 'JSON']
            type_expr=[]
            invalid_types = []
            # validating columns which has to be a list/string for columns_expr
            if not ((isinstance(columns_expr, list) or (isinstance(columns_expr, str))) and all(isinstance(col, str) for col in columns_expr)):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "columns", ["list","str"]), MessageCodes.UNSUPPORTED_DATATYPE)
            if (isinstance(columns_expr, list)):
                if len(columns_expr) == 0:
                    raise TeradataMlException(Messages.get_message(MessageCodes.ARG_EMPTY, "columns_expr"), MessageCodes.ARG_EMPTY)
                else:
                    column_list=columns_expr
            elif (isinstance(columns_expr, str)):
                if columns_expr ==  "":
                    raise TeradataMlException(Messages.get_message(MessageCodes.ARG_EMPTY, "columns_expr"), MessageCodes.ARG_EMPTY)
                else:
                    column_list.append(columns_expr)
            # getting all the columns and data types for given metaexpr
            col_names, col_types = df_utils._get_column_names_and_types_from_metaexpr(self._metaexpr)
            # checking each element in columns_expr to be valid column in dataframe
            for col in column_list:
                if not df_utils._check_column_exists(col, col_names):
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDF_UNKNOWN_COLUMN, ": {}".format(col)), MessageCodes.TDF_UNKNOWN_COLUMN)
                else:
                    type_expr.append(self._metaexpr.t.c[col].type)
            # convert types to string from sqlalchemy type
            columns_types = [repr(type_expr[i]).split("(")[0] for i in range(len(type_expr))]
            # checking each element in passed columns_types to be valid a data type for groupby
            # and create a list of invalid_types
            for col_type in columns_types:
                if col_type in unsupported_types:
                    invalid_types.append(col_type)
            if len(invalid_types) > 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, invalid_types, "ANY, except following {}".format(unsupported_types)), MessageCodes.UNSUPPORTED_DATATYPE)
            groupbyexpr = ', '.join(UtilFuncs._teradata_quote_arg(col, "\"") for col in column_list)
            groupbyObj = DataFrameGroupBy(self._nodeid, self._metaexpr, self._column_names_and_types, self.columns, groupbyexpr, column_list)
            return groupbyObj
        except TeradataMlException:
            raise

    def get_values(self, num_rows = 99999):
        """
        Retrieves all values (only) present in a teradataml DataFrame.
        Values are retrieved as per a numpy.ndarray representation of a teradataml DataFrame.
        This format is equivalent to the get_values() representation of a Pandas DataFrame.

        PARAMETERS:

            num_rows:  Optional Argument.
                       Specifies the number of rows to retrieve values for from a teradataml DataFrame.
                       The num_rows parameter specified needs to be an integer value.
                       The default value is 99999.
                       Types: int

        RETURNS:
            Numpy.ndarray representation of a teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:

            >>> df1 = DataFrame.from_table('df_admissions_train')
            >>> df1
               masters   gpa     stats programming admitted
            id
            15     yes  4.00  advanced    advanced        1
            7      yes  2.33    novice      novice        1
            22     yes  3.46    novice    beginner        0
            17      no  3.83  advanced    advanced        1
            13      no  4.00  advanced      novice        1
            38     yes  2.65  advanced    beginner        1
            26     yes  3.57  advanced    advanced        1
            5       no  3.44    novice      novice        0
            34     yes  3.85  advanced    beginner        0
            40     yes  3.95    novice    beginner        0

            # Retrieve all values from the teradataml DataFrame

            >>> vals = df1.get_values()
            >>> vals
            array([['yes', 4.0, 'advanced', 'advanced', 1],
                   ['yes', 3.45, 'advanced', 'advanced', 0],
                   ['yes', 3.5, 'advanced', 'beginner', 1],
                   ['yes', 4.0, 'novice', 'beginner', 0],
                                 . . .
                   ['no', 3.68, 'novice', 'beginner', 1],
                   ['yes', 3.5, 'beginner', 'advanced', 1],
                   ['yes', 3.79, 'advanced', 'novice', 0],
                   ['no', 3.0, 'advanced', 'novice', 0],
                   ['yes', 1.98, 'advanced', 'advanced', 0]], dtype=object)

            # Retrieve values for a given number of rows from the teradataml DataFrame

            >>> vals = df1.get_values(num_rows = 3)
            >>> vals
            array([['yes', 4.0, 'advanced', 'advanced', 1],
                   ['yes', 3.45, 'advanced', 'advanced', 0],
                   ['yes', 3.5, 'advanced', 'beginner', 1]], dtype=object)

            Access specific values from the entire set received as per below:

            # Retrieve all values from an entire row (for example, the first row):

            >>> vals[0]
            array(['yes', 4.0, 'advanced', 'advanced', 1], dtype=object)

            # Alternatively, specify a range to retrieve values from  a subset of rows (For example, first 3 rows):

            >>> vals[0:3]
            array([['yes', 4.0, 'advanced', 'advanced', 1],
            ['yes', 3.45, 'advanced', 'advanced', 0],
            ['yes', 3.5, 'advanced', 'beginner', 1]], dtype=object)

            # Alternatively, retrieve all values from an entire column (For example, the first column):

            >>> vals[:, 0]
            array(['yes', 'yes', 'yes', 'yes', 'yes', 'no', 'yes', 'yes', 'yes',
                   'yes', 'no', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no',
                   'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes',
                   'yes', 'yes', 'no', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no',
                   'yes'], dtype=object)

            # Alternatively, retrieve a single value from a given row and column (For example, 3rd row, and 2nd column):

            >>> vals[2,1]
            3.5

            Note:
            1) Row and column indexing starts from 0, so the first column = index 0, second column = index 1, and so on...

            2) When a Pandas DataFrame is saved to the Teradata database & retrieved back as a teradataml DataFrame, the get_values()
               method on a Pandas DataFrame and the corresponding teradataml DataFrames have the following type differences:
                   - teradataml DataFrame get_values() retrieves 'bool' type Pandas DataFrame values (True/False) as BYTEINTS (1/0)
                   - teradataml DataFrame get_values() retrieves 'Timedelta' type Pandas DataFrame values as equivalent values in seconds.

        """
        return self.to_pandas(self._index_label, num_rows).get_values()

    @property
    def shape(self):
        """
        Returns a tuple representing the dimensionality of the DataFrame.

        PARAMETERS:
            None

        RETURNS:
            Tuple representing the dimensionality of this DataFrame.

        Examples:
            >>> df = DataFrame('phrases')
            >>> df
                     phrase_id     word
            model_id
            1                1   killer
            1                2     nice
            1                2  weather
            1                1  problem
            1                1    clown
            1                1    crazy
            >>> df.shape
            (6,3)

        RAISES:
            TeradataMlException (TDMLDF_INFO_ERROR)
        """
        try:
            # To know the number of rows in a DF, we need to execute the node
            # Generate/Execute AED nodes
            if self._table_name is None:
                self._table_name = df_utils._execute_node_return_db_object_name(self._nodeid)

            # The dimension of the DF is (# of rows, # of columns)
            return df_utils._get_row_count(self._table_name), len(self._column_names_and_types)

        except TeradataMlException:
            raise

        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR),
                                      MessageCodes.TDMLDF_INFO_ERROR) from err

    @property
    def size(self):
        """
        Returns a value representing the number of elements in the DataFrame.

        PARAMETERS:
            None

        RETURNS:
            Value representing the number of elements in the DataFrame.

        Examples:
            >>> df = DataFrame('phrases')
            >>> df
                     phrase_id     word
            model_id
            1                1   killer
            1                2     nice
            1                2  weather
            1                1  problem
            1                1    clown
            1                1    crazy
            >>> df.size
            18

        RAISES:
            None
        """
        dimension = self.shape
        return dimension[0] * dimension[1]

    def merge(self, right, on=None, how="inner", left_on=None, right_on=None, use_index=False,
              lsuffix=None, rsuffix=None):
        """
         Merges two teradataml DataFrames together.
         
         Supported merge operations are:
             - inner: Returns only matching rows, non-matching rows are eliminated.
             - left: Returns all matching rows plus non-matching rows from the left teradataml DataFrame.
             - right: Returns all matching rows plus non-matching rows from the right teradataml DataFrame.
             - full: Returns all rows from both teradataml DataFrames, including non matching rows.

         PARAMETERS:
         
            right:       Required argument. 
                         Specifies right teradataml DataFrame on which merge is to be performed.
                         Types: teradataml DataFrame
            
            on:          Optional argument. 
                         Specifies list of conditions that indicate the columns used for the merge.
                         Types: str or list of str
                     
                         Examples:
                          1. ["a","b"] indicates df1.a = df2.a and df1.b = df2.b.
                          2. ["a = b", "c = d"] indicates df1.a = df2.b and df1.c = df2.d
                  
                         Default is None. When no arguments are provided for this condition, the merge is performed 
                         using the indexes of the teradataml DataFrames. Both teradataml DataFrames are required to 
                         have index labels to perform a merge operation when no arguments are provided for this condition.
                         When either teradataml DataFrame does not have a valid index label in the above case, an exception is thrown.
                          
            how:         Optional argument. 
                         Specifies the type of merge to perform. Supports inner, left, right and full merge operations.
                         Default value is "inner".
                         Types: str
                      
            left_on:     Optional argument. 
                         Specifies column to merge on, in the left teradataml DataFrame.
                         Default value is None.
                         Types: str or list of str
                         
                         When both the 'on' and 'left_on' parameters are unspecified, the index columns 
                         of the teradataml DataFrames are used to perform the merge operation.
                      
            right_on:    Optional argument. 
                         Specifies column to merge on, in the right teradataml DataFrame.
                         Default value is None.
                         Types: str or list of str
                         
                         When both the 'on' and 'left_on' parameters are unspecified, the index columns 
                         of the teradataml DataFrames are used to perform the merge operation.
                       
            use_index:  Optional argument. 
                         Specifies whether (or not) to use index from the teradataml DataFrames as the merge key(s).
                         Default value is False.
                         Types: bool
                         
                         When False, and 'on', 'left_on', and 'right_on' are all unspecified, the index columns
                         of the teradataml DataFrames are used to perform the merge operation.
                         
            lsuffix:     Optional argument. 
                         Specifies suffix to be added to the left table columns.
                         Default value is None.
                         Types: str
                         
                         Note: A suffix is required if teradataml DataFrames being merged have columns with the same name.
                      
            rsuffix:     Optional argument. 
                         Specifies suffix to be added to the right table columns.
                         Default value is None.
                         Types: str
                     
                         Note: A suffix is required if teradataml DataFrames being merged have columns with the same name.

         RAISES:
           TeradataMlException

         RETURNS:
            teradataml DataFrame

         EXAMPLES:
            
            # Example set-up teradataml DataFrames for merge
            
            >>> from datetime import datetime, timedelta
            >>> dob = datetime.strptime('31101991', '%d%m%Y').date()
            
            >>> df1 = pd.DataFrame(data={'col1': [1, 2,3],
                           'col2': ['teradata','analytics','platform'],
                           'col3': [1.3, 2.3, 3.3],
                           'col5': ['a','b','c'],
                            'col 6': [dob, dob + timedelta(1), dob + timedelta(2)],
                            "'col8'":[3,4,5]})
            
            >>> df2 = pd.DataFrame(data={'col1': [1, 2, 3],
                                'col4': ['teradata', 'analytics', 'are you'],
                                'col3': [1.3, 2.3, 4.3],
                                 'col7':['a','b','d'],
                                 'col 6': [dob, dob + timedelta(1), dob + timedelta(3)],
                                 "'col8'": [3, 4, 5]})
            
            >>> copy_to_sql(df1, "t1", primary_index="col1")
            >>> copy_to_sql(df2, "t2", primary_index="col1")

            >>> df1 = DataFrame("table1")
            >>> df2 = DataFrame("table2")
            
            >>> df1
                 'col8'       col 6       col2  col3 col5
            col1                                         
            2         4  1991-11-01  analytics   2.3    b
            1         3  1991-10-31   teradata   1.3    a
            3         5  1991-11-02   platform   3.3    c
            
            >>> df2
                 'col8'       col 6  col3       col4 col7
            col1                                         
            2         4  1991-11-01   2.3  analytics    b
            1         3  1991-10-31   1.3   teradata    a
            3         5  1991-11-03   4.3    are you    d            
            
            1) Specify both types of 'on' conditions as well as teradataml DataFrame indexes as merge keys:
            
            >>> df1.merge(right = df2, how = "left", on = ["col3","col2=col4"], use_index = True, lsuffix = "t1", rsuffix = "t2")
            
              t2_col1 col5    t2_col 6 t1_col1 t2_'col8'  t1_col3       col4  t2_col3  col7       col2    t1_col 6 t1_'col8'
            0       2    b  1991-11-01       2         4      2.3  analytics      2.3     b  analytics  1991-11-01         4
            1       1    a  1991-10-31       1         3      1.3   teradata      1.3     a   teradata  1991-10-31         3
            2    None    c        None       3      None      3.3       None      NaN  None   platform  1991-11-02         5

            
            2) Specify left_on, right_on conditions along with teradataml DataFrame indexes as merge keys:
            
            >>> df1.merge(right = df2, how = "right", left_on = "a", right_on = "c", use_index = True, lsuffix = "t1", rsuffix = "t2")
            
              t2_col1  col5    t2_col 6 t1_col1 t2_'col8'  t1_col3       col4  t2_col3 col7       col2    t1_col 6 t1_'col8'
            0       2     b  1991-11-01       2         4      2.3  analytics      2.3    b  analytics  1991-11-01         4
            1       1     a  1991-10-31       1         3      1.3   teradata      1.3    a   teradata  1991-10-31         3
            2       3  None  1991-11-03    None         5      NaN    are you      4.3    d       None        None      None
            
            
            3) If teradataml DataFrames to be merged do not contain common columns, lsuffix and rsuffix are not required:
            
            >>> new_df1 = df1.select(['col2', 'col5'])
            >>> new_df2 = df2.select(['col4', 'col7'])
            
            >>> new_df1
              col5       col2
            0    b  analytics
            1    a   teradata
            2    c   platform
             
            >>> new_df2
              col7       col4
            0    b  analytics
            1    a   teradata
            2    d    are you

            >>> new_df1.merge(right = new_df2, how = "inner", on = "col5=col7")
              col5       col4       col2 col7
            0    b  analytics  analytics    b
            1    a   teradata   teradata    a
            
            
            4) When no merge conditions are specified, teradataml DataFrame indexes are used as merge keys.
            
            >>> df1.merge(right = df2, how = "full", lsuffix = "t1", rsuffix = "t2")
              t2_col1 col5    t2_col 6 t1_col1 t2_'col8'  t1_col3       col4  t2_col3 col7       col2    t1_col 6 t1_'col8'
            0       2    b  1991-11-01       2         4      2.3  analytics      2.3    b  analytics  1991-11-01         4
            1       1    a  1991-10-31       1         3      1.3   teradata      1.3    a   teradata  1991-10-31         3
            2       3    c  1991-11-03       3         5      3.3    are you      4.3    d   platform  1991-11-02         5
            
         """
        tdp = preparer(td_dialect)
         
        if not isinstance(right, DataFrame):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "right", "TeradataML DataFrame"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        if on is not None and not isinstance(on, str) and not isinstance(on, list):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "on", "'str' or 'list of str'"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        if left_on is not None and not isinstance(left_on, str) and not isinstance(left_on, list):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "left_on", "'str' or 'list of str'"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        if right_on is not None and not isinstance(right_on, str) and not isinstance(right_on, list):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "right_on", "'str' or 'list of str'"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        if (right_on is not None and left_on is None) or (right_on is None and left_on is not None):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.MUST_PASS_ARGUMENT, "left_on", "right_on"),
                MessageCodes.MUST_PASS_ARGUMENT)

        if not isinstance(use_index, bool):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "use_index", "bool"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        if isinstance(on,list) and all(isinstance(elem, str) for elem in on):
            join_conditions = on
        elif isinstance(on, str):
            join_conditions = [on]
        else:
            join_conditions = []

        if isinstance(left_on, list) and isinstance(right_on, list) and len(left_on) != len(right_on):
            raise TeradataMlException(
                  Messages.get_message(MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS, "left_on", "right_on"),
                  MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS)

        elif isinstance(left_on, list) and isinstance(right_on, str) and len(left_on) != 1:
            raise TeradataMlException(
                  Messages.get_message(MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS, "left_on", "right_on"),
                  MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS)

        elif isinstance(right_on, list) and isinstance(left_on, str) and len(right_on) != 1:
            raise TeradataMlException(
                  Messages.get_message(MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS, "left_on", "right_on"),
                MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS)

        if left_on is not None and not isinstance(left_on, list):
            left_on = [left_on]

        if right_on is not None and not isinstance(right_on, list):
            right_on = [right_on]

        if left_on is not None and right_on is not None:
            for left_column, right_column in zip(left_on, right_on):
                join_conditions.append("{} = {}".format(tdp.quote(left_column), tdp.quote(right_column)))

        # If user did not pass any arguments which form join conditions,
        # Merge is performed using index columns of TeradataML DataFrames
        if on is None and left_on is None and right_on is None and not use_index:
            if self._index_label is None or right._index_label is None:
                raise TeradataMlException(
                    Messages.get_message(MessageCodes.TDMLDF_INDEXES_ARE_NONE), MessageCodes.TDMLDF_INDEXES_ARE_NONE)
            else:
                use_index = True

        if use_index:
            if self._index_label is None or right._index_label is None:
                    raise TeradataMlException(
                    Messages.get_message(MessageCodes.TDMLDF_INDEXES_ARE_NONE), MessageCodes.TDMLDF_INDEXES_ARE_NONE)
                
            left_index_labels = self._index_label
            right_index_labels = right._index_label
            if not isinstance(self._index_label, list):
                left_index_labels = [left_index_labels]
            if not isinstance(right._index_label, list):
                right_index_labels = [right_index_labels]
        
            for left_index_label, right_index_label in zip(left_index_labels, right_index_labels):
                join_conditions.append("{} = {}".format(tdp.quote(left_index_label), tdp.quote(right_index_label)))
                

        return self.join(other=right, on=join_conditions, how=how, lsuffix=lsuffix, rsuffix=rsuffix)

class DataFrameGroupBy (DataFrame):
    """
    This class integrate GroupBy clause with AED.
    Updates AED node for DataFrame groupby object.

    """
    def __init__(self, nodeid, metaexpr, column_names_and_types, columns, groupbyexpr, column_list):
        super(DataFrameGroupBy, self).__init__()
        self._nodeid = self._aed_utils._aed_groupby(nodeid, groupbyexpr)
        self._metaexpr = metaexpr
        self._column_names_and_types = column_names_and_types
        self._columns = columns
        self.groupby_column_list = column_list


class MetaData():
    """
    This class contains the column names and types for a dataframe.
    This class is used for printing DataFrame.dtypes

    """

    def __init__(self, column_names_and_types):
        """
        Constructor for TerdataML MetaData.

        PARAMETERS:
            column_names_and_types - List containing column names and Python types.

        EXAMPLES:
            meta = MetaData([('col1', 'int'),('col2', 'str')])

        RAISES:

        """
        self._column_names_and_types = column_names_and_types

    def __repr__(self):
        """
        This is the __repr__ function for MetaData.
        Returns a string containing column names and Python types.

        PARAMETERS:

        EXAMPLES:
            meta = MetaData([('col1', 'int'),('col2', 'str')])
            print(meta)

        RAISES:

        """
        if self._column_names_and_types is not None:
            return df_utils._get_pprint_dtypes(self._column_names_and_types)
        else:
            return ""
