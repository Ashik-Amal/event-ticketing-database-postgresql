import psycopg2

# ---------- DATABASE CONNECTION ----------
conn = psycopg2.connect(
    dbname="global_expo",
    user="postgres",
    password="root",
    host="localhost",
    port="5432"
)

print("PROGRAM STARTED")

cursor = conn.cursor()

# ---------- FILE HANDLING ----------
input_file = open("input.txt", "r")
output_file = open("output.txt", "w")

def log(msg):
    output_file.write(msg + "\n")

# ---------- PROCESS TRANSACTIONS ----------
for line in input_file:
    line = line.strip()
    if not line:
        continue

    parts = line.split("#")
    txn_type = parts[0]

    log(f"\n--- Transaction Type: {txn_type} ---")

    try:
        # A — Insert spectator
        if txn_type == "A":
            sno, sname, semail = parts[1:]
            cursor.execute(
                "INSERT INTO spectator VALUES (%s,%s,%s)",
                (sno, sname, semail)
            )
            conn.commit()
            log("DBMS Response: SUCCESS")
            log("Spectator inserted.")

        # B — Insert event
        elif txn_type == "B":
            ecode, desc, loc, date, time, maxp = parts[1:]
            cursor.execute(
                "INSERT INTO event VALUES (%s,%s,%s,%s,%s,%s)",
                (ecode, desc, loc, date, time, maxp)
            )
            conn.commit()
            log("DBMS Response: SUCCESS")
            log("Event inserted.")

        # C — Delete spectator (only if no valid tickets)
        elif txn_type == "C":
            sno = parts[1]
            cursor.execute("""
                DELETE FROM spectator s
                WHERE s.sno = %s
                AND NOT EXISTS (
                    SELECT 1 FROM ticket t
                    WHERE t.sno = s.sno
                    AND NOT EXISTS (
                        SELECT 1 FROM cancel c WHERE c.tno = t.tno
                    )
                )
            """, (sno,))
            conn.commit()
            log("DBMS Response: SUCCESS")
            log(f"Spectator {sno} deleted if allowed.")

        # D — Delete event (only if all tickets cancelled)
        elif txn_type == "D":
            ecode = parts[1]
            cursor.execute("""
                DELETE FROM event e
                WHERE e.ecode = %s
                AND NOT EXISTS (
                    SELECT 1 FROM ticket t
                    WHERE t.ecode = e.ecode
                    AND NOT EXISTS (
                        SELECT 1 FROM cancel c WHERE c.tno = t.tno
                    )
                )
            """, (ecode,))
            conn.commit()
            log("DBMS Response: SUCCESS")
            log(f"Event {ecode} deleted if allowed.")

        # E — Issue ticket
        elif txn_type == "E":
            tno, ecode, sno = parts[1:]
            cursor.execute("""
                INSERT INTO ticket (tno, ecode, sno)
                SELECT %s,%s,%s
                WHERE NOT EXISTS (
                    SELECT 1 FROM ticket
                    WHERE ecode = %s AND sno = %s
                )
            """, (tno, ecode, sno, ecode, sno))
            conn.commit()
            log("DBMS Response: SUCCESS")
            log("Ticket issued if no duplicate.")

        # F — Travel query
        elif txn_type == "F":
            cursor.execute("""
                SELECT e.elocation, e.edate, COUNT(DISTINCT t.sno)
                FROM event e
                JOIN ticket t ON e.ecode = t.ecode
                LEFT JOIN cancel c ON c.tno = t.tno
                WHERE c.tno IS NULL
                GROUP BY e.elocation, e.edate
            """)
            rows = cursor.fetchall()
            log("DBMS Response: SUCCESS")
            for r in rows:
                log(str(r))

        # G — Total tickets (all events)
        elif txn_type == "G":
            cursor.execute("""
                SELECT e.edesc, COUNT(t.tno)
                FROM event e
                LEFT JOIN ticket t ON e.ecode = t.ecode
                GROUP BY e.edesc
                ORDER BY e.edesc
            """)
            rows = cursor.fetchall()
            log("DBMS Response: SUCCESS")
            for r in rows:
                log(str(r))

        # H — Total tickets for an event
        elif txn_type == "H":
            ecode = parts[1]
            cursor.execute("""
                SELECT e.edesc, COUNT(t.tno)
                FROM event e
                LEFT JOIN ticket t ON e.ecode = t.ecode
                WHERE e.ecode = %s
                GROUP BY e.edesc
            """, (ecode,))
            rows = cursor.fetchall()
            log("DBMS Response: SUCCESS")
            for r in rows:
                log(str(r))

        # I — Schedule for spectator
        elif txn_type == "I":
            sno = parts[1]
            cursor.execute("""
                SELECT s.sname, e.edate, e.elocation, e.etime, e.edesc
                FROM spectator s
                JOIN ticket t ON s.sno = t.sno
                JOIN event e ON t.ecode = e.ecode
                LEFT JOIN cancel c ON c.tno = t.tno
                WHERE s.sno = %s AND c.tno IS NULL
            """, (sno,))
            rows = cursor.fetchall()
            log("DBMS Response: SUCCESS")
            for r in rows:
                log(str(r))

        # J — Ticket details
        elif txn_type == "J":
            tno = parts[1]
            cursor.execute("""
                SELECT s.sname, t.ecode,
                CASE
                    WHEN c.tno IS NULL THEN 'VALID'
                    ELSE 'CANCELLED'
                END
                FROM ticket t
                JOIN spectator s ON s.sno = t.sno
                LEFT JOIN cancel c ON c.tno = t.tno
                WHERE t.tno = %s
            """, (tno,))
            rows = cursor.fetchall()
            log("DBMS Response: SUCCESS")
            for r in rows:
                log(str(r))

        # K — View cancelled tickets for event
        elif txn_type == "K":
            ecode = parts[1]
            cursor.execute("""
                SELECT c.tno, s.sname, c.cdate, c.cuser
                FROM cancel c
                JOIN spectator s ON s.sno = c.sno
                WHERE c.ecode = %s
            """, (ecode,))
            rows = cursor.fetchall()
            log("DBMS Response: SUCCESS")
            for r in rows:
                log(str(r))

        # L — Empty all tables
        elif txn_type == "L":
            cursor.execute("""
                TRUNCATE TABLE cancel, ticket, spectator, event CASCADE
            """)
            conn.commit()
            log("DBMS Response: SUCCESS")
            log("All tables truncated.")

        else:
            log("DBMS Response: UNKNOWN TRANSACTION")

    except Exception as e:
        conn.rollback()
        log("DBMS Response: ERROR")
        log(str(e))

# ---------- CLEANUP ----------
input_file.close()
output_file.close()
cursor.close()
conn.close()

print("PROGRAM FINISHED")
