import psycopg2


class DataBase:
    def __init__(self):
        self.connect = psycopg2.connect(host="tuxa.sme.utc", database="dblo17", user="lo17xxx", password="dblo17")

    def __del__(self):
        self.connect.close()

    def execute(self, query):
        cursor = self.connect.cursor()
        cursor.execute(query)
        if "COUNT" in query.upper():
            yield cursor.fetchone()
        else:
            for row in cursor:
                yield tuple(map(str.strip, row))
        cursor.close()


if __name__ == '__main__':
    # Test database connection
    db = DataBase()
    query = "SELECT * FROM titre  LEFT JOIN date ON titre.fichier = date.fichier " \
            "WHERE date.annee = '2011'"
    for row in db.execute(query):
        print(row)
