import os, json, time, threading
from flask import Flask, jsonify
import pymysql
import redis

app = Flask(__name__)

# Hostnames come from environment variables and default to the container names
MYSQL_HOST = os.environ.get("MYSQL_HOST", "mysql")
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
DB_NAME = "fooddb"


def get_db(use_db=True):
    return pymysql.connect(
        host=MYSQL_HOST,
        user="root",
        password=os.environ.get("MYSQL_PASSWORD", ""),
        database=DB_NAME if use_db else None,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=3,
    )


def get_cache():
    return redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True,
                       socket_connect_timeout=3)


def init_db():
    # MySQL takes a while to start, so retry in the background
    for attempt in range(1, 31):
        try:
            conn = get_db(use_db=False)
            with conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            conn.select_db(DB_NAME)
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS orders "
                            "(id INT PRIMARY KEY, customer VARCHAR(50), "
                            "item VARCHAR(50), status VARCHAR(20))")
                cur.execute("INSERT IGNORE INTO orders VALUES "
                            "(1,'Asha','Biryani','Delivered'),"
                            "(2,'Ravi','Masala Dosa','On the way'),"
                            "(3,'Meera','Paneer Roll','Preparing')")
            conn.commit()
            conn.close()
            print("Database ready", flush=True)
            return
        except Exception as e:
            print(f"Waiting for MySQL at '{MYSQL_HOST}' (try {attempt}/30): {e}", flush=True)
            time.sleep(2)
    print("Giving up: MySQL not reachable", flush=True)


@app.route("/")
def home():
    return jsonify({"service": "food-delivery-order-service", "status": "running"})


@app.route("/health/db")
def health_db():
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS ok")
            row = cur.fetchone()
        conn.close()
        return jsonify({"mysql": "connected", "host": MYSQL_HOST, "result": row})
    except Exception as e:
        return jsonify({"mysql": "error", "host": MYSQL_HOST, "detail": str(e)}), 500


@app.route("/health/redis")
def health_redis():
    try:
        pong = get_cache().ping()
        return jsonify({"redis": "connected", "host": REDIS_HOST, "ping": pong})
    except Exception as e:
        return jsonify({"redis": "error", "host": REDIS_HOST, "detail": str(e)}), 500


@app.route("/orders/<int:order_id>")
def get_order(order_id):
    key = f"order:{order_id}"
    try:
        cache = get_cache()
        cached = cache.get(key)
        if cached:
            return jsonify({"source": "redis-cache", "order": json.loads(cached)})
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
            order = cur.fetchone()
        conn.close()
        if not order:
            return jsonify({"error": "order not found"}), 404
        cache.setex(key, 60, json.dumps(order))
        return jsonify({"source": "mysql-database", "order": order})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    threading.Thread(target=init_db, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
