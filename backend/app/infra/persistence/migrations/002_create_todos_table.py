from yoyo import step

up_sql = """
CREATE TABLE IF NOT EXISTS todos (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    owner_id UUID,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);
"""


down_sql = """DROP TABLE IF EXISTS todos;"""


steps = [
    step(up_sql, down_sql),
]
