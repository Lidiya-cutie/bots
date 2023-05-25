import sqlite3 as sq

class SqliteDb:
    def __init__(self, file='sqlite.db'):
        self.file = file
        self.connection = __import__('sqlite3').connect(database=self.file,  check_same_thread=False, timeout=5)
        self.cursor = self.connection.cursor()
        self.create_db()
    
    def create_db(self):
        """
        Создаются таблицы докторов для поиска
        и пользователей телеграм бота
        """
        self.create_table_doctors()
        self.create_table_users()

    def create_table_users(self):
        q = """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            is_active_ping BOOLEAN,
            doctor_id varchar(40),
            last_seen_datetime DATETIME,
            FOREIGN KEY (doctor_id) REFERENCES doctors (id)
        );"""
        self.cursor.execute(q)
        self.connection.commit()

    def create_table_doctors(self):
        q = """CREATE TABLE IF NOT EXISTS doctors (
            id VARCHAR(40) PRIMARY KEY,
            doctor_id INTEGER,
            speciality_id INTEGER,
            hospital_id INTEGER
        );"""
        self.cursor.execute(q)
        self.connection.commit()
    
    def add_user(self, user_id: int):
        q = """INSERT INTO USERS (id) values (?)"""
        self.cursor.execute(q, (user_id,))
        self.connection.commit()
    
    def add_doctor(self, doctor_id, speciality_id, hospital_id: int):
        q = """INSERT INTO doctors (id, doctor_id, speciality_id, hospital_id) values (?, ?, ?, ?)"""
        id = f"{hospital_id}_{speciality_id}_{doctor_id}"
        self.cursor.execute(q, (id, doctor_id, speciality_id, hospital_id))
        self.connection.commit()