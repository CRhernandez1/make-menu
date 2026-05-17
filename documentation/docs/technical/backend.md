---
title: Backend
icon: lucide/server
---

# Backend

El backend de MakeMenu está escrito en **Django** sobre Python 3.13 y expone una API REST que consume el frontend. Esta página describe la organización del código, las apps que componen el proyecto y las decisiones de diseño más importantes.

## Stack

| Capa                  | Tecnología                            |
| --------------------- | ------------------------------------- |
| Lenguaje              | Python 3.13                           |
| Framework             | Django 6.0                            |
| Gestor de dependencias | uv                                   |
| Base de datos         | SQLite (Fase 1) / PostgreSQL (futuro) |
| Cola de tareas        | django-rq sobre Redis                 |
| Email transaccional   | Brevo (SMTP)                          |
| Contenedores          | Docker + docker-compose               |

## Organización por apps

El proyecto se divide en seis aplicaciones Django con responsabilidades bien diferenciadas:

| App              | Responsabilidad                                                        |
| ---------------- | ---------------------------------------------------------------------- |
| `users`          | Autenticación, tokens de sesión, registro y perfil                     |
| `establishments` | Locales, mesas, equipo (staff) e invitaciones                          |
| `products`       | Catálogo: productos, ingredientes, categorías, alérgenos y componentes |
| `orders`         | Pedidos: ciclo de vida, líneas, estado por plato y entrada pública     |
| `menu`           | Endpoints públicos consumidos desde el QR (productos y mesas)          |
| `shared`         | Decoradores y serializadores reutilizables entre apps                  |

## Autenticación

Decidimos usar un **token UUID propio almacenado en una cookie `HttpOnly`** en lugar de JWT en `localStorage`. El JavaScript del navegador no puede leer la cookie, lo que mitiga ataques XSS. La cookie se renueva en el login y se borra en el logout.

El flujo es:

1. El cliente envía `username` y `password` a `POST /api/users/login/`.
2. El backend autentica con `authenticate()` de Django y, si es correcto, hace `Token.objects.get_or_create(user=user)`.
3. Si la petición incluye `remember_me=True`, el token se prolonga 30 días.
4. La respuesta incluye el perfil completo (para evitar una segunda llamada `GET /profile/`) y devuelve la cookie `auth_token`.

## Decoradores compartidos

Toda la lógica transversal de las vistas vive en `shared/decorators.py`:

- `require_http_methods(*methods)`: rechaza con `405` los métodos no permitidos.
- `parse_json(view)`: parsea `request.body` y deja el resultado en `request.payload`.
- `get_instance_or_404(model, field, label)`: busca una instancia por un campo (normalmente el CIF del establecimiento) y la inyecta en `request.instance`.
- `require_role(role=None)`: comprueba que el usuario tiene una entrada en la tabla `Manage` para el `request.instance` actual.

Estos decoradores se encadenan en cada vista para describir los requisitos de forma declarativa:

```python
@csrf_exempt
@require_http_methods('POST')
@auth_required
@get_instance_or_404(Establishment, 'cif', 'Establishment')
@require_role(Manage.Role.MANAGER)
@parse_json
def add_product(request, establishment_cif):
    ...
```

## App `orders`

Es la app más extensa. Maneja todo el ciclo de vida del pedido. Para evitar duplicación entre los roles, las consultas comunes se centralizan en helpers privados (`_get_est_ids_by_role`, `_list_orders_for_role`, `_advance_order`, etc.) y los endpoints públicos solo delegan en ellos pasando el rol correspondiente.

La máquina de estados de un pedido es:

```
INITIATED → IN_PROGRESS → DONE
```

Adicionalmente puede pasar a `CANCELLED` desde cualquier estado activo. Cada transición a `DONE` registra `closed_at = timezone.now()` para tener histórico de tiempos de servicio.

En la cocina, el endpoint `kitchen_toggle_item` marca un plato individual como listo. Si era el primero, el pedido pasa automáticamente de `INITIATED` a `IN_PROGRESS`; si tras marcar quedan cero pendientes, pasa a `DONE`. Esto evita que la cocina tenga que pulsar dos botones por pedido.

### Endpoint público

`create_public_order` es el único endpoint que no requiere autenticación. Lo invoca el cliente final desde el navegador después de escanear el QR. Está envuelto en `@transaction.atomic` para garantizar que el pedido y todas sus líneas se creen juntos o no se cree nada. Si algún producto del payload no está disponible, el pedido sigue adelante con los demás y la respuesta incluye `skipped_product_ids` para que el frontend pueda avisar al cliente.

## App `establishments`

Gestiona los locales, sus mesas, el equipo asignado y las invitaciones de personal.

La tabla intermedia `Manage` enlaza `User` con `Establishment` y guarda el rol del miembro (manager, waiter o kitchen) más un campo `end_date`. Eliminar a un miembro pone `end_date`, no borra la fila, para conservar el histórico de quién trabajó en cada local.

`generate_invitation` crea un `Invitation` con un UUID y un rol. El UUID viaja al frontend, que lo convierte en código QR o en un enlace `https://makemenu.../register?code=<uuid>`. `validate_invitation` se llama desde el frontend antes de pintar el formulario de registro, devolviendo el nombre del local y el rol para que el nuevo empleado sepa a qué se está uniendo.

Hay una comprobación explícita en `edit_staff` y `remove_staff` para que un manager no pueda cambiarse el rol a sí mismo ni eliminarse del equipo (se quedaría bloqueado fuera del local).

## App `products`

Contiene cuatro entidades principales (`Product`, `Category`, `Ingredient`, `Allergen`) más una tabla pivote `Component` que enlaza un producto con sus ingredientes (cantidad, unidad, si se puede quitar a petición del cliente).

`toggle_product_available` invierte el booleano `available` con un único POST, sin necesidad de pasar por el formulario completo de edición. Se usa cuando un plato se agota en cocina.

Los alérgenos siguen los 14 oficiales del **Reglamento UE 1169/2011** (gluten, lácteos, frutos secos, etc.). El endpoint `allergens_list` es público para que los formularios de ingredientes puedan listarlos sin requerir autenticación.

## App `menu`

No tiene modelos propios: actúa como fachada pública para los datos de `establishments` y `products`. Su existencia separada facilita aplicar reglas distintas (sin autenticación, filtrando solo lo disponible) sin tener que repartir condicionales por todos los endpoints privados.

## Tareas asíncronas

Las tareas que pueden tardar (envío de emails de bienvenida) se procesan fuera del ciclo request-response con **django-rq** sobre Redis. Esto permite responder al cliente HTTP inmediatamente sin esperar a que el SMTP de Brevo acepte el correo. El worker se ejecuta como un servicio separado en el `docker-compose.yml`:

```bash
uv run manage.py rqworker default
```

## Datos de prueba

Para poblar la base de datos en desarrollo se usan **factory-boy** y **Faker**. La carpeta `factories/` contiene una factoría por modelo principal, configurada con locale `es_ES` para que los datos generados (nombres, direcciones, teléfonos) tengan sentido en castellano.

`UniqueFaker` es una utilidad propia que envuelve a `factory.Faker` para garantizar valores únicos. La usamos sobre el CIF de los establecimientos, ya que `bothify` por sí solo puede generar duplicados si se llama muchas veces.

## Configuración

`backend/main/settings.py` lee la configuración sensible de variables de entorno con `python-dotenv`:

| Variable             | Uso                                                                |
| -------------------- | ------------------------------------------------------------------ |
| `SECRET_KEY`         | Clave secreta de Django                                            |
| `BREVO_SMTP_USER`    | Usuario SMTP del proveedor de email                                |
| `BREVO_SMTP_KEY`     | Clave SMTP                                                         |
| `DEFAULT_FROM_EMAIL` | Remitente de los emails transaccionales                            |
| `FRONTEND_URL`       | URL pública del frontend (se usa para construir enlaces en emails) |
| `REDIS_HOST`         | Host de Redis (para la cola de tareas)                             |

En producción `DEBUG = False` y los dominios permitidos se listan en `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` y `CSRF_TRUSTED_ORIGINS`.

Para CORS se usa `django-cors-headers` con `CORS_ALLOW_CREDENTIALS = True`, necesario para que el navegador envíe la cookie `auth_token` en peticiones cross-origin durante el desarrollo.
