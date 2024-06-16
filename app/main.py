import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tinytuya


# Define a Pydantic model for the request body
class SwitchState(BaseModel):
    state: str


app = FastAPI()

# load config json

with open("../config/config.json") as f:
    config = json.load(f)


@app.post("/switch")
async def switch(state: SwitchState):
    if state.state not in ["on", "off"]:
        raise HTTPException(status_code=400, detail="State must be 'on' or 'off'")

    c = tinytuya.Cloud(
        apiRegion=config["apiRegion"],
        apiKey=config["apiKey"],
        apiSecret=config["apiSecret"],
        apiDeviceID=config["apiDeviceID"],
    )

    commands = {
        "commands": [
            {"code": "switch_1", "value": state.state == "on"},
        ]
    }

    result = c.sendcommand(config["deviceId"], commands)
    return result
