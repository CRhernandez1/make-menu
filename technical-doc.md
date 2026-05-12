# Documentación técnica del proyecto

Esta documentación tiene como objetivo explicar detalladamente como funciona cada cosa del proyecto.

## Orders

### Views

#### Helpers privados

Estas funciones empiezan con un guion bajo \_ para indicar que son de uso interno y no están conectadas a ninguna URL directamente. Centralizan la lógica de seguridad y negocio.

##### \_get_est_ids_by_role(user, role)

- Su propósito es obtener de forma rápida y ligera todos los identificadores (IDs) de los establecimientos vinculados a un usuario según el rol que desempeñe (por ejemplo: manager, waiter, kitchen).
- values_list: En lugar de cargar en memoria todos los campos de los modelos completos (como lo hace filter), le indica a la base de datos que seleccione únicamente la columna especificada (establishment_id), reduciendo drásticamente el uso de memoria y mejorando la velocidad.
- flat=True: Aplanamiento de la estructura de datos. Por defecto, values_list devuelve una lista de tuplas [(1,), (2,)]. Al usar flat=True, transforma esa estructura en una lista plana unidimensional [1, 2] que es compatible con otras consultas (como \_\_in).
- Evalúa la consulta de forma inmediata (forzando la ejecución en la base de datos) y convierte el QuerySet perezoso en una lista nativa de Python. Esto aísla los datos en memoria y cierra la conexión con la base de datos de forma segura.

##### \_get_primary_establishment(user, role)

- Esta función sirve para obtener el establecimiento principal en el que opera un usuario para un rol determinado (como camarero o cocinero). A diferencia de un gerente (que puede gestionar varios locales a la vez), un camarero o un cocinero suelen estar asignados a un único local operativo en un momento dado.
- est_ids = \_get_est_ids_by_role(user, role): Llama al helper que ya conocemos para obtener la lista de IDs de establecimientos asociados al usuario.
- if not est_ids: return None: Actúa como barrera de seguridad. Si la lista está vacía (el usuario no tiene establecimientos asignados con ese rol), devuelve None en lugar de intentar hacer una consulta que fallaría.
- return Establishment.objects.get(pk=est_ids[0]).first(): Toma el primer ID de la lista (el establecimiento principal o predeterminado) y hace una consulta a la base de datos para obtener el objeto Establishment completo. Se usa el first() para que devuelva None en lugar de una exception.

##### <span style="color: #ffff00;">\_list_orders_for_role(request, role)</span>

Su propósito principal es unificar la lógica de negocio para listar los pedidos de los distintos roles (como Manager o Camarero)

- Validación de Seguridad y Permisos

  ```python
  allowed_est_ids = _get_est_ids_by_role(request.user, role)
  if not allowed_est_ids:
  return JsonResponse([], safe=False)
  ```

  ¿Qué hace? Utiliza la función \_get_est_ids_by_role para obtener los identificadores de los locales que el usuario tiene permitido gestionar según su rol.

  ¿Por qué? Actúa como una barrera de seguridad. Si el usuario no tiene locales asignados, devuelve una lista vacía de inmediato, evitando consultas innecesarias a la base de datos.

- Definición de la Consulta Base (QuerySet)

  ```python
  queryset = Order.objects.filter(establishment_id__in=allowed_est_ids).select_related(
      'table', 'establishment'
  )
  ```

  ¿Qué hace? Construye el queryset inicial filtrando por los establecimientos permitidos.

  Optimización (select_related): Carga en la misma consulta los datos de la mesa y del local. Esto previene el problema N+1, mejorando el rendimiento de la base de datos al realizar un JOIN en lugar de consultar cada tabla por separado al serializar.

- Filtro por Establecimiento

  ```Python
  requested_est_id = request.GET.get('establishment_id')

  if requested_est_id and requested_est_id.isdigit():
  parsed_est_id = int(requested_est_id)
  if parsed_est_id in allowed_est_ids:
  queryset = queryset.filter(establishment_id=parsed_est_id)
  ```

  ¿Qué hace? Verifica si en los parámetros de la URL viene el campo establishment_id.

  Seguridad: Confirma que sea un número entero y comprueba que esté dentro de los establecimientos permitidos para ese usuario. Previene que un usuario intente acceder a datos de otros establecimientos modificando la URL.

- Filtro por Rango de Tiempo

  ```python
  requested_days = request.GET.get('days')

  if requested_days and requested_days.isdigit():
      time_limit = timezone.now() - timedelta(days=int(requested_days))
      queryset = queryset.filter(placed_at__gte=time_limit)
  ```

  ¿Qué hace? Procesa el parámetro days desde la petición GET.

  Cálculo: Resta la cantidad de días indicados a la fecha actual y filtra todos los pedidos cuya fecha de creación (placed_at) sea posterior o igual a ese límite.

- Orden y Serialización
  ```Python
  orders_sorted = queryset.order_by('-placed_at')
  return OrderSerializer(orders_sorted, request=request).json_response()
  ```
  ¿Qué hace? Ordena de forma descendente los pedidos por fecha de creación (los más recientes primero) y utiliza el serializador para retornar la respuesta HTTP en formato JSON.

##### \_get_order_details_for_role

Esta función sirve para obtener los detalles de un pedido específico

- est_ids = \_get_est_ids_by_role(request.user, role): Llama al helper que ya conocemos para obtener los IDs de los establecimientos a los que el usuario tiene acceso según el rol actual.

- order = get_object_or_404(Order, pk=order_id, establishment_id\_\_in=est_ids): Busca el pedido en la base de datos usando su clave primaria (pk=order_id): Utiliza establishment_id\_\_in=est_ids como filtro. Si el usuario intenta acceder a un pedido de un establecimiento que no puede gestionar, Django lanzará un error 404 (Pedido no encontrado) en lugar de mostrar información confidencial.

- order_details = order.details.select_related('product'): Accede a las líneas del pedido (order.details) y utiliza select_related('product') para cargar el producto asociado en la misma consulta SQL, evitando el problema N+1.

- return OrderDetailSerializer(order_details, request=request).json_response(): Serializa la colección de detalles y retorna el resultado en formato JSON listo para el frontend.

##### \_advance_order

Esta función tiene como cometido centralizar el flujo de los pedidos en la aplicación. Su propósito es cambiar el estado de un pedido (INITIATED → IN_PROGRESS → DONE)

- est_ids = \_get_est_ids_by_role(request.user, role): Obtiene la lista de establecimientos permitidos para el usuario según el rol que ejecuta (ya sea camarero o cocinero). Si el usuario no tiene locales asignados, devuelve un error 403 Forbidden.

- Recuperación del pedido

  ```Python
  try:
      order = Order.objects.get(id=order_id, establishment_id__in=est_ids)
  except Order.DoesNotExist:
      return JsonResponse({'error': 'Pedido no encontrado.'}, status=404)
  ```

  Qué hace: Intenta buscar el pedido en la base de datos que coincida con el ID proporcionado y que pertenezca a uno de los establecimientos a los que el usuario tiene acceso.

  Seguridad: Si el pedido no existe o pertenece a otro local, lanza un error 404 Not Found en lugar de exponer información confidencial.

- Transiciones de estados

  ```Python
  if order.status == Order.Status.INITIATED:
  order.status = Order.Status.IN_PROGRESS
  elif order.status == Order.Status.IN_PROGRESS:
  order.status = Order.Status.DONE
  order.closed_at = timezone.now()
  else:
  return JsonResponse({'error': 'Este pedido no se puede avanzar.'}, status=400)
  ```

  Qué hace: Evalúa el estado actual del pedido y lo avanza al siguiente paso lógico:

  Si está en INITIATED (Iniciado), pasa a IN_PROGRESS (En proceso).

  Si está en IN_PROGRESS, pasa a DONE (Completado) y registra automáticamente la hora de cierre (closed_at).

  Si el estado es cualquier otro (por ejemplo, ya está completado o cancelado), devuelve un error 400 Bad Request.

- Guardado y Respuesta

  ```Python
  order.save()
  return JsonResponse(...)
  ```

  Qué hace: Guarda los cambios en la base de datos y devuelve un mensaje de confirmación legible para el frontend con el nuevo estado y su traducción.

##### \_get_active_order_for_table(table, establishment)

Esta función sirve para determinar si una mesa tiene un pedido en curso que aún no ha sido cobrado. Es la base para saber si una mesa está ocupada o libre en el sistema.

Order.objects.filter(...): Inicia la consulta a la base de datos filtrando por los siguientes criterios:

- table=table: Busca los pedidos asociados a esa mesa específica.

- establishment=establishment: Asegura que el pedido pertenezca al establecimiento actual (seguridad multi-tenant).

- status\_\_in=[...]: Filtra por estados en los que el pedido sigue "vivo" (Iniciado, En Progreso, o Terminado en cocina pero no cobrado).

- .exclude(paid=True): Descarta cualquier pedido que ya haya sido pagado anteriormente, independientemente de su estado.

- .first(): Devuelve el primer resultado encontrado (un objeto Order), o en su defecto None. Se usa porque una mesa no debería tener más de un pedido activo a la vez.

#### Manager y camarero: Pedidos

- list_manager_orders(request)
- get_order_details(request, order_id: int)
- list_waiter_orders(request)
- get_waiter_order_details(request, order_id: int)

  Estos cuatro endpoints sirven como puntos de acceso a la API para los roles de Manager y Camarero (Waiter). Su única función es validar la petición HTTP (GET) y garantizar que el usuario esté autenticado mediante el decorador @auth_required, delegando el resto de la lógica de negocio y seguridad a las funciones privadas \_list_orders_for_role y \_get_order_details_for_role, pasándoles el rol correspondiente. De este modo, aseguran que cada usuario acceda de forma segura y optimizada únicamente a los pedidos y tickets de los establecimientos que tiene permiso para gestionar.

#### Mesas

##### <span style="color: #ffff00;">waiter_tables(request)</span>

Esta función tiene como objetivo listar todas las mesas del establecimiento, mostrar su estado actual (libre, pendiente, en progreso, terminado) y adjuntar la información del pedido si la mesa está ocupada.

- Obtención del Establecimiento

  ```Python
  establishment = _get_primary_establishment(request.user, 'waiter')
  if not establishment:
      return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)
  ```

  ¿Qué hace? Busca el local principal del camarero. Si no hay ninguno asignado, devuelve un error 403 (Prohibido) para evitar que vea información de la sala.

- Obtención de las Mesas

  ```Python
  tables = establishment.tables.filter(active=True).order_by('number')
  ```

  ¿Qué hace? Trae todas las mesas activas de ese establecimiento y las ordena por número. Realiza una única consulta a la base de datos.

- Obtención Optimizada de Pedidos Activos

  ```Python
  active_orders = Order.objects.filter(
      establishment=establishment,
      status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS, Order.Status.DONE],
      paid=False,
  ).annotate(items_count=Count('details'))
  ```

  ¿Qué hace? Busca todos los pedidos que siguen activos y sin pagar para el local.

  Optimización (annotate): Cuenta cuántos platos tiene cada pedido a nivel de base de datos antes de cargarlos en memoria. Esto evita tener que consultar los detalles de cada pedido uno por uno más adelante.

- Creación del Mapa en Memoria

  ```Python
  active_orders_map = {order.table_id: order for order in active_orders}
  ```

  ¿Qué hace? Convierte el resultado anterior en un diccionario de Python en la RAM, utilizando el ID de la mesa como clave.

  ¿Por qué? Permite al sistema encontrar el pedido de una mesa al instante en milisegundos, sin necesidad de hacer más peticiones a la base de datos.

- Definición del Mapa de Estados

  ```Python
  STATUS_MAP = {
      Order.Status.INITIATED: 'pending',
      Order.Status.IN_PROGRESS: 'in_progress',
      Order.Status.DONE: 'done',
  }
  ```

  ¿Qué hace? Mapea los estados internos de Django (números o constantes de la base de datos) a las cadenas de texto que el frontend (Vue) espera recibir. Elimina la necesidad de utilizar estructuras condicionales largas (if/elif).

- Construcción de los Datos de las Mesas

  ```Python
  tables_data = []
  for table in tables:
      active_order = active_orders_map.get(table.id)
      ...
  ```

  ¿Qué hace? Recorre cada mesa obtenida en el paso 2 y busca si existe un pedido en el mapa. Si lo hay, asigna los datos de la cuenta (total, productos, fecha, estado). Si no, marca la mesa como libre.

- Respuesta
  ```Python
  return JsonResponse(
      {
          'establishment': establishment.name,
          'tables': tables_data,
      }
  )
  ```
  ¿Qué hace? Devuelve un único diccionario en formato JSON que contiene el nombre del restaurante y la lista con todas las mesas procesadas.

##### <span style="color: #ffff00;">waiter_table_order(request, table_num)</span>

Esta función sirve para obtener el pedido activo de una mesa específica junto con todos sus detalles (los productos o platos que la componen).

- Obtención del Establecimiento

  ```Python
  establishment = _get_primary_establishment(request.user, 'waiter')
  if not establishment:
      return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)
  ```

  ¿Qué hace? Comprueba en qué establecimiento está trabajando el camarero actualmente. Si no está asignado a ningún local, devuelve un error 403 (Prohibido) por motivos de seguridad.

- Búsqueda Optimizada del Pedido

  ```Python
  active_order = (
      Order.objects.filter(
          table__number=table_num,
          establishment=establishment,
          status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS, Order.Status.DONE],
          paid=False,
      )
      .prefetch_related(
          Prefetch('details', queryset=OrderDetail.objects.select_related('product'))
      )
      .first()
  )
  ```

  ¿Qué hace? Busca el pedido activo para la mesa solicitada que no esté pagado (paid=False).

  Optimización (Uso de prefetch_related y Prefetch):

  Cruza la tabla Order directamente con la tabla de mesas usando el número (table\_\_number).

  Al mismo tiempo, precarga los detalles del pedido y los productos asociados. Esto significa que cuando leamos los datos más adelante, Python ya los tendrá en la memoria RAM y no volverá a consultar la base de datos (evitando el problema N+1).

- Manejo de Errores con Evaluación Perezosa

  ```Python
  if not active_order:
      if not establishment.tables.filter(number=table_num).exists():
          return JsonResponse({'error': 'Mesa no encontrada.'}, status=404)
      return JsonResponse({'order': None})
  ```

  ¿Qué hace? Si no encuentra ningún pedido activo:

  Solo en este caso, realiza una comprobación para ver si la mesa realmente existe en el establecimiento.

  Si la mesa no existe, devuelve un error 404.

  Si la mesa existe pero está libre (no tiene pedidos), devuelve un order: null, permitiendo que la interfaz del camarero sepa que la mesa está vacía.

- Construcción y Retorno de la Respuesta
  ```Python
  return JsonResponse(
      {
          'order': {
              'id': active_order.id,
              'status': active_order.status,
              'status_display': active_order.get_status_display(),
              'table_number': table_num,
              'placed_at': active_order.placed_at.isoformat(),
              'total': f'{active_order.total:.2f}',
              'paid': active_order.paid,
              'items': [
                  {
                      'id': d.id,
                      'product_name': d.product.name,
                      'price': f'{d.price:.2f}',
                      'quantity': d.quantity,
                      'notes': d.notes,
                  }
                  for d in active_order.details.all()
              ],
          }
      }
  )
  ```
  ¿Qué hace? Si hay un pedido activo, formatea toda la información en un diccionario y lo serializa en JSON. Utiliza los datos pre-cargados para iterar por los productos sin realizar consultas adicionales.

##### waiter_advance_order(request, order_id):

El endpoint waiter_advance_order actúa como punto de acceso para que los camareros puedan avanzar el estado de un pedido (requiere petición POST y está protegido por @auth_required y @csrf_exempt). Su única función es delegar la lógica de seguridad y el cambio de estado a la función interna \_advance_order indicando el rol de 'waiter', lo que permite mantener el código centralizado, seguro y reutilizable para otros roles operativos.

##### waiter_cancel_order(request, order_id):

Esta función permite al camarero cancelar un pedido que todavía se encuentra activo (en estado iniciado o en proceso)

- Validación de Permisos del Camarero

  ```Python
  est_ids = _get_est_ids_by_role(request.user, 'waiter')
  if not est_ids:
      return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)
  ```

  ¿Qué hace? Consulta a qué establecimientos tiene acceso el usuario con el rol de camarero. Si la lista está vacía, devuelve un error 403 (Prohibido).

- Recuperación del Pedido

  ```Python
  try:
      order = Order.objects.get(
          id=order_id,
          establishment_id__in=est_ids,
          status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS],
      )
  except Order.DoesNotExist:
      return JsonResponse({'error': 'Pedido no encontrado o ya cerrado.'}, status=404)
  ```

  ¿Qué hace? Busca en la base de datos el pedido mediante su ID, asegurando que pertenezca a los establecimientos del usuario y que se encuentre en un estado permitido para ser cancelado.

  Seguridad: Si no se cumplen las condiciones, lanza una excepción que es capturada para devolver un error 404.

- Actualización y Persistencia en Base de Datos

  ```Python
  order.status = Order.Status.CANCELLED
  order.closed_at = timezone.now()
  order.save()
  ```

  ¿Qué hace? Modifica las propiedades del objeto en la memoria RAM y posteriormente envía la consulta de guardado a la base de datos mediante .save().

- Respuesta Exitosa
  ```Python
  return JsonResponse({'message': 'Pedido cancelado.'})
  ```
  ¿Qué hace? Retorna una respuesta en formato JSON confirmando la cancelación de la comanda.

##### waiter_close_table(request, table_num)

Esta función sirve para cerrar una mesa en el sistema. Su propósito principal es finalizar el ciclo de vida del pedido en curso, marcándolo como pagado, actualizando su estado a completado y registrando la fecha y hora exacta en la que se cerró la cuenta.

- Obtención del Establecimiento Principal

  ```Python
  establishment = _get_primary_establishment(request.user, 'waiter')
  if not establishment:
      return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)
  ```

  ¿Qué hace? Verifica a qué establecimiento está vinculado el camarero. Si no hay un establecimiento principal asociado, devuelve un error 403 (Prohibido) por motivos de seguridad.

- Recuperación de la Mesa

  ```Python
  try:
      table = establishment.tables.get(number=table_num)
  except Table.DoesNotExist:
      return JsonResponse({'error': 'Mesa no encontrada.'}, status=404)
  ```

  ¿Qué hace? Busca la mesa solicitada (table_num) dentro del establecimiento del usuario.

  Seguridad y Validación: Si la mesa no existe en ese local, devuelve un error 404 (No encontrado) en lugar de exponer datos de otras ubicaciones.

- Obtención del Pedido Activo

  ```Python
  active_order = _get_active_order_for_table(table, establishment)

  if not active_order:
      return JsonResponse({'error': 'No hay pedido activo en esta mesa.'}, status=400)
  ```

  ¿Qué hace? Utiliza la función auxiliar que ya conocemos para comprobar si existe un pedido activo y sin pagar en esa mesa.

  Control de flujo: Si no hay pedido activo, devuelve un error 400 (Petición incorrecta) ya que no hay nada que cerrar.

- Actualización del Pedido

  ```Python
  active_order.paid = True
  active_order.status = Order.Status.DONE
  active_order.closed_at = timezone.now()
  active_order.save()
  ```

  ¿Qué hace? Modifica las propiedades del objeto en memoria y persiste los cambios en la base de datos mediante .save():

  Pone el atributo paid a True.

  Define el estado final del pedido como completado (DONE).

  Guarda el momento exacto del cierre.

- Respuesta de Confirmación
  ```Python
  return JsonResponse(
      {
          'message': f'Mesa {table.number} cerrada. Total: {active_order.total:.2f}€',
          'total': f'{active_order.total:.2f}',
      }
  )
  ```
  ¿Qué hace? Devuelve un objeto JSON con un mensaje de éxito legible por el usuario y el monto total cobrado para la interfaz del frontend.

#### Kitchen

##### <span style="color: #ffff00;">kitchen_active_orders(request)</span>

Esta función es el punto de acceso para la pantalla de la cocina. Su objetivo es obtener todos los pedidos que se encuentran en preparación (iniciados o en progreso) y devolverlos junto con el detalle de los platos, las notas, y el estado de preparación de cada uno.

- Obtención del Establecimiento y Seguridad

  ```Python
  establishment = _get_primary_establishment(request.user, 'kitchen')
  if not establishment:
      return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)
  ```

  ¿Qué hace? Verifica a qué establecimiento está vinculado el usuario con rol de cocina. Si no hay ningún local asignado, devuelve un error 403 (Prohibido) por motivos de seguridad.

- Consulta a la Base de Datos

  ```Python
  orders = (
      Order.objects.filter(
          establishment=establishment,
          status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS],
      )
      .select_related('table')
      .prefetch_related('details__product')
      .order_by('placed_at')
  )
  ```

  ¿Qué hace? Filtra los pedidos de ese establecimiento cuyo estado sea iniciado o en proceso.

  Optimización implementada:

  select_related('table'): Une la tabla de mesas en una sola consulta para obtener el número de mesa.

  prefetch_related('details\_\_product'): Precarga los detalles de cada pedido y sus respectivos productos para evitar consultas adicionales al recorrerlos.

- Procesamiento de los Pedidos

  ```Python
  orders_data = []
  for order in orders:
      items = order.details.all()
      ready_count = items.filter(ready=True).count()
      total_count = items.count()
  ```

  ¿Qué hace? Recorre cada pedido para construir un formato adecuado para el frontend:

  Extrae todos los detalles del pedido con order.details.all().

  Calcula cuántos platos están marcados como listos (ready_count) y el total de platos (total_count).

- Construcción del JSON

  ```Python
      orders_data.append(
          {
              'id': order.id,
              'status': order.status,
              'status_display': order.get_status_display(),
              'table_number': order.table.number,
              'placed_at': order.placed_at.isoformat(),
              'total': f'{order.total:.2f}',
              'ready_count': ready_count,
              'total_count': total_count,
              'items': [
                  {
                      'id': d.id,
                      'product_name': d.product.name,
                      'quantity': d.quantity,
                      'notes': d.notes,
                      'ready': d.ready,
                  }
                  for d in items
              ],
          }
      )
  ```

  ¿Qué hace? Formatea cada elemento y lo añade a la lista que será enviada al frontend (Vue o la interfaz de cocina).

- Respuesta
  ```Python
  return JsonResponse(
      {
          'establishment': establishment.name,
          'orders': orders_data,
      }
  )
  ```
  ¿Qué hace? Retorna la respuesta en formato JSON de forma completamente segura con el nombre del establecimiento y todos los pedidos procesados.

##### kitchen_advance_order(request, order_id)

El endpoint kitchen_advance_order actúa como punto de acceso para que el personal de cocina pueda avanzar el estado de un pedido (requiere una petición POST y está protegido por los decoradores @auth_required y @csrf_exempt). Su única función es delegar toda la lógica de seguridad y el cambio de estado a la función interna \_advance_order, pasándole el rol de 'kitchen'. Esto permite mantener el código centralizado, seguro y reutilizable para operar los pedidos de manera eficiente en la cocina.

##### <span style="color: #ffff00;">kitchen_toggle_item(request, item_id)</span>

Esta función es el motor de control de preparación por plato en la pantalla de la cocina. Permite al personal marcar o desmarcar un plato específico (OrderDetail) como listo. Además, contiene lógica inteligente para avanzar el estado del pedido completo dependiendo de si todos los platos han sido preparados o no.

- Validación de Permisos

  ```Python
  est_ids = _get_est_ids_by_role(request.user, 'kitchen')
  if not est_ids:
      return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)
  ```

  ¿Qué hace? Verifica que el usuario tenga el rol de cocina y obtiene los establecimientos a los que tiene acceso. Si no está asignado a ninguno, devuelve un error 403 (Prohibido).

- Búsqueda del Plato (OrderDetail)

  ```Python
  try:
      item = OrderDetail.objects.select_related('order').get(
          id=item_id,
          order__establishment_id__in=est_ids,
          order__status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS],
      )
  except OrderDetail.DoesNotExist:
      return JsonResponse({'error': 'Plato no encontrado.'}, status=404)
  ```

  ¿Qué hace? Busca la línea del pedido (OrderDetail) por su ID.

  Seguridad y optimización: \* Usa select_related('order') para traer el pedido asociado de una sola vez, evitando consultas extra más adelante.

  Comprueba que el pedido pertenece al establecimiento del usuario y que aún se encuentra en un estado activo en la cocina.

- Conmutación del Estado

  ```Python
  item.ready = not item.ready
  item.save()
  ```

  ¿Qué hace? Invierte el valor del booleano ready (si estaba listo, pasa a pendiente, y viceversa) y lo guarda en la base de datos.

- Actualización del Estado del Pedido (de Iniciado a En Progreso)

  ```Python
  order = item.order

  if order.status == Order.Status.INITIATED:
      order.status = Order.Status.IN_PROGRESS
      order.save()
  ```

  ¿Qué hace? Si el pedido estaba recién creado (INITIATED) y la cocina marca un plato como listo, el pedido cambia automáticamente de estado a en proceso (IN_PROGRESS).

- Verificación de Pedido Completado

  ```Python
  all_ready = not order.details.filter(ready=False).exists()
  if all_ready:
      order.status = Order.Status.DONE
      order.closed_at = timezone.now()
      order.save()
  ```

  ¿Qué hace? Comprueba si quedan platos pendientes en el pedido (ready=False).

  ¿Por qué es inteligente? Si no hay ningún plato pendiente, asume que se han terminado de preparar todos los platos del pedido. Pasa el pedido a estado completado (DONE), registra la hora de cierre (closed_at) y guarda el cambio.

- Respuesta
  ```Python
  return JsonResponse(
      {
          'message': f'{"Listo" if item.ready else "Pendiente"}: {item.product.name}',
          'item_ready': item.ready,
          'order_status': order.status,
          'order_done': all_ready,
      }
  )
  ```
  ¿Qué hace? Devuelve un resumen en JSON para que el frontend actualice la interfaz de usuario en tiempo real (por ejemplo, cambiar el color del plato y del ticket si el pedido se ha completado).

##### kitchen_complete_order(request, order_id)

Esta función es el botón de "completar todo" en la pantalla de la cocina. Permite al personal marcar todos los platos pendientes de un pedido como listos de una sola vez (mediante una operación en lote o batch) y finaliza el estado del pedido automáticamente.

- Validación de Permisos

  ```Python
  est_ids = _get_est_ids_by_role(request.user, 'kitchen')
  if not est_ids:
      return JsonResponse({'error': 'No estás asignado a ningún establecimiento.'}, status=403)
  ```

  ¿Qué hace? Verifica que el usuario tenga el rol de cocina y obtiene los establecimientos a los que tiene acceso. Si no está asignado a ninguno, devuelve un error 403 (Prohibido).

- Recuperación del Pedido

  ```Python
  try:
      order = Order.objects.get(
          id=order_id,
          establishment_id__in=est_ids,
          status__in=[Order.Status.INITIATED, Order.Status.IN_PROGRESS],
      )
  except Order.DoesNotExist:
      return JsonResponse({'error': 'Pedido no encontrado.'}, status=404)
  ```

  ¿Qué hace? Busca el pedido por su ID asegurando que pertenezca a los establecimientos del usuario y que aún se encuentre en un estado activo (iniciado o en progreso). Si no se cumplen las condiciones, devuelve un error 404 (No encontrado).

- Actualización en Bloque (Batch Update)

  ```Python
  order.details.filter(ready=False).update(ready=True)
  order.status = Order.Status.DONE
  order.closed_at = timezone.now()
  order.save()
  ```

  ¿Qué hace? Modifica la base de datos de manera eficiente y rápida:

  update(ready=True): Busca todas las líneas del pedido que no estaban listas y las actualiza todas juntas en una sola instrucción SQL, en lugar de una por una.

  Cambia el estado del pedido a completado (DONE).

  Registra la fecha y hora de cierre (closed_at).

- Respuesta Exitosa

  ```Python
  return JsonResponse(
      {
          'message': f'Pedido #{order.id} completado.',
          'order_done': True,
      }
  )
  ```

  ¿Qué hace? Devuelve un mensaje de confirmación en formato JSON indicando al frontend que el pedido ha sido procesado exitosamente.

  💡 Detalle de la lógica de negocio
  Optimización: Al utilizar .update() en lugar de recorrer los elementos uno a uno llamando a .save(), se evita saturar la base de datos con múltiples consultas individuales. Es una acción muy eficiente para operaciones en lote.

#### Público: Crear pedido desde QR

##### create_public_order(request, establishment_cif)

Esta función es el punto de entrada público de tu API (por ejemplo, cuando un cliente escanea un código QR en una mesa y realiza un pedido sin iniciar sesión). Su objetivo es validar la solicitud, comprobar la existencia de los productos y crear el pedido completo en una sola transacción segura.

- Validación de Establecimiento y Mesa

  ```Python
  try:
      establishment = Establishment.objects.get(cif=establishment_cif)
  except Establishment.DoesNotExist:
      return JsonResponse({'error': 'Establecimiento no encontrado'}, status=404)

  table_num = request.payload.get('table')
  items = request.payload.get('items', [])
  # ... validación de existencia de la mesa
  ```

  ¿Qué hace? Busca el establecimiento por su CIF y extrae el número de mesa y los ítems del payload. Si el local o la mesa no existen, devuelve un error 404.

- Validación de Productos (Pre-evaluación)

  ```Python
  for item in items:
      product_id = item.get('product_id')
      try:
          product = establishment.products.get(pk=product_id, available=True)
          # ... suma de totales y adición a la lista temporal
      except Product.DoesNotExist:
          invalid_ids.append(product_id)
  ```

  ¿Qué hace? Recorre la lista enviada por el cliente. Comprueba si cada producto existe y está disponible en ese establecimiento.

  Ventaja de seguridad: Si un cliente intenta pedir un producto que no existe, el pedido continúa con el resto y los IDs inválidos se guardan en invalid_ids para avisar al frontend.

- Creación del Pedido y Guardado en Bloque (Bulk Create)

  ```Python
  order = Order.objects.create(
      establishment=establishment,
      table=table,
      total=total,
  )

  OrderDetail.objects.bulk_create(
      [
          OrderDetail(
              order=order,
              product=item['product'],
              quantity=item['quantity'],
              price=item['price'],
              notes=item['notes'],
          )
          for item in order_items
      ]
  )
  ```

  ¿Qué hace? Crea el pedido principal en la base de datos.

  Optimización (bulk_create): En lugar de hacer un bucle y guardar (.save()) cada detalle por separado, los añade todos juntos en una única consulta SQL masiva, lo que ahorra una cantidad enorme de recursos en la base de datos.

- Respuesta Exitosa

  ```Python
  response = {'ok': True, 'order_id': order.pk}
  if invalid_ids:
      response['skipped_product_ids'] = invalid_ids

  return JsonResponse(response, status=201)
  ```

  ¿Qué hace? Devuelve una respuesta 201 (Creado) junto con el ID del nuevo pedido y los IDs de los productos que se omitieron por no estar disponibles.

### URLs (orders/urls.py)

El archivo `orders/urls.py` define las rutas para las diferentes operaciones de pedidos según el rol del usuario:

- **Manager**: Rutas para listar pedidos del manager (`manager-orders/`) y ver detalles (`manager-orders/<int:order_id>/details/`).
- **Camarero (Waiter)**:
  - Listado de pedidos (`waiter-orders/` y detalles).
  - Gestión de mesas (`waiter/tables/`, `waiter/tables/<int:table_num>/order/`, `waiter/tables/<int:table_num>/close/`).
  - Gestión de estados de pedido (`waiter/orders/<int:order_id>/advance/`, `waiter/orders/<int:order_id>/cancel/`).
- **Cocina (Kitchen)**: Rutas para ver pedidos activos (`kitchen/orders/`), avanzar estado de pedido (`kitchen/orders/<int:order_id>/advance/`) y alternar el estado de preparación de un plato (`kitchen/items/<int:item_id>/toggle/`).
- **Público**: Ruta para que los clientes creen pedidos escaneando el QR (`public/<str:establishment_cif>/`).

---

## Users

### Views

#### Autenticación y Perfil

##### login(request)

Maneja la autenticación de los usuarios y devuelve un token de sesión junto con el perfil del usuario.

- **Validación de Credenciales**: Utiliza `authenticate` de Django para verificar `username` y `password`.
- **Gestión de Tokens**: Crea o recupera un `Token` para el usuario. Si se solicita `remember_me`, genera un token de larga duración.
- **Cookie Segura**: Establece el token en una cookie `HttpOnly` para prevenir ataques XSS, con configuración `samesite='Lax'`.
- **Respuesta Unificada**: Devuelve los datos del perfil (usando `MemberSerializer`) en la misma petición para evitar múltiples llamadas desde el frontend.

##### register(request)

Permite a los nuevos usuarios registrarse en la plataforma utilizando un código de invitación.

- **Validación de Campos**: Verifica que todos los campos requeridos estén presentes.
- **Validación de Invitación**: Busca la invitación por su ID y comprueba que no haya sido usada (`is_used=False`). Si es inválida, devuelve un error 400.
- **Creación de Usuario**: Crea el usuario base (`User`) y asocia su número de teléfono al perfil `Member` si se proporciona.
- **Asignación de Rol**: Crea una relación `Manage` para vincular al nuevo usuario con el establecimiento correspondiente y el rol definido en la invitación.
- **Invalidación de Invitación**: Marca la invitación como usada para que no pueda ser reutilizada.

##### logout(request)

Cierra la sesión del usuario autenticado.

- Elimina el token de la base de datos (`request.user.token.delete()`).
- Borra la cookie `auth_token` de la respuesta, invalidando la sesión en el frontend.

##### profile(request)

Devuelve los datos del perfil del usuario autenticado. Utiliza el decorador `@auth_required` para garantizar la seguridad.

### URLs (users/urls.py)

Define los endpoints de gestión de usuarios:

- `login/`: Iniciar sesión.
- `register/`: Registrar un nuevo usuario con invitación.
- `logout/`: Cerrar sesión.
- `profile/`: Obtener los datos del perfil del usuario actual.

---

## Establishments

### Views

#### Gestión de Establecimientos

##### establishments_list(request)

Devuelve la lista de establecimientos donde el usuario autenticado tiene el rol de Manager o forma parte del equipo.

##### establishment_detail, edit_establishment, add_establishment, delete_establishment

Endpoints CRUD (Crear, Leer, Actualizar, Borrar) para los establecimientos.

- **Seguridad**: Todos están protegidos por `@auth_required`, `@get_instance_or_404`, y `@require_role(Manage.Role.MANAGER)`, asegurando que solo los managers puedan modificar los datos.
- **add_establishment**: Al crear un local, automáticamente asigna al usuario creador como `MANAGER` del mismo en la tabla `Manage`.

##### toggle_establishment(request, establishment_cif)

Permite al manager abrir o cerrar (activar/desactivar) el establecimiento para recibir pedidos públicos de forma rápida.

#### Gestión de Mesas (Tables)

##### tables_list, table_detail, add_table, edit_table, delete_table, change_table_status

Endpoints para la administración de las mesas del restaurante.

- **Validación de Duplicados en add_table**: Al crear una mesa, verifica que no exista ya otra mesa con el mismo número en el establecimiento (`filter(number=form.cleaned_data['number']).exists()`).
- **Estado de Mesa en change_table_status**: Permite marcar una mesa como activa o inactiva (por ejemplo, si está fuera de servicio o reservada) mediante una inversión booleana (`table.active = not table.active`).

#### Gestión de Personal (Staff) y Permisos

##### staff_list, edit_staff, remove_staff

Endpoints para visualizar y gestionar a los empleados asignados a un local.

- **Protección de auto-modificación**: En `edit_staff` y `remove_staff`, verifica explícitamente que el manager no intente cambiar su propio rol o eliminarse a sí mismo (`if manage.member == request.user: return JsonResponse(...)`).

#### Invitaciones (Invitations)

##### generate_invitation(request)

Permite a un Manager generar un código temporal (invitación) para que un nuevo empleado se registre y se una a su equipo.

- **Verificación de Manager**: Confirma que el usuario que realiza la petición es realmente Manager de algún local.
- **Creación Segura**: Crea la invitación asociada al establecimiento y rol seleccionado.
- **Respuesta**: Devuelve un `invitation_id` (UUID) que el frontend utilizará para generar un código QR o enlace.

##### validate_invitation(request, invitation_id)

Valida si una invitación es correcta y aún no ha sido utilizada.

- **is_valid()**: Utiliza el método del modelo para comprobar la validez.
- **Datos de Pre-registro**: Si es válida, devuelve el nombre del establecimiento y el rol para mostrar una pantalla de registro personalizada al nuevo empleado.

### URLs (establishments/urls.py)

Estructura modular de endpoints para la gestión integral:

- **Base**: `establishments/` (listado y creación).
- **Invitaciones**: `invite/` y `invite/validate/<uuid>/`.
- **CRUD del Local**: `/<cif>/`, `/<cif>/edit/`, `/<cif>/toggle/`, etc.
- **Anidación de Productos**: Incluye las rutas de productos (`products.urls`) dentro del prefijo `/<cif>/products/`.
- **Mesas y Staff**: Rutas específicas bajo el prefijo del CIF del local (`/<cif>/tables/...` y `/<cif>/staff/...`).

---

## Products

### Views

#### Gestión de Productos

##### products_list, product_detail, add_product, edit_product, delete_product

Endpoints para gestionar el catálogo de productos de un establecimiento.

- **Seguridad y Ámbito**: Restringidos al local correspondiente (`establishment_cif`) y accesibles según el rol. Modificaciones (`add`, `edit`, `delete`) requieren rol de `MANAGER`.
- **Borrado en Cascada Seguro**: En `delete_product`, elimina explícitamente los componentes (recetas) asociados al producto antes de borrar el producto en sí (`product.components.all().delete()`).

##### upload_product_image(request, establishment_cif, product_id)

Permite subir una imagen para un producto específico.

- Extrae la imagen del objeto `request.FILES`.
- Devuelve la URL absoluta de la imagen (`request.build_absolute_uri()`) lista para ser mostrada en el frontend.

##### toggle_product_available(request, establishment_cif, product_id)

Activa o desactiva la disponibilidad de un producto (por ejemplo, si se agota en cocina) con una simple inversión de estado (`product.available = not product.available`).

#### Gestión de Ingredientes y Categorías

##### ingredients_list, ingredient_detail, add_ingredient, edit_ingredient, delete_ingredient

##### categories_list, add_category, edit_category, delete_category

Endpoints CRUD para los bloques de construcción del menú.

- En la creación y edición de ingredientes (`add_ingredient`, `edit_ingredient`), procesa dinámicamente la lista de alérgenos asociada utilizando `.set()` sobre la relación ManyToMany (`ingredient.allergens.set(...)`).

#### Alérgenos

##### allergens_list(request)

Ruta pública/global para obtener la lista maestra de alérgenos disponibles en el sistema (Gluten, Lácteos, etc.).

#### Componentes (Recetas de Productos)

##### components_list, add_component, delete_component

Gestionan la receta o composición de un producto en base a ingredientes.

- **Optimización**: `components_list` utiliza `select_related('ingredient')` para obtener los datos del ingrediente (nombre) en la misma consulta, optimizando la lectura.
- **Validación Cruzada**: En `add_component`, comprueba tanto la existencia del producto como la del ingrediente dentro del mismo establecimiento antes de vincularlos.

### URLs (products/urls.py)

Maneja las rutas relacionadas con el menú interno:

- **Productos**: `/`, `/add/`, `/<id>/`, `/<id>/image/`, `/<id>/toggle/`, etc.
- **Categorías**: `/categories/...`
- **Ingredientes**: `/ingredients/...`
- **Componentes**: Anidados bajo un producto específico (`/<id>/components/...`).

---

## Menu

### Views

Este módulo se centra en las vistas públicas que son accesibles sin necesidad de autenticación (por ejemplo, el menú digital o escaneo de QR).

##### public_tables(request, establishment_cif)

Devuelve la lista de mesas de un establecimiento específico que se encuentran activas (`active=True`). Si el establecimiento no existe, devuelve 404.

##### public_products(request, establishment_cif)

Muestra el catálogo público de productos de un establecimiento.

- **Filtro de Disponibilidad**: Filtra la consulta con `available=True` asegurando que el cliente no vea productos que están temporalmente agotados.
- **Uso del request en Serializer**: Pasa el objeto `request` al `ProductSerializer` para poder construir correctamente las URLs absolutas de las imágenes de los productos.

### URLs (menu/urls.py)

Rutas públicas para el menú digital:

- `/<cif>/tables/`: Listado de mesas activas.
- `/<cif>/products/`: Menú disponible para el cliente.
