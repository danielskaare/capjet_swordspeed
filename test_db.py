# import pandas and datetime
import pandas as pd
from urllib.request import pathname2url
from tkinter import *
import matplotlib.pyplot as plt
# import matplotlib.dates as matpldate
import numpy as np
import configparser
from datetime import datetime, timedelta
import time
import os.path
from tkinter import messagebox
import webbrowser
import sqlite3
from sqlite3 import Error
import warnings
import subprocess as sp
import sys
import glob
import math
# from pykalman import KalmanFilter
# from matplotlib.ticker import FormatStrFormatter
# from decimal import Decimal
# matplotlib.use("wx")

# from pylab import *



# Creates a message log file for all errors and print outs
#  save_stdout = sys.stdout
#  log_file = open(".\\OutputData\\message.log", "a")
#  errorlog_file = open(".\\OutputData\\error.log", "a")
#  sys.stdout = log_file
#  sys.stderr = errorlog_file
print("\n\n-------------------------------------------> " + str(datetime.utcnow()) + " (UTC) <-------------------------------------------")
print("--== Capjet Sword Speed Script Starts ==--")


class UpdateDB:
    def create_table(conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    # def create_table_sql(conn, create_table_sql):
    #     # Outdated will be removed
    #     """ create a table from the create_table_sql statement
    #     :param conn: Connection object
    #     :param create_table_sql: a CREATE TABLE statement
    #     :return:
    #     """
    #     try:
    #         c = conn.cursor()
    #         c.execute(create_table_sql)
    #     except Error as e:
    #         print(e)

    def init_capjet_raw_string(database, raw_string_header):
        raw_string_header_list = raw_string_header.split(",")
        for i, val in enumerate(raw_string_header_list):
            if i == 0 and val == 'time':
                raw_string_for_sql = ""
            elif i == 0 and val != 'time':
                print("First column in raw_capjet_string NEEDS to be 'time'! Make sure it is and change the script")
                raw_string_for_sql = str(val) + " NUMERIC, "
            else:
                raw_string_for_sql = raw_string_for_sql + str(val) + " NUMERIC, "

        sql_create_capjet_raw_string_table = """ CREATE TABLE IF NOT EXISTS capjet_raw_string (id INTEGER NOT NULL, trenching_id NUMERIC, time TEXT, kp NUMERIC, easting NUMERIC, northing NUMERIC, """ + str(raw_string_for_sql) + """capjet_type TEXT, """ + """timestamp_utc TEXT DEFAULT (CURRENT_TIMESTAMP), PRIMARY KEY (id)); """
        dburi = 'file:{}?mode=rw'.format(pathname2url(database))
        try:
            conn = sqlite3.connect(dburi, uri=True)
        except (sqlite3.OperationalError, UnboundLocalError, FileExistsError):
            if not os.path.exists(os.path.dirname(database)):
                os.makedirs(os.path.dirname(database))
                print("Created new folders: " + str(os.path.dirname(database)))
            dburi = 'file:{}?mode=rwc'.format(pathname2url(database))
            # try:
            conn = sqlite3.connect(dburi, uri=True)
            # except:
            #  print("Path to database: " + str(database) + " does not exist. Creating directories")
            #    print("Unexpected error:" + str(sys.exc_info()[0]))
            err2 = "Database: " + str(database) + " does not exist and will be created. Continue..."
            print(err2)
            # QtWidgets.QMessageBox.about(self, "Info...", err2)
        # except:
        # print("Unexpected error:" + str(sys.exc_info()[0]))
        if conn is not None:
            # create CJA RawString table
            UpdateDB.create_table(conn, sql_create_capjet_raw_string_table)
        else:
            print("Error! cannot create the database connection.")
        return conn

    # def init_table(conn, create_table_sql, raw_string_header, CJX):
    #     for idx, val in enumerate(raw_string_header):
    #         if idx == 0:
    #             # Skip first which should be time
    #             sql_create_column = ""
    #         else:
    #             sql_create_column = sql_create_column + val + " NUMERIC, "
    #
    #     sql_create_capjet_raw_string_table = """ CREATE TABLE IF NOT EXISTS capjet_raw_string (id INTEGER NOT NULL, trenching_id NUMERIC, time TEXT, kp NUMERIC, easting NUMERIC, northing NUMERIC, """ + sql_create_column + sql_create_column + """capjet_type TEXT,""" + """timestamp_utc TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP), PRIMARY KEY (id)); """
    #
    #     dburi = 'file:{}?mode=rw'.format(pathname2url(conn))
    #     try:
    #         conn = sqlite3.connect(dburi, uri=True)
    #     except (sqlite3.OperationalError, UnboundLocalError, FileExistsError):
    #         if not os.path.exists(os.path.dirname(conn)):
    #             os.makedirs(os.path.dirname(database))
    #             print("Created new folders: " + str(os.path.dirname(database)))
    #         dburi = 'file:{}?mode=rwc'.format(pathname2url(conn))
    #         # try:
    #         conn = sqlite3.connect(dburi, uri=True)
    #         # except:
    #         #  print("Path to database: " + str(database) + " does not exist. Creating directories")
    #         #    print("Unexpected error:" + str(sys.exc_info()[0]))
    #         err2 = "Database: " + str(conn) + " does not exist and will be created. Continue..."
    #         print(err2)
    #         # QtWidgets.QMessageBox.about(self, "Info...", err2)
    #     # except:
    #     # print("Unexpected error:" + str(sys.exc_info()[0]))
    #     if conn is not None:
    #         # create CJA RawString table
    #         UpdateDB.create_table(conn, sql_create_capjet_raw_string_table)
    #     else:
    #         print("Error! cannot create the database connection.")
    #
    #     return conn

    def initializeDB(database):
            sql_create_trenching_table = """ CREATE TABLE IF NOT EXISTS trenching (
                                                                id INTEGER NOT NULL,
                                                                trenching_pass_id INTEGER,
                                                                rpl_id TEXT,
                                                                time TEXT,
                                                                trenching_id NUMERIC NOT NULL,
                                                                easting NUMERIC,
                                                                northing NUMERIC,
                                                                kp NUMERIC NOT NULL,
                                                                dcc NUMERIC,
                                                                sword_stbd NUMERIC,
                                                                sword_port NUMERIC,
                                                                sword_depth NUMERIC,
                                                                speed_along_line NUMERIC,
                                                                speed_over_ground NUMERIC,
                                                                roll NUMERIC,
                                                                pitch NUMERIC,
                                                                heading NUMERIC,
                                                                power NUMERIC,
                                                                comment TEXT,
                                                                timestamp_utc TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),
                                                                PRIMARY KEY (id)
                                                            ); """

            sql_create_database_log_table = """ CREATE TABLE IF NOT EXISTS database_log (
                                                           id INTEGER PRIMARY KEY NOT NULL,
                                                           changes TEXT NOT NULL,
                                                           table_name TEXT NOT NULL,
                                                           updated_by TEXT,
                                                           timestamp_utc TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP)
                                                       ); """

            dburi = 'file:{}?mode=rw'.format(pathname2url(database))
            try:
                conn = sqlite3.connect(dburi, uri=True)
            except (sqlite3.OperationalError, UnboundLocalError, FileExistsError):
                if not os.path.exists(os.path.dirname(database)):
                    os.makedirs(os.path.dirname(database))
                    print("Created new folders: " + str(os.path.dirname(database)))
                dburi = 'file:{}?mode=rwc'.format(pathname2url(database))
                # try:
                conn = sqlite3.connect(dburi, uri=True)
                # except:
                #  print("Path to database: " + str(database) + " does not exist. Creating directories")
                # print("Unexpected error:" + str(sys.exc_info()[0]))
                err2 = "Database: " + str(database) + " does not exist and will be created. Continue..."
                print(err2)
                # QtWidgets.QMessageBox.about(self, "Info...", err2)
            # except:
            #   print("Unexpected error:" + str(sys.exc_info()[0]))
            if conn is not None:
                # create projects table
                UpdateDB.create_table(conn, sql_create_trenching_table)
                # create videolog table
                # UpdateDB.create_table(conn, sql_create_videolog_table)
                # create Operation type table
                #            UpdateDB.create_table(conn, sql_create_operation_type_table)
                # create database_log table
                UpdateDB.create_table(conn, sql_create_database_log_table)
            else:
                print("Error! cannot create the database connection.")
            return conn


sqlitepath = os.path.realpath('D:\\temp\\DB\\Dummy08.sqlite')

Config = configparser.ConfigParser()
Config.read('D:\\iSurvey\\Python\\Capjet_Sword_Speed_v1.08\\Config_Sword_Speed_CapjetA_TEST.ini')
raw_string_header = Config["Capjet RAW String"]['Raw_string_header']
CJX = 'CJA'

# UpdateDB.create_table_sql(os.path.realpath(sqlitepath))
# UpdateDB.init_table(os.path.realpath(sqlitepath), raw_string_header, CJX)
UpdateDB.initializeDB(os.path.realpath(sqlitepath))
print("finished DB init")
UpdateDB.init_capjet_raw_string(os.path.realpath(sqlitepath), raw_string_header)
print('SQL DB CAPJET RAW String table Init OK')
# UpdateDB.write_result_CJ_RAW(os.path.realpath(sqlitepath), merged, tid, CJX)