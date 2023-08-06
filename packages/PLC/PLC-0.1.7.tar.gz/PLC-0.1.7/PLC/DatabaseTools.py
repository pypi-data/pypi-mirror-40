import sqlite3
import os
def LoadDb(Path, table):
    try:
        conn = sqlite3.connect(Path)
        c = conn.cursor()
        c.execute('SELECT * From {table}'.format(table=table))
        Results = c.fetchall()
        conn.commit()
        conn.close()
        return Results
    except sqlite3.Error as e:
        print(e)
def CreateDatabase(Filename):
    try:
        if not os.path.isfile(Filename):
            conn = sqlite3.connect(Filename)
            c = conn.cursor()
            c.execute(
                '''
                create table MP
                (
                  MP    TEXT,
                  Seconds TEXT
                );
                ''')
            c.execute(
                '''
                create table Notes
                (
                  Notes TEXT
                );
                ''')
            c.execute(
                '''
                create table NewWords
                (
                Word       TEXT not null,
                Def        TEXT not null,
                Sentence   TEXT not null,
                Pronouncer TEXT not null
                );
                ''')
            c.execute(
                '''
                create table MakeTrueSentences
                (
                  Word       TEXT not null,
                  Pronouncer TEXT not null
                );
                ''')
            c.execute(
                '''
                create table ComprehensionCheckQuestions
                (
                  Question   TEXT not null,
                  Pronouncer TEXT not null
                );
                '''
            )
            c.execute(
                '''
                create table Chunks
                (
                  Chunk      TEXT not null,
                  Pronouncer TEXT not null
                );
                '''
            )
            conn.commit()
            conn.close()
    except sqlite3.Error as e:
        print(str(e))
def AddtoDatabase(Filename, Tablename, datas):
    try:
        if not os.path.isfile(Filename):
            CreateDatabase(Filename)
        conn = sqlite3.connect(Filename)
        c = conn.cursor()
        c.execute("INSERT INTO {} VALUES ('{}');".format(Tablename, "', '".join(datas)))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(str(e))