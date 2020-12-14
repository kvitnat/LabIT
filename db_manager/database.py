import json
from enum import Enum
import os


class Types(Enum):
    INTEGER = 0
    REAL = 1
    CHAR = 2
    STRING = 3
    TEXT = 4
    INTEGERINVL = 5


def validate_type(my_type, value):
    my_type = Types(my_type)
    if my_type == Types.INTEGER:
        if isinstance(value, int):
            return True
        else:
            return False
    elif my_type == Types.REAL:
        if isinstance(value, float):
            return True
        else:
            return False
    elif my_type == Types.CHAR:
        if isinstance(value, str) and len(value) == 1:
            return True
        else:
            return False
    elif my_type == Types.STRING:
        if isinstance(value, str):
            return True
        else:
            return False
    elif my_type == Types.TEXT:
        if isinstance(value, str):
            return True
        else:
            return False
    elif my_type == Types.INTEGERINVL:
        if isinstance(value, list) and len(value) == 2:
            if isinstance(value[0], int) and isinstance(value[1], int):
                if value[0] <= value[1]:
                    return True
        return False
    else:
        return False


class Table:
    filename = ""
    data = {}
    column_names = []
    types = []

    def __init__(self, filename):
        self.filename = filename

    def create(self):
        self.save_to_file()

    def save_to_file(self):
        with open(self.filename, "w") as f:
            json.dump({
                "column_names": self.column_names,
                "types": self.types,
                "data": self.data
            }, f, indent=4)

    def row_count(self):
        if self.data == {}:
            return 0
        else:
            return len(list(self.data.values())[0])

    def get_html(self):
        return self.filename[:-5] + ".html"

    def add_row(self, fields):
        table = self.data
        for i in range(len(self.column_names)):
            if validate_type(self.types[i], fields[i]):
                table[self.column_names[i]].append(fields[i])
            else:
                raise TypeError("types do not match")
        self.save_to_file()

    def add_column(self, column_name, column_type):
        if column_name in self.column_names:
            raise LookupError("column with this name already exists.")
        self.column_names.append(column_name)
        if type(column_type) == int:
            self.types.append(column_type)
        else:
            self.types.append(column_type.value)
        self.data[column_name] = []
        for i in range(self.row_count()):
            self.data[column_name].append(None)
        self.save_to_file()

    def delete_column(self, column_name):
        if column_name not in self.column_names:
            raise LookupError("column you tried to delete does not exist")
        index = self.column_names.index(column_name)
        self.column_names.remove(column_name)
        self.types.remove(self.types[index])
        self.data.pop(column_name)
        self.save_to_file()

    def load(self):
        with open(self.filename) as json_file:
            table_file = json.load(json_file)
        self.data = table_file["data"]
        self.column_names = table_file["column_names"]
        self.types = table_file["types"]

    def print_table(self):
        for column in self.data:
            print(column, end=" ")
        print(" ")
        if self.data != {}:
            for i in range(self.row_count()):
                for column in self.data:
                    print(self.data[column][i], end=" ")
                print(" ")
        else:
            print("empty table")

    @staticmethod
    def compare_rows(table1, i, table2, j):
        result = True
        for column in table1.data:
            result = result and table1.data[column][i] == table2.data[column][j]
            # print("comparing: " + str(table1.data[column][i]) + " and " + str(table2.data[column][j]))
        # print(result)
        return result

    @staticmethod
    def intersection(table1, table2, table_filename):
        if table1.column_names != table2.column_names or table1.types != table2.types:
            raise LookupError("tables do not match")
        table = Table(table_filename)
        for i in range(len(table1.column_names)):
            table.add_column(table1.column_names[i], table1.types[i])
        if table1.data != {} and table2.data != {}:
            for i in range(table1.row_count()):
                for j in range(table2.row_count()):
                    if Table.compare_rows(table1, i, table2, j):
                        row = []
                        for column in table1.data:
                            row.append(table1.data[column][i])
                        table.add_row(row)
        return table


class Database:
    tables = []
    database_name = ""

    def create_db(self):
        pass

    def add_table(self, table_name):
        self.tables.append(table_name)

    def get_table(self, table_name):
        pass

    def __init__(self):
        pass

    def load(self, path):
        self.database_name = path
        self.tables = os.listdir(path)


class DBManager:
    path = ""

    def __init__(self):
        pass

    @staticmethod
    def add_extension(table_name):
        return table_name + ".json"

    def exists(self, db_name, table_name):
        table_name_ext = self.add_extension(table_name)
        tables = os.listdir(os.path.join(self.path, db_name))
        if table_name_ext in tables:
            return True
        else:
            return False

    def get_table(self, db_name, table_name):
        table_name_ext = self.add_extension(table_name)
        tables = os.listdir(os.path.join(self.path, db_name))
        if table_name_ext in tables:  # table exists
            table = Table(os.path.join(self.path, db_name, table_name_ext))
            table.load()
            return table
        else:  # new table
            raise LookupError("table with this name does not exist. -" + table_name)

    def create_table(self, db_name, table_name):
        table_name_ext = self.add_extension(table_name)
        tables = os.listdir(os.path.join(self.path, db_name))
        if table_name_ext not in tables:
            table = Table(os.path.join(self.path, db_name, table_name_ext))
            table.create()
            return table
        else:
            raise LookupError("table with this name already exists.")

    def delete_table(self, db_name, table_name):
        path = os.path.join(self.path, db_name, self.add_extension(table_name))
        if os.path.exists(path):
            os.remove(path)
        else:
            raise LookupError("path doesnt exist")

    def get_tables_from_db(self, db_name):
        table_files = os.listdir(os.path.join(self.path, db_name))
        for i in range(len(table_files)):
            table_files[i] = table_files[i][:-5]
        tables = []
        for table in table_files:
            tables.append(self.get_table(db_name, table))
        return tables

    def get_table_names_from_db(self, db_name):
        table_files = os.listdir(os.path.join(self.path, db_name))
        for i in range(len(table_files)):
            table_files[i] = table_files[i][:-5]
            print(table_files[i])
        return table_files
