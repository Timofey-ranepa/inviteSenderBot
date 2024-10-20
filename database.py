import aiosqlite

DB_PATH = "users.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL UNIQUE,
            is_registered INTEGER NOT NULL
        )''')
        await db.commit()

async def add_user(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id, is_registered) VALUES (?, ?)", (user_id, 0))
        await db.commit()

async def update_user_registration(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET is_registered = 1 WHERE user_id = ?", (user_id,))
        await db.commit()

async def is_user_registered(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT is_registered FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None
