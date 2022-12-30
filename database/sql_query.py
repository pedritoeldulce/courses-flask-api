create_tables = """
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        url TEXT NOT NULL,
        module INTEGER NOT NULL,
        chapter INTEGER NOT NULL,
        category TEXT NOT NULL,
        status TEXT NOT NULL
    )
"""