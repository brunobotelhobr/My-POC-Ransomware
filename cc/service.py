import uvicorn
import random
import string
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


class Hostname(BaseModel):
    name: str


app = FastAPI()

key_dict = {}


@app.get("/")
async def get_home() -> HTMLResponse:
    with open("index.html", "r") as f:
        html = f.read()
    return HTMLResponse(content=html, status_code=200)


@app.get("/keys")
async def get_keys(password: str):
    if password == "cochilocachimbocai":
        return key_dict
    else:
        return "Wrong password"


@app.post("/keys")
async def post_key(hostname: Hostname):
    decoded_hostname = hostname.name
    if hostname.name in key_dict:
        return key_dict[hostname.name]
    else:
        
        key = generate_key()
        key_dict[decoded_hostname] = key
        return key


def generate_key(length=16):
    """Generate a random string of printable ASCII characters."""
    printable_chars = string.ascii_letters + string.digits
    return "".join(random.choice(printable_chars) for _ in range(length))


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
