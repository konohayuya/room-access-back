import fastapi
import requests.exceptions

import interface.keihan_bus as keihan_bus

router = fastapi.APIRouter()


# get bus schedule
@router.get('/api/bus/{dest}')
async def get_bus(dest: str):
    """
    :param dest: the destination to bus
    :rtype: List[Dict[str, str]]
    :exception: HTTPException(404)
    """
    try:
        if dest == "nagao":
            return keihan_bus.bus_to_nagao()

        elif dest == "kuzuha":
            return keihan_bus.bus_to_kuzuha()

        elif dest == "hirakatashi-kita":
            return keihan_bus.bus_to_hirakatashi_kita()

        else:
            raise fastapi.HTTPException(status_code=404)
    except requests.exceptions.ConnectionError:
        raise fastapi.HTTPException(status_code=504)
