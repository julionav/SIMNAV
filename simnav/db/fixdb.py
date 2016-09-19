from dynamic_reflect import DbReflection

'''
Script made to fix the parameter and properties of substance database
that uses at the moment commas to separe every 000

It needs at the moment that the commas are replaced.
'''


class DBfix:

    def __init__(self):
        self.db = DbReflection('sqlite:///simnavDB.sqlite')
        self.tables = self.db.dynamic_reflect()
        self.session = self.db.session()

    def fixdb(self):
        for table_value in self.tables.values():
            query = self.session.query(table_value).all()
            for row in query:

                for key_element, value_element in row.__dict__.items():
                    if isinstance(value_element, str) and ',' in value_element:
                        print('coma found: ', key_element, row.NAME)


fix = DBfix()
fix.fixdb()
