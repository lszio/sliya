import uvicorn
from sliya.config import settings


def run_dev_server():
    uvicorn.run("sliya:app", host=settings.SERVER_HOST,
                port=settings.SERVER_PORT, log_level="debug", debug=True)


if __name__ == '__main__':
    run_dev_server()
