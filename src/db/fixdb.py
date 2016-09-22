from dynamic_reflect import DbReflection

'''
Script made to fix the parameter and properties of substance database
that uses at the moment commas to separe every 000

It did the job. This is just here for future use
'''


class DBfix:

    def __init__(self):
        """We reflect the database first"""

        self.db = DbReflection('sqlite:///simnavDB.sqlite')
        self.tables = self.db.dynamic_reflect()
        self.session = self.db.session()

    def fixcommas(self):
        """ Now we fix it """

        """ We get the table and use a query to get all the rows"""
        for table in self.tables.values():
            query = self.session.query(table).all()

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
                self.session.add(row)

        self.session.commit()

    def multiply_constants(self, table_name, column, multiplier):
        """
        It takes a table name, a column of the table, a multiplier and a
        new column name to update the column by multiplying it for every row
        """

        table = self.tables[table_name]
        query = self.session.query(table).all()
        for row in query:
            element = getattr(row, column)
            new_row = element * multiplier
            setattr(row, column, new_row)
        self.session.commit()
        print('It worked on: ', column)


fix = DBfix()
