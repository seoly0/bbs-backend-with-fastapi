from fastapi import APIRouter

# from app.batch.crawler.tasks import schedule_ruliweb_hotdeal

router = APIRouter()
router.tags = ["관리자 - 스케줄"]
router.prefix = "/scheduler"


# @router.get("/ruliweb/hotdeal/run")
# def run_ruliweb_hotdeal():
#     schedule_ruliweb_hotdeal.delay()
#     return True


# @router.get("/ruliweb/hotdeal/cancel")
# def cancel_ruliweb_hotdeal():
#     return True
