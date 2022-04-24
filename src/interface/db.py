import sqlite3
from typing import List, Dict, Union


def new_db() -> sqlite3.Connection:
    conn = sqlite3.connect('room-log.db')

    __create_log_table(conn)
    __create_state_table(conn)
    __create_idm_table(conn)
    return conn


def __create_log_table(conn: sqlite3.Connection):
    query = ('CREATE TABLE IF NOT EXISTS room_log ('
             'id INTEGER PRIMARY KEY,'
             'name TEXT NOT NULL,'
             'state TEXT NOT NULL,'
             'option TEXT NULL,'
             'created_at DATETIME DEFAULT (datetime(\'now\', \'localtime\'))'
             ');')

    conn.execute(query)
    conn.commit()


def insert_log_table(conn: sqlite3.Connection, name: str, state: str, option: str):
    query = ('INSERT INTO room_log (name, state, option)'
             'VALUES (?, ?, ?);')

    conn.execute(query, [name, state, option])
    conn.commit()


def select_log_table(conn: sqlite3.Connection) -> List[Dict[str, str]]:
    query = ('SELECT name, state, option, created_at FROM room_log ORDER BY id desc LIMIT 30;')
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    logs = [{'name': r[0], 'state': r[1], 'option': r[2], 'time': r[3]} for r in rows]
    cur.close()
    return logs


def __create_state_table(conn: sqlite3.Connection):
    query = ('CREATE TABLE IF NOT EXISTS room_state ('
             'id INTEGER PRIMARY KEY,'
             'name TEXT NOT NULL UNIQUE,'
             'state TEXT NOT NULL,'
             'option TEXT NULL,'
             'updated_at DATETIME DEFAULT (datetime(\'now\', \'localtime\'))'
             ');')

    conn.execute(query)

    trigger_query_insert = ('CREATE TRIGGER IF NOT EXISTS auto_reset_state '
                            'BEFORE INSERT ON room_state '
                            'WHEN datetime(date(\'now\', \'localtime\') || \' 00:00:00\') '
                            '> (SELECT updated_at FROM room_state LIMIT 1) '
                            'BEGIN DELETE FROM room_state; '
                            'END')

    # trigger_query_update = ('CREATE TRIGGER IF NOT EXISTS auto_reset_state_update '
    #                         'INSTEAD OF UPDATE OF state ON room_state '
    #                         'WHEN datetime(date(\'now\', \'localtime\') || \' 00:00:00\') '
    #                         '> (SELECT updated_at FROM room_state LIMIT 1) '
    #                         'BEGIN DELETE FROM room_state; '
    #                         'END')

    conn.execute(trigger_query_insert)
    # conn.execute(trigger_query_update)
    conn.commit()


def insert_state_table(conn: sqlite3.Connection, name: str, state: str, option: str):
    query = ('INSERT OR REPLACE INTO room_state (name, state, option, updated_at)'
             'VALUES (?, ?, ?, (datetime(\'now\', \'localtime\')));')

    conn.execute(query, [name, state, option])
    conn.commit()


def select_state_table(conn: sqlite3.Connection) -> List[Dict[str, str]]:
    query = ('SELECT name, state, option FROM room_state;')

    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    state_list = [{'name': r[0], 'state': r[1], 'option': r[2]} for r in rows]
    cur.close()
    return state_list


def select_state_table_name_is_exists(conn: sqlite3.Connection, name: str) -> bool:
    query = ('SELECT id FROM room_state WHERE name = ?')

    cur = conn.cursor()
    cur.execute(query, [name])
    rows = cur.fetchall()
    cur.close()
    return len(rows) > 0


def update_state_table(conn: sqlite3.Connection, name: str, state: str):
    query = ('UPDATE room_state SET state = ?, updated_at = datetime(\'now\', \'localtime\')'
             'WHERE name = ?;')

    conn.execute(query, [state, name])
    conn.commit()


def delete_state_table(conn: sqlite3.Connection, name: str):
    query = 'DELETE FROM room_state WHERE name = ?;'
    conn.execute(query, [name])
    conn.commit()


def truncate_state_table(conn: sqlite3.Connection):
    query = ('DELETE FROM room_state;')
    conn.execute(query)
    conn.commit()


def __create_idm_table(conn: sqlite3.Connection):
    query = ('CREATE TABLE IF NOT EXISTS idm ('
             'id INTEGER PRIMARY KEY,'
             'idm TEXT NOT NULL,'
             'name TEXT'
             ');')

    conn.execute(query)
    conn.commit()


def insert_idm_table(conn: sqlite3.Connection, idm: str, name: str):
    query = ('INSERT INTO idm (idm, name)'
             'VALUES (?, ?);')

    conn.execute(query, [idm, name])
    conn.commit()


def select_idm_table(conn: sqlite3.Connection) -> List[Dict[str, str]]:
    query = ('SELECT idm, name FROM idm;')

    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()

    idm_list = [{'idm': r[0], 'name': r[1]} for r in rows]
    return idm_list


def select_idm_table_idm(conn: sqlite3.Connection, idm: str) -> Union[Dict[str, str], Dict[None, None]]:
    query = ('SELECT idm, name FROM idm WHERE idm = ?;')

    cur = conn.cursor()
    cur.execute(query, [idm])
    row = cur.fetchone()

    cur.close()
    if not row:
        return {}

    return {'idm': row[0], 'name': row[1]}


def update_idm_table_idm(conn: sqlite3.Connection, idm: str, name: str):
    query = ('UPDATE idm SET name = ? WHERE idm = ?;')

    conn.execute(query, [name, idm])
    conn.commit()
