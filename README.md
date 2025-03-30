# Home Service v2

This project is part of the **IITM Mad2 Course Work**.

## Setup Instructions

### Activate Python Virtual Environment
```sh
source env/bin/activate
```

### Running the Flask Server
```sh
python main.py
```

### Running Celery Workers
#### Start the Celery Worker
```sh
celery -A main:celery_app worker -l INFO
```

#### Start Celery Beat Scheduler
```sh
celery -A main:celery_app beat -l INFO
```

### Running the Vue Server
```sh
npm run dev
```

## Redis Commands
### Start Redis Server
```sh
redis-server
```

### Check Redis Status
```sh
redis-cli ping
```

### Connect to Redis CLI
```sh
redis-cli
```

### Set and Get a Key-Value Pair
```sh
SET mykey "Hello Redis"
GET mykey
```

### Flush All Data in Redis
```sh
FLUSHALL
```

### Monitor Redis Activity
```sh
redis-cli monitor
```

### Manage Redis with systemctl
#### Check Redis Status
```sh
systemctl status redis
```

#### Start Redis Service
```sh
systemctl start redis
```

#### Stop Redis Service
```sh
systemctl stop redis
```

#### Restart Redis Service
```sh
systemctl restart redis
```

#### Enable Redis to Start on Boot
```sh
systemctl enable redis
```

#### Disable Redis from Starting on Boot
```sh
systemctl disable redis
```

