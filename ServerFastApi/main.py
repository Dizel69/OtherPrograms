from fastapi import FastAPI, Request, Response, HTTPException
import logging
import requests
import aiohttp
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Запись в файл
        logging.StreamHandler()  # Вывод в консоль
    ]
)

# Настройка CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url}")
    headers = dict(request.headers)
    logging.info(f"Request Headers: {headers}")
    body = await request.body()
    logging.info(f"Request Body: {body.decode('utf-8')}")

    response = await call_next(request)

    logging.info(f"Response: {response.status_code}")
    logging.info(f"Response Headers: {dict(response.headers)}")
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    logging.info(f"Response Body: {response_body.decode('utf-8')}")

    # Прокручиваем тело ответа назад и создаем новый Response объект
    response = Response(content=response_body, status_code=response.status_code, headers=dict(response.headers))

    return response


@app.get("/")
async def read_root():
    return {"message": "Hello, GET request received!"}


@app.post("/data")
async def receive_data(data: dict):
    logging.info(f"Received data: {data}")
    return {"message": "Hello, POST request received!", "data": data}


@app.get("/external_requests")
async def make_external_requests():
    try:
        # Использование requests для синхронного запроса
        response = requests.get("http://httpbin.org/get")
        response.raise_for_status()
        logging.info(f"Requests response: {response.json()}")
    except requests.RequestException as e:
        logging.error(f"Requests error: {e}")
        raise HTTPException(status_code=500, detail="Requests error")

    try:
        # Использование aiohttp для асинхронного запроса
        async with aiohttp.ClientSession() as session:
            async with session.get("http://httpbin.org/get") as response:
                data = await response.json()
                logging.info(f"aiohttp response: {data}")
    except aiohttp.ClientError as e:
        logging.error(f"aiohttp error: {e}")
        raise HTTPException(status_code=500, detail="aiohttp error")

    return {"message": "External requests made successfully"}


if __name__ == "__main__":
    import uvicorn

    print("Starting server at http://127.0.0.1:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
