import uvicorn


def run_dev_server():
    uvicorn.run("sliya:app", host="localhost",
                port=9715, log_level="debug", debug=True)


if __name__ == '__main__':
    run_dev_server()
