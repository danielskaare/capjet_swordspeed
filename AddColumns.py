import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

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

def create_new_columns_in_existing_table(conn, table_name, column_names):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    for idx, val in enumerate(column_names):
        sql_alter_table_add_column = """ALTER TABLE """ + str(table_name) + """ ADD COLUMN """ + str(val) + """ NUMERIC;"""
        print(sql_alter_table_add_column)
        try:
            c = conn.cursor()
            c.execute(sql_alter_table_add_column)
        except Error as e:
            print(e)


def main():
    database = r"D:\temp\MaMe_DBv0.97.sqlite"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS test (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        sql_column_list = "time,heading,pitch,roll,depth,altimeter,sword_front_port_total,sword_front_starboard_total,intake_p_(kw),sword_aft_port_total,sword_aft_starboard_total,wp1_amp,wp1_serialnr,wp1_hours,wp1_starts,wp1_avg_start_amp,wp1_longest_start,wp2_amp,wp2_serialnr,wp2_hours,wp2_starts,wp2_avg_start_amp,wp2_longest_start,wp3_amp,wp3_serialnr,wp3_hours,wp3_starts,wp3_avg_start_amp,wp3_longest_start,hcu1_card_current,hcu1_ambient_temperature,hcu1_ai0_itur_motor_oil_level_j2,hcu1_ai1_mill_motor_oil_level_j3,hcu1_ai2_itur_bearing_house_oil,hcu1_ai3_ai3_mill_fwd_gir_box_oil,hcu1_ai4_mill_aft_gir_box_oil_level,hcu1_ai5_not_used,hcu1_ai6_pressure_hcu,hcu1_ai7_water_ingress_hcu1,hcu2_card_current,hcu2_ambient_temperature,hcu2_ai0_tension_arm_aft_up/down,hcu2_ai1_tension_arm_aft_left,hcu2_ai2_itur_bearing_house_oil,hcu2_ai3_mill_unit_elevator_up/down,hcu2_ai4_mill_unit_tilt_up/down_j6,hcu2_ai5_oil_return_pressure,hcu2_ai6_oil_temp,hcu2_ai7_water_ingress_hcu2,tcui_card_current,tcu1_ambient_tempreature,tcu1_ai0_return_pressure,tcu1_ai1_supply_pressure,tcu1_ai2_spare_j3,tcu1_ai3_spare_j4,tcu1_ai4_motor_leak_j2,tcu1_ai5_motor_temp_j2,tcu1_ai6_oil_temp,tcu1_ai7_water_ingress_tcu1,tcu2_card_current,tcu2_ambient_temperature,tcu2_ai0_return_pressure,tcu2_ai1_supply_pressure,tcu2_ai2_spare_j3,tcu2_ai3_spare_j4,tcu2_ai4_motor_leak_j2,tcu2_ai5_motor_temp_j2,tcu2_ai6_oil_temp,tcu2_ai7_water_ingress_tcu2,sb1_ai0_front_ejector_up/down,sb1_ai1_cable_guide_front_lock,sb1_ai2_cable_guide_aft_lock,sb1_ai3_cableguide_sylinder_fwd,sb1_ai4_cableguide_sylinder_aft,sb1_ai5_mill_1_trykk_fwd,sb1_ai6_mill_2_trykk_aft,sb1_ai7_fwd_tension_cable,sb1_ai8_fwd_cable_wheel_hinged,sb1_ai9_fwd_tension_clamp,sb1_ai10_aft_tension_cable,sb1_ai11_signal_box_oilcomp,sb1_ai12_yoke_sensor,sb1_ai13_light_box_oilcomp,sb1_ai14_aft_tension_clamp,sb1_ai15_spare,sb1_ai16_mill_fwd_2_speed,sb1_ai17_mill_aft_2_speed,sb1_ai18_cardev_filter_rov_modul,sb1_ai19_front_tension_clamp_force,sb1_ai20_front_tension_wheel_drive,sb1_ai21_spare,sb1_ai22_200kw_motor_leak,sb1_ai23_signal_box_water_ingress,sb1_ai24_mill_motor_195kw_temp,sb1_ai25_itur_motor_195kw_temp,sb1_ai26_spare,sb1_ai27_spare,sb1_analog_status1,sb1_analog_status2,sb2_ai21_aft_ejector_assy_left/,sb2_ai22_aft_ejector_assy_up/,sb2_ai23_tcu1_comp,sb2_ai21_tcu2_comp,sb2_ai25_hcu_dirty_comp,sb2_ai26_afte_cable_wheel_hinged,sb2_ai27_spare_virker_ikke_på_prox,sb2_ai28_boot_comp,sb2_ai29_hpu1_motor_comp,sb2_ai30_hpu2_motor_comp,sb2_ai31_tcu1_gear_comp,sb2_ai32_tcu2_gear_comp,sb2_ai33_spare,sb2_ai34_spare,sb2_ai35_spare,sb2_ai36_mill_cardew_1,sb2_ai37_mill_cardew_2,sb2_ai38_water_pump_unit,sb2_ai39_jetting_unit,sb2_ai40_aft_tension_clamp,sb2_ai41_aft_tension_wheel_drive,sb2_di21_spare,sb2_di22_itur_motor,sb2_di23_signal_box_water_ingress,sb2_t24_200kw_aft_temp,sb2_t25_200kw_front_temp,sb2_t26_200kw_bearing_temp,sb2_t25_spare_temp,sb2_analog_status1,sb2_analog_status2,hcu3_1_card_current,hcu3_1_ambient_temperature,hcu3_1_ai0_mill_fwd_speed_j2,hcu3_1_ai1_mill_aft_speed_j3,hcu3_1_ai2_mill_fwd_oil_level_j4,hcu3_1_ai3_mill_aft_oil_lvel_j5,hcu3_1_ai4_leg1_port_fwd_up/down,hcu3_1_ai5_leg2_port_aft_up/down,hcu3_1_ai6_leg3_stb_fwd_up/down,hcu3_1_ai7_leg4_stb_aft_up/down,hcu3_2_card_current,hcu3_2_ambient_temperature,hcu3_2_ai0_wheel2_pox_j10,hcu3_2_ai1_wheel2_prox_j11,hcu3_2_ai2_not_used,hcu3_3_ai3_not_used,hcu3_2_ai4_not_used,hcu3_2_ai5_not_used,hcu3_2_ai6_not_used,hcu3_2_ai7_not_used"
        column_names = sql_column_list.split(",")
        print(column_names)
        create_new_columns_in_existing_table(conn, 'capjet_raw_string', column_names)
    else:
        print("Error! cannot create the database connection.")

main()