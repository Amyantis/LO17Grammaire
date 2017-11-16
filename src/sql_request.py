import psycopg2


class DataBase:
    def __init__(self):
        self.connect = psycopg2.connect(host="tuxa.sme.utc", database="dblo17", user="lo17xxx", password="dblo17")

    def __del__(self):
        self.connect.close()

    def execute(self, query):
        cursor = self.connect.cursor()
        cursor.execute(query)
        print(cursor.fetchone())
        cursor.close()
