# Documentación técnica del frontend

El frontend de MakeMenu está construido con **Vue 3** (Composition API + `<script setup>`), **TypeScript**, **Vite** como bundler, **Pinia** para el estado global, **Vue Router** para la navegación y **Axios** como cliente HTTP. Los estilos se gestionan con **Tailwind CSS**. Esta guía explica la organización del código, los módulos por dominio y las decisiones de arquitectura más relevantes.

## Estructura general (`src/`)

Optamos por una **arquitectura modular por dominio** (también llamada feature-driven). En lugar de agrupar los archivos por tipo (todas las vistas en `views/`, todos los stores en `stores/`), agrupamos por funcionalidad: cada módulo (`auth`, `manager`, `waiter`, `kitchen`, `menu`, `landing`) contiene sus propias vistas, layouts, stores y acciones. Esto facilita mover, eliminar o duplicar un módulo sin tener que tocar carpetas dispersas por todo el proyecto.

```
src/
├── api/              Configuración base de Axios
├── assets/           CSS global y recursos compartidos
├── components/       Componentes globales (Toast, NotFound, etc.)
├── composables/      Lógica reutilizable (useFormatters, useOrderStatus...)
├── interfaces/       Tipos TypeScript compartidos
├── modules/          Módulos por dominio (el grueso del código)
│   ├── auth/
│   ├── kitchen/
│   ├── landing/
│   ├── manager/
│   ├── menu/
│   └── waiter/
├── router/           Definición de rutas y guards
├── App.vue
└── main.ts
```

Cada módulo sigue la misma sub-estructura interna: `layouts/`, `views/`, `stores/`, `actions/` e `interfaces/` cuando aplica.

---

## Cliente HTTP: `src/api/makeMenu.ts`

Toda la comunicación con el backend pasa por una única instancia de Axios:

```ts
export const makeMenuApi = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
})
```

El `withCredentials: true` es imprescindible: hace que el navegador envíe y reciba la cookie `auth_token` (HttpOnly) en todas las peticiones. Sin esa flag, Axios no adjuntaría la cookie y todas las llamadas autenticadas devolverían `401`.

La URL base se lee de la variable de entorno `VITE_API_URL`, que en desarrollo apunta a `http://localhost:8000/api/` y en producción al dominio público.

---

## Enrutamiento y guards (`src/router/index.ts`)

Las rutas se dividen en bloques por dominio. Hay dos tipos de guards:

### Guard global (`beforeEach`)

Protege todas las rutas que no están explícitamente en la lista `PUBLIC_ROUTES` (`home`, `login`, `register`, `NotFound`, `landing`, `public-menu`, `privacy`, `legal`). Si el `authStore` está en estado `Checking` (típicamente al recargar la página con F5), lanza `checkAuthStatus()` para preguntar al backend si la cookie de sesión sigue válida. Si el usuario no acaba autenticado, redirige a `/login`.

### Guard por rol (`requireRoleGuard`)

Es una factory function que recibe el rol esperado y devuelve un guard. Se aplica en cada bloque de rutas (`/manager`, `/waiter`, `/kitchen`) para bloquear el acceso cruzado entre roles. Si un camarero intenta entrar en `/manager/...`, se le redirige al login antes de cargar la vista. La validación es estricta: `authStore.user?.role === expectedRole`.

### Mapa de zonas

- `/` y `/privacy`, `/legal`: landing pública (`LandingLayout`).
- `/auth`: login y registro (`AuthLayout`).
- `/manager`: panel del manager con establecimientos, mesas, productos, ingredientes, equipo, pedidos.
- `/menu/:cif`: menú público que escanean los clientes desde el QR.
- `/waiter`: panel del camarero (estado de sala y pedidos activos).
- `/kitchen`: panel KDS de cocina.
- `/:pathMatch(.*)*`: ruta catch-all que pinta `NotFound404`.

La ruta `/register` tiene un `beforeEnter` propio que valida con una regex que el `code` de la query sea un UUID válido. Si el enlace está corrupto, redirige a `/login` antes de pintar el formulario, evitando una llamada inútil al backend.

---

## Gestión de estado: Pinia

Cada módulo declara sus propios stores. Para evitar duplicar la lógica de manejo de errores de Axios, los stores grandes (manager, waiter, kitchen) definen una función `extractError(error, fallback)` que aplana las respuestas de error del backend:

```ts
function extractError(error: unknown, fallback: string): string {
  if (isAxiosError(error) && error.response?.data) {
    const data = error.response.data
    if (data.message) return data.message
    if (data.error) return data.error
    if (data.errors) {
      return Object.entries(data.errors)
        .map(([field, msgs]) => `${field}: ${(msgs as string[]).join(', ')}`)
        .join('. ')
    }
  }
  return fallback
}
```

El backend a veces devuelve `{message: "..."}`, otras `{error: "..."}` y en validaciones de formulario `{errors: {field: ["msg"]}}`. La función las normaliza a un único string legible para mostrar en un toast.

Casi todas las acciones de los stores devuelven un `ActionResult`:

```ts
interface ActionResult {
  ok: boolean
  message?: string
  error?: string
}
```

Esto permite que el componente que invoca la acción decida si pintar un toast verde, uno rojo o no pintar nada, sin tener que saber nada de Axios.

---

## Módulo `auth`

### `auth.store.ts`

Mantiene dos piezas de estado reactivo:

- `authStatus`: enum con `Checking`, `Authenticated`, `Unauthenticated`.
- `user`: perfil del usuario (nombre, email, rol, avatar...) o `null`.

**No guardamos el token en `localStorage` ni en `sessionStorage`**. El token vive solo en la cookie `HttpOnly` que el backend devuelve en el login. Esta decisión es clave: si un atacante consigue inyectar JavaScript en la página (XSS), no puede leer la cookie y no puede robar la sesión.

Las acciones principales son:

- `login(username, password, rememberMe)`: llama al backend, guarda el perfil y devuelve el rol para que la vista de login pueda redirigir al panel correspondiente.
- `logout()`: pide al backend que destruya la sesión (lo que borra la cookie remotamente) y limpia el estado local.
- `checkAuthStatus()`: pregunta al backend si la cookie sigue siendo válida. Lo invoca el router en cada navegación inicial y `App.vue` al montar.

---

## Módulo `manager`

Es el módulo más extenso. Para no acabar con un store monolítico, el dominio se divide en cuatro stores especializados:

### `establishment.store.ts`

Gestiona la lista de locales del manager (`fetchEstablishments`) y su CRUD completo (`createEstablishment`, `updateEstablishment`, `deleteEstablishment`). Incluye `toggleEstablishment(cif)` para abrir o cerrar el local rápidamente desde una tarjeta, sin tener que entrar en el formulario completo.

### `table.store.ts`

Maneja el plano de mesas del local activo. Funciones: `fetchTables`, `createTable`, `updateTable`, `toggleTable` (para marcar una mesa como fuera de servicio) y `deleteTable`. Todos los mensajes de éxito se devuelven ya formateados con el número de mesa en dos dígitos (`String(payload.number).padStart(2, '0')`) para que los toasts queden consistentes.

### `products.store.ts`

Gestiona productos, categorías, ingredientes y alérgenos del local. Es el store más grande, por lo que las peticiones Axios se externalizan a `modules/manager/actions/getProducts.action.ts` para mantener el store legible.

Tras una eliminación, en lugar de re-fetchear toda la lista, se hace una **actualización optimista local**: `products.value = products.value.filter(p => p.id !== productId)`. Reduce notablemente el tráfico de red cuando el manager limpia varios productos seguidos.

`uploadProductImage(cif, productId, image)` envía la imagen como `multipart/form-data` en lugar de JSON.

### `staff.store.ts`

`fetchStaff`, `updateRole`, `removeMember`. La invitación de personal vive en una vista separada (`StaffInviteView.vue`) que permite elegir el rol (waiter o kitchen) y, si el manager gestiona varios locales, también el establecimiento de destino. La respuesta del backend incluye el UUID que el frontend convierte en código QR mediante `qrcode.vue` para que el nuevo empleado pueda escanearlo.

---

## Módulo `waiter`

Es la herramienta operativa del camarero.

### `waiter.store.ts`

- `fetchTables()`: trae el estado de toda la sala. Cada mesa llega con un campo `status` que es uno de `free`, `pending`, `in_progress`, `done`. Eso permite mapear colores y alertas en la vista sin lógica adicional.
- `fetchOrderDetail(tableNum)`: pide el ticket completo de una mesa para abrir el modal de detalle.
- `advanceOrder(orderId)`: avanza el estado del pedido (Iniciado → En progreso → Listo).
- `cancelOrder(orderId)`: cancela el pedido.
- `closeTable(tableNum)`: cobra y libera la mesa.

Tras cualquiera de las operaciones de mutación, el store re-llama internamente a `fetchTables()` para que la vista refleje el cambio sin tener que hacerlo desde el componente. Es una pequeña pérdida de eficiencia a cambio de simplificar mucho los componentes.

### `WaiterOrders.vue`

Esta vista incluye un sistema de polling con detección de pedidos nuevos. Cada 10 segundos vuelve a llamar al endpoint de listado, compara los IDs nuevos con los conocidos y, si encuentra alguno, pinta un toast en la esquina y reproduce un sonido de notificación generado con la Web Audio API (un par de ondas senoidales muy cortas). Para no acumular peticiones si la red va lenta, hay un guard `isPolling` que descarta nuevas iteraciones mientras una está en vuelo.

---

## Módulo `kitchen`

Vista KDS (Kitchen Display System) optimizada para ser usable a distancia y con pantallas táctiles.

### `kitchen.store.ts`

- `fetchOrders()`: recupera solo los pedidos en `INITIATED` o `IN_PROGRESS`. Cada orden viene con `ready_count` y `total_count` para pintar la barra de progreso del ticket.
- `toggleItem(itemId)`: marca o desmarca un plato individual. El backend devuelve un campo `order_done` que indica si ese toggle ha completado el pedido entero, lo que permite al frontend ocultar el ticket sin esperar al siguiente polling.
- `advanceOrder(orderId)`: completa el pedido entero de una sola vez (útil en hora punta para ahorrar clicks).

---

## Módulo `menu`

Es la interfaz pública que ve el cliente cuando escanea el QR. No requiere autenticación.

- Lee el catálogo del establecimiento con el `cif` que viene en la URL pública.
- Organiza el catálogo por categorías.
- El cliente construye el pedido localmente (en un estado reactivo del store) y al confirmar envía un payload con `table` y `items[]` al endpoint `create_public_order` del backend.
- Si el backend devuelve `skipped_product_ids` (productos que se agotaron mientras el cliente miraba la carta), el frontend muestra un aviso para que sepa qué no se incluyó.

---

## Composables compartidos (`src/composables/`)

Tres composables agrupan lógica reutilizada entre módulos:

- **`useFormatters`**: `formatDate`, `formatTime`, `elapsedTime`, `isUrgent`. Usan `Intl.DateTimeFormat` con locale `es-ES`. Las instancias del formateador están fuera de la función para no recrearlas en cada render.
- **`useOrderStatus`**: devuelve clases de Tailwind (`getStatusClass`, `getStatusDot`) según el status numérico del pedido. Centraliza el mapeo `-1 → danger`, `1 → warning`, `2 → info`, `3 → success`.
- **`useLocalToast`**: toast efímero que se autodescarta tras un timeout, sin necesidad de un store global. Útil para vistas concretas que no necesitan persistencia entre rutas.

---

## Componentes globales (`src/components/`)

- **`ToastContainer.vue`**: gestiona la cola de notificaciones globales que se disparan desde cualquier store o composable.
- **`NotFound404.vue`**: vista 404 fija.

---

## Configuración de build

- **`vite.config.ts`**: alias `@` → `src/`, plugin de Vue y Tailwind. En desarrollo, el dev server arranca en el puerto 5173.
- **`tsconfig.app.json` / `tsconfig.node.json`**: configuración estricta de TypeScript dividida entre el código de la app y el de configuración (Vite, Vitest…).
- **`eslint.config.ts`** + **`.oxlintrc.json`**: linting. Oxlint pasa por defecto en `lint-staged`, ESLint para reglas más específicas de Vue.
- **`Dockerfile`** + **`nginx.conf`**: imagen de producción. Vite compila a `dist/`, nginx sirve los estáticos y hace proxy a `/api/` contra el backend.

---

## Variables de entorno

- `VITE_API_URL`: URL base de la API del backend (ej. `http://localhost:8000/api/`).

`.env.example` recoge esta variable. En producción se inyecta en tiempo de build dentro de la imagen Docker.

---

## Decisiones técnicas resumidas

| Decisión                                                                  | Motivo                                                                                                                  |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Arquitectura modular por dominio en `src/modules/`                        | Facilita encontrar el código, mover/eliminar módulos completos sin tocar muchas carpetas.                               |
| Token solo en cookie `HttpOnly` (sin `localStorage`)                      | Protección contra XSS: el JS nunca toca el token.                                                                       |
| Función `extractError` común en stores                                    | Normaliza las respuestas de error heterogéneas del backend a un único string para los toasts.                           |
| `ActionResult` como return de acciones                                    | El componente que invoca decide cómo notificar al usuario, sin acoplarse a Axios.                                       |
| Polling con `isPolling` guard en lugar de WebSockets                      | Suficiente para el caso de uso (cocina y sala). Evita la complejidad de mantener una conexión persistente en Fase 1.    |
| Actualización optimista local tras eliminaciones                          | Mejor UX y menos tráfico cuando el manager elimina varios productos seguidos.                                           |
| `withCredentials: true` global en Axios                                   | Necesario para que el navegador envíe la cookie de sesión en todas las peticiones, también cross-origin en desarrollo.  |
| Tailwind CSS en lugar de componentes UI pre-empaquetados                  | Más control sobre el diseño visual del producto, sin la sobrecarga de aprender una librería de componentes nueva.       |
