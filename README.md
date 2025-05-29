This repository holds code of the part of the micro-service based application: "MsgFleet". 

## 📌 Responsibilities
This service is responsible for handling user related events. And holds base Message Model
to send queries to db.

## ⚙️ Tech-Stacks

### ⚡️ FastAPI
An Instrument to get the API requests from abroad and handle them with low-latency and
Python friendly annotation via Pydantic.

### 🧾 SqlAlchemy
A flexable ORM to integrate with internal database of the service (Used with Alembic)

### 🗄 Alembic
Migration manager to keep tables up-to-date.

### 🔁 Pydantic
An excellent type annotation and validation library. Pydantic is used to communicate
between functions and methods as this diogram shows: ```DTO -> Logic -> DTO```

### 🔧 alembic-postgresql-enum
Normalizes alembic enums working with postgresql. Alembic does not support postgresql
enums natively well.

### 📦 RabbitMQ 
A message broker which is actively used to communicate between micro-services and
It is also used as a Celery broker.

### 🗂 Redis
A low-latency NoSQL database which is used as a Cache and the Celery Backend

### 📝 Celery
An Asynchronous service which is used to concurently manage a long term tasks

Uses:
  - ```Redis``` - backend
  - ```RabbitMQ``` - Broker

### 🌐 HTTPX
A library which is used to keep communication between services due to flexibility,
support of web-socket and http2 natively.

### 📍 Poetry
A version controller wildly used to execute developer runs and tests.

## 🚀 How to run?

### 📊 Development

#### Install Python
```bash
# Update apt
sudo apt update

# Install Python
sudo apt install python3 -y
```

#### Install Poetry

```bash

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Export paths
export PATH="$HOME/.local/bin:$PATH"

# Test It!
poetry --version
# You should see something like:
# Poetry (version 2.1.2)


```

#### Install Dependencies

```bash
# Install project dependencies via Poetry
poetry install
```


#### Configure the secrets
  - Open ```/secrets/``` directory
  - write .env files. (You should see ```{name}.env.dist``` files. Create env files like: ```{name}.env```)
  - Copy .env.dist file contents
  - Write correct data in it. (Generate if required in development use.)

#### Run this
```bash
# run the project via poetry
poetry run dev
```

This will run /scripts/dev.py file under the hood.

#### Generate or find *.pem or *.key files if any error occures
```bash
#!/bin/bash

# Exit immediately on error
set -e

# Optional: Output directory
KEY_DIR="./keys"
mkdir -p "$KEY_DIR"

# Key names
PRIVATE_KEY="$KEY_DIR/private_key.pem"
PUBLIC_KEY="$KEY_DIR/public_key.pem"

# Generate 2048-bit RSA private key
openssl genpkey -algorithm RSA -out "$PRIVATE_KEY" -pkeyopt rsa_keygen_bits:2048

# Extract public key from private key
openssl rsa -pubout -in "$PRIVATE_KEY" -out "$PUBLIC_KEY"

# Output status
echo "Private key saved to: $PRIVATE_KEY"
echo "Public key saved to: $PUBLIC_KEY"
```

#### 🎉 Celebrate! You have successfully ran the code on development.

### 👥 Production
You will use ```GitHUB Actions``` or ```GitLAB CD/CD``` to run this service.
