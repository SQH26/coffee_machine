from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .database import ensure_database, get_state, reset_state, set_state
from .machine import (
    MENU,
    MachineState,
    apply_successful_order,
    calculate_coin_total,
    check_resources,
    format_report,
    process_transaction,
)
from .openrouter import get_ai_tip
from .schemas import CommandRequest, OrderRequest


@asynccontextmanager
async def lifespan(_: FastAPI):
    ensure_database()
    yield


app = FastAPI(title="Coffee Machine API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _order(drink: str, quarters: int, dimes: int, nickels: int, pennies: int) -> dict:
    drink_name = drink.lower().strip()
    if drink_name not in MENU:
        raise HTTPException(status_code=400, detail="Invalid drink selection.")

    state = get_state()
    enough, resource_message = check_resources(drink_name, state)
    if not enough:
        return {"success": False, "message": resource_message, "report": format_report(state)}

    total_paid = calculate_coin_total(quarters, dimes, nickels, pennies)
    successful, change, transaction_message = process_transaction(drink_name, total_paid)
    if not successful:
        return {"success": False, "message": transaction_message, "report": format_report(state)}

    updated_state = apply_successful_order(drink_name, state)
    set_state(updated_state)

    messages = []
    if transaction_message:
        messages.append(transaction_message)
    messages.append(f"Here is your {drink_name}. Enjoy!")

    return {
        "success": True,
        "message": " ".join(messages),
        "change": change,
        "report": format_report(updated_state),
    }


@app.get("/api/report")
def report() -> dict:
    state = get_state()
    return {
        "water": state.water,
        "milk": state.milk,
        "coffee": state.coffee,
        "money": state.money,
        "text": format_report(state),
    }


@app.post("/api/order")
def order(request: OrderRequest) -> dict:
    return _order(
        request.drink,
        request.coins.quarters,
        request.coins.dimes,
        request.coins.nickels,
        request.coins.pennies,
    )


@app.post("/api/command")
def command(request: CommandRequest) -> dict:
    command_value = request.command.lower().strip()
    if command_value == "off":
        return {"success": True, "message": "Coffee machine is now off.", "should_shutdown": True}
    if command_value == "report":
        state = get_state()
        return {"success": True, "message": format_report(state), "report": format_report(state)}
    if command_value in MENU:
        if request.coins is None:
            raise HTTPException(status_code=400, detail="Coins are required for drink orders.")
        return _order(
            command_value,
            request.coins.quarters,
            request.coins.dimes,
            request.coins.nickels,
            request.coins.pennies,
        )
    raise HTTPException(status_code=400, detail="Unknown command.")


@app.post("/api/reset")
def reset() -> dict:
    state = reset_state()
    return {"success": True, "report": format_report(state)}


@app.get("/api/ai-tip")
async def ai_tip(prompt: str = "Give one concise coffee brewing tip.") -> dict:
    tip = await get_ai_tip(prompt)
    return {"tip": tip}


frontend_out_dir = Path(__file__).resolve().parents[2] / "frontend" / "out"
frontend_index = frontend_out_dir / "index.html"

if frontend_out_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_out_dir), html=True), name="frontend")


@app.get("/", response_model=None)
def root_fallback():
    if frontend_index.exists():
        return FileResponse(frontend_index)
    return {"message": "Frontend build not found. Build Next.js app to serve UI at /."}

