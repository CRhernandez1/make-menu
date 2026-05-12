# Documentación técnica del Frontend

Esta documentación tiene como objetivo explicar detalladamente la estructura, el funcionamiento y la lógica de negocio implementada en el frontend de la aplicación. Está desarrollado con **Vue 3** (Composition API), **Pinia** (gestión de estado global), **Vue Router** (enrutamiento) y **Axios** (cliente HTTP).

## Arquitectura Modular

El proyecto sigue una arquitectura **basada en funcionalidades (Feature-Driven Architecture)**. En lugar de agrupar todos los archivos por su tipo técnico (por ejemplo, todos los stores juntos, todas las vistas juntas), el código se organiza por **módulo de dominio**. Todo el código principal reside en `src/`.

### Directorios principales

- `src/api/`: Contiene la configuración global de Axios. `makeMenu.ts` crea una instancia base (`makeMenuApi`) que incluye `withCredentials: true`. Esto es vital: asegura que todas las peticiones envíen y reciban automáticamente las cookies, permitiendo el sistema de seguridad basado en cookies `HttpOnly` gestionado por el backend.
- `src/router/`: Configuración central de Vue Router, incluyendo rutas y _Guards_ de protección de acceso.
- `src/stores/`: Almacenes de estado globales genéricos (como `counter.ts`).
- `src/modules/`: El corazón de la aplicación. Contiene los módulos de dominio encapsulados (`auth`, `kitchen`, `landing`, `manager`, `menu`, `waiter`). Cada módulo es auto-contenido y define sus propias vistas, stores, layouts y acciones.

---

## Router y Guards (Enrutamiento y Seguridad)

El archivo `src/router/index.ts` define las URLs de la aplicación frontend y gestiona el control de acceso a las diferentes vistas mediante "Navigation Guards".

### Guards de Seguridad

#### Guard Global (`beforeEach`)

Protege todas las rutas de la aplicación por defecto, exceptuando un listado específico declarado en `PUBLIC_ROUTES` (como `home`, `login`, `register`, `public-menu`).

- **Lógica de Verificación**: Comprueba si el usuario está autenticado verificando el `authStatus` en el `useAuthStore()`. Si el estado es `Checking` (por ejemplo, al recargar la página), invoca a `authStore.checkAuthStatus()` para preguntar al backend si la cookie de sesión sigue siendo válida.
- **Redirección Segura**: Si el usuario no está autenticado y la ruta no es pública, intercepta la navegación y lo redirige automáticamente a la pantalla de `/login`.

#### Guard por Rol (`requireRoleGuard`)

Protege las "zonas" o paneles específicos basados en el rol operativo del usuario (Manager, Waiter, Kitchen).

- **Implementación (Factory Function)**: Es una función que recibe el rol esperado (`expectedRole`) y devuelve el _guard_.
- **Validación Estricta**: Antes de permitir el acceso, comprueba si el usuario autenticado tiene el rol exacto especificado (`authStore.user?.role === expectedRole`).
- **Seguridad Perimetral**: Evita que los usuarios excedan sus privilegios (por ejemplo, un camarero intentando acceder a `/manager`). Si se deniega el acceso, se imprime un `console.warn` y se redirige al `/login`.

### Estructura de Rutas

El enrutador está segmentado en grandes bloques lógicos:

- **Pública (`/`)**: Landing page principal y de marketing.
- **Autenticación (`/auth`)**: Login y Registro. En la ruta de registro, utiliza un `beforeEnter` específico que valida (mediante una expresión regular) que el código de invitación pasado por la URL sea un UUID válido. Si el enlace está corrupto, redirige al login de forma preventiva.
- **Manager (`/manager`)**: Panel de control del administrador. Incluye rutas hijas para gestionar establecimientos, mesas (`/:cif/tables`), personal, invitaciones al equipo, visualización de pedidos y configuración del menú y catálogo de productos (`/:cif/products`).
- **Menú (`/menu/:cif`)**: Interfaz pública o Menú digital donde el cliente final escanea el QR, visualiza el catálogo y realiza sus pedidos sin necesidad de autenticarse.
- **Camarero (`/waiter`)**: Panel para la gestión en sala. Permite visualizar el estado de las mesas en tiempo real (`/waiter`) y operar sobre los pedidos activos (`/waiter/orders`).
- **Cocina (`/kitchen`)**: Panel KDS (Kitchen Display System) para visualizar las comandas activas y coordinar la preparación de platos.

---

## Módulos de Dominio y Gestión de Estado (Pinia)

Cada módulo encapsula su lógica en **Stores** de Pinia. El patrón general utilizado en los stores incluye el manejo asíncrono de peticiones mediante **Axios**, control de estados de carga (`loading`), y un sistema robusto de captura y extracción de errores (`extractError`).

### Manejo de Errores Centralizado

En los stores de Manager, Waiter y Kitchen, se utiliza una función de utilidad interna `extractError(error, fallback)`.

- **Qué hace**: Captura los errores lanzados por Axios (`isAxiosError`) y desestructura la respuesta del backend (`error.response.data`).
- **Lógica Inteligente**: Busca propiedades específicas de error como `message`, `error`, o diccionarios complejos de errores de validación (`errors`), y los aplana en un string legible para el usuario. Si el error no es estandarizado o se pierde la conexión, devuelve el mensaje de `fallback` definido por defecto.

### Módulo: Auth (`modules/auth/`)

Gestiona el ciclo de vida completo de la sesión del usuario.

#### Store (`auth.store.ts`)

- **Estado Reactivo**: Guarda el `authStatus` (que puede ser `Checking`, `Authenticated` o `Unauthenticated`) y el objeto `user` con el perfil devuelto por el backend (nombre, email, rol).
- **Seguridad Extrema (Sin LocalStorage)**: El token de sesión _no_ se guarda en la memoria local del navegador (`localStorage` o `sessionStorage`). El token se entrega encapsulado en una cookie `HttpOnly`, lo que garantiza protección total contra inyección de scripts cruzados (XSS), ya que JavaScript no puede leer ni extraer dicha cookie.
- **Acciones Principales**:
  - `login(username, password, rememberMe)`: Ejecuta la petición al backend llamando a `loginAction`. Si es correcta, almacena el perfil en el estado de Pinia y retorna el rol del usuario para su posterior redirección en la vista.
  - `logout()`: Ejecuta `logoutAction()`, destruyendo la sesión en el servidor (que indica al navegador que borre la cookie remotamente) y limpia el estado local a `Unauthenticated`.
  - `checkAuthStatus()`: Endpoint crítico para recuperar la sesión. Llama a `checkAuthAction()` para validar si la cookie sigue activa en el backend. Es invocado principalmente por el _router_ al inicializar la app o al pulsar F5.

### Módulo: Manager (`modules/manager/`)

Contiene todas las herramientas administrativas del gerente. Para evitar un store monolítico gigante, el dominio se divide en varios archivos especializados:

#### `establishment.store.ts`

- Mantiene la lista principal de restaurantes (`establishments`).
- Implementa acciones CRUD completas: `fetchEstablishments`, `createEstablishment`, `updateEstablishment`, `deleteEstablishment`.
- Incluye `toggleEstablishment(cif)`, que activa/desactiva rápidamente la recepción de pedidos públicos. Actualiza la lista automáticamente re-llamando a `fetchEstablishments()`.

#### `table.store.ts`

- Maneja el plano de mesas del local activo.
- Funciones: `fetchTables`, `createTable`, `updateTable`, `deleteTable`, y `toggleTable` (para marcar una mesa como inactiva/fuera de servicio, por ejemplo, si está estropeada o reservada).
- Retorna respuestas estandarizadas usando la interfaz `ActionResult` (`{ ok: boolean, message?: string, error?: string }`) para facilitar al componente visual la muestra de notificaciones (Toasts) de éxito o error.

#### `products.store.ts`

- Un store masivo que se apoya en un patrón de "acciones externas" (`modules/manager/actions/getProducts.action.ts`) para mantener el archivo limpio y no saturarlo con peticiones Axios.
- Gestiona los vectores de: `products`, `categories`, `ingredients`, y `allergens`.
- Incluye lógica especializada para subida de archivos binarios como `uploadProductImage(cif, productId, image)`.
- Realiza actualizaciones optimistas o filtrado de listas locales tras eliminar un recurso (`products.value = products.value.filter(p => p.id !== productId)`) para evitar hacer recargas completas de toda la base de datos a la red tras cada eliminación.

### Módulo: Waiter (`modules/waiter/`)

Herramienta operativa del camarero en sala.

#### Store (`waiter.store.ts`)

- **Gestión de Sala (`fetchTables`)**: Consulta a la API la distribución del restaurante. Devuelve un listado completo donde cada mesa indica su estado exacto: `free`, `pending`, `in_progress` o `done`, permitiendo mapear colores y alertas en la vista.
- **Lectura de Pedidos (`fetchOrderDetail`)**: Obtiene la información detallada de la comanda de una mesa en particular para ver los platos (`OrderItem`), cantidades y notas del cliente.
- **Operaciones de Ciclo de Vida del Pedido**:
  - `advanceOrder(orderId)`: Pasa el pedido de estado Iniciado a En Progreso, o a Completado.
  - `cancelOrder(orderId)`: Cancela y anula la comanda actual.
  - `closeTable(tableNum)`: Cobra el pedido y finaliza el ciclo, liberando la mesa.
  - **Dato clave**: Tras realizar cualquiera de estas operaciones, el store invoca automáticamente a `fetchTables()` para refrescar el estado global de la sala.

### Módulo: Kitchen (`modules/kitchen/`)

Panel KDS (Kitchen Display System) optimizado para rapidez y legibilidad.

#### Store (`kitchen.store.ts`)

- **Cola de Comandas (`fetchOrders`)**: Recupera solo los pedidos activos (`INITIATED` e `IN_PROGRESS`). Se guarda en la variable reactiva `orders`. Cada orden incluye métricas como `ready_count` y `total_count` para mostrar barras de progreso en la vista.
- **Marcado por Plato (`toggleItem`)**: Llama al endpoint de alternancia (`toggle`). Es la funcionalidad más granular; permite marcar una ración específica como "Lista" o devolverla a "Pendiente". El backend devuelve si esta acción ha provocado que todo el pedido se haya completado (`order_done`).
- **Completado de Pedido en Bloque (`advanceOrder`)**: Permite avanzar el pedido entero a su siguiente fase o completarlo de un solo clic o gesto táctil, sin tener que ir marcando plato por plato, optimizando los tiempos en horas punta.

### Módulo: Menu (`modules/menu/`)

Módulo público enfocado exclusivamente en la interfaz del cliente final (UX/UI de consumo).

- Lee los productos mediante el `cif` proporcionado en la URL pública.
- Organiza el catálogo normalmente por categorías para que el cliente pueda montar su pedido (construyendo un `payload` con los `items` y sus `notes` o cantidades).
- Envía el carrito estructurado mediante el endpoint público de creación de pedidos al backend, recibiendo de vuelta el identificador del nuevo pedido o avisos si algún producto se ha agotado entretanto.
