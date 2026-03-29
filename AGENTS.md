# Coffee Machine Program Requirements

## Business Requirements

### 1. Prompt User

Prompt the user by asking:

```
What would you like? (espresso/latte/cappuccino):
```

- Check the user's input to decide what to do next.
- The prompt should reappear every time an action has completed (e.g. once a drink is dispensed), so the machine is ready to serve the next customer.

---

### 2. Turn Off the Coffee Machine

- Enter `off` at the prompt to shut down the machine.
- This is the secret word for maintainers. The program should end execution when this input is received.

---

### 3. Print Report

- Enter `report` at the prompt to generate a status report showing current resource levels.

**Example output:**
```
Water: 100ml
Milk: 50ml
Coffee: 76g
Money: $2.5
```

---

### 4. Check Resources Sufficient

- When a drink is selected, check whether there are enough resources to make it.
- If a resource is insufficient, do **not** proceed — print an appropriate message instead.

**Example:**
> If Latte requires 200ml water but only 100ml remains:
> `"Sorry there is not enough water."`

The same check applies to milk and coffee.

---

### 5. Process Coins

- If resources are sufficient, prompt the user to insert coins.
- Coin values:
  - Quarter = $0.25
  - Dime = $0.10
  - Nickel = $0.05
  - Penny = $0.01
- Calculate the total monetary value of coins inserted.

**Example:**
> 1 quarter + 2 dimes + 1 nickel + 2 pennies
> = 0.25 + (0.10 × 2) + 0.05 + (0.01 × 2) = **$0.52**

---

### 6. Check Transaction Successful

- Verify the user has inserted enough money for the selected drink.

**If insufficient funds:**
> `"Sorry that's not enough money. Money refunded."`

**If sufficient funds:**
- Add the drink cost to the machine's profit total (reflected in the next `report`).

**Example report after a successful Latte purchase:**
```
Water: 100ml
Milk: 50ml
Coffee: 76g
Money: $2.5
```

**If overpaid:**
- Return the difference as change, rounded to 2 decimal places.

> `"Here is $2.45 dollars in change."`

---

### 7. Make Coffee

- If the transaction is successful and resources are sufficient, deduct the required ingredients from the machine's inventory.

**Example — Latte purchase:**

| | Water | Milk | Coffee | Money |
|---|---|---|---|---|
| **Before** | 300ml | 200ml | 100g | $0 |
| **After** | 100ml | 50ml | 76g | $2.5 |

- Once ingredients are deducted, confirm the drink to the user.

> `"Here is your latte. Enjoy!"`
## Technical Decisions

- streamlit front end 
- Python FastAPI backend
- Use OpenRouter for the AI calls. An OPENROUTER_API_KEY is in .env in the project root
- Use `openai/gpt-oss-120b` as the model
- Use SQLLite local database for the database, creating a new db if it doesn't exist
- Start and Stop server scripts for Mac, PC, Linux in scripts/


## Color Scheme

- Accent Yellow: `#ecad0a` - accent lines, highlights
- Blue Primary: `#209dd7` - links, key sections
- Purple Secondary: `#753991` - submit buttons, important actions
- Dark Navy: `#032147` - main headings
- Gray Text: `#888888` - supporting text, labels

## Coding standards

1. Use latest versions of libraries and idiomatic approaches as of today
2. Keep it simple - NEVER over-engineer, ALWAYS simplify, NO unnecessary defensive programming. No extra features - focus on simplicity.
3. Be concise. Keep README minimal. IMPORTANT: no emojis ever
4. When hitting issues, always identify root cause before trying a fix. Do not guess. Prove with evidence, then fix the root cause.

## Working documentation

All documents for planning and executing this project will be in the docs/ directory.
Please review the docs/PLAN.md document before proceeding.