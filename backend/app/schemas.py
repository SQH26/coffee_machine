from pydantic import BaseModel, Field


class CoinInput(BaseModel):
    quarters: int = Field(default=0, ge=0)
    dimes: int = Field(default=0, ge=0)
    nickels: int = Field(default=0, ge=0)
    pennies: int = Field(default=0, ge=0)


class OrderRequest(BaseModel):
    drink: str
    coins: CoinInput


class CommandRequest(BaseModel):
    command: str
    coins: CoinInput | None = None

