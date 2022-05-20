import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.api import api_router
from app.core import tasks
from app.core.config import settings

sentry_sdk.init(
    dsn="https://8724f08298d345ef8e0a42e9be46d183@o1240753.ingest.sentry.io/6394021",
    traces_sample_rate=1.0,
    environment="dev",  # You should read it from environment variable
)


def get_application():
    app = FastAPI(title="chama", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    try:
        app.add_middleware(SentryAsgiMiddleware)
    except Exception as err:
        raise err

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(api_router, prefix="/api")
    return app


app = get_application()
