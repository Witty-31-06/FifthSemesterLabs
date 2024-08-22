import mysql.connector as mysql

pwd = open('pwd.txt', 'r').read()
db = mysql.connect(
    user='root',
    host='localhost',
    passwd=f'{pwd}'
)

print(db)
cursor = db.cursor()
# cursor.execute()
cursor.execute('CREATE DATABASE IF NOT EXISTS ERROR_CORRECTION')
cursor.execute('USE ERROR_CORRECTION')
tables  = {}
tables['DATASET'] = """
CREATE TABLE IF NOT EXISTS DATASET (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    PACKET_SIZE INTEGER,
    PROBABILITY FLOAT,
    TECHNIQUE VARCHAR(10),
    IS_CORRECT BOOLEAN
);
"""
tables['Erroneous_Acceptance'] = """
CREATE TABLE IF NOT EXISTS ERRONEOUS_ACCEPTANCE (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    CORRECT_CODE VARCHAR(255),
    WRONG_CODE VARCHAR(255),
    TECHNIQUE VARCHAR(10)
);
"""
cursor.execute(tables['DATASET'])
cursor.execute(tables['Erroneous_Acceptance'])
db.commit()