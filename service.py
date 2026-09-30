from database import get_db_connection

def get_lines(status: str | None = None):

    conn = get_db_connection()

    if status is None:

        rows = conn.execute("""
            SELECT
                line_id,
                line_name,
                status
            FROM production_lines
            ORDER BY line_id
        """).fetchall()

    else:

        rows = conn.execute("""
            SELECT
                line_id,
                line_name,
                status
            FROM production_lines
            WHERE status = ?
            ORDER BY line_id
        """, (status,)).fetchall()

    conn.close()
    
    result = []
    
    for row in rows:
        result.append(dict(row))
    
    return result

def get_products():

    conn = get_db_connection()

    rows = conn.execute("""
        SELECT
            product_id,
            product_name
        FROM products
        ORDER BY product_id
    """).fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]

def get_production_records():

    conn = get_db_connection()

    rows = conn.execute("""
        SELECT
            r.record_id,
            r.production_date,

            r.line_id,
            l.line_name,

            r.product_id,
            p.product_name,

            r.target_qty,
            r.produced_qty,
            r.defect_qty

        FROM production_records r

        JOIN production_lines l
            ON r.line_id = l.line_id

        JOIN products p
            ON r.product_id = p.product_id

        ORDER BY
            r.production_date DESC,
            r.record_id DESC
    """).fetchall()

    conn.close()

    result = []
            
    for row in rows:
        result.append(dict(row))
    
    return result

def add_production(
    production_date,
    line_id,
    product_id,
    target_qty,
    produced_qty,
    defect_qty
):
    with get_db_connection() as conn:

        cursor = conn.execute(
            """
            INSERT INTO production_records
            (
                production_date,
                line_id,
                product_id,
                target_qty,
                produced_qty,
                defect_qty
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                production_date,
                line_id,
                product_id,
                target_qty,
                produced_qty,
                defect_qty
            )
        )

        conn.commit()

        return cursor.lastrowid

def update_production(
    record_id,
    produced_qty,
    defect_qty
):

    with get_db_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE production_records

            SET produced_qty = ?,
                defect_qty = ?

            WHERE record_id = ?
            """,
            (
                produced_qty,
                defect_qty,
                record_id
            )
        )

        conn.commit()

        return cursor.rowcount

def delete_production(record_id):

    with get_db_connection() as conn:

        cursor = conn.execute(
            """
            DELETE
            FROM production_records
            WHERE record_id = ?
            """,
            (record_id,)
        )

        conn.commit()

        return cursor.rowcount

# ============================================================
# 생산라인 등
# ============================================================

def add_line(
    line_id,
    line_name,
    status
):

    with get_db_connection() as conn:

        conn.execute(
            """
            INSERT INTO production_lines
            (
                line_id,
                line_name,
                status
            )
            VALUES (?, ?, ?)
            """,
            (
                line_id,
                line_name,
                status
            )
        )

        conn.commit()

        return line_id


# ============================================================
# 생산라인 수정
# ============================================================

def update_line(
    line_id,
    line_name,
    status
):

    with get_db_connection() as conn:

        cursor = conn.execute(
            """
            UPDATE production_lines

            SET line_name = ?,
                status = ?

            WHERE line_id = ?
            """,
            (
                line_name,
                status,
                line_id
            )
        )

        conn.commit()

        return cursor.rowcount

  # ============================================================
# 제품 등록
# ============================================================

def add_product(
    product_id,
    product_name
):

    with get_db_connection() as conn:

        conn.execute(
            """
            INSERT INTO products
            (
                product_id,
                product_name
            )
            VALUES (?, ?)
            """,
            (
                product_id,
                product_name
            )
        )

        conn.commit()

        return product_id


# ============================================================
# 제품 수정
# ============================================================

def update_product(
    product_id,
    product_name
):

    with get_db_connection() as conn:

        cursor = conn.execute(
            """
            UPDATE products

            SET product_name = ?

            WHERE product_id = ?
            """,
            (
                product_name,
                product_id
            )
        )

        conn.commit()

        return cursor.rowcount

def add_production_order(
    line_id,
    product_id,
    target_qty,
    planned_start_at,
    due_at
):

    with get_db_connection() as conn:

        cursor = conn.execute(
            """
            INSERT INTO production_orders
            (
                line_id,
                product_id,
                target_qty,
                planned_start_at,
                due_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                line_id,
                product_id,
                target_qty,
                planned_start_at,
                due_at
            )
        )

        conn.commit()

        return cursor.lastrowid    

    