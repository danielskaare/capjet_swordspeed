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

    def create_database_log(conn, database_log_entry):
        """
        Create a new task
        :param conn:
        :param task:
        :return:
        """

        sql = ''' INSERT INTO database_log(changes, table_name, updated_by)
                  VALUES(?, ?, ?) '''
        cur = conn.cursor()
        cur.execute(sql, database_log_entry)
        return cur.lastrowid

    def initCJARawString(database, raw_string_header):
        # Outdated will be removed
        for idx, val in enumerate(raw_string_header):
            if idx == 0:
                # Skip first which should be time
                sql_create_column = ""
            else:
                sql_create_column = sql_create_column + val + " NUMERIC, "

        sql_create_cja_raw_string_table = """ CREATE TABLE IF NOT EXISTS cja_raw_string (id INTEGER NOT NULL, TrenchingID NUMERIC, Time Text, KP NUMERIC, Easting NUMERIC, Northing NUMERIC, """ + """timestamp_utc DEFAULT (CURRENT_TIMESTAMP), PRIMARY KEY (id)); """

        dburi = 'file:{}?mode=rw'.format(pathname2url(database))
        try:
            conn = sqlite3.connect(dburi, uri=True)
        except (sqlite3.OperationalError, UnboundLocalError, FileExistsError):
            if not os.path.exists(os.path.dirname(database)):
                os.makedirs(os.path.dirname(database))
                print("Created new folders: " + str(os.path.dirname(database)))
            dburi = 'file:{}?mode=rwc'.format(pathname2url(database))
            #try:
            conn = sqlite3.connect(dburi, uri=True)
            #except:
                #  print("Path to database: " + str(database) + " does not exist. Creating directories")
            #    print("Unexpected error:" + str(sys.exc_info()[0]))
            err2 = "Database: " + str(database) + " does not exist and will be created. Continue..."
            print(err2)
            # QtWidgets.QMessageBox.about(self, "Info...", err2)
        #except:
            #print("Unexpected error:" + str(sys.exc_info()[0]))
        if conn is not None:
            # create CJA RawString table
            UpdateDB.create_table(conn, sql_create_cja_raw_string_table)
        else:
            print("Error! cannot create the database connection.")

        return conn

    def initCJBRawString(database, raw_string_header):
        # Outdated will be removed
        for idx, val in enumerate(raw_string_header):
            if idx == 0:
                # dtypes = {raw_string_header[0]: str}
                sql_create_column = ""
            else:
                sql_create_column = sql_create_column + val + " NUMERIC,"

        sql_create_cjb_raw_string_table = " CREATE TABLE IF NOT EXISTS cjb_raw_string (id INTEGER NOT NULL, TrenchingID NUMERIC, Time TEXT, KP NUMERIC, Easting NUMERIC, Northing NUMERIC, " + sql_create_column + "timestamp_utc DEFAULT (CURRENT_TIMESTAMP), PRIMARY KEY (id)); "

        dburi = 'file:{}?mode=rw'.format(pathname2url(database))
        try:
            conn = sqlite3.connect(dburi, uri=True)
        except (sqlite3.OperationalError, UnboundLocalError, FileExistsError):
            if not os.path.exists(os.path.dirname(database)):
                os.makedirs(os.path.dirname(database))
                print("Created new folders: " + str(os.path.dirname(database)))
            dburi = 'file:{}?mode=rwc'.format(pathname2url(database))
            #try:
            conn = sqlite3.connect(dburi, uri=True)
            #except:
                #  print("Path to database: " + str(database) + " does not exist. Creating directories")
               # print("Unexpected error:" + str(sys.exc_info()[0]))
            err2 = "Database: " + str(database) + " does not exist and will be created. Continue..."
            print(err2)
            # QtWidgets.QMessageBox.about(self, "Info...", err2)
        #except:
            #print("Unexpected error:" + str(sys.exc_info()[0]))
        if conn is not None:
            # create CJb RawString table
            print("Start creating new cjb raw string table")
            UpdateDB.create_table(conn, sql_create_cjb_raw_string_table)
            print("Finished creating new cjb_raw_string_table")
        else:
            print("Error! cannot create the database connection.")

        return conn

    def init_capjet_raw_string(database, raw_string_header):
        for idx, val in enumerate(raw_string_header):
            if idx == 0:
                # Skip first which should be time
                sql_create_column = ""
            else:
                sql_create_column = sql_create_column + val + " NUMERIC, "

        sql_create_capjet_raw_string_table = """ CREATE TABLE IF NOT EXISTS capjet_raw_string (id INTEGER NOT NULL, trenching_id NUMERIC, time TEXT, kp NUMERIC, easting NUMERIC, northing NUMERIC, """ + str(
            sql_create_column) + """capjet_type TEXT, """ + """timestamp_utc TEXT DEFAULT (CURRENT_TIMESTAMP), PRIMARY KEY (id)); """
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
                conn = sqlite3.connect(dburi, uri=True)
                err2 = "Database: " + str(database) + " does not exist and will be created. Continue..."
                print(err2)
                # QtWidgets.QMessageBox.about(self, "Info...", err2)
            # except:
            #   print("Unexpected error:" + str(sys.exc_info()[0]))
            if conn is not None:
                # create projects table
                UpdateDB.create_table(conn, sql_create_trenching_table)
                UpdateDB.create_table(conn, sql_create_database_log_table)
            else:
                print("Error! cannot create the database connection.")
            return conn

    def write_result_CJA_RAW(dbFile, df_merged, tid):
        # Outdated will be removed
        print("Start updating DB with CJA RAW String...")
        dburi = 'file:{}?mode=rwc'.format(pathname2url(dbFile))
        try:
            conn = sqlite3.connect(dburi, uri=True)
        except:
            print("Unexpected error Trying to open DB:" + str(sys.exc_info()[0]))

        with conn:
            # Make sure the columns is named the same (May differ between Capjet A and B

            # df_merged.columns = ['', 'comment']

            # cols is the order the columns should be uploaded to sqllite
            #  NB! Same Order
            # cols = ['Time', 'tid', 'kp', 'dcc', 'easting', 'northing', 'sword_stbd', 'sword_port', 'speed_along_line',
            #        'speed_over_ground', 'roll', 'pitch', 'heading', 'power', 'comment']


            print("Check if TID" + str(tid) + " already exists in table cja_raw_string")
            cur = conn.cursor()
            cur.execute("SELECT Time, TrenchingID, timestamp_utc FROM cja_raw_string WHERE TrenchingID = ? ORDER BY time DESC LIMIT 1",
                        (tid,))
            try:
                res_query = cur.fetchone()
                dateofTP = res_query[0]
                TIDofTP = res_query[1]
                timestamp_utc = res_query[2]
            except TypeError:
                dateofTP = None
                TIDofTP = None
                timestamp_utc = None
                pass
            if not TIDofTP:
                print("Trenching ID: " + str(tid) + " does not exist in SQLite DB, Table: cja_raw_string")
                try:
                    df_merged.to_sql(name='cja_raw_string', con=conn, index_label='id', if_exists='append',
                              chunksize=None, index=False)
                except sqlite3.IntegrityError as e:
                    print(
                        "Data with same timestamp already consist in database, or same timestamp in the data you are trying to upload. Aborting... \n" + str(
                            e))
                    #  sys.stdout = save_stdout
                    #  log_file.close()
                    return
                except sqlite3.OperationalError as e:
                    print("Missing column in the table: " + str(e))
                    messagebox.showinfo("Column not in Database", str(e) + ".\nYou have to manually add this column. Data NOT written to database.")
                    return

                #except:
                 #   print("Unexpected error:", sys.exc_info()[0])
                try:
                    ''' Update the database_log table with what has been done to the database '''
                    data_log_entry = (
                        'Added CapjetA RAW String data TID' + str(tid) + ' to database', 'cja_raw_string', 'iSURVEY')
                    UpdateDB.create_database_log(conn, data_log_entry)
                    print("Wrote to database_log successfully!")
                    messagebox.showinfo(title='Save to SQLite DB',
                                        message='Successfully written data to: ' + str(dbFile))
                except sqlite3.OperationalError:
                    print("FAILED!")
                    print(
                        "DataBase table Exists (database_log), but has the wrong table structure. Update Table or use a different DB. Database_log entry will not be written to DB")
                return
            else:
                #  print("The tid in SQL DB was trenched: " + str(dateofTP))
                #  if (row != ''):
                savetodb = messagebox.askyesno("Overwrite TID" + str(tid), "CapjetA RAW String with the same TID (" + str(
                    tid) + ") already exists in the SQL database. \n\nThe trenching was performed the " + str(
                    dateofTP) + " and uploaded: " + str(timestamp_utc) + " \n\nDo you want to replace this Trenching ID?")
                if (savetodb):
                    print("Overwriting tid: " + str(tid))
                    mydata = cur.execute("DELETE FROM cja_raw_string WHERE TrenchingID=?", (tid,))
                    try:
                        df_merged.to_sql(name='cja_raw_string', con=conn, index_label='id', if_exists='append',
                                chunksize=None, index=False)
                    except sqlite3.IntegrityError as e:
                        print(
                            "Data with same timestamp already consist in database, or same timestamp in the data you are trying to upload. Aborting... \n" + str(
                                e))
                        #  sys.stdout = save_stdout
                        #  log_file.close()
                        return
                    except sqlite3.OperationalError as e:
                        print("Missing column in the table: " + str(e))
                        messagebox.showinfo("Column not in Database", str(
                            e) + ". You have to manually add this column. Data NOT written to database.")
                        return
                    print("successfully reloaded current data")
                    try:
                        ''' Update the database_log table with what has been done to the database '''
                        data_log_entry = (
                            'Replaced CapjetA RAW String TID' + str(tid) + ' to database', 'cja_raw_string', 'iSURVEY')
                        UpdateDB.create_database_log(conn, data_log_entry)
                        print("Wrote to database_log successfully!")
                        messagebox.showinfo(title='Save to SQLite DB',
                                            message='Successfully written data to: ' + str(dbFile))
                    except sqlite3.OperationalError:
                        print("FAILED!")
                        print(
                            "DataBase table Exists (database_log), but has the wrong table structure. Update Table or use a different DB. Database_log entry will not be written to DB")

                    except sqlite3.AttributeError as e:
                        print("Wrong numbers of fields in database_log: " + str(e))

                else:
                    print("Keeping old tid trenching data")
            #  except:
            #   print("Unexpected error:", sys.exc_info()[0])
        print('SQL DB CJA RAW String table Write Results OK')

    def write_result_CJB_RAW(dbFile, df_merged, tid):
        # Outdated will be removed
        print("Start updating DB with CJB RAW string...")
        dburi = 'file:{}?mode=rwc'.format(pathname2url(dbFile))
        try:
            conn = sqlite3.connect(dburi, uri=True)
        except:
            print("Unexpected error Trying to open DB:" + str(sys.exc_info()[0]))

        with conn:
            # Make sure the columns is named the same (May differ between Capjet A and B

            # df_merged.columns = ['', 'comment']

            # cols is the order the columns should be uploaded to sqllite
            #  NB! Same Order
            # cols = ['Time', 'tid', 'kp', 'dcc', 'easting', 'northing', 'sword_stbd', 'sword_port', 'speed_along_line',
            #        'speed_over_ground', 'roll', 'pitch', 'heading', 'power', 'comment']


            print("Check if TID" + str(tid) + " already exists")
            cur = conn.cursor()
            cur.execute("SELECT Time, TrenchingID, timestamp_utc FROM cjb_raw_string WHERE TrenchingID = ? ORDER BY time DESC LIMIT 1",
                        (tid,))
            try:
                res_query = cur.fetchone()
                dateofTP = res_query[0]
                TIDofTP = res_query[1]
                timestamp_utc = res_query[2]
                print('dateofTP: ' + str(dateofTP))
                print('TIDofTP: ' + str(TIDofTP))
            except TypeError:
                dateofTP = None
                TIDofTP = None
                pass
            if not TIDofTP:
                print("Trenching ID: " + str(tid) + " does not exist in SQLite DB, Table: cjb_raw_string")
                try:
                    df_merged.to_sql(name='cjb_raw_string', con=conn, index_label='id', if_exists='append',
                              chunksize=None, index=False)
                except sqlite3.IntegrityError as e:
                    print(
                        "CJB RAW Table Data with same timestamp already consist in database, or same timestamp in the data you are trying to upload. Aborting... \n" + str(
                            e))
                    #  sys.stdout = save_stdout
                    #  log_file.close()
                    return
                except sqlite3.OperationalError as e:
                    print("Missing column in the table: " + str(e))
                    messagebox.showinfo("Column not in Database", str(e) + ".\nYou have to manually add this column. Data NOT written to database.")
                    return
                #except:
                 #   print("Unexpected error:", sys.exc_info()[0])
                try:
                    ''' Update the database_log table with what has been done to the database '''
                    data_log_entry = (
                        'Added CapjetB RAW String data TID' + str(tid) + ' to database', 'cjb_raw_string', 'iSURVEY')
                    UpdateDB.create_database_log(conn, data_log_entry)
                    print("Wrote to database_log successfully!")
                    messagebox.showinfo(title='Save to SQLite DB',
                                        message='Successfully written data to: ' + str(dbFile))
                except sqlite3.OperationalError:
                    print("FAILED!")
                    print(
                        "DataBase table Exists (database_log), but has the wrong table structure. Update Table or use a different DB. Database_log entry will not be written to DB")
                return
            else:
                #  print("The tid in SQL DB was trenched: " + str(dateofTP))
                #  if (row != ''):
                savetodb = messagebox.askyesno("Overwrite tid" + str(tid), "CapjetB RAW String with the same Trenching ID (" + str(
                    tid) + ") already exists in the SQL database. \n\nThe trenching was performed the " + str(
                    dateofTP) + "and uploaded: " + str(timestamp_utc) + " \n\nDo you want to replace this Trenching ID?")
                if (savetodb):
                    print("Overwriting tid: " + str(tid))
                    mydata = cur.execute("DELETE FROM cjb_raw_string WHERE TrenchingID=?", (tid,))
                    try:
                        df_merged.to_sql(name='cjb_raw_string', con=conn, index_label='id', if_exists='append',
                                chunksize=None, index=False)
                    except sqlite3.IntegrityError as e:
                        print(
                            "Data with same timestamp already consist in database, or same timestamp in the data you are trying to upload. Aborting... \n" + str(
                                e))
                        #  sys.stdout = save_stdout
                        #  log_file.close()
                        return
                    except sqlite3.OperationalError as e:
                        print("Missing column in the table: " + str(e))
                        messagebox.showinfo("Column not in Database", str(
                            e) + ". You have to manually add this column. Data NOT written to database.")
                        return
                    print("successfully reloaded current data")
                    try:
                        ''' Update the database_log table with what has been done to the database '''
                        data_log_entry = (
                            'Replaced CapjetB RAW String TID' + str(tid) + ' to database', 'cjb_raw_string', 'iSURVEY')
                        UpdateDB.create_database_log(conn, data_log_entry)
                        print("Wrote to database_log successfully!")
                        messagebox.showinfo(title='Save to SQLite DB',
                                            message='Successfully written data to: ' + str(dbFile))
                    except sqlite3.OperationalError:
                        print("FAILED!")
                        print(
                            "DataBase table Exists (database_log), but has the wrong table structure. Update Table or use a different DB. Database_log entry will not be written to DB")

                    except sqlite3.AttributeError as e:
                        print("Wrong numbers of fields in database_log: " + str(e))

                else:
                    print("Keeping old tid trenching data")
            #  except:
            #   print("Unexpected error:", sys.exc_info()[0])
        print('SQL DB CJB RAW String table Write Results OK')
        return

    def write_result_capjet_raw_string(dbFile, df_merged, tid, CJX):
        df_merged['capjet_type'] = str(CJX)
        # new function will replace write_result_CJA_RAW and write_result_CJB_RAW
        print("Start updating DB with " + str(CJX) + " RAW string...")
        dburi = 'file:{}?mode=rwc'.format(pathname2url(dbFile))
        try:
            conn = sqlite3.connect(dburi, uri=True)
        except:
            print("Unexpected error Trying to open DB:" + str(sys.exc_info()[0]))

        with conn:
            # Make sure the columns is named the same (May differ between Capjet A and B

            # df_merged.columns = ['', 'comment']

            # cols is the order the columns should be uploaded to sqllite
            #  NB! Same Order
            # cols = ['Time', 'tid', 'kp', 'dcc', 'easting', 'northing', 'sword_stbd', 'sword_port', 'speed_along_line',
            #        'speed_over_ground', 'roll', 'pitch', 'heading', 'power', 'comment']
            print("Check if TID" + str(tid) + " already exists")
            cur = conn.cursor()
            cur.execute("SELECT time, trenching_id, timestamp_utc FROM capjet_raw_string WHERE trenching_id = ? ORDER BY time DESC LIMIT 1",
                        (tid,))
            try:
                res_query = cur.fetchone()
                dateofTP = res_query[0]
                TIDofTP = res_query[1]
                timestamp_utc = res_query[2]
                print('dateofTP: ' + str(dateofTP))
                print('TIDofTP: ' + str(TIDofTP))
            except TypeError:
                dateofTP = None
                TIDofTP = None
                pass
            if not TIDofTP:
                print("Trenching ID: " + str(tid) + " does not exist in SQLite DB, Table: capjet_raw_string")
                try:
                    df_merged.to_sql(name='capjet_raw_string', con=conn, index_label='id', if_exists='append',
                              chunksize=None, index=False)
                except sqlite3.IntegrityError as e:
                    print(
                        str(CJX) + " RAW Table Data with same timestamp already consist in database, or same timestamp in the data you are trying to upload. Aborting... \n" + str(
                            e))
                    #  sys.stdout = save_stdout
                    #  log_file.close()
                    return
                except sqlite3.OperationalError as e:
                    print("Missing column in the table: " + str(e))
                    messagebox.showinfo("Column not in Database", str(e) + ".\nYou have to manually add this column. Data NOT written to database.")
                    return
                #except:
                 #   print("Unexpected error:", sys.exc_info()[0])
                try:
                    ''' Update the database_log table with what has been done to the database '''
                    data_log_entry = (
                        'Added ' + str(CJX) + ' RAW String data TID' + str(tid) + ' to database', 'capjet_raw_string', 'iSURVEY')
                    UpdateDB.create_database_log(conn, data_log_entry)
                    print("Wrote to database_log successfully!")
                    messagebox.showinfo(title='Save to SQLite DB',
                                        message='Successfully written data to: ' + str(dbFile))
                except sqlite3.OperationalError:
                    print("FAILED!")
                    print(
                        "DataBase table Exists (database_log), but has the wrong table structure. Update Table or use a different DB. Database_log entry will not be written to DB")
                return
            else:
                #  print("The tid in SQL DB was trenched: " + str(dateofTP))
                #  if (row != ''):
                savetodb = messagebox.askyesno("Overwrite tid" + str(tid), str(CJX) + " RAW String with the same Trenching ID (" + str(
                    tid) + ") already exists in the SQL database. \n\nThe trenching was performed the " + str(
                    dateofTP) + "and uploaded: " + str(timestamp_utc) + " \n\nDo you want to replace this Trenching ID?")
                if (savetodb):
                    print("Overwriting tid: " + str(tid))
                    mydata = cur.execute("DELETE FROM capjet_raw_string WHERE trenching_id=?", (tid,))
                    try:
                        df_merged.to_sql(name='capjet_raw_string', con=conn, index_label='id', if_exists='append',
                                chunksize=None, index=False)
                    except sqlite3.IntegrityError as e:
                        print(
                            "Data with same timestamp already consist in database, or same timestamp in the data you are trying to upload. Aborting... \n" + str(
                                e))
                        #  sys.stdout = save_stdout
                        #  log_file.close()
                        return
                    except sqlite3.OperationalError as e:
                        print("Missing column in the table: " + str(e))
                        messagebox.showinfo("Column not in Database", str(
                            e) + ". You have to manually add this column. Data NOT written to database.")
                        return
                    print("successfully reloaded current data")
                    try:
                        ''' Update the database_log table with what has been done to the database '''
                        data_log_entry = (
                            'Replaced ' + str(CJX) + ' String TID' + str(tid) + ' to database', 'capjet_raw_string', 'iSURVEY')
                        UpdateDB.create_database_log(conn, data_log_entry)
                        print("Wrote to database_log successfully!")
                        messagebox.showinfo(title='Save to SQLite DB',
                                            message='Successfully written data to: ' + str(dbFile))
                    except sqlite3.OperationalError:
                        print("FAILED!")
                        print(
                            "DataBase table Exists (database_log), but has the wrong table structure. Update Table or use a different DB. Database_log entry will not be written to DB")

                    except sqlite3.AttributeError as e:
                        print("Wrong numbers of fields in database_log: " + str(e))

                else:
                    print("Keeping old tid trenching data")
            #  except:
            #   print("Unexpected error:", sys.exc_info()[0])
        print('SQL DB ' + str(CJX) + ' RAW String table Write Results OK')
        return

    def write_result(dbFile, df, tid):
        print("Start updating DB...")
        dburi = 'file:{}?mode=rwc'.format(pathname2url(dbFile))
        try:
            conn = sqlite3.connect(dburi, uri=True)
        except:
            print("Unexpected error Trying to open DB:" + str(sys.exc_info()[0]))

        with conn:
            # Make sure the columns is named the same (May differ between Capjet A and B

            df.columns = ['trenching_pass_id', 'rpl_id', 'time', 'trenching_id', 'easting', 'northing', 'kp', 'dcc', 'sword_stbd', 'sword_port', 'sword_depth', 'speed_along_line',
                    'speed_over_ground', 'roll', 'pitch', 'heading', 'power', 'comment']

            # cols is the order the columns should be uploaded to sqllite
            #  NB! Same Order
            # cols = ['Time', 'tid', 'kp', 'dcc', 'easting', 'northing', 'sword_stbd', 'sword_port', 'speed_along_line',
            #        'speed_over_ground', 'roll', 'pitch', 'heading', 'power', 'comment', 'timestamp_utc']

            # df = df[cols]

            print("Check if TID" + str(tid) + " already exists")
            cur = conn.cursor()
            cur.execute("SELECT time, trenching_id, timestamp_utc FROM trenching WHERE trenching_id = ? ORDER BY time DESC LIMIT 1", (tid,))
            try:
                res_query = cur.fetchone()
                dateofTP = res_query[0]
                TIDofTP = res_query[1]
                timestamp_utc = res_query[2]
            except TypeError:
                dateofTP = None
                TIDofTP = None
                timestamp_utc = None
                pass
            if not TIDofTP:
                print("Trenching ID: " + str(tid) + " does not exist in SQLite DB")
                try:
                    df.to_sql(name='trenching', con=conn, index_label='id', if_exists='append',
                              chunksize=None, index=False)
                except sqlite3.IntegrityError as e:
                    print("Data with same timestamp already consist in database, or same timestamp in the data you are trying to upload. Aborting... \n" + str(e))
                    #  sys.stdout = save_stdout
                    #  log_file.close()
                    return
                try:
                    ''' Update the database_log table with what has been done to the database '''
                    data_log_entry = (
                        'Added trenching data TID' + str(tid) + ' to database', 'trenching', 'iSURVEY')
                    UpdateDB.create_database_log(conn, data_log_entry)
                    print("Wrote to database_log successfully!")
                    messagebox.showinfo(title='Save to SQLite DB',
                                        message='Successfully written data to: ' + str(dbFile))
                except sqlite3.OperationalError:
                    print("FAILED!")
                    print(
                        "DataBase table Exists (database_log), but has the wrong table structure. Update Table or use a different DB. Database_log entry will not be written to DB")
                return
            else:
                #  print("The tid in SQL DB was trenched: " + str(dateofTP))
                #  if (row != ''):
                savetodb = messagebox.askyesno("Overwrite tid"+ str(tid), "Trenching data with the same TID (" + str(tid) + ") already exists in the SQL database. \n\nThe trenching was performed the " + str(dateofTP) + " and uploaded the " + str(timestamp_utc) + ". \n\nDo you want to replace this Trenching ID?")
                if (savetodb):
                    print("Overwriting tid: " + str(tid))
                    mydata = cur.execute("DELETE FROM trenching WHERE trenching_id=?", (tid,))
                    df.to_sql(name='trenching', con=conn, index_label='id', if_exists='append',
                              chunksize=None, index=False)
                    print("successfully reloaded current data")
                    try:
                        ''' Update the database_log table with what has been done to the database '''
                        data_log_entry = (
                        'Replaced trenching data TID' + str(tid) + ' to database', 'trenching', 'iSURVEY')
                        UpdateDB.create_database_log(conn, data_log_entry)
                        print("Wrote to database_log successfully!")
                        messagebox.showinfo(title='Save to SQLite DB',
                                            message='Successfully written data to: ' + str(dbFile))
                    except sqlite3.OperationalError:
                        print("FAILED!")
                        print("DataBase table Exists (database_log), but has the wrong table structure. Update Table or use a different DB. Database_log entry will not be written to DB")

                    except sqlite3.AttributeError as e:
                        print("Wrong numbers of fields in database_log: " + str(e))

                else:
                    print("Keeping old tid trenching data")
            #  except:
             #   print("Unexpected error:", sys.exc_info()[0])
        print("Finished updating DB!")
        return


# disable the speed filtering warning when overwriting its own values
pd.options.mode.chained_assignment = None  # default='warn'

# Suppress Future warnings of: There is a disagreement between Numpy and
# native python on what should happen when you compare a strings to numpy's numeric types
warnings.simplefilter(action='ignore', category=FutureWarning)

def add1():
    try:
        value = float(tid.get('1.0', 'end-1c'))
        value += 1.0
        tid.delete('1.0', END)
        tid.insert(END, value)
    except ValueError as s:
        print("Increment TID did failed: " + str(s))
        return

def subtract1():
    try:
        value = float(tid.get('1.0', 'end-1c'))
        value -= 1.0
        tid.delete('1.0', END)
        tid.insert(END, value)
    except ValueError as s:
        print("Decrement TID did failed: " + str(s))
        return

def addpass1():
    try:
        value = int(t_pass_nr.get('1.0', 'end-1c'))
        value += 1
        t_pass_nr.delete('1.0', END)
        t_pass_nr.insert(END, value)
    except ValueError as s:
        print("Increment Pass Nr. did failed: " + str(s))
        return

def subtractpass1():
    try:
        value = int(t_pass_nr.get('1.0', 'end-1c'))
        value -= 1
        t_pass_nr.delete('1.0', END)
        t_pass_nr.insert(END, value)
    except ValueError as s:
        print("Decrement Pass Nr. did failed: " + str(s))
        return

def limitKpStartField(*args):
    value = kpstart_value.get()
    if len(value) > 8:
        kpstart_value.set(value[:8])
        print("Textfield too long! Max:8")

def limitKpEndField(*args):
    value = kpend_value.get()
    if len(value) > 8:
        kpend_value.set(value[:8])
        print("Textfield too long! Max:8")

def limitTimeStartField(*args):
    value = timestartgui_value.get()
    if len(value) > 21:
        timestartgui_value.set(value[:21])
        print("Textfield too long! Max:21")

def limitTimeEndField(*args):
    value = timeendgui_value.get()
    if len(value) > 21:
        timeendgui_value.set(value[:21])
        print("Textfield too long! Max:21")

def limitNumberField(*args):
    value = kpstart_value.get()
    if len(value) > 7: kpstart_value.set(value[:7])

def menu_instructions():
    webbrowser.open("Instructions_v0.91.pdf")
    return

def menu_settings():
    webbrowser.open("Config_Capjet_Sword_Speed.ini")
    return

def open_messagelog():
    # sys.stdout = save_stdout
    # webbrowser.open(".\\OutputData\\message.log", "a+")
    return

def email_support():
    return

# def videologgerA_settings():
#     #os_command_string = "notepad.exe Batch_Script_VideoLogger_A.bat"
#     #os.system(os_command_string)
#     sp.Popen(["notepad.exe", "Batch_Script_VideoLogger_A.bat"])
#     #webbrowser.open("Batch_Script_VideoLogger_A.bat")
#     return


# def videologgerB_settings():
#     #os_command_string = "notepad.exe Batch_Script_VideoLogger_B.bat"
#     #os.system(os_command_string)
#     #webbrowser.open("Batch_Script_VideoLogger_B.bat")
#     sp.Popen(["notepad.exe", "Batch_Script_VideoLogger_B.bat"])
#     return

def main_setup_settings():
    webbrowser.open("Config_Main_Setup.ini")
    return

# def capjetA_settings():
#     webbrowser.open("Config_Sword_Speed_CapjetA.ini")
#     return

def current_settings():
    index = SETUP_NAME.index(setup_file_variable.get())
    file = SETUP_PATH[index]
    webbrowser.open(file)
    return

def current_batch_script_settings():
    index = SETUP_NAME.index(setup_file_variable.get())
    file = SETUP_BATCH_PATH[index]
    sp.Popen(["notepad.exe", file])
    return

# def capjetB_settings():
#     webbrowser.open("Config_Sword_Speed_CapjetB.ini")
#     return

def menu_about():
    streng="Capjet Sword Speed was created by iSurvey for easier and faster filtering the Sword and Speed data from the Offshore Trenching operations. \n\nThis Scripts is made especially for the Nexans Nordlink project onboard Polar King. \n\nProgram was last compiled by Daniel Skaare the 23.06.2019 (v1.08)\n\n Thank you for using it!"
    messagebox.showinfo("About...", streng)
    return

def menu_versions():
    streng="v1.07:\n- Added settings profiles, so multiple settings can be set up and run\n\n" \
           "v1.08:\n- Capjet raw string will only write to one table in the master file 'capjet_raw_string\n" \
           "- Added depth plot with the possibility to turn it off since it is rather slow\n" \
           "- Added this version list\n" \
           "- Added date conversion on the videologger since this year it was not set up as default format. This is very slow (25s for one TID!) Videologger should be set as default\n" \
           "- Added new variables in settings ini file: [Batch Script]-DestLoc=D:\\temp\InputData, [Default]-Plot_depth_figure = False\n"
    messagebox.showinfo("About...", streng)
    return

def plot_results(panda_data, CJX, df_etr, df_etr_proc, tid):
    #Read in Config file
    Config = configparser.ConfigParser()

    # Get settings file from selected INI file in GUI
    setup_file = SETUP_PATH[SETUP_NAME.index(setup_file_variable.get())]
    Config.read(setup_file)
    capjettype1 = Config["DEFAULT"]['CapjetType1']
    capjettype2 = Config["DEFAULT"]['CapjetType2']
    E = Config["DEFAULT"]['Easting_column']
    N = Config["DEFAULT"]['Northing_column']
    HDG = Config["DEFAULT"]['Heading_column']
    KP = Config["DEFAULT"]['KP_column']
    DCC = Config["DEFAULT"]['DCC_column']
    Sword1 = Config["DEFAULT"]['Sword1_column']
    Sword2 = Config["DEFAULT"]['Sword2_column']
    SOG = Config["DEFAULT"]['Speed_column']
    Capjet_col = Config["DEFAULT"]['Capjet_column']
    Extra_data1 = Config["MISC"]['Extra_data1_avg_column']
    Extra_data2 = Config["MISC"]['Extra_data2_avg_column']
    Extra_data3 = Config["MISC"]['Extra_data3_avg_column']
    DoB_req_KP = Config["DEFAULT"]['DoB_req_KP']
    DoB_req_Depth = Config["DEFAULT"]['DoB_req_Depth']
    dcclowest = Config.getfloat('DCC','DCC_lowest')
    dcchighest = Config.getfloat('DCC','DCC_highest')
    speedlowest = Config.getfloat("Speed",'Speed_lowest')
    speedhighest = Config.getfloat("Speed",'Speed_highest')
    plot_depth_fig = Config.getboolean("DEFAULT", 'Plot_depth_figure')
    # reformat_videologger_timeformat = Config.getboolean("DEFAULT", 'Reformat_videologger_timeformat')
    kps = [float(i) for i in DoB_req_KP.split(',')]
    req = [float(i) for i in DoB_req_Depth.split(',')]
    # use_kalman = Config["Kalman Filter"]['Use_kalman']
    # use_kalman = False

    data1 = {'DateTime': df_etr['Date'] + ' ' + df_etr['Time'], 'WaterDepth': df_etr['WaterDepth']}
    etr_plot = pd.DataFrame(data=data1)
    etr_plot['DateTime'] = pd.to_datetime(etr_plot['DateTime'], format='%d-%m-%y %H:%M:%S:%f"', errors='ignore')
    etr_plot['WaterDepth'] = pd.to_numeric(etr_plot['WaterDepth'])
    #etr_plot.set_index(['Time'], inplace=True)

    data1 = {'DateTime': df_etr_proc['Date'] + ' ' + df_etr_proc['Time'], 'WaterDepth': df_etr_proc['WaterDepth']}
    etr_proc_plot = pd.DataFrame(data=data1)
    etr_proc_plot['DateTime'] = pd.to_datetime(etr_proc_plot['DateTime'], format='%d-%m-%y %H:%M:%S:%f"', errors='ignore')
    #etr_proc_plot.set_index(['Time'], inplace=True)

    # etr_time['Time'] = pd.to_datetime(df_etr['Date'] + ' ' + df_etr['Time'], format='%d-%m-%y %H:%M:%S:%f"', errors='ignore')
    # etr_proc_time['Time'] = pd.to_datetime(df_etr_proc['Date'] + ' ' + df_etr_proc['Time'], format='%d-%m-%y %H:%M:%S:%f"', errors='ignore')
    # data.set_index(['time'], inplace=True)
    kpmin = panda_data[KP].min()
    kpmax = panda_data[KP].max()
    # Plot Figure1 and results
    fig = plt.figure()
    fig.subplots_adjust(left=None, bottom=None, right=0.75, top=None,
                wspace=None, hspace=None)
    ax1 = fig.add_subplot(211)
    ax1.set_title("TID: %s, %s %s KP %s - KP %s" %(str(tid), capjettype1, capjettype2, str(kpmin), str(kpmax)))
    ax1.set_ylabel('Sword Depth [m]')
    ax1.plot(kps, req, 'r--', label='Requirement')
    ax1.plot(panda_data[KP], panda_data['STBD_Sword_Depth'], 'g.-', label=Sword1)
    ax1.plot(panda_data[KP], panda_data['Port_Sword_Depth'], 'b.-', label=Sword2)
    ax1.plot(panda_data[KP], panda_data['Sword_Depth'], 'k-', label='Sword Depth')
    #plt.gca().invert_yaxis()
    leg = ax1.legend(bbox_to_anchor=(1.03, 1), loc=2, borderaxespad=0.)
    ax2 = fig.add_subplot(212, sharex=ax1)
    ax2.plot(panda_data[KP], panda_data['SAL'], 'b--', label='SAL')
    ax2.plot(panda_data[KP], panda_data[SOG], 'g--', label=SOG)
    ax2.plot(panda_data[KP], panda_data['Speed_Along_Line'], 'y', label='SAL smooth')
    ax2.plot(panda_data[KP], panda_data['Speed_Over_Ground'], 'm', label='SOG smooth')
    ax2.plot([kpmin, kpmax], [speedhighest, speedhighest], 'r--', label='Filter1')
    ax2.plot([kpmin, kpmax], [speedlowest, speedlowest], 'r--', label='Filter2')
    ax2.set_xlabel(KP)
    ax2.set_ylabel('Capjet Speed [m/min]')
    leg2 = ax2.legend(bbox_to_anchor=(1.03, 1), loc=2, borderaxespad=0.)
    plt.xlim([kpmin, kpmax])
    # thismanager = get_current_fig_manager()
    # thismanager.window.SetPosition((500, 0))
    plt.show(block=False)

    #Plot Figure2 and results
    fig2 = plt.figure()
    fig2.subplots_adjust(left=None, bottom=None, right=0.84, top=None,
                        wspace=None, hspace=None)
    ax1 = fig2.add_subplot(311)
    ax1.set_title("TID: %s, %s %s KP %s - KP %s" % (str(tid), capjettype1, capjettype2, str(kpmin), str(kpmax)))
    ax1.set_xlabel('KP')
    ax1.set_ylabel('[Deg]')
    ax1.plot(panda_data[KP], panda_data['Roll'], 'g', label=Extra_data1)
    ax1.plot(panda_data[KP], panda_data['Pitch'], 'b', label=Extra_data2)
    leg1 = ax1.legend(bbox_to_anchor=(1.03, 1), loc=2, borderaxespad=0.)
    ax2 = fig2.add_subplot(312, sharex=ax1)
    ax2.plot(panda_data[KP], panda_data[HDG], 'r', label='Gyro')
    ax2.set_xlabel(KP)
    ax2.set_ylabel('HDG [Deg]')
    leg2 = ax2.legend(bbox_to_anchor=(1.03, 1), loc=2, borderaxespad=0.)
    plt.xlim([kpmin, kpmax])

    ax3 = fig2.add_subplot(313, sharex=ax1)
    ax3.plot(panda_data[KP], panda_data['Capjet_Power'], 'k', label=Extra_data3)
    ax3.set_xlabel(KP)
    ax3.set_ylabel('Power [kW]')
    leg3 = ax3.legend(bbox_to_anchor=(1.03, 1), loc=2, borderaxespad=0.)
    plt.xlim([kpmin, kpmax])
    plt.show(block=False)

        #Plot Figure3 and results
    # Sub figure 1
    fig3 = plt.figure()
    # ax1 = fig3.add_subplot(411)
    ax1 = plt.subplot2grid((3, 2), (0, 0), colspan=2)
    ax1.set_title("TID: %s, %s %s KP %s - KP %s" % (str(tid), capjettype1, capjettype2, str(kpmin), str(kpmax)))
    ax1.set_xlabel('Easting [m]')
    ax1.set_ylabel('Northing [m]')
    ax1.plot(df_etr['Easting'], df_etr['Northing'], 'k.', label='RAW ETR')
    # if use_kalman:
    #     ax1.plot(df_etr_proc['Easting_Kal'], df_etr_proc['Northing_Kal'], 'c', label='KALMAN ETR')
    ax1.plot(panda_data[E], panda_data[N], 'g', label='Capjet Track per meter')
    ax1.plot(df_etr_proc['Easting'], df_etr_proc['Northing'], 'b', label='PROC ETR')
    # ax1yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    # ax1xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax1.legend()

    # # Sub figure 2
    # ax2 = plt.subplot2grid((3, 2), (0, 0))
    # ax2.set_xlabel('Time [dd-mm-yy hh:mm:ss]')
    # ax2.set_ylabel('Depth [m]')
    # ax2.plot(etr_plot.index, etr_plot['WaterDepth'], 'k.', label='RAW Depth')
    # ax2.plot(etr_proc_plot.index, etr_proc_plot['WaterDepth'], 'b', label='PROC Depth')
    # ax2.legend()
    # print("worked")

    # Sub figure 3
    ax3 = plt.subplot2grid((3, 2), (2, 0), colspan=1)
    ax3.plot(df_etr[KP], df_etr['Easting'], 'k.', label='RAW ETR')
    ax3.plot(panda_data[KP], panda_data[E], 'g', label='Capjet Track per meter')
    # ax2.plot(df_etr_proc[KP], df_etr_proc['Easting'], 'b', label='PROC ETR')
    ax3.set_xlabel(KP)
    ax3.set_ylabel(E)
    ax3.legend()

    # Sub figure 4
    ax4 = plt.subplot2grid((3, 2), (2, 1), colspan=1, sharex=ax2)
    ax4.plot(df_etr[KP], df_etr['Northing'], 'k.', label='RAW ETR')
    ax4.plot(panda_data[KP], panda_data[N], 'g', label='Capjet Track per meter')
    #ax3.plot(df_etr_proc[KP], df_etr_proc['Northing'], 'b', label='PROC ETR')
    ax4.set_xlabel(KP)
    ax4.set_ylabel(N)
    ax4.legend()
    #ax3.set_ylim([panda_data[N].min(), panda_data[N].max()])
    plt.show(block=False)


        #Plot Figure4 and results
    missing_data = pd.DataFrame(data={'KP': panda_data[KP]})
    missing_data['MissingData'] = panda_data[Capjet_col].isna()
    missing_data['MissingData'] = missing_data['MissingData'].map({True: 'Yes', False: 'No'})

    fig4 = plt.figure()
    fig4.subplots_adjust(left=None, bottom=None, right=0.83, top=None,
                        wspace=None, hspace=None)
    ax1 = fig4.add_subplot(211)
    ax1.set_title("TID: %s, %s %s KP %s - KP %s" % (str(tid), capjettype1, capjettype2, str(kpmin), str(kpmax)))
    ax1.set_ylabel('DCC')
    ax1.plot(panda_data[KP], panda_data[DCC], 'b', label='DCC')
    ax1.plot([panda_data[KP].min(), panda_data[KP].max()], [dcclowest, dcclowest], 'r--', label='Filter 1')
    ax1.plot([panda_data[KP].min(), panda_data[KP].max()], [dcchighest, dcchighest], 'r--', label='Filter 2')
    leg = ax1.legend(bbox_to_anchor=(1.03, 1), loc=2, borderaxespad=0.)
    ax2 = fig4.add_subplot(212, sharex=ax1)
    ax2.plot(missing_data['KP'], missing_data['MissingData'], 'k.')
    ax2.set_xlabel(KP)
    ax2.set_ylabel('Missing Data?')
    # leg2 = ax2.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

    plt.show(block=False)
    # Plot Figure 5 - Test
    if plot_depth_fig == True:
        print("Plotting depth figure takes additional time.. (This can be turned off in config file)")

        etr_plot['DateTime'] = pd.to_datetime(etr_plot['DateTime'])
        etr_proc_plot['DateTime'] = pd.to_datetime(etr_proc_plot['DateTime'])
        fig5 = plt.figure()
        ax1 = fig5.add_subplot(211)
        #ax1.set_xlabel('Time [dd-mm-yy hh:mm:ss]')
        ax1.set_ylabel('Depth [m]')
        ax1.plot(etr_plot['DateTime'], etr_plot['WaterDepth'], 'b', label='RAW Depth')
        ax1.legend()
        #plt.show(block=False)

        #ax2.set_xlabel('Time [dd-mm-yy hh:mm:ss]')
        ax1.set_ylabel('Depth [m]')
        #ax2.plot(etr_plot['WaterDepth'], 'k.', label='RAW Depth')
        ax1.plot(etr_proc_plot['DateTime'], etr_proc_plot['WaterDepth'], 'k', label='PROC Depth')
        #plt.xticks(rotation='vertical')
        ax1.legend()
        plt.show(block=False)

    return


def run_script(CJX, tid, t_pass_nr, time_start_gui, time_end_gui, kpstart, kpend, CheckVar1, CheckVar2):

   #   log_file = open(".\\OutputData\\message.log", "a")
   #   sys.stdout = log_file
    try:
        tid = float(tid.get('1.0', 'end-1c'))
        # tid = tid.strip('\n')
    except ValueError:
        messagebox.showwarning("Abort...", "Trenching ID is not a number")
        #  sys.stdout = save_stdout
        #  log_file.close()
        return
    try:
        t_pass_nr = float(t_pass_nr.get('1.0', 'end-1c'))
        # t_pass_nr = t_pass_nr.strip('\n')
    except ValueError:
        messagebox.showwarning("Abort...", "Trenching Pass Number is NOT an integer")
        # sys.stdout = save_stdout
        # log_file.close()
        return
    try:
        kplowest = float(kpstart_value.get())
    except ValueError:
        messagebox.showwarning("Abort...", "Lowest KP is NOT a number: " + str(kpstart_value.get()))
        # sys.stdout = save_stdout
        # log_file.close()
        return
    try:
        kphighest = float(kpend_value.get())
    except ValueError:
        messagebox.showwarning("Abort...", "Highest KP is NOT number: " + str(kpend_value.get()))
        # sys.stdout = save_stdout
        # log_file.close()
        return

    if kphighest < kplowest:
        messagebox.showwarning("Abort...", "KP lowest must by lower than KP highest! \n\n Er du innleigd på dette prosjektet kanskje??")
        return

    try:
        # time_start_gui = str(time_start_gui.get('1.0', 'end-1c'))
        # time_start_gui = time_start_gui.strip('\n')
        time_start_gui = str(time_start_gui.get())
        time_start_gui = time_start_gui.strip('\n')
    except ValueError as e:
        messagebox.showwarning("Abort...", "Time start is not a valid string: " + str(e))
        # sys.stdout = save_stdout
        # log_file.close()
        return
    try:
        # time_end_gui = str(time_end_gui.get('1.0', 'end-1c'))
        # time_end_gui = time_end_gui.strip('\n')
        time_end_gui = str(time_end_gui.get())
        time_end_gui = time_end_gui.strip('\n')
    except ValueError as e:
        messagebox.showwarning("Abort...", "Time end is not a valid string:" + str(e))
        # sys.stdout = save_stdout
        # log_file.close()
        return

    print('You pushed the ' + str(CJX) + ' button' + ' On task plan: ' + str(tid) + ' To filter between: ' + str(time_start_gui) + ' -> ' + str(time_end_gui))
    start_time = time.time()

    #Read in Config file
    Config = configparser.ConfigParser()
    setup_file = SETUP_PATH[SETUP_NAME.index(setup_file_variable.get())]
    if (Config.read(setup_file) == []):
        err0 = str(setup_file) + " file not found in current directory"
        print(err0)
        messagebox.showwarning("Try Again...", err0)
        return

    projnr = Config["DEFAULT"]['ProjectNr']
    runlineid = Config["DEFAULT"]['RunlineID']
    sqlitepath = Config["DEFAULT"]['SQLiteDB']
    dateformat = Config["DEFAULT"]['DateFormat']
    capjettype1 = Config["DEFAULT"]['CapjetType1']
    capjettype2 = Config["DEFAULT"]['CapjetType2']
    print("Capjet chosen: " + capjettype1 + " and " + capjettype2)
    # kplowest = Config.getfloat("DEFAULT", 'KP_lowest')
    # kphighest = Config.getfloat("DEFAULT", 'KP_highest')
    #   datestart = Config["DEFAULT"]['Date_start']
    #  timestart2 = Config["DEFAULT"]['Time_start']
    timestart2 = time_start_gui
    # dateend = Config["DEFAULT"]['Date_end']
    #  timeend2 = Config["DEFAULT"]['Time_end']
    timeend2 = time_end_gui
    timefilterformat = Config["DEFAULT"]['Time_filter_format_gui']
    E = Config["DEFAULT"]['Easting_column']
    N = Config["DEFAULT"]['Northing_column']
    HDG = Config["DEFAULT"]['Heading_column']
    KP = Config["DEFAULT"]['KP_column']
    DCC = Config["DEFAULT"]['DCC_column']
    Depth = Config["DEFAULT"]['Depth_column']
    Sword1 = Config["DEFAULT"]['Sword1_column']
    Sword2 = Config["DEFAULT"]['Sword2_column']
    SOG = Config["DEFAULT"]['Speed_column']
    Time = Config["DEFAULT"]['Time_column']
    Date = Config["DEFAULT"]['Date_column']
    Capjet_col = Config["DEFAULT"]['Capjet_column']
    interpol = Config.getboolean("DEFAULT",'Interpolate_Data')
    Export_dir = Config["DEFAULT"]['Export_dir']
    Extra_data1 = Config["MISC"]['Extra_data1_avg_column']
    Extra_data2 = Config["MISC"]['Extra_data2_avg_column']
    Extra_data3 = Config["MISC"]['Extra_data3_avg_column']
    Extra_data1_lowest = Config.getfloat("MISC",'Extra_data1_lowest')
    Extra_data1_highest = Config.getfloat("MISC",'Extra_data1_highest')
    Extra_data1_smooth_factor = Config.getint("MISC",'Extra_data1_smooth_factor')
    Extra_data2_lowest = Config.getfloat("MISC",'Extra_data2_lowest')
    Extra_data2_highest = Config.getfloat("MISC",'Extra_data2_highest')
    Extra_data2_smooth_factor = Config.getint("MISC",'Extra_data2_smooth_factor')
    Extra_data3_lowest = Config.getfloat("MISC",'Extra_data3_lowest')
    Extra_data3_highest = Config.getfloat("MISC",'Extra_data3_highest')
    Extra_data3_smooth_factor = Config.getint("MISC",'Extra_data3_smooth_factor')
    Position_smooth_factor = Config.getint("Position", 'Position_smooth_factor')
    sword1lowest = Config.getfloat("Sword1",'Sword1_lowest')
    sword1highest = Config.getfloat("Sword1",'Sword1_highest')
    sword2lowest = Config.getfloat("Sword2",'Sword2_lowest')
    sword2highest = Config.getfloat("Sword2",'Sword2_highest')
    dcclowest = Config.getfloat('DCC','DCC_lowest')
    dcchighest = Config.getfloat('DCC','DCC_highest')
    speedlowest = Config.getfloat("Speed",'Speed_lowest')
    speedhighest = Config.getfloat("Speed",'Speed_highest')
    speedsmoothfactor = Config.getint("Speed",'Speed_smooth_factor')
    remkpfilt1 = Config["KP Filter"]['remove_KP_filter1']
    remkpfilt2 = Config["KP Filter"]['remove_KP_filter2']
    remkpfilt3 = Config["KP Filter"]['remove_KP_filter3']
    remkpfilt4 = Config["KP Filter"]['remove_KP_filter4']
    remkpfilt5 = Config["KP Filter"]['remove_KP_filter5']
    remkpfilt6 = Config["KP Filter"]['remove_KP_filter6']
    remkpfilt7 = Config["KP Filter"]['remove_KP_filter7']
    remkpfilt8 = Config["KP Filter"]['remove_KP_filter8']
    remasffilt1 = Config["ASFIndex Filter"]['remove_ASF_filter1']
    remasffilt2 = Config["ASFIndex Filter"]['remove_ASF_filter2']


    # use_kalman = Config["Kalman Filter"]['Use_kalman']
    use_kalman = False
    smooth_etr_proc = Config.getint("ETR PROC", 'Smooth_position')
    smooth_depth_etr_proc = Config.getint("ETR PROC", 'Smooth_depth')

    # Check if Export Dir exists
    if not os.path.isdir(Export_dir):
        answer = messagebox.askyesnocancel("Create Directory?", "Directory " + str(Export_dir) + " does not exist. Create it? \n\n If not Default Output Folder will be used")
        if answer:
            os.mkdir(Export_dir)
        else:
            Export_dir = os.getcwd() + '\\OutputData'

    print(Export_dir)

    if CheckVar1.get():
        print("Run batch script is checked, start copying files")
        # Batch script needs mm-dd-yyyy
        try:
            d = datetime.strptime(timestart2, timefilterformat)
            dend = datetime.strptime(timeend2, timefilterformat)
        except ValueError as e:
            # print(d)
            # print(dend)
            err0 = "Start and/or Stop date is not in correct format, did you forget seconds?\n\n" + str(e)
            print(err0)
            messagebox.showwarning("Try Again...", err0)
            return
        dend = dend + timedelta(days=2)  # Due to Robocopy
        batch_date_start = d.strftime('%Y') + d.strftime('%m') + d.strftime('%d')  # robocopy
        batch_date_end = dend.strftime('%Y') + dend.strftime('%m') + dend.strftime('%d')  # robocopy

        # xcopy batch_date_start = d.strftime('%m') + '-' + d.strftime('%d') + '-' + d.strftime('%Y')
        # xcopy batch_date_end = dend.strftime('%m') + '-' + dend.strftime('%d') + '-' + dend.strftime('%Y')
        print('Start copy data from date(mm-dd-yyyy): ' + str(batch_date_start) + ' To: ' + str(batch_date_end))
        if CJX == 'CJA':
            print("run CJA script")

            # Get Batch Script file from selected setup
            batch_script_file = SETUP_BATCH_PATH[SETUP_NAME.index(setup_file_variable.get())]
            p = sp.Popen([batch_script_file, str(tid), batch_date_start, batch_date_end], stdout=sp.PIPE, shell=True)
            # p = sp.Popen(["Batch_Script_VideoLogger_A.bat", str(tid), batch_date], stdout=sp.PIPE, shell=True)
            stdout2, stderr2 = p.communicate()
            file = open("OutputData/BatchLogfile_VideoLogger_A_TID" + str(tid) + ".log", "wb")
            file.write(stdout2)

            file = open("OutputData/BatchLogfile_VideoLogger_A_TID" + str(tid) + ".log", "r")
            line_list = file.readlines()
            file.close()
            input_file = line_list[-1].replace('\n', '')
            print("Successfully created:  " + str(input_file))
            # read csv file
            try:
                df = pd.read_csv(os.path.realpath(input_file))
            except IOError as e:
                err0 = str(input_file) + " file not found. Run Batch Script to create it, or untick Batch Script and create an CSV in './InputData/input_" + str(tid) + ".csv"
                print(err0)
                messagebox.showwarning("Try Again...", err0)
                # sys.stdout = save_stdout
                # log_file.close()
                return

        elif CJX == 'CJB':
            print("Run batch script is checked, start copying files")
            if CJX == 'CJB':
                print("run CJB script")
                # Get Batch Script file from selected setup
                batch_script_file = SETUP_BATCH_PATH[SETUP_NAME.index(setup_file_variable.get())]
                p = sp.Popen([batch_script_file, str(tid), batch_date_start, batch_date_end], stdout=sp.PIPE, shell=True)
                stdout2, stderr2 = p.communicate()
                file = open("OutputData/BatchLogfile_VideoLogger_B_TID" + str(tid) + ".log", "wb")
                file.write(stdout2)

                file = open("OutputData/BatchLogfile_VideoLogger_B_TID" + str(tid) + ".log", "r")
                line_list = file.readlines()
                file.close()
                input_file = line_list[-1].replace('\n', '')
                print("Successfully created:  " + str(input_file))
                # read csv file
                try:
                    df = pd.read_csv(os.path.realpath(input_file))
                except IOError as e:
                    err0 = str(
                        input_file) + " file not found. Run Batch Script to create it, or untick Batch Script and create an CSV in './InputData/input_TID" + str(tid) + ".csv"
                    print(err0)
                    messagebox.showwarning("Try Again...", err0)
                    # sys.stdout = save_stdout
                    # log_file.close()
                    return
    else:

        batch_script_loc = Config["Batch Script"]['DestLoc']
        print("Batch Script not selected. Will look for the input file in this location" + str(batch_script_loc) + "\input_TID" + str(tid) + ".csv' and run script from that")
        # read csv file
        try:
            input_file = str(batch_script_loc) + "\input_TID" + str(tid) + ".csv"
            print(str(input_file))
            df = pd.read_csv(input_file)
        except IOError as e:
            err0 = str(input_file) + " file not found. Run Batch Script to create it, or untick Batch Script and create an CSV in " + str(input_file)
            print(err0)
            messagebox.showwarning("Try Again...", err0)
            # sys.stdout = save_stdout
            # log_file.close()
            return


    # filtering on capjet
    try:
        df_filtered = df[(df[Capjet_col] == capjettype1) | (df[Capjet_col] == capjettype2)]
    except KeyError as e:
        print("The Capjet Column does not include this value: " + str(e) + " Aborting script....")
        # sys.stdout = save_stdout
        # log_file.close()
        return

    #df_filtered = df

    #Filter: Remove multiple headers
    try:
        df_filtered = df_filtered[(df_filtered[remasffilt1] != remasffilt1)]
    except (TypeError, KeyError) as e:
        pass
        # print("Check remasffilt1. Can not find: " + str(e))

    try:
        df_filtered = df_filtered[(df_filtered[remasffilt2] != remasffilt2)]
    except (TypeError, KeyError) as e:
        pass
        # print("Check remasffilt2. Can not find: " + str(e))

    try:
        #Filter: Remove unvalid data
        df_filtered = df_filtered[(df_filtered[KP] != remkpfilt1)]
        df_filtered = df_filtered[(df_filtered[KP] != remkpfilt2)]
        df_filtered = df_filtered[(df_filtered[KP] != remkpfilt3)]
        df_filtered = df_filtered[(df_filtered[KP] != remkpfilt4)]
        df_filtered = df_filtered[(df_filtered[KP] != remkpfilt5)]
        df_filtered = df_filtered[(df_filtered[KP] != remkpfilt6)]
        df_filtered = df_filtered[(df_filtered[KP] != remkpfilt7)]
        df_filtered = df_filtered[(df_filtered[KP] != remkpfilt8)]

    except TypeError as e:
        print("The input_TID" + str(tid) + ".csv only include one dataset/video")



    # Convert Datestring to string
 #   try:
  #      df_filtered[dateformat] = pd.to_string(df_filtered[dateformat])
   # except ValueError as e:
    #    print('Problems converting datestring to string: ' str(e))


    #  Replace CONV.ERR
    df_filtered[Date] = df_filtered[Date].replace(['CONV.ERR'], np.nan).ffill()
    #  Filter: Set data time span
    try:
        df_filtered['Time'] = pd.to_datetime(df_filtered[Date] + ' ' + df_filtered[Time], format=dateformat, errors='ignore')
        #df_filtered['Time'] = [datetime.strptime(x, dateformat) for x in df_filtered['Time']]
        datetime_start = datetime.strptime(timestart2, timefilterformat)
        datetime_end = datetime.strptime(timeend2, timefilterformat)
    except ValueError as e:
        err1 = 'ERROR: ' + str(e) + ' Change the DateFormat in the ini file'
        print(err1)
        messagebox.showwarning("Try Again...", err1)
        # sys.stdout = save_stdout
        # log_file.close()
        return
    except TypeError as e:
        err1 = "Check the Date string in the input.csv. Is the first value 'CONV.ERR'? Change it to a proper date\n\n" + str(e)
        print(err1)
        messagebox.showwarning("Try Again...", err1)
        # sys.stdout = save_stdout
        # log_file.close()
        return
    try:
        date_text = df_filtered['Time'].iloc[1]
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        try:
            start_time_test = time.time()
            print("Start reformating Videologger timeformat... Takes time....")
            df_filtered['Time'] = pd.to_datetime(df_filtered['Time'])
            print("Finished in: %.3f seconds" % (time.time() - start_time_test))
        except:
            print("Error: Trying to convert input.csv to standard timeformat...")

    try:
        df_filtered = df_filtered[( df_filtered['Time'] >= datetime_start) & (df_filtered['Time'] <= datetime_end)]
    except TypeError as e:
        err1 = "Check the Date string in the input.csv. Looks like the value is: " + str(df_filtered['Time'].iloc[1]) + " while the start date format is: " + str(datetime_end) +  " \n\n" + str(e)
        print(err1)
        messagebox.showwarning("Try Again...", err1)
        return



    #Convert DataFrame into correct dtypes
    try:
        df_filtered[E] = pd.to_numeric(df_filtered[E])
        df_filtered[N] = pd.to_numeric(df_filtered[N])
        df_filtered[HDG] = pd.to_numeric(df_filtered[HDG])
        df_filtered[KP] = pd.to_numeric(df_filtered[KP])
        df_filtered[Sword1] = pd.to_numeric(df_filtered[Sword1])
        df_filtered[Sword2] = pd.to_numeric(df_filtered[Sword2])
        df_filtered[DCC] = pd.to_numeric(df_filtered[DCC])
        df_filtered[SOG] = pd.to_numeric(df_filtered[SOG])
        df_filtered[Extra_data1] = pd.to_numeric(df_filtered[Extra_data1])
        df_filtered[Extra_data2] = pd.to_numeric(df_filtered[Extra_data2])
        df_filtered[Extra_data3] = pd.to_numeric(df_filtered[Extra_data3])

    except ValueError as e:
        err1 = str(e) + ". \nAdd a new filter in the Config ini file. \nAdd that string under_remove_KP_filterX_ and try again. \n \nStop executing script."
        print(err1)
        messagebox.showwarning("Try Again...", err1)
        # sys.stdout = save_stdout
        # log_file.close()
        return
    except KeyError as e:
        err1 = "Have you defined the columns correctly in the ini file? Error column: " + str(e) +" \n \nStop executing script."
        print(err1)
        messagebox.showwarning("Try Again...", err1)
        # sys.stdout = save_stdout
        # log_file.close()
        return

    # Export Capjet RAW Track
    try:
        dateformatet = pd.to_datetime(df_filtered['Time'], format=dateformat, errors='ignore')
        d = {'DateTime': dateformatet, 'Date': dateformatet.dt.strftime('%d-%m-%y'), 'Time': dateformatet.dt.strftime('%H:%M:%S.%f').str[:-3], 'Easting': df_filtered[E], 'Northing': df_filtered[N], 'WaterDepth': df_filtered[Depth], 'Roll': df_filtered['Roll'], 'Pitch':  df_filtered['Pitch'], 'Heading': df_filtered[HDG], KP: df_filtered[KP]}
        # d = {'DateTime': dateformatet, '#DAY-MONTH-YEAR': dateformatet.dt.strftime('%d-%m-%y'), 'HOUR:MIN:SEC.AAA': dateformatet.dt.strftime('%H:%M:%S.%f').str[:-3], 'EASTING': df_filtered[E], 'NORTHING': df_filtered[N], 'DEPTH': df_filtered[Depth], 'ROLL': df_filtered['Roll'], 'PITCH': df_filtered['Pitch'], 'HEADING': df_filtered[HDG]}

        df_etr = pd.DataFrame(data=d)
        df_etr['Tide'] = 0.00
        df_etr_proc = pd.DataFrame(data=d)
        df_etr_proc['Tide'] = 0.00
        df_etr_proc[DCC] = df_filtered[DCC]
        Export_dir = Export_dir + '/TID' + str(tid) + '/'
        export_etr1 = projnr + ' ISAS B02 TID' + str(tid) + ' RAW KP' + "{:.3f}".format(df_filtered[KP].min()) + '-' + "{:.3f}".format(df_filtered[KP].max()) + ' ' + capjettype1 + capjettype2 + '.etr'
        df_etr = df_etr.sort_values(by='DateTime')
        # df_etr[['EASTING', 'NORTHING']] = df_etr[['EASTING', 'NORTHING']].astype(str)
        # df_etr.round({'EASTING': 3, 'NORTHING': 3})
        try:
            if not os.path.exists(Export_dir):
                os.mkdir(Export_dir)
            df_etr[['Date', 'Time', 'Easting', 'Northing', 'WaterDepth', 'Roll', 'Pitch', 'Heading', 'Tide']].to_csv(Export_dir + export_etr1, sep=' ', index=False)
            # df_etr[['#DAY-MONTH-YEAR', 'HOUR:MIN:SEC.AAA', 'EASTING', 'NORTHING', 'DEPTH', 'ROLL', 'PITCH', 'HEADING', 'TIDE']].to_csv(export_etr1, sep='\t', index=False)
        except IOError as e:
            err2 = "Close the: " + export_etr1 + " file and try again to get the Capjet Track ETR!"
            messagebox.showwarning("Try Again...", str(e))
            print(err2)
        print("Successfully exported RAW E-TRACK to: " + str(export_etr1))
    except:
        print("failed to export ETR")
        print("Unexpected error:", sys.exc_info()[0])
        pass



    # Calculate from Knots to meter/min
    df_filtered[SOG] = 0.514444444*df_filtered[SOG]*60
    # Read in target depth
    # Remove all data not in the valid area
    df_filtered = df_filtered[( df_filtered[KP] >= kplowest) & (df_filtered[KP] <= kphighest)]
    df_filtered = df_filtered[( df_filtered[DCC] >= dcclowest) & (df_filtered[DCC] <= dcchighest) ]


    df_etr_proc = df_etr_proc[( df_etr_proc[KP] >= kplowest) & (df_etr_proc[KP] <= kphighest)]
    df_etr_proc = df_etr_proc[( df_etr_proc[DCC] >= dcclowest) & (df_etr_proc[DCC] <= dcchighest) ]

   # smooth ETR PROC
    df_etr_proc['Northing'] = df_etr_proc['Northing'].rolling(smooth_etr_proc, center=True, min_periods=1).mean()
    df_etr_proc['Easting'] = df_etr_proc['Easting'].rolling(smooth_etr_proc, center=True, min_periods=1).mean()
    df_etr_proc['WaterDepth'] = df_etr_proc['WaterDepth'].rolling(smooth_depth_etr_proc, center=True, min_periods=1).mean()

    df_etr_proc = df_etr_proc.round({'Easting': 2, 'Northing': 2, 'WaterDepth': 2, 'Roll': 2, 'Pitch': 2,'Heading': 2, KP: 3, DCC: 2})

    # df_filtered = df_filtered[( df_filtered[Sword1] >= sword1lowest) & (df_filtered[Sword1] <= sword1highest) ]
    # df_filtered = df_filtered[( df_filtered[Sword2] >= sword2lowest) & (df_filtered[Sword2] <= sword2highest) ]

    # Filter Unreasonable values
    df_filtered[Sword1][(df_filtered[Sword1] < sword1lowest) | (df_filtered[Sword1] > sword1highest)] = np.NaN
    df_filtered[Sword2][(df_filtered[Sword2] < sword2lowest) | (df_filtered[Sword2] > sword2highest)] = np.NaN
    df_filtered[Extra_data1][(df_filtered[Extra_data1] < Extra_data1_lowest) | (df_filtered[Extra_data1] > Extra_data1_highest)] = np.NaN
    df_filtered[Extra_data2][(df_filtered[Extra_data2] < Extra_data2_lowest ) | (df_filtered[Extra_data2] > Extra_data2_highest)] = np.NaN
    df_filtered[Extra_data3][(df_filtered[Extra_data3] < Extra_data3_lowest ) | (df_filtered[Extra_data3] > Extra_data3_highest)] = np.NaN

    
    # Round
    df_filtered = df_filtered.round({KP: 3, Sword1: 2, Sword2: 2, Extra_data1: 2, Extra_data2: 2, Extra_data3: 3})

    # sort
    df_filtered = df_filtered.sort_values(KP, ascending=True)

    # Filter SOG Speed
    df_filtered[SOG][df_filtered[SOG]<speedlowest]=np.NaN
    df_filtered[SOG][df_filtered[SOG]>speedhighest]=np.NaN
    
    # Filter max values
    df_filtered['STBD_Sword_Depth'] = df_filtered.groupby([KP])[Sword1].transform(max)
    df_filtered['Port_Sword_Depth'] = df_filtered.groupby([KP])[Sword2].transform(max)
    df_filtered['Swords_Depth'] = (df_filtered['STBD_Sword_Depth'] + df_filtered['Port_Sword_Depth'])/2
    df_filtered['Speed_Over_Ground'] = df_filtered.groupby([KP])[SOG].transform(np.mean)
    df_filtered['Roll'] = df_filtered.groupby([KP])[Extra_data1].transform(np.mean)
    df_filtered['Pitch'] = df_filtered.groupby([KP])[Extra_data2].transform(np.mean)
    df_filtered['Capjet_Power'] = df_filtered.groupby([KP])[Extra_data3].transform(np.mean)

    # Filter position as median for every KP
    df_filtered[E] = df_filtered.groupby([KP])[E].transform(np.median)
    df_filtered[N] = df_filtered.groupby([KP])[N].transform(np.median)
    before = len(df_filtered.KP)
    df_filtered = df_filtered.drop_duplicates([KP])
    df_shifted = df_filtered.shift(1)

    try:
        df_filtered['deltaT'] = (df_filtered['Time'] - df_shifted['Time']) / np.timedelta64(1, 's')
    except TypeError as e:
        print("Something went wrong, Is the Date_start in the ini file set to high? " + str(e))
        # sys.stdout = save_stdout
        # log_file.close()
        return
        
    df_filtered['SAL'] = abs((df_filtered[KP] - df_shifted[KP])*1000/((df_filtered['Time'] - df_shifted['Time']) / np.timedelta64(1, 's')/60))

    # Filter SAL Speed
    df_filtered.SAL[df_filtered.SAL < speedlowest] = np.NaN
    df_filtered.SAL[df_filtered.SAL > speedhighest] = np.NaN
    df_filtered['Speed_Along_Line'] = df_filtered['SAL'].rolling(speedsmoothfactor, center=True, min_periods=1).sum()/speedsmoothfactor
    df_filtered['Speed_Over_Ground'] = df_filtered[SOG].rolling(speedsmoothfactor, center=True, min_periods=1).sum()/ speedsmoothfactor
    df_filtered['Roll'] = df_filtered['Roll'].rolling(Extra_data1_smooth_factor, center=True, min_periods=1).sum()/Extra_data1_smooth_factor
    df_filtered['Pitch'] = df_filtered['Pitch'].rolling(Extra_data2_smooth_factor, center=True, min_periods=1).sum()/Extra_data2_smooth_factor
    df_filtered['Capjet_Power'] = df_filtered['Capjet_Power'].rolling(Extra_data3_smooth_factor, center=True,min_periods = 1).sum()/Extra_data3_smooth_factor
    # df_filtered[E] = df_filtered[E].rolling(Position_smooth_factor, center=True, min_periods=1).sum() / Position_smooth_factor
    # df_filtered[N] = df_filtered[N].rolling(Position_smooth_factor, center=True, min_periods=1).sum() / Position_smooth_factor
    df_filtered[E] = df_filtered[E].rolling(Position_smooth_factor, center=True, min_periods=1).mean()
    df_filtered[N] = df_filtered[N].rolling(Position_smooth_factor, center=True, min_periods=1).mean()

    # Apply Kalman Filtering of ETR PROC, https://pykalman.github.io/
    # if use_kalman:
    #    measurements = df_etr_proc[['Easting', 'Northing']].values
    #
    #    initial_state_mean = [measurements[0, 0],
    #                          0,
    #                          measurements[0, 1],
    #                          0]
    #
    #    transition_matrix = [[1, 1, 0, 0],
    #                         [0, 1, 0, 0],
    #                         [0, 0, 1, 1],
    #                         [0, 0, 0, 1]]
    #
    #    observation_matrix = [[1, 0, 0, 0],
    #                          [0, 0, 1, 0]]
    #
    #    kf1 = KalmanFilter(transition_matrices=transition_matrix,
    #                       observation_matrices=observation_matrix,
    #                       initial_state_mean=initial_state_mean)
    #    print('Calculating Kalman 1 of 2')
    #    kf1 = kf1.em(measurements, n_iter=1)
    #
    #    kf2 = KalmanFilter(transition_matrices=transition_matrix,
    #                       observation_matrices=observation_matrix,
    #                       initial_state_mean=initial_state_mean,
    #                       observation_covariance=1 * kf1.observation_covariance,
    #                       em_vars=['transition_covariance', 'initial_state_covariance'])
    #    print('Calculating Kalman 2 of 2')
    #    kf2 = kf2.em(measurements, n_iter=1)
    #    (smoothed_state_means, smoothed_state_covariances) = kf2.smooth(measurements)
    #
    #    df_etr_proc['Easting_Kal'] = smoothed_state_means[:, 0]
    #    df_etr_proc['Northing_Kal'] = smoothed_state_means[:, 2]


    export_etr2 = projnr + ' ISAS B02 TID' + str(tid) + ' PROC KP' + "{:.3f}".format(
        df_etr_proc[KP].min()) + '-' + "{:.3f}".format(df_etr_proc[KP].max()) + ' ' + capjettype1 + capjettype2 + '.etr'

    df_etr_proc = df_etr_proc.sort_values(by='DateTime')
    # df_etr[['EASTING', 'NORTHING']] = df_etr[['EASTING', 'NORTHING']].astype(str)
    # df_etr.round({'EASTING': 3, 'NORTHING': 3})
    try:
        if not os.path.exists(Export_dir):
            os.mkdir(Export_dir)
        df_etr_proc[['Date', 'Time', 'Easting', 'Northing', 'WaterDepth', 'Roll', 'Pitch', 'Heading', 'Tide']].to_csv(Export_dir + export_etr2, sep=' ', index=False)
        # df_etr[['#DAY-MONTH-YEAR', 'HOUR:MIN:SEC.AAA', 'EASTING', 'NORTHING', 'DEPTH', 'ROLL', 'PITCH', 'HEADING', 'TIDE']].to_csv(export_etr1, sep='\t', index=False)
        print("Successfully exported PROCESSED E-TRACK to: " + str(export_etr2))
    except IOError as e:
        err2 = "Close the: " + export_etr2 + " file and try again to get the Capjet Track ETR!"
        messagebox.showwarning("Try Again...", str(e))
        print(err2)

    except:
        print("failed to export PROC ETR")
        print("Unexpected error:", sys.exc_info()[0])
    pass


    if (df_filtered.size == 0):
        err3 = "You have filtered all data \n\n No Data Left!"
        messagebox.showwarning("Try Again...", err3)
        print("No Data left")
        return

    # Reindex to KP values for interpolation?
    df_filtered = df_filtered.set_index(np.round((df_filtered[KP]*1000), decimals=3))
    new_index = np.arange(int(df_filtered[KP].min()*1000), int(df_filtered[KP].max()*1000)+1, 1)
    df_filtered = df_filtered.reindex(index=new_index)


    df_filtered[KP] = df_filtered[KP].interpolate()

    if np.isnan(df_filtered[KP].iloc[0]):
        df_filtered = df_filtered.iloc[1:]
        print("Removed first KP line, no biggy")

    if (interpol == True):
        df_filtered = df_filtered.interpolate()
        print("Data is interpolated")
    else:
        print("Data is NOT interpolated")
    # Export to CSV
    df_filtered['TrenchingPassID'] = t_pass_nr
    df_filtered['RunlineID'] = runlineid
    df_filtered['TrenchingID'] = tid
    df_filtered['Sword_Depth'] = (df_filtered['STBD_Sword_Depth'] + df_filtered[ 'Port_Sword_Depth']) / 2
    df_filtered = df_filtered.round({E: 2, N: 2, KP: 3, DCC: 2, 'STBD_Sword_Depth': 2, 'Port_Sword_Depth': 2, 'Sword_Depth': 2, 'SAL': 3, 'Speed_Along_Line': 2, SOG: 2, 'Speed_Over_Ground': 2, 'deltaT': 3, 'Roll': 2, 'Pitch': 2, 'Capjet_Power': 2})
    #print(df_filtered['RunlineID'])
   # print(len(df_filtered['RunlineID']))
    #df_filtered['Time'] = df_filtered['Time'].replace(np.nan, ' ', regex=True)
    export_table = pd.concat([df_filtered['TrenchingPassID'], df_filtered['RunlineID'], df_filtered['Time'], df_filtered['TrenchingID'], df_filtered[E], df_filtered[N], df_filtered[KP], df_filtered[DCC],  df_filtered['STBD_Sword_Depth'], df_filtered['Port_Sword_Depth'], df_filtered['Sword_Depth'], df_filtered['Speed_Along_Line'], df_filtered['Speed_Over_Ground'], df_filtered['Roll'], df_filtered['Pitch'], df_filtered['Gyro'], df_filtered['Capjet_Power'], df_filtered[Capjet_col]], axis=1)
    export_csv1 = projnr + ' ISAS B02 TID' + str(tid) + ' KP' + "{:.3f}".format(df_filtered[KP].min()) + '-' + "{:.3f}".format(df_filtered[KP].max()) + ' ' + capjettype1 + capjettype2 + '.csv'
    try:
        if not os.path.exists(Export_dir):
            os.mkdir(Export_dir)
        export_table.to_csv(Export_dir + export_csv1, sep=',', index=True)
    except IOError as e:
        err2 = "Close the: " + export_csv1 + " file and try again to get the CSV export!"
        messagebox.showwarning("Try Again...", str(e))
        print(err2)

    # Plot Results
    plot_results(df_filtered, CJX, df_etr, df_etr_proc, tid)
    print("--- %.3f seconds ---" % (time.time() - start_time))
    savetodb = messagebox.askyesnocancel("Save to SQLite Table: trenching", "Do you want to upload current result to database: " + str(sqlitepath) + "?\n\n NB! Please QC your data before uploading it to DB")
    if savetodb:
        try:
            UpdateDB.initializeDB(os.path.realpath(sqlitepath))
            #print('Init OK')
            col_orig = export_table.columns
            UpdateDB.write_result(os.path.realpath(sqlitepath), export_table, tid)
            export_table.columns = col_orig
        except:
            print("Failed to write result to database....", sys.exc_info()[0])
            messagebox.showerror("Error writing 'trenching' to DB",
                                 "The trenching data could not be written to SQLite DB: " + str(sqlitepath) +
                                 " Error message is: \n" + str(sys.exc_info()[0]) + "\n\n Continue Executing script")
            pass
    if savetodb is None:
        print("Aborting script...")
        return
    if CheckVar2.get():
        print("Start Capjet RAWString2DB")
        start_time = time.time()
        # CapjetRAWString2DB
        raw_string_path = os.path.realpath(Config["Capjet RAW String"]['Raw_string_path'])
        raw_string_header = Config["Capjet RAW String"]['Raw_string_header']
        raw_string_sep = Config["Capjet RAW String"]['Raw_string_sep']
        raw_string_suffix = Config["Capjet RAW String"]['Raw_string_suffix']
        raw_string_dateformat = Config["Capjet RAW String"]['RAW_string_dateformat']
        dtime = int(Config["Capjet RAW String"]['Lookup_time_delta'])
        raw_string_header = [str(i) for i in raw_string_header.split(',')]
        #print("CJ RAW String header: " + str(raw_string_header))
        #print(raw_string_header)

        # Go Through CJ RAW string and define type, first needs to be Time and value string
        for idx, val in enumerate(raw_string_header):
            if idx == 0:
                dtypes = {raw_string_header[0]: str} # Time stamp of raw signal
            else:
                dtypes[raw_string_header[idx]] = np.float64

        if os.path.isfile(raw_string_path):
            print("Start reading in one file" + str(raw_string_path))
            try:
                df_temp = pd.read_csv(raw_string_path, skiprows=1, nrows=2)
                if len(df_temp.columns) != len(raw_string_header):
                    messagebox.showwarning("Wrong length CJ Raw String",
                                           "Not equal length for file: " + str(raw_string_path) + "\n\nHeader length: " + str(
                                               len(raw_string_header)) + "\nFile length: " + str(
                                               len(df_temp.columns)) + "\nSkipping this file")
                    df3 = pd.DataFrame()
                else:
                    df3 = pd.read_csv(raw_string_path, sep=str(raw_string_sep), index_col=None, names=raw_string_header,
                                      dtype=dtypes, parse_dates=[0], skiprows=1, dayfirst=True,
                                      error_bad_lines=False)
                    try:
                        # print(df3['Time'])
                        df3['Time'] = pd.to_datetime(df3['Time'])
                        print("Successfully read in")
                        print("Start filtering on time")
                    except ValueError as e:
                        print('ERROR: ' + str(
                            e) + ' Change the DateFormat in the ini file under [Capjet RAW String] Not implemented')
                        messagebox.showwarning("Time Column CJ Raw string",
                                               "File: " + str(raw_string_path) + " is not read in. Due to: " + str(
                                                   e) + "\nYou need to fix this manually for now....")
                        return

            except TypeError as e:
                print("Failed:")
                try:
                    df_temp2 = pd.read_csv(raw_string_path, nrows=1)
                    print("Number of columns in file: " + str(len(df_temp2.columns)) + ". Expected: " + str(
                        len(raw_string_header)))
                    print("Skipped file. NO CJ Raw string read in")
                except TypeError as e:
                    print("Skipped file. NO CJ Raw string read in")
                    pass
            if df3.empty:
                messagebox.showwarning("No CJ Raw String", "No valid Capjet Raw String data was found")
                return
        else: # Path Selected, read in multiple files
            allFiles = glob.glob(raw_string_path + "/*." + str(raw_string_suffix))
            df3 = pd.DataFrame()
            list_ = []
            for file_ in allFiles:
                try:
                    print("Start read in File: " + str(file_))
                    df_temp = pd.read_csv(file_, skiprows=1, nrows=2)
                    if len(df_temp.columns) != len(raw_string_header):
                        print("Header length: " + str(
                                                   len(raw_string_header)) + "\nFile length: " + str(
                                                   len(df_temp.columns)) + "\nSkipping this file")
                        messagebox.showwarning("Wrong length CJ Raw String",
                                               "Not equal length for file: " + str(file_) + "\n\nHeader length: " + str(
                                                   len(raw_string_header)) + "\nFile length: " + str(
                                                   len(df_temp.columns)) + "\nSkipping this file")
                    else:
                        df_temp = pd.read_csv(file_, sep=str(raw_string_sep), index_col=None, names=raw_string_header,
                                              dtype=dtypes, parse_dates=[0], skiprows=1, dayfirst=True,
                                              error_bad_lines=False)
                        try:
                            # print(df3['Time'])
                            df_temp['time'] = pd.to_datetime(df_temp['time'])
                            list_.append(df_temp)
                            print("Successfully read in")
                        except ValueError as e:
                            print('ERROR: ' + str(
                                e) + ' Change the DateFormat in the ini file under [Capjet RAW String] Not implemented')
                            messagebox.showwarning("Time Column CJ Raw string",
                                                   "File: " + str(file_) + " is not read in. Due to: " + str(e) + "\nYou need to fix this manually for now....")
                            pass

                except TypeError as e:
                    print("Failed:" + str(e))
                    try:
                        df_temp2 = pd.read_csv(file_, nrows=1)
                        print("Number of columns in file: " + str(len(df_temp2.columns)) + ". Expected: " + str(len(raw_string_header)))
                        print("Skipped file. Continue reading in files")
                    except TypeError as e:
                        print("Skipped file. Continue reading in files")
                        pass
                except ValueError as e:
                    print("Failed:" + str(e))
                    messagebox.showwarning("Failed to read in CJ Raw String", "Could not read in file: " + str(file_) + "\n\nError: " + str(e) + "\n\nContinuing reading in files....")
                    pass
                # except:
                #     print("Failed to read CSV", sys.exc_info()[0])
            if not list_:
                e = "No Realterm RAW files found, is the folder correct? Folder: " + str(raw_string_path)
                print(e)
                messagebox.showwarning("Try Again...", str(e))
                return
            df3 = pd.concat(list_)
            if df3.empty:
                messagebox.showwarning("No CJ Raw String", "No valid Capjet Raw String data was found")
                return
            print("CJ RAW String is concated, start filtering on time")

        # Continue with the read in string


        # export_csv_cjraw = './OutputData/' + projnr + ' ISAS B02 CapjetRAWString TID' + str(tid) + ' ' + str(min(df3['Time'])).replace(':', '').replace('-', '') + '-' + str(max(df3['Time'])).replace(':', '').replace('-', '') + ' ' + capjettype1 + capjettype2 + '.csv'
        # try:
        #     df3.to_csv(export_csv_cjraw, sep=',', index=False)
        # except IOError as e:
        #     err2 = "Close the: " + export_csv_cjraw + " file and try again to get the CSV export!"
        #     messagebox.showwarning("Try Again...", str(e))
        #     print(err2)

        # datetime_start = datetime.strptime(datetime_start, raw_string_dateformat)
        # datetime_end = datetime.strptime(datetime_end, raw_string_dateformat)
        df3 = df3[(df3.ix[:, 0] >= datetime_start) & (df3.ix[:, 0] <= datetime_end)]
        df3 = df3.sort_values(by='time')
        export_csv_cjraw = Export_dir + projnr + ' ISAS B02 CapjetString-RAW TID' + str(
            tid) + ' KP' + "{:.3f}".format(df_filtered[KP].min()) + '-' + "{:.3f}".format(
            df_filtered[KP].max()) + ' ' + capjettype1 + capjettype2 + '.txt'
        try:
            df3.to_csv(export_csv_cjraw, sep=',', index=False)
        except IOError as e:
            err2 = "Close the: " + export_csv_cjraw + " file and try again to get the Capjet RAW String export"
            messagebox.showwarning("Try Again...", str(e))
            print(err2)
            pass

        # export_table['Time'] = export_table['Time'].interpolate()
        df_pos = pd.concat([export_table['TrenchingID'], export_table['Time'], export_table[KP], export_table[E], export_table[N]], axis=1)
        df_pos = df_pos.sort_values(by='Time')
        df_pos = df_pos.dropna(subset=['Time'])

        merged = pd.merge_asof(left=df_pos, right=df3, left_on='Time', right_on='time', direction='nearest', tolerance=pd.Timedelta(seconds=dtime))
        merged = merged.sort_values(by=KP)

        # Interpolate for every meter
        merged = merged.set_index(np.round((merged[KP] * 1000), decimals=3))
        new_index = np.arange(int(merged[KP].min() * 1000), int(merged[KP].max() * 1000) + 1, 1)
        merged = merged.reindex(index=new_index)
        merged[KP] = merged[KP].interpolate()
        if (interpol == True):
            merged = merged.interpolate()
            print("Capjet String is interpolated")
        else:
            print("Capjet String is NOT interpolated")

        # Export CSV file of the data
        export_csv_cjrawstringmerged = Export_dir + projnr + ' ISAS B02 CapjetString-KP TID' + \
                                       str(tid) + ' KP' + "{:.3f}".format(merged[KP].min()) + '-' + \
                                       "{:.3f}".format(merged[KP].max()) + ' ' + capjettype1 + capjettype2 + '.csv'
        try:
            merged.to_csv(export_csv_cjrawstringmerged, sep=',', index=False)
        except IOError as e:
            err2 = "Close the: " + export_csv_cjrawstringmerged + " file and try again to get the Capjet RAW String export"
            messagebox.showwarning("Try Again...", str(e))
            print(err2)
            pass
        # Plot All CJ RAW String DATA
        num_nrows = 6
        num_ncols = math.ceil(len(raw_string_header) /num_nrows)

        if CJX == 'CJB':
            fig, axes = plt.subplots(nrows=num_nrows, ncols=num_ncols, sharex=True)
            titles = raw_string_header[1:]
            y_vals = []
            for id, val in enumerate(titles):
                y_vals.append(merged[str(val)])
            # axes.flat returns the set of axes as a flat (1D) array instead
            # of the two-dimensional version we used earlier
            for ax, title, y in zip(axes.flat, titles, y_vals):
                ax.plot(merged['KP'], y, 'b')
                ax.set_title(title)
                ax.grid(True)
            plt.suptitle('CapjetB RAW String for TID' + str(tid) + " KP" + str(merged[KP].min()) + "-" + str(merged[KP].max()), fontsize=16)
            plt.show(block=False)
            plt.savefig(Export_dir + projnr + ' ISAS B02 Plot TID' + \
                        str(tid) + ' KP' + "{:.3f}".format(merged[KP].min()) + '-' + \
                        "{:.3f}".format(merged[KP].max()) + ' ' + capjettype1 + capjettype2 + '.png', dpi=300)
            print("--- CJ_Raw_String2DB:  %.3f seconds ---" % (time.time() - start_time))
            # savetodb2 = messagebox.askyesno("Save to SQLite Table: cjb_raw_string",
            #                                 "Do you want to upload Capjet RAW String Data to database: " + str(
            #                                     sqlitepath) + "?\n\n NB! Please QC your data before uploading it to DB")
            # if savetodb2:
            #     try:
            #         merged = merged.rename(columns={E: 'Easting', N: 'Northing', KP: 'KP'})
            #         UpdateDB.initializeDB(os.path.realpath(sqlitepath))
            #         UpdateDB.initCJBRawString(os.path.realpath(sqlitepath), raw_string_header)
            #         print('SQL DB CJB RAW String table Init OK')
            #         UpdateDB.write_result_CJB_RAW(os.path.realpath(sqlitepath), merged, tid)
            #     except:
            #         print("Failed to write result to database....", sys.exc_info()[0])
            #         pass

        elif CJX == 'CJA':
            fig, axes = plt.subplots(nrows=num_nrows, ncols=num_ncols, sharex=True)
            titles = raw_string_header[1:]
            y_vals = []
            for id, val in enumerate(titles):
                y_vals.append(merged[str(val)])
            # axes.flat returns the set of axes as a flat (1D) array instead
            # of the two-dimensional version we used earlier
            for ax, title, y in zip(axes.flat, titles, y_vals):
                ax.plot(merged['KP'], y, 'r')
                ax.set_title(title)
                ax.grid(True)
            plt.suptitle('CapjetA RAW String for TID' + str(tid) + " KP" + str(merged[KP].min()) + "-" + str(merged[KP].max()), fontsize=16)
            fig.text(0.5, 0.04, 'KP', ha='center')
            plt.show(block=False)
            plt.savefig(Export_dir + projnr + ' ISAS B02 Plot TID' + \
                                       str(tid) + ' KP' + "{:.3f}".format(merged[KP].min()) + '-' + \
                                       "{:.3f}".format(merged[KP].max()) + ' ' + capjettype1 + capjettype2 + '.png', dpi=300)
            print("--- CJ_Raw_String2DB:  %.3f seconds ---" % (time.time() - start_time))
            # savetodb2 = messagebox.askyesno("Save to SQLite Table: cja_raw_string", "Do you want to upload CapjetA RAW String Data to database: " + str(
            #     sqlitepath) + "?\n\n NB! Please QC your data before uploading it to DB")
            # if savetodb2:
            #    # try:
            #     merged = merged.rename(columns={E: 'Easting', N: 'Northing', KP: 'KP'})
            #     UpdateDB.initializeDB(os.path.realpath(sqlitepath))
            #     UpdateDB.initCJARawString(os.path.realpath(sqlitepath), raw_string_header)
            #     print('SQL DB CJA RAW String table Init OK')
            #     UpdateDB.write_result_CJA_RAW(os.path.realpath(sqlitepath), merged, tid)
            #     #except:
            #      #   print("Failed to write result to database, Table: cja_raw_string....", sys.exc_info()[0])
            #       #  pass

        savetodb2 = messagebox.askyesno("Save to SQLite Table: capjet_raw_string",
                                        "Do you want to upload Capjet RAW String Data to database: " + str(
                                            sqlitepath) + "?\n\n NB! Please QC your data before uploading it to DB")
        if savetodb2:
            # try:
            merged = merged.rename(columns={'TrenchingID': 'trenching_id', 'Time': 'time', KP: 'kp', E: 'easting', N: 'northing'})
            # Check that masterfile (sqlite database exist, create if not)
            UpdateDB.initializeDB(os.path.realpath(sqlitepath))
            # Check that masterfile includes capjet_raw_string table, create if not
            UpdateDB.init_capjet_raw_string(os.path.realpath(sqlitepath), raw_string_header)
            print('SQL DB CAPJET RAW String table Init OK')
            # Write cj raw string result to database
            UpdateDB.write_result_capjet_raw_string(os.path.realpath(sqlitepath), merged, tid, CJX)
            # except:
            #   print("Failed to write result to database, Table: cja_raw_string....", sys.exc_info()[0])
            #  pass

        print("Finished CJ RAWString2DB")






    print("--== End of Script ==--")
    # sys.stdout = save_stdout
    # log_file.close()
    return

# Start of GUI

root = Tk()

root.title("Capjet Sword and Speed Script")

# kpstart_value = StringVar(value=0.000)
# kpstart_value.trace('w', limitKpStartField)
# kpend_value = StringVar(value=500.000)
# kpend_value.trace('w', limitKpEndField)
#
# timestartgui_value = StringVar(value='2004-01-01 00:00:01')
# timestartgui_value.trace('w', limitTimeStartField)
# timeendgui_value = StringVar(value='2034-12-30 23:59:59')
# timeendgui_value.trace('w', limitTimeEndField)

kpstart_value = StringVar(value=295.622)
kpstart_value.trace('w', limitKpStartField)
kpend_value = StringVar(value=307.806)
kpend_value.trace('w', limitKpEndField)

timestartgui_value = StringVar(value='2019-06-14 14:15:46')
timestartgui_value.trace('w', limitTimeStartField)
timeendgui_value = StringVar(value='2019-06-16 11:50:44')
timeendgui_value.trace('w', limitTimeEndField)



frame = Frame()
frame.pack()

frame_setup_select = Frame()
frame_setup_select.pack()
frame_tid = Frame()
frame_tid.pack()
frame_pass = Frame()
frame_pass.pack()
frame_start_kp = Frame()
frame_start_kp.pack()
frame_end_kp = Frame()
frame_end_kp.pack()
frame_start_time = Frame()
frame_start_time.pack()
frame_end_time = Frame()
frame_end_time.pack()
frame2 = Frame()
frame2.pack()
button_run_1 = Button(frame2, text="Run Capjet A", command=lambda: run_script('CJA', tid, t_pass_nr, time_start_gui, time_end_gui, kpstart, kpend, CheckVar1, CheckVar2), height=5, width=20)
button_run_2 = Button(frame2, text="Run Capjet B", command=lambda: run_script('CJB', tid, t_pass_nr, time_start_gui, time_end_gui, kpstart, kpend, CheckVar1, CheckVar2), height=5, width=20)
button_run_close = Button(frame2, text="Close All Plots", command=lambda: plt.close('all'), height=2, width=15)
label1 = Label(frame, text="Small script to filter the Capjet sword and speed. \nWritten so all VisualSoft or Option files and the entire project can be calculated in one go.\n\nThe Start and End time format can be defined in the Filter Settings INI file.\nDefault is  [Default: yyyy-mm-dd hh:mm:ss].")
# ---------- START OF DROP DOWN MENU
# Create a Tkinter variable

try:
    Config_Main_Setup = configparser.ConfigParser()
    Config_Main_Setup.read("Config_Main_Setup.ini")
except (NameError, KeyError) as e:
    messagebox.showwarning("Error...", "Can not locate Config_Main_Setup.ini in main program folder. Please check if file exists\n\n" + str(e))
    pass

setup_name_list = list(Config_Main_Setup.items('DISPLAY NAME'))
setup_path_list = list(Config_Main_Setup.items('FILE PATH'))
setup_batch_path_list = list(Config_Main_Setup.items('BATCH SCRIPT'))

#SETUP = []
SETUP_NAME = []
SETUP_PATH = []
SETUP_BATCH_PATH = []

for x in setup_name_list:
    #SETUP.append(x[0])
    SETUP_NAME.append(x[1])
for x in setup_path_list:
    SETUP_PATH.append(x[1])
for x in setup_batch_path_list:
    SETUP_BATCH_PATH.append(x[1])

label_setup = Label(frame_setup_select, text="Select Setup file:")
setup_file_variable = StringVar(root)
setup_file_variable.set(SETUP_NAME[0]) # default value

setup_selector = OptionMenu(frame_setup_select, setup_file_variable, *SETUP_NAME)
setup_selector.pack()
# ---------- END OF DROP DOWN MENU

label2 = Label(frame_tid, text="TID Nr:        ")
# label3 = Label(root, text="OR,\n\n Use Inputfile: ")
label4 = Label(frame_pass, text="Pass Nr:      ")
label_time_start = Label(frame_start_time, text="Start Time:")
label_time_end = Label(frame_end_time, text="End Time: ")
# tid = Text(root, height=1, width=7, )
kpstartlabel = Label(frame_start_kp, text="Lowest KP: ")
kpendlabel = Label(frame_end_kp, text="Highest KP:")

kpstart = Entry(frame_start_kp, width=10, textvariable=kpstart_value)
kpend = Entry(frame_end_kp, width=10, textvariable=kpend_value)
tid = Text(frame_tid, height=1, width=10)
t_pass_nr = Text(frame_pass, height=1, width=10)
time_start_gui = Entry(frame_start_time, width=21, textvariable=timestartgui_value)
time_end_gui = Entry(frame_end_time, width=21, textvariable=timeendgui_value)
# inputPath = Text(root, height=1, width=90, )



# End test

# Read in Config file to get Capjet RAW string to visually show it in GUI
# try:
#     ConfigA = configparser.ConfigParser()
#     ConfigA.read("Config_Sword_Speed_CapjetA.ini")
#     ConfigB = configparser.ConfigParser()
#     ConfigB.read("Config_Sword_Speed_CapjetB.ini")
#     CJA_raw_string_path = ConfigA["Capjet RAW String"]['Raw_string_path']
#     CJB_raw_string_path = ConfigB["Capjet RAW String"]['Raw_string_path']
#     label_CJRAW_string = "CJA RAW Realterm: \n" + str(CJA_raw_string_path) + "\nCJB RAW Realterm Input: \n" + str(
#         CJB_raw_string_path)
# except (NameError, KeyError) as e:
#     messagebox.showwarning("Error...", "Update INI files. Missing: " + str(e) + " I.e: CJX_raw_string_path=C:\\bla\\bla\\bla")
#     CJA_raw_string_path = "C:\\temp"
#     CJB_raw_string_path = "C:\\temp"
#     label_CJRAW_string = "CJA RAW Realterm: " + str(CJA_raw_string_path) + "\nCJB: " + str(
#         CJB_raw_string_path)
#     pass
# except:
#     print("Unexpected error Loading INI files:" + str(sys.exc_info()[0]))

CheckVar1 = IntVar()
CheckVar1.set(1)
CheckVar2 = IntVar()
CheckVar2.set(1)
C1 = Checkbutton(frame2, text="Run Batch Script?", variable=CheckVar1, onvalue=True, offvalue=False, height=1, width=20)

C2 = Checkbutton(frame2, text="Run Capjet RAW String2DB?", variable=CheckVar2, onvalue=True, offvalue=False, height=1, width=20)
# label_CJ_raw = Label(frame2, text=label_CJRAW_string)


label1.pack()
# #Start test
# dayValue = StringVar(value=0.000)
# dayValue.trace('w', limitTextField)
#
# day_entry1=Entry(frame2, bg="#282B2B", fg="white", width=10, textvariable=dayValue)
# day_entry1.pack()


#KP Start and END
kpstartlabel.pack(side=LEFT,pady=2, padx=5)
kpstart.pack(side=LEFT, pady=2, padx=5)
kpendlabel.pack(side=LEFT, pady=2, padx=5)
kpend.pack(side=LEFT, pady=2, padx=5)

# kpstart.insert(END, kpstart_value.get())
# kpend.insert(END, 500.000)

# Script pack
label_setup.pack(side=LEFT, padx=5)
setup_selector.pack(side=RIGHT, padx=5)
# TID and pass number labels
label2.pack(side=LEFT, padx=5)
tid.insert(END, 0)

tid.pack(side=LEFT, padx=5)
tidup = Button(frame_tid, text="^", command=add1)
tidup.pack(side=LEFT,)
tiddown = Button(frame_tid, text="v", command=subtract1)
tiddown.pack(side=LEFT,)

label4.pack(side=LEFT, pady=2, padx=5)
t_pass_nr.pack(side=LEFT, pady=2, padx=5)
t_pass_nr.insert(END, 0)
tid.pack(side=LEFT, padx=5)
tpass_up = Button(frame_pass, text="^", command=addpass1)
tpass_up.pack(side=LEFT)
tpass_down = Button(frame_pass, text="v", command=subtractpass1)
tpass_down.pack(side=LEFT)

# Time labels
label_time_start.pack(side=LEFT, padx=5)
time_start_gui.pack(side=LEFT, padx=5)
# time_start_gui.insert(END, '2004-01-01 00:00:01')
label_time_end.pack(side=LEFT, padx=5)
time_end_gui.pack(side=LEFT, padx=5)
# time_end_gui.insert(END, '2024-12-30 23:59:59')

# inputPath.insert(END, "C:\\Users\\dags\\Documents\\iSURVEY\\Python_Scripts\\Capjet_Sword_Speed_v0.99\\InputData")
C1.pack()
C2.pack()
#label_CJ_raw.pack()
# label3.pack()
# inputPath.pack()

button_run_1.pack(pady=5, padx=5)
button_run_2.pack(pady=5, padx=5)
button_run_close.pack(pady=5, padx=5)


menubar = Menu(root)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
#filemenu.add_command(label="Open", command=hello)
#filemenu.add_command(label="Save", command=hello)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)

editmenu.add_command(label="Open Main Setup", command=main_setup_settings)
editmenu.add_separator()
editmenu.add_command(label="Open Selected Filter Settings", command=current_settings)
#editmenu.add_command(label="Open Capjet A Settings", command=capjetA_settings)
#editmenu.add_command(label="Open Capjet B Settings", command=capjetB_settings)
# editmenu.add_separator()
editmenu.add_command(label="Open Selected Batch Script for copying RAW files", command=current_batch_script_settings)
#editmenu.add_command(label="Batch Script for VideoLogger A", command=videologgerA_settings)
#editmenu.add_command(label="Batch Script for VideoLogger B", command=videologgerB_settings)


#editmenu.add_command(label="Copy", command=hello)
#editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Setup", menu=editmenu)

# create Troubleshoot menubar
# troubleshootmenu = Menu(menubar, tearoff=0)
# menubar.add_cascade(label="Troubleshoot", menu=troubleshootmenu)
# troubleshootmenu.add_command(label="Open message log", command=open_messagelog)
# troubleshootmenu.add_separator()
# troubleshootmenu.add_command(label="E-mail Support", command=email_support)


helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Instructions", command=menu_instructions)
helpmenu.add_command(label="About", command=menu_about)
helpmenu.add_command(label="Version History", command=menu_versions)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar)

root.mainloop()
