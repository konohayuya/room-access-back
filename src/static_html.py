import fastapi
# for vue compiled files

router = fastapi.APIRouter()


@router.get("/")
async def show_root():
    return fastapi.responses.FileResponse('src/dist/index.html', media_type='text/html')


@router.get("/{rest_of_path:path}")
async def show_files(rest_of_path: str):
    return fastapi.responses.FileResponse('src/dist/'+rest_of_path)
