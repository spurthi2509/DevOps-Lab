# Q3: Demo Commands

Commands used to demonstrate each task, run in PowerShell from `q3-food-delivery`.

## Setup: Check Containers Are Running
```powershell
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

## Task 1: Flask Application with Order Endpoint
```powershell
Get-Content app\app.py | Select-String "@app.route"
```

## Task 2: Custom Bridge Network
```powershell
docker network ls --filter name=food-delivery-net
```

## Task 3: Three Containers on the Same Network
```powershell
docker network inspect food-delivery-net --format "{{range .Containers}}{{.Name}} {{end}}"
```

## Task 4: Connecting by Container Name, Not IP
```powershell
Get-Content app\app.py | Select-String "MYSQL_HOST|REDIS_HOST"
```

## Task 5: Verify Database, Redis and Application Endpoint
```powershell
docker exec redis redis-cli FLUSHALL
Start-Process "http://localhost:5000/health/db"
Start-Sleep -Seconds 2
Start-Process "http://localhost:5000/health/redis"
Start-Sleep -Seconds 2
Start-Process "http://localhost:5000/orders/1"
```
Refresh the `/orders/1` tab within 60 seconds to show the cached response (`redis-cache`).

## Task 6: Controlled Port Exposure, Host vs Internal Access
```powershell
docker ps --format "table {{.Names}}\t{{.Ports}}"

Test-NetConnection localhost -Port 5000 -WarningAction SilentlyContinue | Select-Object -ExpandProperty TcpTestSucceeded
Test-NetConnection localhost -Port 3306 -WarningAction SilentlyContinue | Select-Object -ExpandProperty TcpTestSucceeded
Test-NetConnection localhost -Port 6379 -WarningAction SilentlyContinue | Select-Object -ExpandProperty TcpTestSucceeded

docker run --rm --network food-delivery-net busybox nc -zv mysql 3306
docker run --rm --network food-delivery-net busybox nc -zv redis 6379
```

## Task 7a: AppArmor Attempt
AppArmor is not enforced on Docker Desktop for Windows, so the profile is ignored here.
```powershell
Get-Content apparmor\food-delivery-profile
docker info --format "{{.SecurityOptions}}"
docker run --rm --security-opt apparmor=food-delivery-profile python:3.12-slim cat /etc/passwd
```

## Task 7b: Alternative Security Test (not AppArmor)
```powershell
docker run --rm --read-only --cap-drop ALL python:3.12-slim sh -c "touch /test.txt"
docker run --rm python:3.12-slim sh -c "touch /test.txt && echo write-succeeded"
```

## Extra: Connectivity Failure, Diagnosis and Fix
```powershell
docker rm -f flask-broken
docker run -d --name flask-broken -p 5001:5000 food-flask
Start-Sleep -Seconds 5
Start-Process "http://localhost:5001/health/db"
docker logs flask-broken --tail 10
docker network inspect food-delivery-net --format "{{range .Containers}}{{.Name}} {{end}}"
docker inspect flask-broken --format "{{json .NetworkSettings.Networks}}"
docker network connect food-delivery-net flask-broken
Start-Sleep -Seconds 5
Start-Process "http://localhost:5001/health/db"
docker network inspect food-delivery-net --format "{{range .Containers}}{{.Name}} {{end}}"
```

## Final: Finish on the Working Website
```powershell
docker exec redis redis-cli FLUSHALL
Start-Process "http://localhost:5000/orders/1"
```
