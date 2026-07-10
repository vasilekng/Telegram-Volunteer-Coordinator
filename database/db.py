import aiosqlite

DB_NAME = 'bot.db'

async def db_start():
    """Создает таблицы при первом запуске бота"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT,
                district TEXT,
                description TEXT,
                contacts TEXT,
                photo_path TEXT,
                status TEXT DEFAULT 'new',
                volunteer_id INTEGER
            )
        ''')
        await db.commit()

async def create_request(user_id, category, district, desc, contacts, photo):
    """Сохраняет новую заявку в базу и возвращает её ID"""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('''
            INSERT INTO requests (user_id, category, district, description, contacts, photo_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, category, district, desc, contacts, photo))
        await db.commit()
        return cursor.lastrowid

async def get_new_requests():
    """Достает из базы все новые заявки"""
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row 
        async with db.execute("SELECT * FROM requests WHERE status = 'new'") as cursor:
            return await cursor.fetchall()

async def close_request(req_id: int):
    """Меняет статус заявки на 'done' (выполнено)"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE requests SET status = 'done' WHERE id = ?", (req_id,))
        await db.commit()