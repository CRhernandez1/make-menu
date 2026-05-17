---
title: Casos de uso
icon: lucide/users-round
---

# Casos de uso

Los casos de uso se agrupan por actor. La plataforma tiene cuatro actores: **manager**, **camarero**, **cocinero** y **cliente final**.

## Actores y resumen

| Actor          | Acceso                              | Casos de uso principales                                                            |
| -------------- | ----------------------------------- | ----------------------------------------------------------------------------------- |
| Manager        | Autenticado, rol `manager`          | Gestión de establecimiento, equipo, catálogo y consulta de pedidos                  |
| Camarero       | Autenticado, rol `waiter`           | Vista de sala, cobro y cierre de mesa, gestión de pedidos activos                   |
| Cocinero       | Autenticado, rol `kitchen`          | KDS de pedidos activos, marcado por plato, avance automático del estado del pedido  |
| Cliente final  | Sin autenticación, accede por QR    | Consultar la carta, montar el carrito, enviar el pedido                             |

---

## Caso de uso CU-01: Iniciar sesión

- **Actor**: Manager, Camarero o Cocinero.
- **Precondición**: el usuario está dado de alta en la plataforma.
- **Flujo principal**:
  1. El usuario accede a `/login`.
  2. Introduce su usuario y contraseña.
  3. Marca opcionalmente "recordarme".
  4. Pulsa "Iniciar sesión".
  5. El sistema valida las credenciales contra el backend.
  6. El backend devuelve el perfil completo (incluido el rol) y deposita una cookie de sesión.
  7. El frontend redirige al panel correspondiente al rol del usuario.
- **Flujo alternativo**: si las credenciales son incorrectas, el sistema muestra "Credenciales incorrectas." y el usuario puede reintentar.

---

## Caso de uso CU-02: Crear un nuevo establecimiento

- **Actor**: Manager.
- **Precondición**: el usuario ha iniciado sesión.
- **Flujo principal**:
  1. El manager pulsa "Crear establecimiento" en `/manager/establishments`.
  2. Rellena el formulario (nombre, CIF, dirección, teléfono...).
  3. El sistema valida el CIF (formato y unicidad).
  4. El sistema crea el establecimiento y asigna automáticamente al usuario como manager del mismo.
  5. El frontend redirige a la vista detallada del nuevo local.
- **Postcondición**: el manager tiene un nuevo establecimiento en su listado.

---

## Caso de uso CU-03: Invitar a un nuevo miembro al equipo

- **Actor**: Manager.
- **Precondición**: el manager gestiona al menos un establecimiento.
- **Flujo principal**:
  1. El manager entra en `/manager/invite`.
  2. Selecciona el establecimiento de destino (si gestiona varios).
  3. Selecciona el rol (camarero o cocinero).
  4. Pulsa "Generar invitación".
  5. El sistema crea un `Invitation` con un UUID y devuelve el código y el enlace.
  6. El frontend genera un QR escaneable y muestra el enlace web.
  7. El manager comparte el QR o el enlace con el invitado.
- **Flujo alternativo**: si el invitado no usa la invitación antes de su caducidad, queda invalidada automáticamente.

---

## Caso de uso CU-04: Registrarse mediante una invitación

- **Actor**: Empleado invitado (futuro camarero o cocinero).
- **Precondición**: el empleado tiene un enlace o QR válido.
- **Flujo principal**:
  1. El empleado abre el enlace `https://makemenu.../register?code=<uuid>`.
  2. El frontend valida el formato del UUID y llama al backend para verificar que la invitación sigue siendo válida.
  3. El sistema muestra el nombre del establecimiento y el rol al que se va a unir.
  4. El empleado rellena sus datos (usuario, contraseña, email, nombre).
  5. El sistema crea el usuario, lo asocia al establecimiento con el rol indicado y marca la invitación como usada.
  6. El frontend redirige al login.
- **Flujo alternativo**: si la invitación ya está usada o caducada, el sistema muestra el mensaje "Invitación inválida o ya usada." y redirige al login.

---

## Caso de uso CU-05: Configurar un producto del catálogo

- **Actor**: Manager.
- **Precondición**: el manager está dentro de un establecimiento concreto.
- **Flujo principal**:
  1. El manager entra en `/manager/establishments/<cif>/products`.
  2. Pulsa "Añadir producto".
  3. Rellena nombre, descripción, precio y selecciona categoría.
  4. Sube una imagen del producto.
  5. Opcionalmente define la receta añadiendo ingredientes con cantidad y unidad.
  6. Marca si cada ingrediente es retirable a petición del cliente.
  7. Guarda el producto.
- **Postcondición**: el producto aparece en la carta pública y los alérgenos se calculan automáticamente.

---

## Caso de uso CU-06: Realizar un pedido como cliente

- **Actor**: Cliente final.
- **Precondición**: el cliente está físicamente en el establecimiento. El establecimiento está abierto.
- **Flujo principal**:
  1. El cliente escanea el QR de la mesa con la cámara del móvil.
  2. El navegador abre la carta del establecimiento con la mesa precargada.
  3. El cliente navega por las categorías y revisa los productos.
  4. Añade los productos deseados al carrito con la cantidad y notas que quiera.
  5. Pulsa "Enviar pedido".
  6. El sistema valida que todos los productos estén disponibles, crea el pedido en cocina y devuelve confirmación con el número de pedido.
- **Flujo alternativo**: si algún producto se ha agotado mientras tanto, el sistema lo retira del pedido y avisa al cliente en pantalla.

---

## Caso de uso CU-07: Marcar platos como listos (cocina)

- **Actor**: Cocinero.
- **Precondición**: el cocinero ha iniciado sesión y hay al menos un pedido activo.
- **Flujo principal**:
  1. El cocinero ve el KDS con todos los pedidos activos en tarjetas.
  2. Selecciona la tarjeta del pedido que está preparando.
  3. Pulsa el botón "Listo" en cada plato a medida que lo termina.
  4. La barra de progreso del pedido se actualiza automáticamente.
  5. Cuando marca el último plato pendiente, el pedido pasa a "Listo" automáticamente y desaparece de la cola.
- **Flujo alternativo**: el cocinero puede usar "Completar todo" para marcar todos los platos pendientes de una sola vez.

---

## Caso de uso CU-08: Cobrar y cerrar una mesa (camarero)

- **Actor**: Camarero.
- **Precondición**: la mesa tiene un pedido activo no pagado.
- **Flujo principal**:
  1. El camarero ve en la vista de sala que una mesa está marcada como "Listo".
  2. Abre el detalle de la mesa y consulta el ticket.
  3. Cobra al cliente (por medios externos a la plataforma).
  4. Pulsa "Cerrar mesa".
  5. El sistema marca el pedido como pagado, finalizado y registra la hora de cierre. La mesa pasa a "Libre".
- **Postcondición**: la mesa está disponible para nuevos clientes.

---

## Caso de uso CU-09: Cancelar un pedido (camarero)

- **Actor**: Camarero.
- **Precondición**: la mesa tiene un pedido activo (iniciado o en progreso).
- **Flujo principal**:
  1. El camarero abre el detalle del pedido.
  2. Pulsa "Cancelar pedido".
  3. El sistema pide confirmación.
  4. El camarero confirma.
  5. El sistema marca el pedido como cancelado y registra la hora de cierre.
- **Postcondición**: el pedido no aparece en cocina y la mesa vuelve a estar libre.

---

## Caso de uso CU-10: Consultar el histórico de pedidos

- **Actor**: Manager o Camarero.
- **Precondición**: el usuario ha iniciado sesión.
- **Flujo principal**:
  1. El usuario entra en la vista de pedidos.
  2. Selecciona el filtro temporal deseado (24 h, 3 días, 7 días, todos).
  3. Si gestiona varios establecimientos (manager), selecciona uno o todos.
  4. El sistema devuelve la lista paginada ordenada por fecha descendente.
  5. El usuario puede abrir cualquier pedido para ver su ticket detallado.

---

## Diagrama resumen de actores

| **MANAGER** *(gestión)*  | **OPERATIVOS** *(servicio)*   | **CLIENTE FINAL** *(consumo)*  |
| ------------------------ | ----------------------------- | ------------------------------ |
| · Crear locales          | **Camarero**                  | · Escanea el QR                |
| · Mesas + QR             | · Estado de sala              | · Ve la carta digital          |
| · Invitar al equipo      | · Cobrar y cerrar mesa        | · Monta el carrito             |
| · Catálogo y precios     | · Cancelar pedidos            | · Envía el pedido              |
| · Ver pedidos            |                               |                                |
|                          | **Cocinero**                  | *Sin login, sin app.*          |
| *Sesión autenticada*     | · KDS de pedidos              | *100% en el navegador.*        |
| *Cookie HttpOnly.*       | · Marcar platos               |                                |

**Acceso a la plataforma:**

- **Manager y Operativos** acceden con usuario y contraseña al panel correspondiente a su rol.
- **Cliente final** entra directamente desde el QR de la mesa, sin registro ni instalación.
- Las tres rutas las separa el router del frontend mediante guards por rol que verifican `authStore.user.role` contra el rol esperado para cada bloque de rutas.
