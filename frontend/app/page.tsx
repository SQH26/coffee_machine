"use client";

import { useMemo, useState } from "react";

type Coins = {
  quarters: number;
  dimes: number;
  nickels: number;
  pennies: number;
};

const defaultCoins: Coins = {
  quarters: 0,
  dimes: 0,
  nickels: 0,
  pennies: 0
};

export default function Home() {
  const [command, setCommand] = useState("espresso");
  const [coins, setCoins] = useState<Coins>(defaultCoins);
  const [result, setResult] = useState("What would you like? (espresso/latte/cappuccino):");
  const [report, setReport] = useState("");
  const [aiTip, setAiTip] = useState("");
  const [loading, setLoading] = useState(false);

  const total = useMemo(() => {
    return (
      coins.quarters * 0.25 +
      coins.dimes * 0.1 +
      coins.nickels * 0.05 +
      coins.pennies * 0.01
    ).toFixed(2);
  }, [coins]);

  const onCoinChange = (key: keyof Coins, value: string) => {
    const parsed = Number.parseInt(value, 10);
    setCoins((prev) => ({ ...prev, [key]: Number.isNaN(parsed) ? 0 : Math.max(parsed, 0) }));
  };

  const submit = async () => {
    setLoading(true);
    try {
      const payload: { command: string; coins?: Coins } = { command };
      if (command === "espresso" || command === "latte" || command === "cappuccino") {
        payload.coins = coins;
      }
      const response = await fetch("/api/command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      if (!response.ok) {
        setResult(data.detail ?? "Request failed.");
      } else {
        setResult(data.message ?? "Done.");
        if (data.report) {
          setReport(data.report);
        }
      }
    } catch {
      setResult("Unable to reach backend.");
    } finally {
      setLoading(false);
    }
  };

  const refreshReport = async () => {
    const response = await fetch("/api/report");
    const data = await response.json();
    setReport(data.text ?? "");
  };

  const fetchTip = async () => {
    const response = await fetch("/api/ai-tip");
    const data = await response.json();
    setAiTip(data.tip ?? "");
  };

  const reset = async () => {
    await fetch("/api/reset", { method: "POST" });
    setCoins(defaultCoins);
    setResult("Machine reset. What would you like? (espresso/latte/cappuccino):");
    setReport("");
  };

  return (
    <main>
      <h1>Coffee Machine</h1>
      <p className="subtitle">What would you like? (espresso/latte/cappuccino):</p>

      <section className="card">
        <label className="label" htmlFor="command">Command</label>
        <select id="command" value={command} onChange={(e) => setCommand(e.target.value)}>
          <option value="espresso">espresso</option>
          <option value="latte">latte</option>
          <option value="cappuccino">cappuccino</option>
          <option value="report">report</option>
          <option value="off">off</option>
        </select>

        {(command === "espresso" || command === "latte" || command === "cappuccino") && (
          <>
            <div className="grid">
              <div>
                <label className="label" htmlFor="quarters">Quarters</label>
                <input id="quarters" type="number" min={0} value={coins.quarters} onChange={(e) => onCoinChange("quarters", e.target.value)} />
              </div>
              <div>
                <label className="label" htmlFor="dimes">Dimes</label>
                <input id="dimes" type="number" min={0} value={coins.dimes} onChange={(e) => onCoinChange("dimes", e.target.value)} />
              </div>
              <div>
                <label className="label" htmlFor="nickels">Nickels</label>
                <input id="nickels" type="number" min={0} value={coins.nickels} onChange={(e) => onCoinChange("nickels", e.target.value)} />
              </div>
              <div>
                <label className="label" htmlFor="pennies">Pennies</label>
                <input id="pennies" type="number" min={0} value={coins.pennies} onChange={(e) => onCoinChange("pennies", e.target.value)} />
              </div>
            </div>
            <p>Inserted: ${total}</p>
          </>
        )}

        <button onClick={submit} disabled={loading}>{loading ? "Processing..." : "Submit"}</button>
        <button className="secondary" onClick={refreshReport}>Report</button>
        <button className="secondary" onClick={fetchTip}>AI Tip</button>
        <button className="secondary" onClick={reset}>Reset</button>
      </section>

      <section className="card">
        <p className="label">Machine Response</p>
        <pre>{result}</pre>
      </section>

      <section className="card">
        <p className="label">Report</p>
        <pre>{report || "No report fetched yet."}</pre>
      </section>

      <section className="card">
        <p className="label">AI Tip</p>
        <pre>{aiTip || "No tip fetched yet."}</pre>
      </section>
    </main>
  );
}
