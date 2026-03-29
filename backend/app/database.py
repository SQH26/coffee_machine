import sqlite3
from pathlib import Path

from .machine import MachineState


DEFAULT_STATE = MachineState(water=300, milk=200, coffee=100, money=0.0)


def db_path() -> Path:
    return Path(__file__).resolve().parents[2] / "instance" / "coffee_machine.db"


def ensure_database() -> None:
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS machine_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                water INTEGER NOT NULL,
                milk INTEGER NOT NULL,
                coffee INTEGER NOT NULL,
                money REAL NOT NULL
            )
            """
        )
        row = conn.execute("SELECT id FROM machine_state WHERE id = 1").fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO machine_state (id, water, milk, coffee, money) VALUES (1, ?, ?, ?, ?)",
                (
                    DEFAULT_STATE.water,
                    DEFAULT_STATE.milk,
                    DEFAULT_STATE.coffee,
                    DEFAULT_STATE.money,
                ),
            )
        conn.commit()


def get_state() -> MachineState:
    ensure_database()
    with sqlite3.connect(db_path()) as conn:
        row = conn.execute(
            "SELECT water, milk, coffee, money FROM machine_state WHERE id = 1"
        ).fetchone()
    if row is None:
        return DEFAULT_STATE
    return MachineState(water=row[0], milk=row[1], coffee=row[2], money=round(row[3], 2))


def set_state(state: MachineState) -> None:
    ensure_database()
    with sqlite3.connect(db_path()) as conn:
        conn.execute(
            "UPDATE machine_state SET water = ?, milk = ?, coffee = ?, money = ? WHERE id = 1",
            (state.water, state.milk, state.coffee, round(state.money, 2)),
        )
        conn.commit()


def reset_state() -> MachineState:
    set_state(DEFAULT_STATE)
    return DEFAULT_STATE

