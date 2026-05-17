---
title: Despliegue
icon: lucide/rocket
---

# Despliegue

MakeMenu se despliega con **Docker Compose** sobre un servidor Linux. El despliegue está diseñado para ser reproducible: un mismo `docker-compose.yml` arranca el backend, el worker de tareas asíncronas, Redis y el frontend con nginx.

## Arquitectura del despliegue

<div style="text-align:center;margin:1.5rem 0">
<svg viewBox="0 0 600 700" xmlns="http://www.w3.org/2000/svg" style="max-width:600px;width:100%;height:auto;font-family:system-ui,-apple-system,sans-serif">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#1a5c2e"/>
    </marker>
  </defs>

  <!-- Cliente -->
  <rect x="210" y="20" width="180" height="60" rx="10" ry="10" fill="#f0f7f0" stroke="#1a5c2e" stroke-width="2"/>
  <text x="300" y="48" text-anchor="middle" font-size="15" font-weight="700" fill="#1a1a18">Cliente final</text>
  <text x="300" y="67" text-anchor="middle" font-size="11" fill="#555">(navegador)</text>

  <!-- Arrow Cliente -> nginx -->
  <line x1="300" y1="80" x2="300" y2="135" stroke="#1a5c2e" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="320" y="113" font-size="11" fill="#555">HTTPS</text>

  <!-- nginx -->
  <rect x="210" y="145" width="180" height="60" rx="10" ry="10" fill="#f0f7f0" stroke="#1a5c2e" stroke-width="2"/>
  <text x="300" y="173" text-anchor="middle" font-size="15" font-weight="700" fill="#1a1a18">nginx</text>
  <text x="300" y="192" text-anchor="middle" font-size="11" fill="#555">(frontend)</text>

  <!-- Arrow nginx -> Django -->
  <line x1="300" y1="205" x2="300" y2="260" stroke="#1a5c2e" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="320" y="238" font-size="11" fill="#555">proxy_pass /api/</text>

  <!-- Django -->
  <rect x="210" y="270" width="180" height="60" rx="10" ry="10" fill="#f0f7f0" stroke="#1a5c2e" stroke-width="2"/>
  <text x="300" y="298" text-anchor="middle" font-size="15" font-weight="700" fill="#1a1a18">Django</text>
  <text x="300" y="317" text-anchor="middle" font-size="11" fill="#555">(backend)</text>

  <!-- Split from Django to SQLite and Redis -->
  <path d="M 300 330 L 300 370" stroke="#1a5c2e" stroke-width="2" fill="none"/>
  <path d="M 110 370 L 490 370" stroke="#1a5c2e" stroke-width="2" fill="none"/>
  <line x1="110" y1="370" x2="110" y2="425" stroke="#1a5c2e" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="490" y1="370" x2="490" y2="425" stroke="#1a5c2e" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- SQLite -->
  <rect x="20" y="435" width="180" height="60" rx="10" ry="10" fill="#f0f7f0" stroke="#1a5c2e" stroke-width="2"/>
  <text x="110" y="463" text-anchor="middle" font-size="15" font-weight="700" fill="#1a1a18">SQLite</text>
  <text x="110" y="482" text-anchor="middle" font-size="11" fill="#555">(volumen)</text>

  <!-- Redis -->
  <rect x="400" y="435" width="180" height="60" rx="10" ry="10" fill="#f0f7f0" stroke="#1a5c2e" stroke-width="2"/>
  <text x="490" y="463" text-anchor="middle" font-size="15" font-weight="700" fill="#1a1a18">Redis</text>
  <text x="490" y="482" text-anchor="middle" font-size="11" fill="#555">(cola RQ)</text>

  <!-- Arrow Redis -> RQ worker -->
  <line x1="490" y1="495" x2="490" y2="550" stroke="#1a5c2e" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- RQ worker -->
  <rect x="400" y="560" width="180" height="60" rx="10" ry="10" fill="#f0f7f0" stroke="#1a5c2e" stroke-width="2"/>
  <text x="490" y="588" text-anchor="middle" font-size="15" font-weight="700" fill="#1a1a18">RQ worker</text>
  <text x="490" y="607" text-anchor="middle" font-size="11" fill="#555">(envío de emails)</text>
</svg>
</div>

## Servicios del `docker-compose.yml`

### `backend`

Imagen construida desde `./backend/Dockerfile`. Arranca Django con el comando por defecto definido en el Dockerfile. Expone el puerto 8000 internamente (no se publica al host: el tráfico entra siempre a través de nginx).

Variables de entorno relevantes:

| Variable                | Origen                                 |
| ----------------------- | -------------------------------------- |
| `DEBUG`                 | `False` en producción                  |
| `DJANGO_ALLOWED_HOSTS`  | Dominio + IP del servidor              |
| `SECRET_KEY`            | Variable `.env` del host               |
| `BREVO_SMTP_USER`       | Variable `.env` del host               |
| `BREVO_SMTP_KEY`        | Variable `.env` del host               |
| `REDIS_HOST`            | `redis` (hostname del servicio Docker) |

Volúmenes:

- `./backend/media:/app/media` — uploads de imágenes de producto.
- `./backend/db.sqlite3:/app/db.sqlite3` — base de datos persistente.
- `static_volume:/app/staticfiles` — estáticos generados por `collectstatic`, compartidos con nginx.

### `worker`

Misma imagen que el backend, pero ejecuta `uv run manage.py rqworker default` en lugar del servidor web. Procesa las tareas encoladas (envío de emails) sin bloquear el ciclo request-response del backend.

### `redis`

Imagen oficial `redis:alpine`. Solo se usa internamente para la cola de tareas, no se expone al host.

### `frontend`

Imagen construida desde `./frontend/Dockerfile`. El build de Vite produce `dist/`, que se sirve con **nginx**. La configuración de nginx (`./frontend/nginx.conf`) hace dos cosas:

1. Sirve los estáticos del SPA y devuelve `index.html` para rutas no encontradas (SPA fallback).
2. Hace `proxy_pass` de `/api/` al servicio `backend:8000`.

El frontend monta los mismos volúmenes que el backend para acceder a `staticfiles` y `media` (las imágenes de productos cargadas en `media/` deben ser accesibles directamente vía nginx).

Publica el puerto `80` del host.

## Variables sensibles

El `.env` del host (no commiteado) contiene:

```
SECRET_KEY=<clave_django>
BREVO_SMTP_USER=<usuario_brevo>
BREVO_SMTP_KEY=<clave_brevo>
DEFAULT_FROM_EMAIL=MakeMenu <no-reply@makemenu.es>
FRONTEND_URL=https://makemenu.arkania.es
```

## Script `deploy.sh`

El despliegue completo se ejecuta con un único script en la raíz del repositorio:

```bash
#!/bin/bash
set -e

git pull origin main
docker compose down
docker compose up --build -d
docker compose exec backend uv run manage.py migrate --noinput
docker compose exec backend uv run manage.py collectstatic --noinput
cp backend/db.sqlite3 backend/db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)
echo "Despliegue completado"
```

El flujo es:

1. Trae los últimos cambios de `main`.
2. Para los contenedores existentes.
3. Reconstruye las imágenes (`--build`) y arranca en segundo plano (`-d`).
4. Aplica migraciones pendientes.
5. Recopila los estáticos de Django en el volumen compartido.
6. Hace una copia de seguridad de la base de datos con timestamp.

Los archivos `db.sqlite3.backup.*` están en el `.gitignore` para que no acaben en el repositorio.

## Despliegue inicial en un servidor nuevo

1. Instalar Docker y Docker Compose.
2. Clonar el repositorio: `git clone <repo> /opt/makemenu && cd /opt/makemenu`.
3. Crear el archivo `.env` con las variables sensibles (ver sección anterior).
4. Crear el archivo `backend/.env` con las mismas variables (lo lee Django con `python-dotenv`).
5. Ejecutar `./deploy.sh`.
6. Crear un superusuario para acceder al admin: `docker compose exec backend uv run manage.py createsuperuser`.

## Actualización del entorno

Para aplicar cambios después del despliegue inicial basta con volver a ejecutar `./deploy.sh`. Si los cambios incluyen nuevas variables de entorno, hay que actualizar el `.env` antes de relanzar.

## Comprobaciones post-despliegue

Después de cada despliegue conviene comprobar:

- `curl https://makemenu.arkania.es/api/users/profile/` devuelve `401` (la cookie no llega, comportamiento esperado).
- El login funciona desde un navegador.
- El worker está corriendo: `docker compose logs worker --tail 20`.
- Las migraciones están al día: `docker compose exec backend uv run manage.py showmigrations`.

## Backups

El script `deploy.sh` crea un backup automático de la base de datos con cada despliegue. Para retener solo los últimos N backups y evitar que crezca indefinidamente, en producción tenemos una tarea cron semanal:

```cron
0 3 * * 0  find /opt/makemenu/backend -name 'db.sqlite3.backup.*' -mtime +30 -delete
```

Para una migración futura a PostgreSQL, este flujo de backups se sustituiría por `pg_dump` programado.
