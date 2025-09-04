CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS annotations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    start_offset INTEGER NOT NULL,
    end_offset INTEGER NOT NULL,
    entity_id TEXT NOT NULL,
    entity_label TEXT NOT NULL,
    FOREIGN KEY(document_id) REFERENCES documents(id)
);
