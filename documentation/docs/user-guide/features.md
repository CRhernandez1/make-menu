---
title: Funcionalidades
icon: lucide/list-checks
---

# Funcionalidades

Esta página describe en detalle cada funcionalidad de MakeMenu agrupada por rol. Sirve como referencia rápida para entender qué se puede hacer desde cada perfil y dónde encontrarlo en la interfaz.

## Funcionalidades del manager

El manager es el rol con mayor nivel de acceso. Tiene visibilidad completa sobre uno o varios establecimientos y puede configurar todos los aspectos operativos.

### Gestión de establecimientos

- Crear un nuevo establecimiento con sus datos fiscales (nombre comercial, razón social, CIF, dirección, teléfono, descripción).
- Editar los datos del establecimiento.
- Abrir o cerrar el establecimiento al público con un único clic. Cuando el establecimiento está cerrado, los códigos QR de las mesas siguen funcionando pero no permiten enviar pedidos.
- Eliminar un establecimiento (con confirmación previa, ya que borra también todas sus mesas, productos y pedidos).
- Cambiar entre establecimientos desde el selector superior si el manager gestiona varios.

### Gestión de mesas

- Crear mesas indicando número y aforo máximo de comensales.
- Editar el aforo de una mesa existente.
- Marcar una mesa como activa o inactiva (útil cuando está temporalmente fuera de servicio o reservada para un evento privado).
- Eliminar una mesa.
- Generar el código QR de cada mesa para imprimir y colocar físicamente. El QR contiene un enlace al menú público del local con el número de mesa precargado.

### Gestión del equipo

- Ver el listado de personal con su rol activo.
- Cambiar el rol de un miembro entre camarero y cocinero.
- Eliminar a un miembro del equipo. Esto marca su relación como cerrada (`end_date`) pero conserva el histórico para futuras consultas.
- Generar invitaciones por código QR o enlace web. La invitación es de un único uso y caduca si el invitado no la utiliza.
- Si el manager gestiona varios establecimientos, elige a cuál se asigna la invitación en el momento de generarla.

> El manager no puede cambiarse el rol a sí mismo ni eliminarse del equipo. Esto evita bloqueos accidentales que dejarían el establecimiento sin gestor.

### Gestión del catálogo

#### Categorías

- Crear, editar y eliminar categorías para organizar la carta (entrantes, principales, bebidas, postres...).
- Las categorías determinan el orden en que se muestran los productos al cliente.

#### Ingredientes

- Crear ingredientes con nombre, descripción y unidad de medida.
- Asociar uno o varios alérgenos a cada ingrediente (de la lista oficial del Reglamento UE 1169/2011).
- Marcar un ingrediente como agotado para reflejarlo en los productos que lo contienen.

#### Productos

- Crear productos con nombre, descripción, precio, categoría e imagen.
- Asociar la receta (componentes) indicando qué ingredientes contiene, en qué cantidad y si el cliente puede pedir quitar alguno.
- Marcar un producto como disponible o agotado de forma rápida sin tener que abrir el formulario de edición.
- Subir o cambiar la imagen del producto.

#### Alérgenos

- Consultar la lista maestra de los 14 alérgenos oficiales.
- Los alérgenos se asocian a nivel de ingrediente, y se calculan automáticamente para cada producto en base a los ingredientes que lo componen.

### Visualización de pedidos

- Ver el listado completo de pedidos del establecimiento.
- Filtrar por establecimiento (si gestiona varios) y por antigüedad (últimas 24 horas, 3 días, 7 días, todo el histórico).
- Abrir el ticket de cualquier pedido para ver el detalle: productos, cantidades, notas del cliente y total.

---

## Funcionalidades del camarero

El camarero opera en sala. Su panel está pensado para ser usado desde una tablet o móvil mientras se mueve por el local.

### Vista de sala

- Listado visual de todas las mesas activas del establecimiento con su estado en tiempo real:
  - **Libre**: la mesa no tiene ningún pedido activo.
  - **Pendiente**: el cliente acaba de enviar el pedido y aún no se ha empezado a preparar.
  - **En progreso**: la cocina ha empezado a preparar al menos un plato.
  - **Listo**: todos los platos del pedido están preparados y la mesa está lista para cobrar.
- Cada mesa muestra el número de productos del pedido y el tiempo transcurrido desde que se envió.

### Gestión de pedidos activos

- Ver el ticket detallado de cualquier mesa: productos, cantidades, notas y total.
- Avanzar manualmente el estado de un pedido si se quiere forzar el cambio (por ejemplo, marcarlo como listo cuando la cocina no lo ha hecho).
- Cancelar un pedido activo (con confirmación, ya que es una acción irreversible).
- Cerrar la mesa cuando el cliente paga: marca el pedido como pagado, cambia su estado a finalizado y libera la mesa para el siguiente cliente.

### Notificaciones en tiempo real

- Toast visual + sonido de notificación cuando entra un pedido nuevo. El polling se hace cada 10 segundos.
- El nuevo pedido se resalta en la lista durante unos segundos para que el camarero lo identifique rápidamente.

### Histórico de pedidos

- Acceso al listado de pedidos cerrados con los mismos filtros que tiene el manager (por establecimiento y por antigüedad).

---

## Funcionalidades del cocinero

El cocinero tiene el panel KDS (Kitchen Display System). Está pensado para una pantalla fija en cocina, posiblemente táctil, donde el personal pueda ver y marcar pedidos sin ratón.

### Cola de pedidos activos

- Visualización en tarjetas de todos los pedidos en estado **iniciado** o **en progreso** del establecimiento.
- Cada tarjeta muestra:
  - Número de pedido y mesa.
  - Lista de productos con cantidad y notas del cliente (alergias, modificaciones, sin un ingrediente, etc.).
  - Barra de progreso indicando cuántos platos están listos sobre el total.
  - Tiempo transcurrido desde que entró el pedido.
- Los pedidos se ordenan por antigüedad (los más viejos primero).

### Marcado de platos

- Cada plato del pedido tiene un botón para marcarlo como listo o devolverlo a pendiente.
- Cuando se marca el primer plato de un pedido, el pedido pasa automáticamente de **iniciado** a **en progreso**.
- Cuando se marcan todos los platos, el pedido pasa automáticamente a **listo** y desaparece de la cola.

### Completar pedido entero

- Botón para marcar todos los platos pendientes de un pedido como listos de una sola vez. Útil en hora punta cuando se quiere despachar un pedido rápido sin ir plato a plato.

---

## Funcionalidades del cliente final

El cliente no tiene cuenta ni necesita instalar nada. Toda su interacción es desde el navegador del móvil tras escanear el QR de la mesa.

### Acceso a la carta

- Escaneo del QR de la mesa → la página de la carta se abre directamente con la mesa precargada.
- Visualización del catálogo organizado por categorías.
- Cada producto muestra:
  - Imagen.
  - Nombre y descripción.
  - Precio.
  - Alérgenos (calculados a partir de los ingredientes).

### Construcción del pedido

- Añadir productos al carrito con la cantidad deseada.
- Añadir notas a un producto (por ejemplo, "sin cebolla", "punto medio").
- Ver el resumen del carrito antes de confirmar.
- Modificar cantidades o eliminar productos antes de enviar.

### Envío del pedido

- Confirmar y enviar el pedido directamente a la cocina del local.
- Si algún producto se ha agotado entre que el cliente lo añadió y envió, el sistema lo avisa indicando qué productos no se incluyeron.
- Tras enviar, el cliente recibe la confirmación con el número de pedido.

---

## Funcionalidades transversales

### Seguridad

- Cookies de sesión `HttpOnly`: el JavaScript del navegador no puede leer el token de sesión, lo que mitiga ataques XSS.
- Validación estricta de roles en cada endpoint del backend: un camarero no puede acceder a datos del panel del manager aunque manipule la URL.
- Aislamiento multi-tenant: cada manager solo ve sus propios establecimientos. Las queries del backend filtran siempre por los establecimientos donde el usuario tiene un rol activo.

### Rendimiento

- Polling cada 10 segundos en las vistas de camarero y cocina, con guard para evitar acumulación de peticiones si la red va lenta.
- Optimizaciones de base de datos (`select_related`, `prefetch_related`, `bulk_create`) para mantener tiempos de respuesta bajos incluso con varios cientos de pedidos en histórico.

### Compatibilidad

- Funciona en cualquier navegador moderno (Chrome, Safari, Firefox, Edge) en versiones recientes.
- Diseño responsive: el panel del manager funciona en escritorio y tablet, las vistas del camarero y la cocina están optimizadas para tablet, y el menú del cliente está optimizado para móvil.
- No requiere instalación de ninguna aplicación en ningún dispositivo.
