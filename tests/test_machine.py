from backend.app.machine import (
    MachineState,
    apply_successful_order,
    calculate_coin_total,
    check_resources,
    format_report,
    process_transaction,
)


def test_calculate_coin_total() -> None:
    total = calculate_coin_total(quarters=1, dimes=2, nickels=1, pennies=2)
    assert total == 0.52


def test_check_resources_insufficient_water() -> None:
    state = MachineState(water=100, milk=200, coffee=100, money=0.0)
    enough, message = check_resources("latte", state)
    assert enough is False
    assert message == "Sorry there is not enough water."


def test_process_transaction_insufficient_money() -> None:
    success, change, message = process_transaction("latte", paid_amount=1.0)
    assert success is False
    assert change == 0.0
    assert message == "Sorry that's not enough money. Money refunded."


def test_process_transaction_change() -> None:
    success, change, message = process_transaction("espresso", paid_amount=2.0)
    assert success is True
    assert change == 0.5
    assert message == "Here is $0.5 dollars in change."


def test_apply_successful_order_updates_inventory_and_money() -> None:
    state = MachineState(water=300, milk=200, coffee=100, money=0.0)
    updated = apply_successful_order("latte", state)
    assert updated.water == 100
    assert updated.milk == 50
    assert updated.coffee == 76
    assert updated.money == 2.5


def test_format_report_output() -> None:
    state = MachineState(water=100, milk=50, coffee=76, money=2.5)
    assert format_report(state) == "Water: 100ml\nMilk: 50ml\nCoffee: 76g\nMoney: $2.5"

