import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sistem_sewa_lapangan"
        )
        return conn

    except mysql.connector.Error as err:
        print("Koneksi gagal:", err)
        return None