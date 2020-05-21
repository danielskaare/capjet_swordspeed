import xlwings as xw
import pandas as pd
import configparser
import os.path
from tkinter import messagebox

#  df = pd.DataFrame([[9, 5], [3, 4]], columns=['c1', 'c2'], index=['r1', 'r2'])

book_path = 'c:\\temp\\xlwings\\XXXXX_Project_Name_Proc_Log.xlsx'
book_name = os.path.basename(book_path)
sheet_name = 'CJ_Proc_Log'

def format_sheet():
    sheet.range('A1:H3').color = (255, 200, 255)  # Purple
    sheet.range('A1:B3').api.Font.Bold = True
    sheet.range('A1:B3').api.HorizontalAlignment = 2
    sheet.range('A1:B3').rows.autofit()
    adr = sheet.range('A4').expand('right').address
    sheet.range(str(adr)).api.Font.Bold = True
    sheet.range(adr).color = (200, 200, 200)  # Grey
    sheet.range(adr).columns.autofit()

def proc_log_init():
    print("Init Proc Log")

    # Read in Config file
    Config = configparser.ConfigParser()
    # Get settings file from selected INI file in GUI
    setup_file = "C:\\Users\\dags\\Desktop\\Capjet Sword Speed Stuff\\24 CAPJET DATA\\24 CAPJET DATA\\Setup Files\\13771 MAME CONF CapjetA.ini"
    if not Config.read(setup_file):
        err0 = str(setup_file) + " file not found in current directory"
        print(err0)
        messagebox.showwarning("Try Again...", err0)
        return
    Config.read(setup_file)
    projnr = Config["DEFAULT"]['ProjectNr']
    runlineid = Config["DEFAULT"]['RunlineID']
    sqlitepath = Config["DEFAULT"]['SQLiteDB']
    timefilterformat = Config["DEFAULT"]['Time_filter_format_gui']
    interpol = Config.getboolean("DEFAULT", 'Interpolate_Data')
    Export_dir = Config["DEFAULT"]['Export_dir']
    Position_smooth_factor = Config.getint("Position", 'Position_smooth_factor')
    sword1lowest = Config.getfloat("Sword1", 'Sword1_lowest')
    sword1highest = Config.getfloat("Sword1", 'Sword1_highest')
    sword2lowest = Config.getfloat("Sword2", 'Sword2_lowest')
    sword2highest = Config.getfloat("Sword2", 'Sword2_highest')
    dcclowest = Config.getfloat('DCC', 'DCC_lowest')
    dcchighest = Config.getfloat('DCC', 'DCC_highest')
    speedlowest = Config.getfloat("Speed", 'Speed_lowest')
    speedhighest = Config.getfloat("Speed", 'Speed_highest')
    speedsmoothfactor = Config.getint("Speed", 'Speed_smooth_factor')
    cj_sting_loopup_delta = Config.getint("Capjet RAW String", 'Lookup_time_delta')
    sheet.range('A1').value = "Project Nr.:"
    sheet.range('A2').value = "Runline ID:"
    sheet.range('A3').value = "MasterFile Path"
    sheet.range('B1').value = str(projnr)
    sheet.range('B2').value = str(runlineid)
    sheet.range('B3').value = str(sqlitepath)
    adr = sheet.range('A1').end('down').address
    adr = adr[:3] + str(int(adr[3:]) + 1)
    print("Inser proc log line at: " + str(adr))
    tid_nr = 1
    pass_nr = 2
    kp_low = 3
    kp_high = 4
    time_start = 5
    time_end = 6
    kp_ref = 7
    capjet_button_pussed = 8
    settings_vec = [timefilterformat, interpol, Export_dir, Position_smooth_factor, sword1lowest, sword1highest,
                    sword2lowest, sword2highest, dcclowest, dcchighest, speedlowest, speedhighest, speedsmoothfactor,
                    cj_sting_loopup_delta]
    settings_vec_header = ['timefilterformat', 'interpol', 'Export_dir', 'Position_smooth_factor', 'sword1lowest',
                           'sword1highest', 'sword2lowest', 'sword2highest', 'dcclowest', 'dcchighest', 'speedlowest',
                           'speedhighest', 'speedsmoothfactor', 'cj_sting_loopup_delta']
    gui_data_vec = [tid_nr, pass_nr, kp_low, kp_high, time_start, time_end, kp_ref,
                    capjet_button_pussed]
    gui_data_vec_header = ['tid_nr', 'pass_nr', 'kp_low', 'kp_high', 'time_start', 'time_end', 'kp_ref',
                           'capjet_button_pussed']
    excel_header = gui_data_vec_header
    excel_add_new_line = gui_data_vec

    for i in range(len(settings_vec_header)):
        excel_header.append(settings_vec_header[i])

    for i in range(len(settings_vec)):
        excel_add_new_line.append(settings_vec[i])
    if int(adr[3:]) - 1 < 4:
        print("PROC LOG header doesnt exist")
        sheet.range('A4').value = [excel_header]
        sheet.range('A5').value = excel_add_new_line
    else:
        sheet.range(adr).value = excel_add_new_line
    format_sheet()


if os.path.isfile(book_path):
    wb = xw.Book(book_path)
    print(xw.apps.keys())
    all_sheets = xw.Book(book_name).sheets  # active book
    try:
        sheet = wb.sheets.add(str(sheet_name))
    except ValueError as e:
        sheet = wb.sheets[sheet_name]
else:
    print(str(book_path) + " Does not exist, creating excel document")
    wb = xw.Book()
    wb.save(book_path)
    sheet = wb.sheets.add(str(sheet_name))

proc_log_init()
check_