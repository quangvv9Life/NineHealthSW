import psycopg2


class DatabaseConnection:
    def __init__(self, database):
        self.DATABASE_URI = f'postgresql://postgres:xxx!@xx.xx.1.3:12432/{database}'
        self.connection = psycopg2.connect(self.DATABASE_URI)


class FoodCategory:
    def __init__(self, parent_id, parent_name, child_id, child_name, food_id):
        self.parent_id = parent_id
        self.parent_name = parent_name
        self.child_id = child_id
        self.child_name = child_name
        self.food_id = food_id
