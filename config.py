import psycopg2


class DatabaseConnection:
    def __init__(self, database):
        self.DATABASE_URI = f'postgresql://postgres:postgres@192.168.1.2:11432/{database}'
        self.connection = psycopg2.connect(self.DATABASE_URI)
