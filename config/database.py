# # import sqlite3
# # import os
# #
# # DATABASE_FILE = "doctor_patient.db"
# # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # REPORTS_DIR = os.path.join(BASE_DIR, "..", "reports")
# # os.makedirs(REPORTS_DIR, exist_ok=True)
# #
# # def get_db_connection():
# #     conn = sqlite3.connect(DATABASE_FILE)
# #     conn.row_factory = sqlite3.Row
# #     return conn
# #
# #
# # # Create tables
# # def create_tables():
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
# #
# #     cursor.execute("""
# #     CREATE TABLE IF NOT EXISTS patients (
# #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #         name TEXT NOT NULL,
# #         age INTEGER NOT NULL,
# #         gender TEXT NOT NULL,
# #         contact TEXT NOT NULL,
# #         address TEXT NOT NULL
# #     )
# #     """)
# #
# #     cursor.execute("""
# #     CREATE TABLE IF NOT EXISTS reports (
# #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #         patient_id INTEGER NOT NULL,
# #         test_name TEXT NOT NULL,
# #         report_path TEXT NOT NULL,
# #         disease TEXT,
# #         FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
# #     )
# #     """)
# #
# #
# #
# #
# #     cursor.execute("""
# #     CREATE TABLE IF NOT EXISTS prescriptions (
# #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #         patient_id INTEGER NOT NULL,
# #         doctor_id INTEGER NOT NULL,
# #         prescription TEXT NOT NULL,
# #         date TEXT NOT NULL,
# #         FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
# #     )
# #     """)
# #
# #     conn.commit()
# #     conn.close()
# #
# # create_tables()
# #
# # import sqlite3
# # from config.settings import logger
# #
# # DATABASE_PATH = "medical_system.db"
# #
# # def get_db_connection():
# #     conn = sqlite3.connect(DATABASE_PATH)
# #     create_tables(conn)  # Ensure tables exist before returning connection
# #     conn.row_factory = sqlite3.Row
# #     return conn
# #
# # def create_tables(conn):
# #     """
# #     Creates necessary tables if they do not exist.
# #     """
# #     try:
# #         cursor = conn.cursor()
# #
# #         # Create patients table if not exists
# #         cursor.execute("""
# #         CREATE TABLE IF NOT EXISTS patients (
# #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# #             name TEXT NOT NULL,
# #             age INTEGER NOT NULL,
# #             gender TEXT NOT NULL,
# #             contact TEXT NOT NULL,
# #             address TEXT NOT NULL
# #         );
# #         """)
# #
# #         # Create reports table if not exists
# #         cursor.execute("""
# #         CREATE TABLE IF NOT EXISTS reports (
# #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# #             patient_id INTEGER,
# #             test_name TEXT,
# #             file_path TEXT,
# #             disease TEXT DEFAULT NULL,
# #             FOREIGN KEY (patient_id) REFERENCES patients(id)
# #         );
# #         """)
# #
# #         # Create test_requests table if needed
# #         cursor.execute("""
# #         CREATE TABLE IF NOT EXISTS test_requests (
# #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# #             patient_id INTEGER,
# #             test_name TEXT NOT NULL,
# #             status TEXT DEFAULT 'requested',
# #             result TEXT DEFAULT NULL,
# #             FOREIGN KEY (patient_id) REFERENCES patients(id)
# #         );
# #         """)
# #
# #         conn.commit()
# #         logger.info("Database tables ensured successfully.")
# #     except Exception as e:
# #         logger.error(f"Error creating tables: {str(e)}")
# #         raise Exception("Failed to create database tables")
# #
# import sqlite3
# import os
# from config.settings import logger
#
# # Database and directory setup
# DATABASE_FILE = "medical_system.db"
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# REPORTS_DIR = os.path.join(BASE_DIR, "reports")
# os.makedirs(REPORTS_DIR, exist_ok=True)  # Ensure reports directory exists
#
# def get_db_connection():
#     """
#     Establishes a connection to the SQLite database and ensures tables exist.
#     """
#     conn = sqlite3.connect(DATABASE_FILE)
#     conn.row_factory = sqlite3.Row  # Enables dictionary-like access to rows
#     create_tables(conn)  # Ensure tables exist before returning connection
#     return conn
#
# def create_tables(conn):
#     """
#     Creates all necessary tables if they do not exist.
#     """
#     try:
#         cursor = conn.cursor()
#
#         # Patients table
#         cursor.execute("""
#         CREATE TABLE IF NOT EXISTS patients (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             age INTEGER NOT NULL,
#             gender TEXT NOT NULL,
#             contact TEXT NOT NULL,
#             address TEXT NOT NULL
#         );
#         """)
#
#         # Reports table
#         cursor.execute("""
#         CREATE TABLE IF NOT EXISTS reports (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             patient_id INTEGER NOT NULL,
#             test_name TEXT NOT NULL,
#             file_path TEXT NOT NULL,
#             disease TEXT DEFAULT NULL,
#             FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
#         );
#         """)
#
#         # Prescriptions table
#         cursor.execute("""
#         CREATE TABLE IF NOT EXISTS prescriptions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             patient_id INTEGER NOT NULL,
#             doctor_id INTEGER NOT NULL,
#             prescription TEXT NOT NULL,
#             date TEXT NOT NULL,
#             FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
#         );
#         """)
#
#         # Test Requests table
#         cursor.execute("""
#         CREATE TABLE IF NOT EXISTS test_requests (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             patient_id INTEGER NOT NULL,
#             test_name TEXT NOT NULL,
#             status TEXT DEFAULT 'requested',
#             result TEXT DEFAULT NULL,
#             FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
#         );
#         """)
#
#         conn.commit()
#         logger.info("Database tables ensured successfully.")
#
#     except Exception as e:
#         logger.error(f"Error creating tables: {str(e)}")
#         raise Exception("Failed to create database tables")
#
# # Ensure tables exist on script execution
# if __name__ == "__main__":
#     conn = get_db_connection()
#     conn.close()
import sqlite3
import os
from fastapi import FastAPI
from config.settings import logger

# Define database file
DATABASE_FILE = "medical_system.db"

# Create reports directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def get_db_connection():
    """
    Establish a connection to the SQLite database and ensure tables exist.
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        create_tables(conn)  # Ensure tables exist before returning connection
        logger.info("Database connected successfully")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
        return None

def create_tables(conn):
    """
    Create necessary tables if they do not exist.
    """
    try:
        cursor = conn.cursor()

        # Create Patients Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            contact TEXT NOT NULL,
            address TEXT NOT NULL
        );
        """)

        # Create Reports Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            test_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            disease TEXT DEFAULT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );
        """)

        # Create Prescriptions Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            prescription TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );
        """)

        # Create Test Requests Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            test_name TEXT NOT NULL,
            status TEXT DEFAULT 'requested',
            result TEXT DEFAULT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );
        """)

        conn.commit()
        logger.info("Database tables created successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error creating tables: {e}")

# Ensure tables exist at startup
conn = get_db_connection()
if conn:
    conn.close()
