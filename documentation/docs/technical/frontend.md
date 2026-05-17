---
title: Frontend
icon: lucide/layout-dashboard
---

# Frontend

El frontend de MakeMenu está construido con **Vue 3** (Composition API + `<script setup>`), **TypeScript**, **Vite** como bundler, **Pinia** para el estado global, **Vue Router** para la navegación y **Axios** como cliente HTTP. Los estilos se gestionan con **Tailwind CSS**.

## Estructura del código

Optamos por una **arquitectura modular por dominio** (también llamada feature-driven). En lugar de agrupar los archivos por tipo (todas las vistas en `views/`, todos los stores en `stores/`), agrupamos por funcionalidad: cada módulo contiene sus propias vistas, layouts, stores y acciones. Esto facilita mover, eliminar o duplicar un módulo sin tener que tocar carpetas dispersas.

```
src/
├── api/              Configuración base de Axios
├── assets/           CSS global y recursos compartidos
├── components/       Componentes globales (Toast, NotFound, etc.)
├── composables/      Lógica reutilizable
├── interfaces/       Tipos TypeScript compartidos
├── modules/          Módulos por dominio
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

## Cliente HTTP

Toda la comunicación con el backend pasa por una única instancia de Axios:

```ts
export const makeMenuApi = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
})
```

El `withCredentials: true` es imprescindible: hace que el navegador envíe y reciba la cookie `auth_token` (HttpOnly) en todas las peticiones. Sin esa flag, Axios no la adjuntaría y todas las llamadas autenticadas devolverían `401`.

## Enrutamiento y guards

Las rutas se dividen en bloques por dominio. Hay dos tipos de guards:

### Guard global

Protege todas las rutas excepto las explícitamente declaradas en `PUBLIC_ROUTES` (landing, login, registro, menú público, 404, privacidad, legal). Si el `authStore` está en estado `Checking` (típicamente al recargar la página), lanza `checkAuthStatus()` para preguntar al backend si la cookie de sesión sigue siendo válida. Si el usuario no acaba autenticado, redirige a `/login`.

### Guard por rol

`requireRoleGuard(role)` es una factory function que se aplica en cada bloque de rutas (`/manager`, `/waiter`, `/kitchen`) para bloquear el acceso cruzado entre roles. Si un camarero intenta entrar en `/manager/...`, se le redirige al login antes de cargar la vista.

La ruta `/register` tiene un `beforeEnter` propio que valida con una regex que el `code` de la query sea un UUID válido. Si el enlace está corrupto, redirige a `/login` antes de pintar el formulario.

## Gestión de estado

Cada módulo declara sus propios stores con Pinia. Para no duplicar la lógica de manejo de errores de Axios, los stores grandes (manager, waiter, kitchen) definen una función `extractError(error, fallback)` que aplana las distintas formas en que el backend devuelve errores (`{message}`, `{error}`, `{errors: {field: [...]}}`) a un único string legible.

Las acciones devuelven un `ActionResult`:

```ts
interface ActionResult {
  ok: boolean
  message?: string
  error?: string
}
```

Esto permite que el componente que invoca la acción decida si pintar un toast verde, uno rojo o no pintar nada, sin tener que saber nada de Axios.

## Módulo `auth`

Mantiene el estado de sesión del usuario. Tres piezas:

- `authStatus`: `Checking`, `Authenticated`, `Unauthenticated`.
- `user`: perfil completo (nombre, email, rol, avatar...) o `null`.
- Acciones: `login`, `logout`, `checkAuthStatus`.

**No guardamos el token en `localStorage`**. El token vive solo en la cookie `HttpOnly` que devuelve el backend. Esta decisión es deliberada: si un atacante consigue inyectar JavaScript en la página (XSS), no puede leer la cookie y no puede robar la sesión.

## Módulo `manager`

Es el módulo más extenso. Para no acabar con un store monolítico, el dominio se divide en cuatro stores especializados:

- **`establishment.store.ts`**: lista de locales y su CRUD. Incluye `toggleEstablishment` para abrir/cerrar el local rápidamente desde una tarjeta.
- **`table.store.ts`**: plano de mesas del local activo. Mensajes con el número de mesa en dos dígitos (`01`, `02`...) para que los toasts queden consistentes.
- **`products.store.ts`**: productos, categorías, ingredientes y alérgenos. Las peticiones Axios se externalizan a `actions/getProducts.action.ts` para mantener el store legible. Tras una eliminación se hace **actualización optimista local** (`products.value = products.value.filter(...)`) en lugar de re-fetchear toda la lista.
- **`staff.store.ts`**: gestión del equipo. La invitación de personal vive en una vista aparte (`StaffInviteView.vue`) que permite elegir rol y, si el manager gestiona varios locales, el establecimiento de destino.

## Módulo `waiter`

Vista operativa del camarero.

- `fetchTables()`: trae el estado de toda la sala. Cada mesa llega con un campo `status` (`free`, `pending`, `in_progress`, `done`) que permite mapear colores y alertas en la vista.
- `closeTable(tableNum)`: cobra y libera la mesa.

`WaiterOrders.vue` incluye un sistema de **polling con detección de pedidos nuevos**. Cada 10 segundos vuelve a llamar al endpoint de listado, compara los IDs nuevos con los conocidos y, si encuentra alguno, pinta un toast en la esquina y reproduce un sonido de notificación generado con la Web Audio API. Hay un guard `isPolling` para descartar nuevas iteraciones mientras una está en vuelo, evitando que la red lenta acumule peticiones.

## Módulo `kitchen`

Vista KDS (Kitchen Display System) optimizada para pantallas táctiles a distancia.

- `fetchOrders()`: recupera solo los pedidos en `INITIATED` o `IN_PROGRESS`. Cada orden incluye `ready_count` y `total_count` para pintar la barra de progreso.
- `toggleItem(itemId)`: marca o desmarca un plato individual. El backend devuelve `order_done` para que el frontend pueda ocultar el ticket inmediatamente si toggle completó el pedido.
- `advanceOrder(orderId)`: completa el pedido entero de una sola vez (útil en hora punta).

## Módulo `menu`

Es la interfaz pública que ve el cliente cuando escanea el QR. No requiere autenticación.

Lee el catálogo del establecimiento con el `cif` que viene en la URL pública, lo organiza por categorías y permite construir un pedido localmente. Al confirmar envía un payload con `table` e `items[]` al endpoint `create_public_order` del backend. Si el backend devuelve `skipped_product_ids` (productos que se agotaron mientras el cliente miraba la carta), la interfaz lo avisa.

## Composables compartidos

Tres composables centralizan lógica reutilizada entre módulos:

- **`useFormatters`**: formato de fechas, horas y tiempos relativos con `Intl.DateTimeFormat` y locale `es-ES`.
- **`useOrderStatus`**: devuelve clases de Tailwind según el status numérico del pedido.
- **`useLocalToast`**: toast efímero que se autodescarta, sin necesidad de un store global.

## Build y configuración

- **Vite**: dev server en `:5173`, alias `@` → `src/`.
- **TypeScript**: configuración estricta dividida entre código de app y código de configuración.
- **ESLint + Oxlint**: Oxlint en `lint-staged` por velocidad, ESLint para reglas específicas de Vue.
- **Docker + nginx**: en producción Vite compila a `dist/` y nginx sirve los estáticos y hace proxy a `/api/` contra el backend.

## Variables de entorno

| Variable       | Uso                                                  |
| -------------- | ---------------------------------------------------- |
| `VITE_API_URL` | URL base de la API del backend                       |

Se inyectan en tiempo de build, ya que Vite las resuelve durante la compilación.

## Estilos y convenciones de Tailwind

El proyecto usa **Tailwind CSS v4** con la integración de Vite. No hay archivo `tailwind.config.js` la configuración se gestiona directamente en el CSS de entrada. Todos los estilos son utilidades de Tailwind inline en los componentes; no hay CSS personalizado salvo el archivo global de assets.  

## Usabilidad y accesibilidad

La interfaz sigue principios básicos de usabilidad y accesibilidad web. Los colores de acento cumplen con ratios de contraste suficientes para texto sobre fondos claros. Los botones y controles interactivos tienen estados `hover` y `focus` visibles, y los inputs incluyen `focus:ring` para navegación por teclado. Los estados de carga, error y vacío están cubiertos en todas las vistas para que el usuario siempre reciba feedback visual. Las etiquetas de formulario están asociadas a sus campos, y los iconos SVG decorativos no incluyen texto alternativo innecesario. En vistas críticas como el KDS de cocina y la carta pública, el diseño prioriza la legibilidad a distancia con tamaños de texto generosos y áreas de toque amplias, pensadas para uso táctil en entornos de hostelería.

### Paleta de colores

La interfaz gira en torno a dos rampas principales:

| Rol | Clase |
|-----|-------|
| Acción principal, activo, acento | `bg-emerald-400`, `text-emerald-600`, `border-emerald-400` |
| Hover de acento | `bg-emerald-500` |
| Fondo de acento suave | `bg-emerald-50`, `bg-emerald-100` |
| Texto sobre fondo claro | `text-gray-700`, `text-gray-800` |
| Texto secundario / placeholder | `text-gray-400`, `text-gray-500` |
| Fondo de página | `bg-gray-50` |
| Superficie de tarjeta | `bg-white` |
| Bordes | `border-gray-200`, `border-gray-100` |
| Peligro / eliminar | `bg-red-400`, `hover:bg-red-500` |
| Estado disponible | `bg-green-100 text-green-700` |
| Estado no disponible | `bg-red-100 text-red-600` |

### Bordes y radios

Se usa `rounded-xl` como radio estándar para botones, inputs y tarjetas pequeñas, y `rounded-2xl` para tarjetas y contenedores más grandes. Los bordes son siempre `border border-gray-200` con grosor de `1px`.

### Sombras

Las sombras son siempre semánticas y ligeras. El patrón habitual es `shadow-md shadow-emerald-400/20` en botones primarios y `shadow-sm` en tarjetas.

### Botones

Tres variantes recurrentes:

```html
<!-- Primario -->
<button class="px-4 py-2 bg-emerald-400 text-white text-sm font-semibold rounded-xl hover:bg-emerald-500 transition-colors shadow-sm shadow-emerald-400/20">

<!-- Destructivo -->
<button class="px-4 py-2 bg-red-400 text-white text-sm font-semibold rounded-xl hover:bg-red-500 transition-colors">

<!-- Outline -->
<button class="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-xl border border-gray-200 hover:bg-gray-50 transition-colors">
```

### Inputs y selects

```html
<input class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300">
<select class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-lg p-2 outline-none cursor-pointer focus:ring-2 focus:ring-emerald-300">
```

### Tarjetas

```html
<div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-4">
```

### Tipografía

| Rol | Clase |
|-----|-------|
| Título de sección | `text-xl font-bold text-gray-700` |
| Subtítulo | `text-sm font-semibold text-gray-700` |
| Etiqueta de categoría | `text-xs font-semibold uppercase tracking-widest text-gray-400` |
| Texto de cuerpo | `text-sm text-gray-500` |
| Precio | `text-emerald-600 font-bold` |

### Layout y espaciado

El patrón de layout más común es `flex items-center justify-between` para cabeceras de sección, y `grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4` para rejillas de tarjetas. El espaciado interno de vistas usa `space-y-6` como ritmo vertical base.

### Badges y etiquetas

```html
<!-- Categoría de producto -->
<span class="text-xs text-emerald-600 font-medium bg-emerald-50 px-2 py-0.5 rounded-full">

<!-- Badge de navegación activo -->
<span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-white text-emerald-600">
```

### Transiciones

Todas las transiciones usan `transition-colors` o `transition-all` con la duración por defecto de Tailwind (`150ms`). No se usan animaciones complejas salvo el toggle de disponibilidad en la carta, que usa `transition-transform duration-200`.