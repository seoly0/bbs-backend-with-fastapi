import os
from logging import getLogger

import psutil
from fastapi import FastAPI

import boot
from app.api import admin, v1
from utils.moduleUtils import module_to_list

boot_list = module_to_list(boot, get="boot")

# 선행 실행
for exe in boot_list:
    exe.execute()

# 무결성 검사
all_green = True
for ver in boot_list:
    all_green = all_green and ver.verify()
if not all_green:
    parent_pid = os.getpid()
    parent = psutil.Process(parent_pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.parent().kill()
    parent.kill()

logger = getLogger(__name__)

app = FastAPI(
    docs_url=None,
    openapi_url=None,
)


@app.on_event("startup")
async def startup():
    logger.info("App Start - Bulletin Board System By Seoly")


@app.on_event("shutdown")
async def shutdown():
    logger.info("App Terminated")


# Mount APIs
app.mount(path="/api/v1", app=v1, name="v1")
app.mount(path="/api/admin", app=admin, name="admin")
