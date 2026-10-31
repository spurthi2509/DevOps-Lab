# Q3: Food Delivery Platform with Docker Networking

Flask order service + MySQL + Redis on a custom Docker bridge network (food-delivery-net). See WRITEUP.md for the approach, tools and flowchart prepared before execution.

## Layout
- app/: Flask app (app.py), Dockerfile, requirements.txt
- apparmor/: AppArmor profile (food-delivery-profile)
- evidence/: real command outputs and a screenshot, numbered in the order they were run

## What was demonstrated
1. Custom bridge network: evidence/01
2. MySQL and Redis started with NO published ports; only Flask publishes 5000: evidence/02, 03
3. Flask reaches MySQL and Redis by container name (host "mysql" / "redis"), never by IP:
   - endpoint: 04, database: 05, redis: 06
   - first /orders/1 served from mysql-database (07), repeat served from redis-cache (08)
   - screenshot: order-endpoint.png
4. Internal vs host access:
   - from the host, ports 3306 and 6379 are NOT reachable (False), port 5000 is (True): 09, 10, 11
   - from inside the network, mysql:3306 and redis:6379 are reachable: 12
5. AppArmor / security test (see limitation below): 13 to 16
6. Deliberate connectivity failure, diagnosis and fix: 17 to 23
7. Network details and final container list: 24, 25

## AppArmor: limitation
AppArmor is a Linux kernel feature and was NOT enforced on this machine (Windows with Docker Desktop):
- evidence/13 shows Docker's security options list seccomp and cgroupns, with no apparmor.
- evidence/14 shows the container still printed /etc/passwd with --security-opt apparmor=food-delivery-profile, i.e. the profile was ignored.
The profile in apparmor/ was therefore not tested. On a Linux host it would be loaded with: sudo apparmor_parser -r food-delivery-profile

Substitute security test (a different mechanism, NOT AppArmor): a container run with --read-only --cap-drop ALL could not write a file (evidence/15: Read-only file system), while the same command in an unrestricted container succeeded (evidence/16).

## Deliberate failure and diagnosis
A second Flask container (flask-broken) was started on the default bridge network instead of food-delivery-net.
- Symptom: / worked, but /health/db returned "Name or service not known" for host mysql (17, 18).
- Logs showed repeated failed attempts to resolve mysql (19).
- Network inspection showed food-delivery-net listed mysql, redis and flask but not flask-broken (20), and flask-broken was only on the default bridge network (21). The default bridge has no name-based DNS.
- Fix: docker network connect food-delivery-net flask-broken. Afterwards /health/db returned "connected" (22) and the network listed flask-broken (23).

## Notes
- MySQL ran with MYSQL_ALLOW_EMPTY_PASSWORD=yes for this throwaway lab. No passwords or secrets are stored in this repo.
- app.py retries the MySQL connection at startup because MySQL takes a while to become ready.
