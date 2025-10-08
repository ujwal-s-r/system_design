import os
import redis
from fastapi import FastAPI

app = FastAPI()

# Get the Redis hostname from the environment variable we set in docker-compose.yml
# Default to 'localhost' if the variable is not set
redis_host = os.getenv("REDIS_HOST", "localhost")

# Connect to our Redis container
# The decode_responses=True argument makes sure Redis returns strings, not bytes
r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)


@app.get("/")
def read_root():
    # When this endpoint is hit, increment the 'visits' key in Redis by 1
    # The incr command is atomic, making it safe for concurrent requests
    visits = r.incr("visits")
    return {"message": "Hello from FastAPI!", "visits": int(visits)}