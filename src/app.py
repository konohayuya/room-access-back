import fastapi
import uvicorn

import bus
import state
import static_html

api = fastapi.FastAPI()

api.include_router(state.router)


def main():
    # start srv program
    uvicorn.run(api, host='localhost', port=8083, log_level="warning")


if __name__ == '__main__':
    main()
