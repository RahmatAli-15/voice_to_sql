import json
import sqlite3
from agents.llm_agent import LLMAgent

class TradingAgent:
    def __init__(self, db_path="trades.db", model="llama-3.1-8b-instant"):
        self.db = db_path
        self.llm = LLMAgent(model=model)

    # Convert question → SQL
    def text_to_sql(self, question):
        schema = {
            "trades": [
                "trade_id","symbol","type","entry","exit","profit",
                "psychology","session","strategy","source","confidence",
                "rr_ratio","mistake","market_condition","trade_date"
            ]
        }

        prompt = f"""
Generate VALID SQLite SQL ONLY.
Return ONLY the SQL with no explanation.

Schema:
{json.dumps(schema)}

Question:
{question}

SQL:
"""
        sql = self.llm.ask(prompt).strip()

        if not sql.endswith(";"):
            sql += ";"

        return sql

    # Execute once + one-sentence summary
    def ask(self, question):
        sql = self.text_to_sql(question)

        # Print SQL for debugging
        print("\n===== GENERATED SQL =====")
        print(sql)
        print("=========================\n")

        # Execute SQL ONCE (no fixing)
        try:
            conn = sqlite3.connect(self.db)
            cur = conn.cursor()
            rows = cur.execute(sql).fetchall()
            conn.close()
        except Exception as e:
            return f"SQL Error: {e}"

        # One-sentence answer
        summary_prompt = f"""
Summarize the SQL results in ONE short sentence only.

Question: {question}
SQL: {sql}
Results: {rows}

One-sentence answer:
"""
        answer = self.llm.ask(summary_prompt)
        answer = answer.split(".")[0].strip() + "."
        return answer
