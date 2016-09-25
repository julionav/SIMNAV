from dynamic_reflect import DbReflection
from copy import deepcopy

'''
Script made to fix the parameter and properties of substance database
that uses at the moment commas to separe every 000

It multiply some constants in the db and interexchange two columns

It did the job. This is just here for future use
'''



"""We reflect the database first"""

db = DbReflection('sqlite:///simnavDB.sqlite')
tables = db.dynamic_reflect()
session = db.session()

def fixcommas():
    """ Now we fix it """

    """ We get the table and use a query to get all the rows"""
    for table in tables.values():
        query = session.query(table).all()

        """ We get every row of the table """
        for row in query:

            # We get the info of the columns in the table
            for key_element, element in row.__dict__.items():

                # The comma is eliminated from the element
                if isinstance(element, str) and ',' in element:

                    """ try and except is used to suppress the errors
                    of trying to conver the compound name to float
                    """
                    try:
                        setattr(row, key_element,
                                float(element.replace(',', '')))
                    except:
                        continue

            session.add(row)

    session.commit()

def multiply_constants(table_name, column, multiplier):
    """
    It takes a table name, a column of the table, a multiplier and a
    new column name to update the column by multiplying it for every row
    """

    table = tables[table_name]
    query = session.query(table).all()
    for row in query:
        element = getattr(row, column)
        new_row = element * multiplier
        setattr(row, column, new_row)
    session.commit()
    print('It worked on: ', column)

def interexchange_columns(table_name, column1, column2):
    """
    It takes a table name and two columns name and it interexchange the
    values of the columns
    """
    table = tables[table_name]
    query = session.query(table).all()

    for row in query:
        # We get the elements of the columns for a row
        element_column1 = getattr(row, column1)
        element_column2 = getattr(row, column2)

        #Now we interexchange them
        setattr(row, column1, element_column2)
        setattr(row, column2, element_column1)

    session.commit()

if __name__ == '__main__':
