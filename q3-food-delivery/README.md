# Q3: Food Delivery Platform with Docker Networking

I built a small food delivery order service made of three containers: a **Flask** API, a **MySQL** database and a **Redis** cache. They run on a custom Docker bridge network called `food-delivery-net` and talk to each other by container name. Only the Flask port is published to my laptop. The approach, tools and flowchart were written in my record before I ran anything.

**Setup:** Windows laptop, Docker Desktop (WSL2), PowerShell for Docker commands, Git Bash for files and Git.

## What's in this folder

| Path | Contents |
|---|---|
| `app/` | The Flask app (`app.py`), its `Dockerfile` and `requirements.txt` |
| `apparmor/` | The AppArmor profile I wrote (`food-delivery-profile`) |
| `evidence/` | Real command outputs, numbered in the order I ran them, plus a screenshot |

## How it works

```
Browser / curl  --(port 5000)-->  Flask  --(mysql:3306)-->  MySQL
                                    |
                                    +-----(redis:6379)--->  Redis
        (all three on food-delivery-net; MySQL and Redis have no published ports)
```

Flask checks Redis first. If an order isn't cached, it reads it from MySQL and stores it in Redis for 60 seconds.

## What I demonstrated

| # | Task | Result | Evidence |
|---|---|---|---|
| 1 | Create the custom network | `food-delivery-net` created | `01` |
| 2 | Run MySQL and Redis with no published ports, Flask with only port 5000 | `docker ps` shows a host port for Flask only | `02`, `03` |
| 3 | Flask connects by container name, not IP | Hosts shown as `mysql` and `redis` | `04`, `05`, `06` |
| 4 | Database and cache operations | First `/orders/1` came from `mysql-database`, the repeat from `redis-cache` | `07`, `08`, `order-endpoint.png` |
| 5 | Internal vs host access | From the host, 3306 and 6379 failed and 5000 worked. Inside the network, `mysql:3306` and `redis:6379` were reachable | `09` to `12` |
| 6 | AppArmor and a security test | Not enforced on my machine (see below), with a substitute test | `13` to `16` |
| 7 | Deliberate failure, diagnosis and fix | Found and fixed (see below) | `17` to `23` |
| 8 | Final network details and container list | Saved | `24`, `25` |

## AppArmor: what happened

AppArmor is a Linux kernel feature, and it was **not enforced** on my machine:

- `evidence/13` shows Docker's security options listing only `seccomp` and `cgroupns`, with no `apparmor`.
- `evidence/14`: with `--security-opt apparmor=food-delivery-profile`, the container still printed `/etc/passwd`, so the profile was ignored.

That means the profile in `apparmor/` was **not tested**. On a Linux host with AppArmor I would load it with `sudo apparmor_parser -r food-delivery-profile` and repeat the same test.

**Substitute test (a different mechanism, not AppArmor):** a container run with `--read-only --cap-drop ALL` could not create a file (`Read-only file system`, `evidence/15`), while the same command in an unrestricted container succeeded (`evidence/16`).

## The deliberate failure

I started a second Flask container, `flask-broken`, on the default bridge network instead of `food-delivery-net`.

1. **Symptom:** the home page worked, but `/health/db` returned `Name or service not known` for the host `mysql` (`17`, `18`).
2. **Logs:** repeated failed attempts to resolve `mysql` (`19`).
3. **Network check:** `food-delivery-net` listed `mysql`, `redis` and `flask` but not `flask-broken` (`20`), and `flask-broken` was only on the default `bridge` network (`21`).
4. **Cause:** the default bridge has no name-based DNS, so `mysql` could not be resolved.
5. **Fix:** `docker network connect food-delivery-net flask-broken`. Afterwards `/health/db` returned `connected` (`22`) and the network listed `flask-broken` (`23`).

## Notes

- MySQL runs with `MYSQL_ALLOW_EMPTY_PASSWORD=yes`. This is a throwaway lab setup, and no passwords or secrets are stored in this repo.
- `app.py` retries the MySQL connection when it starts, because MySQL takes a while to become ready.
- This is a lab setup, not production: it uses Flask's development server and has no volume, so the data is lost when the MySQL container is removed.
