# Documentación técnica del backend

Esta documentación describe la arquitectura interna del backend de MakeMenu, escrito en Django sobre Python 3.13. Está organizada por apps siguiendo la misma estructura del repositorio (`orders`, `users`, `establishments`, `products`, `menu`, `shared`). El objetivo es que cualquier desarrollador que llegue por primera vez al proyecto pueda situar rápidamente qué hace cada módulo y por qué se tomaron determinadas decisiones de diseño.

## Visión general de la arquitectura

El proyecto se organiza en **seis aplicaciones Django** con responsabilidades bien diferenciadas:

| App              | Responsabilidad                                                        |
| ---------------- | ---------------------------------------------------------------------- |
| `users`          | Autenticación, tokens de sesión, registro y perfil                     |
| `establishments` | Locales, mesas, equipo (staff) e invitaciones                          |
| `products`       | Catálogo: productos, ingredientes, categorías, alérgenos y componentes |
| `orders`         | Pedidos: ciclo de vida, líneas, estado por plato y entrada pública     |
| `menu`           | Endpoints públicos consumidos desde el QR (productos y mesas)          |
| `shared`         | Decoradores y serializadores reutilizables entre apps                  |

La API es REST, sirve JSON y se consume desde el frontend Vue 3 mediante Axios. La autenticación se basa en un token UUID propio almacenado en una **cookie HttpOnly** para mitigar XSS (el JavaScript del navegador no puede leerla). Decidimos no usar JWT porque, al ser una aplicación que se sirve desde el mismo dominio que el frontend en producción, una cookie de sesión cumple el mismo papel sin la complejidad de manejar refresh tokens.

## Decoradores compartidos (`shared/decorators.py`)

Toda la lógica transversal de las vistas vive en `shared/decorators.py`. Esto evita repetir validaciones en cada endpoint y mantiene las vistas centradas en la lógica de negocio.

- `require_http_methods(*methods)`: rechaza con `405 Method not allowed` cualquier petición cuyo método HTTP no esté en la lista permitida.
- `parse_json(view)`: intenta parsear `request.body` como JSON y lo deja accesible en `request.payload`. Si el JSON no es válido, devuelve `400`.
- `get_instance_or_404(model, field, label)`: busca una instancia del modelo por un campo (típicamente el `cif` del establecimiento) y la inyecta en `request.instance`. Si no la encuentra devuelve `404`.
- `require_role(role=None)`: comprueba que el usuario tenga una entrada en la tabla `Manage` para el `request.instance` actual. Si se pasa un rol concreto (por ejemplo `Manage.Role.MANAGER`), exige que coincida.

Estos decoradores se encadenan para describir los requisitos de cada endpoint de forma declarativa. Un patrón habitual en la app `products` es:

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

El orden importa: `auth_required` debe ir antes que `require_role` porque este último necesita un `request.user` válido.

---

## App `orders`

Es la app más extensa del backend. Maneja todo el flujo de un pedido: desde que un cliente lo crea escaneando el QR hasta que el camarero cierra la mesa. Para evitar duplicación entre vistas de manager, camarero y cocina, las operaciones comunes se centralizan en helpers privados (con guion bajo) y los endpoints públicos solo delegan en ellos pasando el rol correspondiente.

### Helpers privados

Las funciones `_get_est_ids_by_role`, `_get_primary_establishment`, `_list_orders_for_role`, `_get_order_details_for_role`, `_advance_order` y `_get_active_order_for_table` concentran las consultas y la lógica de seguridad multi-tenant.

`_get_est_ids_by_role(user, role)` devuelve la lista plana de IDs de establecimientos donde el usuario ejerce el rol indicado:

```python
return list(
    user.manages.filter(role=role, end_date__isnull=True).values_list(
        'establishment_id', flat=True
    )
)
```

Se usa `values_list('establishment_id', flat=True)` en lugar de `filter(...).all()` para traer únicamente la columna que necesitamos. En un manager que gestione varios locales puede suponer una diferencia notable de memoria. El `flat=True` aplana la salida a `[1, 2, 3]` en lugar de `[(1,), (2,), (3,)]`, lo que la hace directamente compatible con un lookup `__in` de Django.

`_list_orders_for_role(request, role)` es el núcleo del listado de pedidos. Construye el queryset base filtrando por los establecimientos permitidos y aplica `select_related('table', 'establishment')` para resolver el problema N+1 al serializar. A continuación procesa dos parámetros opcionales: `establishment_id` (para filtrar a un solo local cuando el manager tiene varios) y `days` (para limitar el histórico a las últimas N jornadas). Sobre el parámetro `establishment_id` siempre se comprueba que el valor recibido esté en la lista de IDs permitidos del usuario, evitando que alguien manipule la URL para acceder a pedidos de otro local.

`_advance_order(request, order_id, role)` centraliza la máquina de estados:

```
INITIATED → IN_PROGRESS → DONE
```

Si el pedido está en otro estado (ya cerrado, cancelado…) devuelve `400 Bad Request`. Cuando pasa a `DONE`, también guarda `closed_at = timezone.now()` para tener histórico de tiempos de servicio.

### Vistas públicas: manager, waiter y kitchen

Sobre los helpers anteriores se montan los endpoints visibles. La mayoría son una sola línea que delega:

```python
@require_http_methods('GET')
@auth_required
def list_manager_orders(request) -> JsonResponse:
    return _list_orders_for_role(request, 'manager')
```

Los endpoints específicos de cada rol añaden lógica propia:

- **`waiter_tables`**: lista todas las mesas activas del local del camarero. Para evitar el N+1 al cruzar mesas con su pedido activo, hace una sola consulta `Order.objects.filter(...).annotate(items_count=Count('details'))` y luego construye un diccionario `{table_id: order}` en memoria. Cada mesa se resuelve después en O(1).
- **`waiter_table_order`**: devuelve el ticket completo de una mesa concreta. Usa `prefetch_related(Prefetch('details', queryset=OrderDetail.objects.select_related('product')))` para precargar productos en una sola consulta extra.
- **`waiter_close_table`**: cierra la mesa marcando el pedido como `paid=True`, `status=DONE` y guardando `closed_at`. No se permite "reabrir" la mesa una vez cerrada.
- **`kitchen_active_orders`**: devuelve los pedidos en estado `INITIATED` o `IN_PROGRESS`. Para cada pedido calcula `ready_count` y `total_count` para que la vista de cocina pueda pintar una barra de progreso por ticket.
- **`kitchen_toggle_item`**: marca un plato individual como listo o lo devuelve a pendiente. Cada toggle puede provocar un cambio de estado automático del pedido completo: si era `INITIATED` y se marca el primer plato, pasa a `IN_PROGRESS`; si tras marcar quedan cero pendientes, pasa a `DONE`. Esto evita que la cocina tenga que pulsar dos botones por pedido.
- **`kitchen_complete_order`**: completa el pedido entero de una vez. Usa `order.details.filter(ready=False).update(ready=True)` en lugar de un bucle con `.save()` para hacerlo en una única consulta SQL.

### Endpoint público: `create_public_order`

Es el único endpoint de `orders` que no requiere autenticación, ya que lo invoca el cliente final desde el navegador después de escanear el QR. Está envuelto en `@transaction.atomic` para garantizar que el pedido y todas sus líneas se creen juntos o no se cree nada.

El flujo es:

1. Localiza el establecimiento por su CIF (404 si no existe).
2. Valida que el payload incluya `table` e `items`.
3. Recorre los items y comprueba uno a uno que el producto exista en el establecimiento y siga disponible. Los que no cumplan se acumulan en `invalid_ids` para devolverlos al final.
4. Si al menos un item es válido, crea el `Order` y todas las líneas con `OrderDetail.objects.bulk_create(...)` (una sola consulta INSERT en lugar de N).
5. Devuelve `201` con `order_id` y, si los hubo, la lista de `skipped_product_ids` para que el frontend pueda avisar al cliente.

### URLs (`orders/urls.py`)

Las rutas se agrupan por rol:

- **Manager**: `manager-orders/` y `manager-orders/<order_id>/details/`.
- **Waiter**: `waiter-orders/`, `waiter/tables/`, `waiter/tables/<table_num>/order/`, `waiter/tables/<table_num>/close/`, `waiter/orders/<order_id>/advance/`, `waiter/orders/<order_id>/cancel/`.
- **Kitchen**: `kitchen/orders/`, `kitchen/orders/<order_id>/advance/`, `kitchen/orders/<order_id>/complete/`, `kitchen/items/<item_id>/toggle/`.
- **Público**: `public/<establishment_cif>/`.

---

## App `users`

Maneja autenticación, registro mediante invitación y perfil. El modelo `Member` extiende al `User` de Django con campos extra (teléfono, avatar, etc.), y el modelo `Token` guarda un UUID por usuario que sirve como clave de sesión.

### Login

`login(request)` recibe `username` y `password`, autentica con `authenticate()` de Django y, si el usuario es válido, hace `Token.objects.get_or_create(user=user)` para obtener o crear su token. Si la petición incluye `remember_me=True`, el token se prolonga 30 días; si no, se trata como cookie de sesión.

La respuesta incluye dos cosas:

1. El perfil completo del usuario serializado con `MemberSerializer` (rol, nombre, email, avatar…). Esto evita una segunda llamada `GET /profile/` justo después del login.
2. Una cookie `auth_token` con `httponly=True` y `samesite='Lax'`. Decidimos guardar el token en cookie en lugar de devolverlo en el body porque así el frontend nunca tiene que tocarlo: Axios la envía automáticamente con `withCredentials: true`.

### Registro con invitación

`register(request)` solo deja registrarse a usuarios que vienen con un `invitation_id` válido. El flujo es:

1. Valida que estén presentes todos los campos obligatorios.
2. Busca la invitación con `Invitation.objects.get(id=invitation_id, is_used=False)`. Si no existe o ya se usó, devuelve `400`.
3. Crea el `User` con `User.objects.create_user(...)` (que ya encripta la contraseña).
4. Crea la relación `Manage` para vincular al nuevo usuario con el establecimiento y rol de la invitación.
5. Marca la invitación como `is_used=True` para que no pueda reciclarse.

Toda la función está envuelta en `@transaction.atomic`, así que si falla cualquier paso intermedio (por ejemplo, un username duplicado), la BD queda como estaba.

### Logout y perfil

`logout(request)` borra el token del usuario y elimina la cookie del navegador con `response.delete_cookie('auth_token')`. `profile(request)` simplemente devuelve el perfil del usuario autenticado (usa `@auth_required`, así que si no hay sesión devuelve `401` automáticamente).

### Tarea asíncrona: envío de email de bienvenida

El registro de un manager por parte del equipo de MakeMenu desencadena el envío de un email con sus credenciales. Para no bloquear la respuesta HTTP, esta tarea se encola en `django-rq` y la procesa un worker en segundo plano (`backend/users/tasks.py::send_manager_email_task`). El email se envía vía Brevo (SMTP) y la URL del frontend se lee de `settings.FRONTEND_URL` para no hardcodear `localhost:5173`.

### URLs

- `login/`, `logout/`, `register/`, `profile/`.

---

## App `establishments`

Gestiona los locales, sus mesas, el equipo asignado y las invitaciones de personal.

### Modelos relevantes

- `Establishment`: nombre, CIF, dirección, teléfono, descripción, `opened` (si recibe pedidos).
- `Manage`: tabla intermedia entre `User` y `Establishment` con un campo `role` (manager, waiter, kitchen) y `end_date`. Borrar a un miembro pone `end_date`, no elimina la fila, para conservar histórico.
- `Table`: número, número máximo de comensales, flag `active`.
- `Invitation`: UUID, establecimiento, rol, `is_used`, `created_by`, `expires_at`.

### Gestión del local

Los endpoints `establishments_list`, `establishment_detail`, `add_establishment`, `edit_establishment`, `delete_establishment` y `toggle_establishment` cubren el CRUD habitual más un endpoint específico para abrir/cerrar el local (`opened = not opened`) sin tener que ir al formulario completo de edición.

Cuando un usuario crea un nuevo local con `add_establishment`, automáticamente se le asigna como `MANAGER` del mismo creando una entrada en `Manage`. Es la única vista de la app que no requiere el decorador `@require_role(MANAGER)`, porque obviamente todavía no lo es.

### Gestión de mesas

`add_table` valida que no exista ya otra mesa con ese número en el mismo local. Si existe, devuelve `409 Conflict` en lugar de `400` para que el frontend pueda distinguir el caso de un duplicado del de un payload inválido.

`change_table_status` invierte el booleano `active`. Se usa para sacar mesas temporalmente de servicio (reparación, reserva especial…) sin tener que borrarlas.

### Staff e invitaciones

`staff_list`, `edit_staff` y `remove_staff` operan sobre la tabla `Manage`. En `edit_staff` y `remove_staff` hay una comprobación explícita para que el manager **no pueda cambiarse el rol a sí mismo ni eliminarse** del equipo. Si lo hiciera, podría bloquearse fuera del propio local.

`generate_invitation` crea un `Invitation` con un UUID y un rol (waiter o kitchen). Si el manager gestiona varios locales puede pasar `establishment_id` en el body para elegir a cuál pertenece la invitación; si no, se usa el primero. El UUID se devuelve al frontend, que lo usa para generar un código QR o un enlace `https://makemenu.../register?code=<uuid>`.

`validate_invitation` se llama desde el frontend antes de pintar el formulario de registro. Devuelve el nombre del local y el rol para que el nuevo empleado vea a qué establecimiento se está uniendo.

### URLs

- Base: `establishments/`, `establishments/add/`.
- Invitaciones: `invite/`, `invite/validate/<uuid>/`.
- Operaciones por local: `/<cif>/`, `/<cif>/edit/`, `/<cif>/toggle/`, `/<cif>/delete/`.
- Mesas: `/<cif>/tables/...`.
- Staff: `/<cif>/staff/...`.
- Productos: anidados bajo `/<cif>/products/...` (delegando en `products.urls`).

---

## App `products`

Es el catálogo del local. Tiene cuatro entidades principales: `Product`, `Category`, `Ingredient`, `Allergen`, más una tabla pivote `Component` que enlaza un producto con sus ingredientes (cantidad, unidad, si se puede quitar a petición del cliente).

### Productos

CRUD estándar (`products_list`, `product_detail`, `add_product`, `edit_product`, `delete_product`) más dos endpoints específicos:

- `upload_product_image`: recibe la imagen en `request.FILES['product_image']`, la guarda en `media/` y devuelve la URL absoluta con `request.build_absolute_uri()` para que el frontend la pueda pintar directamente.
- `toggle_product_available`: invierte el booleano `available`. Se usa cuando se agota un plato en cocina sin tener que borrarlo del catálogo.

En `delete_product` se borran primero los `Component` asociados antes que el propio producto. Aunque la `ForeignKey` ya tiene `on_delete=CASCADE`, lo hacemos explícito para tener control sobre el orden y poder añadir lógica futura (por ejemplo, conservar histórico de recetas).

### Ingredientes, categorías y alérgenos

Todos siguen el mismo patrón CRUD que productos. La particularidad de los ingredientes es la relación ManyToMany con alérgenos: al crear o editar un ingrediente, si el payload incluye `allergens` (una lista de IDs), se aplica con `ingredient.allergens.set(request.payload['allergens'])`, que añade y quita en una sola operación.

`allergens_list` es el único endpoint público de la app (sin `@auth_required`). Devuelve la lista maestra de alérgenos del sistema (los 14 oficiales del Reglamento UE 1169/2011: gluten, lácteos, frutos secos, etc.) para que los formularios de ingredientes los puedan mostrar.

### Componentes

`components_list`, `add_component` y `delete_component` gestionan las recetas. `components_list` usa `select_related('ingredient')` para traer el nombre del ingrediente en la misma consulta, evitando un N+1 al iterar.

### URLs

- Productos: `/`, `/add/`, `/<id>/`, `/<id>/edit/`, `/<id>/delete/`, `/<id>/image/`, `/<id>/toggle/`.
- Categorías: `/categories/...`.
- Ingredientes: `/ingredients/...`.
- Componentes: anidados como `/<product_id>/components/...`.

---

## App `menu`

Esta app no tiene modelos propios: actúa como fachada pública para los datos de `establishments` y `products`. Su existencia separada del resto facilita aplicar reglas distintas (sin autenticación, con filtros más restrictivos) sin tener que repartir condicionales por los endpoints privados.

- `public_tables(request, establishment_cif)`: devuelve las mesas del local filtradas por `active=True`. Si el establecimiento no existe, devuelve `404`.
- `public_products(request, establishment_cif)`: devuelve el catálogo con `available=True`. Se pasa el `request` al serializer para que pueda construir URLs absolutas de las imágenes (`request.build_absolute_uri(product.product_image.url)`).

Las URLs son `/<cif>/tables/` y `/<cif>/products/`.

---

## Settings y configuración

`backend/main/settings.py` lee la configuración sensible de variables de entorno con `python-dotenv`:

- `SECRET_KEY`: clave secreta de Django.
- `BREVO_SMTP_USER` y `BREVO_SMTP_KEY`: credenciales del proveedor de email.
- `DEFAULT_FROM_EMAIL`: remitente de los emails transaccionales.
- `FRONTEND_URL`: URL pública del frontend (se usa para construir enlaces en los emails).
- `REDIS_HOST`: host de Redis (usado por `django-rq` para la cola de tareas).

`DEBUG = False` en producción. `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` y `CSRF_TRUSTED_ORIGINS` contienen los dominios donde se sirve la aplicación.

Para CORS se usa `django-cors-headers` con `CORS_ALLOW_CREDENTIALS = True`, necesario para que el navegador envíe la cookie `auth_token` en peticiones cross-origin desde el frontend en desarrollo.

---

## Tareas asíncronas con `django-rq`

Las tareas que pueden tardar (envío de emails de bienvenida, generación de PDFs en el futuro) se procesan fuera del ciclo request-response usando `django-rq` sobre Redis. Esto permite responder al cliente HTTP inmediatamente sin esperar a que Brevo acepte el correo.

La cola se ejecuta con `uv run manage.py rqworker default`, que en producción corre como un servicio separado dentro del `docker-compose.yml`.

---

## Datos de prueba: `factories/` y `fixtures/`

Para poblar la base de datos en desarrollo se usan `factory-boy` y `faker`. La carpeta `factories/` contiene una factoría por modelo principal (`EstablishmentFactory`, `UserFactory`, `OrderFactory`, etc.) configuradas con locale `es_ES` para que los datos generados (nombres, direcciones, teléfonos) tengan sentido en castellano.

`UniqueFaker` es una utilidad propia (`factories/extras.py`) que envuelve a `factory.Faker` para garantizar valores únicos. La usamos sobre el CIF de los establecimientos, ya que `factory.Faker('bothify')` por sí solo puede generar duplicados si se llama muchas veces.

La carpeta `fixtures/` contiene snapshots JSON con datos coherentes (alérgenos oficiales, plantillas de cartas) que se cargan con `manage.py loaddata`.

---

## Comandos de desarrollo

El proyecto usa `uv` como gestor de dependencias y un `justfile` con los comandos más comunes:

```
just dev       # arranca el servidor de desarrollo
just migrate   # aplica migraciones
just shell     # abre el shell de Django
just seed      # carga fixtures + ejecuta factories
just worker    # arranca el worker de django-rq
```

---

## Decisiones técnicas resumidas

| Decisión                                                         | Motivo                                                                                                                                |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Token UUID en cookie `HttpOnly` en lugar de JWT en `localStorage` | Mitigación XSS. El JS nunca toca el token.                                                                                            |
| Decoradores apilables (`@auth_required`, `@require_role`, etc.)   | Mantiene las vistas legibles y evita repetir validaciones.                                                                            |
| App `menu` separada con endpoints públicos                       | Aísla las reglas "público vs autenticado" en lugar de mezclarlas en cada vista.                                                       |
| `select_related` y `prefetch_related` en listados de pedidos     | Resuelve el problema N+1 al serializar mesas, pedidos y productos en un solo viaje a la base de datos.                                |
| Borrado lógico de `Manage` con `end_date`                        | Conserva histórico de quién trabajó en cada local. Los listados activos filtran por `end_date__isnull=True`.                          |
| `django-rq` para emails                                          | No bloquear la respuesta HTTP cuando el SMTP tarda. Se monta una cola simple sin tener que añadir Celery (que sería sobreingeniería). |
| SQLite en producción de Fase 1                                   | Tamaño esperado de la BD pequeño durante el piloto. Migración prevista a PostgreSQL cuando se supere el umbral de un local activo.    |
