from dataclasses import dataclass


MENU = {
    "espresso": {"ingredients": {"water": 50, "coffee": 18, "milk": 0}, "cost": 1.5},
    "latte": {"ingredients": {"water": 200, "coffee": 24, "milk": 150}, "cost": 2.5},
    "cappuccino": {"ingredients": {"water": 250, "coffee": 24, "milk": 100}, "cost": 3.0},
}


@dataclass
class MachineState:
    water: int
    milk: int
    coffee: int
    money: float


def format_report(state: MachineState) -> str:
    return (
        f"Water: {state.water}ml\n"
        f"Milk: {state.milk}ml\n"
        f"Coffee: {state.coffee}g\n"
        f"Money: ${state.money}"
    )


def check_resources(drink: str, state: MachineState) -> tuple[bool, str | None]:
    recipe = MENU[drink]["ingredients"]
    for ingredient, required in recipe.items():
        available = getattr(state, ingredient)
        if available < required:
            return False, f"Sorry there is not enough {ingredient}."
    return True, None


def calculate_coin_total(quarters: int, dimes: int, nickels: int, pennies: int) -> float:
    total = (quarters * 0.25) + (dimes * 0.10) + (nickels * 0.05) + (pennies * 0.01)
    return round(total, 2)


def process_transaction(drink: str, paid_amount: float) -> tuple[bool, float, str]:
    cost = MENU[drink]["cost"]
    if paid_amount < cost:
        return False, 0.0, "Sorry that's not enough money. Money refunded."
    change = round(paid_amount - cost, 2)
    if change > 0:
        return True, change, f"Here is ${change} dollars in change."
    return True, 0.0, ""


def apply_successful_order(drink: str, state: MachineState) -> MachineState:
    recipe = MENU[drink]["ingredients"]
    cost = MENU[drink]["cost"]
    return MachineState(
        water=state.water - recipe["water"],
        milk=state.milk - recipe["milk"],
        coffee=state.coffee - recipe["coffee"],
        money=round(state.money + cost, 2),
    )

