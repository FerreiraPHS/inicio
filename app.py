import os
import sqlite3
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

DB_PATH = os.path.join(os.path.dirname(__file__), "clients.db")

app = FastAPI()


def init_db():
    first_time = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            sheet TEXT
        )
        """
    )
    if first_time:
        data = [
            ("Alice", "alice@example.com", "A"),
            ("Bob", "bob@example.com", "A"),
            ("Carol", "carol@example.com", "B"),
            ("Dave", "dave@example.com", "B"),
        ]
        c.executemany("INSERT INTO clients (name, email, sheet) VALUES (?, ?, ?)", data)
    conn.commit()
    conn.close()


def get_clients(sheet: str | None = None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if sheet:
        c.execute(
            "SELECT id, name, email, sheet FROM clients WHERE sheet = ? ORDER BY id",
            (sheet,),
        )
    else:
        c.execute("SELECT id, name, email, sheet FROM clients ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return rows


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
async def index(sheet: str | None = None):
    rows = get_clients(sheet)
    html = ["<html><head><title>Clientes</title></head><body>"]
    html.append("<h1>Clientes</h1>")
    html.append("<form method='get'>")
    html.append(f"Sheet: <input name='sheet' value='{sheet or ''}'>")
    html.append("<button type='submit'>Filtrar</button>")
    html.append("</form>")
    html.append("<table border='1'>")
    html.append("<tr><th>ID</th><th>Nome</th><th>Email</th><th>Sheet</th></tr>")
    for row in rows:
        html.append("<tr>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>")
    html.append("</table>")
    html.append("</body></html>")
    return "\n".join(html)
