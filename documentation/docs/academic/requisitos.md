---
title: Requisitos
icon: lucide/clipboard-list
---

# Requisitos del sistema

## Requisitos funcionales

Los requisitos funcionales se agrupan por módulo. Cada uno se identifica con un código `RF-xx`.

### Autenticación y registro

| Código  | Descripción                                                                                                          |
| ------- | -------------------------------------------------------------------------------------------------------------------- |
| RF-01   | El sistema permitirá a los usuarios registrados iniciar sesión con usuario y contraseña.                             |
| RF-02   | El sistema mantendrá la sesión del usuario mediante una cookie `HttpOnly` que el navegador enviará automáticamente.  |
| RF-03   | El sistema permitirá al usuario elegir entre sesión normal (caduca al cerrar el navegador) o "recordarme" (30 días). |
| RF-04   | El sistema permitirá cerrar sesión, borrando el token en el backend y la cookie en el cliente.                       |
| RF-05   | El registro de nuevo personal solo será posible mediante una invitación generada por un manager.                     |
| RF-06   | La invitación caducará tras su primer uso.                                                                           |
| RF-07   | El frontend validará el formato del código de invitación (UUID) antes de pintar el formulario de registro.           |

### Gestión de establecimientos

| Código  | Descripción                                                                                              |
| ------- | -------------------------------------------------------------------------------------------------------- |
| RF-10   | Un usuario podrá crear nuevos establecimientos, quedando automáticamente asignado como manager.          |
| RF-11   | Un manager podrá editar los datos de su establecimiento (nombre, dirección, CIF, descripción, teléfono). |
| RF-12   | Un manager podrá abrir o cerrar su establecimiento al público con un único clic.                         |
| RF-13   | Un manager podrá eliminar un establecimiento, previa confirmación.                                       |
| RF-14   | Un manager podrá gestionar varios establecimientos desde la misma cuenta y cambiar entre ellos.          |

### Gestión de mesas

| Código  | Descripción                                                                                       |
| ------- | ------------------------------------------------------------------------------------------------- |
| RF-20   | El manager podrá crear, editar y eliminar mesas indicando número y aforo máximo.                  |
| RF-21   | El sistema impedirá crear dos mesas con el mismo número en un mismo establecimiento.              |
| RF-22   | El manager podrá marcar una mesa como activa o inactiva (fuera de servicio).                      |
| RF-23   | El sistema generará un código QR único por mesa con un enlace al menú público y la mesa cargados. |

### Gestión del equipo

| Código  | Descripción                                                                                                    |
| ------- | -------------------------------------------------------------------------------------------------------------- |
| RF-30   | El manager podrá listar a todo el personal de su establecimiento con su rol activo.                            |
| RF-31   | El manager podrá cambiar el rol de un miembro entre camarero y cocinero.                                       |
| RF-32   | El manager podrá eliminar a un miembro del equipo (el sistema lo marca como cerrado pero conserva histórico).  |
| RF-33   | El manager podrá generar invitaciones especificando el rol y, si gestiona varios locales, el establecimiento.  |
| RF-34   | El sistema impedirá que un manager se elimine a sí mismo o cambie su propio rol.                               |

### Catálogo

| Código  | Descripción                                                                                                          |
| ------- | -------------------------------------------------------------------------------------------------------------------- |
| RF-40   | El manager podrá crear, editar y eliminar productos con nombre, descripción, precio, categoría e imagen.             |
| RF-41   | El manager podrá marcar un producto como disponible o agotado con un solo clic.                                      |
| RF-42   | El manager podrá crear, editar y eliminar categorías para organizar la carta.                                        |
| RF-43   | El manager podrá crear, editar y eliminar ingredientes asociándoles uno o varios alérgenos.                          |
| RF-44   | El sistema calculará automáticamente los alérgenos de cada producto en base a los ingredientes que lo componen.      |
| RF-45   | El manager podrá definir la receta de un producto (componentes) indicando cantidad, unidad y si es retirable.        |
| RF-46   | El sistema mantendrá la lista oficial de los 14 alérgenos del Reglamento UE 1169/2011 como datos maestros.           |

### Pedidos: cliente final

| Código  | Descripción                                                                                                       |
| ------- | ----------------------------------------------------------------------------------------------------------------- |
| RF-50   | El cliente podrá acceder a la carta del establecimiento sin autenticarse, escaneando el código QR de la mesa.     |
| RF-51   | El cliente podrá navegar por las categorías y ver los productos disponibles con su precio y alérgenos.            |
| RF-52   | El cliente podrá añadir productos al carrito con la cantidad y notas que desee.                                   |
| RF-53   | El cliente podrá enviar el pedido a la cocina, recibiendo confirmación con el número de pedido.                   |
| RF-54   | El sistema avisará si algún producto se ha agotado entre que se añadió al carrito y se envió el pedido.           |

### Pedidos: camarero

| Código  | Descripción                                                                                                          |
| ------- | -------------------------------------------------------------------------------------------------------------------- |
| RF-60   | El camarero podrá ver todas las mesas de su establecimiento con su estado actual (libre/pendiente/en progreso/listo). |
| RF-61   | El camarero recibirá una notificación visual y sonora cuando entre un pedido nuevo.                                  |
| RF-62   | El camarero podrá ver el ticket detallado de cualquier mesa.                                                         |
| RF-63   | El camarero podrá avanzar manualmente el estado de un pedido.                                                        |
| RF-64   | El camarero podrá cancelar un pedido activo (con confirmación).                                                      |
| RF-65   | El camarero podrá cerrar la mesa marcándola como pagada y finalizada.                                                |
| RF-66   | El camarero podrá consultar el histórico de pedidos con filtros por antigüedad.                                      |

### Pedidos: cocina

| Código  | Descripción                                                                                                 |
| ------- | ----------------------------------------------------------------------------------------------------------- |
| RF-70   | El cocinero verá todos los pedidos activos (iniciados o en progreso) ordenados por antigüedad.              |
| RF-71   | Cada pedido mostrará una barra de progreso con `ready_count / total_count` platos preparados.               |
| RF-72   | El cocinero podrá marcar y desmarcar cada plato como listo individualmente.                                 |
| RF-73   | Al marcar el primer plato, el pedido pasará automáticamente de Iniciado a En progreso.                      |
| RF-74   | Al marcar todos los platos, el pedido pasará automáticamente a Listo y desaparecerá de la cola.             |
| RF-75   | El cocinero podrá completar el pedido entero de una sola vez con un botón "Completar todo".                 |

## Requisitos no funcionales

| Código   | Categoría        | Descripción                                                                                                                                          |
| -------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| RNF-01   | Rendimiento      | Los listados de pedidos responderán en menos de 300 ms con hasta 500 pedidos en histórico.                                                           |
| RNF-02   | Rendimiento      | Las consultas a base de datos evitarán el problema N+1 mediante `select_related` y `prefetch_related`.                                               |
| RNF-03   | Seguridad        | El token de sesión vivirá únicamente en una cookie `HttpOnly` inaccesible para JavaScript.                                                           |
| RNF-04   | Seguridad        | Cada endpoint autenticado validará el rol del usuario contra el establecimiento solicitado.                                                          |
| RNF-05   | Seguridad        | Las contraseñas se almacenarán hasheadas con el mecanismo por defecto de Django (PBKDF2 + SHA256 + salt).                                            |
| RNF-06   | Seguridad        | Los datos personales se tratarán conforme al RGPD: minimización de datos, derecho al olvido, base legal documentada.                                 |
| RNF-07   | Usabilidad       | El interfaz será responsive y funcionará correctamente en móvil (cliente), tablet (camarero/cocina) y escritorio (manager).                          |
| RNF-08   | Usabilidad       | Las acciones críticas (eliminar producto, cancelar pedido) requerirán confirmación.                                                                  |
| RNF-09   | Compatibilidad   | Compatible con las dos últimas versiones mayores de Chrome, Safari, Firefox y Edge.                                                                  |
| RNF-10   | Compatibilidad   | No requerirá instalar ninguna aplicación nativa en ningún dispositivo.                                                                               |
| RNF-11   | Mantenibilidad   | El código seguirá las convenciones idiomáticas de cada framework (Django para backend, Vue 3 + Composition API para frontend).                       |
| RNF-12   | Mantenibilidad   | Cada módulo del frontend será autocontenido para facilitar cambios y refactorizaciones.                                                              |
| RNF-13   | Mantenibilidad   | El backend usará decoradores apilables para centralizar la lógica transversal (autenticación, roles, validación de método HTTP).                     |
| RNF-14   | Despliegue       | El sistema se desplegará con `docker compose up` desde un único `docker-compose.yml` y un script `deploy.sh`.                                        |
| RNF-15   | Despliegue       | Las variables sensibles vivirán fuera del repositorio (en `.env` no commiteado).                                                                     |
| RNF-16   | Disponibilidad   | El sistema tolerará caídas temporales del servicio SMTP de email sin bloquear el resto de funcionalidad (cola asíncrona con `django-rq`).            |
| RNF-17   | Cumplimiento     | La aplicación cumplirá con el Reglamento UE 1169/2011 mostrando los alérgenos de cada producto al cliente.                                            |
