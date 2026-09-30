CREATE TABLE IF NOT EXISTS production_lines (
    line_id TEXT PRIMARY KEY,
    line_name TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS production_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    production_date TEXT NOT NULL,
    line_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    target_qty INTEGER NOT NULL,
    produced_qty INTEGER NOT NULL,
    defect_qty INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY (line_id)
        REFERENCES production_lines(line_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS production_orders (

    order_id INTEGER PRIMARY KEY AUTOINCREMENT,

    line_id TEXT NOT NULL,

    product_id TEXT NOT NULL,

    target_qty INTEGER NOT NULL,

    status TEXT NOT NULL DEFAULT 'planned',

    planned_start_at TEXT NOT NULL,

    due_at TEXT NOT NULL,

    actual_start_at TEXT,

    actual_end_at TEXT,

    created_at TEXT DEFAULT (datetime('now', 'localtime')),

    FOREIGN KEY (line_id)
        REFERENCES production_lines(line_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
    
);


INSERT OR IGNORE INTO production_lines
(line_id, line_name, status)
VALUES
('LINE-01', '조립라인 1', 'running'),
('LINE-02', '조립라인 2', 'running'),
('LINE-03', '포장라인 1', 'stopped');


INSERT OR IGNORE INTO products
(product_id, product_name)
VALUES
('PROD-A', '스마트 센서'),
('PROD-B', '제어 모듈'),
('PROD-C', 'IoT Gateway');

INSERT INTO production_records
(
    production_date,
    line_id,
    product_id,
    target_qty,
    produced_qty,
    defect_qty
)
VALUES
('2026-09-27', 'LINE-01', 'PROD-A', 1000, 930, 12),
('2026-09-27', 'LINE-02', 'PROD-B', 800, 760, 8),
('2026-09-27', 'LINE-03', 'PROD-C', 500, 420, 15),
('2026-09-26', 'LINE-01', 'PROD-A', 1000, 980, 6),
('2026-09-26', 'LINE-02', 'PROD-B', 800, 790, 5);