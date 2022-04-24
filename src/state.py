import fastapi
from typing import List, Dict, Optional
from pydantic import BaseModel

import interface.db as db

conn = db.new_db()

router = fastapi.APIRouter()

next_parson: List[str] = []


class __PostLoginBody(BaseModel):
    name: str
    temp: str


# post room login + DB
@router.post('/api/login')
async def post_login(payload: __PostLoginBody):
    """
    Login to room with temp
    :param payload: login person name and temp
    """

    db.insert_state_table(conn, payload.name, 'login', payload.temp)
    db.insert_log_table(conn, payload.name, 'login', payload.temp)
    return


class __PostLoginName(BaseModel):
    name: str


# post next person name
@router.post('/api/name')
async def post_name(payload: __PostLoginName):
    """
    Signal from card reader interface
    :param payload: next login person name
    """
    if len(next_parson) != 0 and next_parson[-1] == payload.name:
        return

    next_parson.append(payload.name)
    return


# get next person name
@router.get('/api/name')
async def get_name():
    """
    :rtype: str
    """
    if len(next_parson) == 0:
        return
        # raise fastapi.HTTPException(status_code=404)

    return next_parson.pop(0)


# get person state
@router.get('/api/state')
async def get_state():
    """
    :rtype: List[Dict[str, str]]
    """
    states = db.select_state_table(conn)
    return states


class __PutStateBody(BaseModel):
    name: str
    state: str


# put person state change + DB
@router.put('/api/state')
async def post_state(payload: __PutStateBody):
    """
    :param payload: person name and state
    """

    if not db.select_state_table_name_is_exists(conn, payload.name):
        raise fastapi.HTTPException(status_code=404)

    if payload.state == 'in-home':
        db.delete_state_table(conn, payload.name)
    else:
        db.update_state_table(conn, payload.name, payload.state)
    db.insert_log_table(conn, payload.name, payload.state, "")
    return


# get logs  + DB
@router.get('/api/log')
async def get_log():
    """
    :rtype: List[Dict]
    """
    logs = db.select_log_table(conn)
    return logs


@router.get('/api/idm')
async def get_idm():
    """
    Return List of idm
    :rtype:List[Dict[str, str]]
    """
    idm_list = db.select_idm_table(conn)
    return idm_list


class __PostIDMBody(BaseModel):
    idm: str
    name: Optional[str] = ""


@router.post('/api/idm')
async def post_idm(payload: __PostIDMBody):
    """
    :rtype : None
    """
    idm_dict = db.select_idm_table_idm(conn, payload.idm)

    if len(idm_dict) < 1:
        db.insert_idm_table(conn, payload.idm, payload.name)

        if not payload.name:
            pass

        else:
            next_parson.append(payload.name)

    else:
        if not idm_dict['name']:
            pass

        else:
            next_parson.append(idm_dict['name'])

    return


@router.put('/api/idm')
async def put_idm(payload: __PostIDMBody):
    """
    :rtype : None
    """
    idm_dict = db.select_idm_table_idm(conn, payload.idm)
    if not payload.name:
        raise fastapi.HTTPException(status_code=400)

    db.update_idm_table_idm(conn, payload.idm, payload.name)
