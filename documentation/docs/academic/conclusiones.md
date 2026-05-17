---
title: Conclusiones y trabajo futuro
icon: lucide/flag
---

# Conclusiones y trabajo futuro

## Conclusiones

MakeMenu es el resultado del Trabajo de Fin de Ciclo del CFGS en Desarrollo de Aplicaciones Web. Ha sido un proyecto extenso que nos ha permitido integrar la práctica totalidad de los conocimientos adquiridos durante el ciclo: programación con Python y JavaScript, frameworks web modernos (Django y Vue 3), bases de datos relacionales, diseño de interfaces, seguridad en aplicaciones web, contenedorización y despliegue.

### Cumplimiento de objetivos

Los objetivos planteados al inicio se han cumplido en su totalidad. La plataforma permite a un cliente final pedir desde su móvil sin instalar nada, ofrece un panel de gestión completo al manager, una vista en tiempo real al camarero y un KDS funcional para la cocina. El sistema soporta gestión multi-establecimiento, está internacionalizable y se despliega con un único script en menos de diez minutos.

A nivel técnico se han alcanzado los requisitos no funcionales más exigentes: las consultas críticas se sirven en menos de 300 ms gracias a las optimizaciones de Django (`select_related`, `prefetch_related`, `bulk_create`), la autenticación es resistente a XSS al no exponer el token al JavaScript del navegador, y el aislamiento multi-tenant está validado en cada endpoint del backend.

### Lecciones aprendidas

A lo largo del desarrollo nos enfrentamos a varios problemas que merece la pena destacar:

- **El problema N+1 al listar pedidos**: la primera implementación del listado de pedidos del camarero hacía una consulta por cada mesa para obtener su pedido activo. Con un local de 20 mesas, eso eran 21 consultas. La refactorización a un único `Order.objects.filter(...).annotate(items_count=Count('details'))` y un diccionario en memoria por `table_id` redujo la latencia de la vista de sala de ~600 ms a menos de 80 ms.
- **Decisión sobre dónde guardar el token de sesión**: la primera versión guardaba el token en `localStorage`. Tras revisar las recomendaciones de OWASP sobre XSS, decidimos migrar a una cookie `HttpOnly`. El cambio implicó reescribir el cliente Axios para usar `withCredentials: true` y ajustar las cabeceras CORS del backend, pero el resultado es claramente más seguro.
- **Coordinación entre vistas de camarero y cocina**: el avance automático del estado del pedido cuando la cocina marca el último plato como listo evita un paso manual y fricción innecesaria. Es una de las micro-decisiones de UX más comentadas positivamente cuando enseñamos el producto a hosteleros.
- **Notificaciones de pedidos nuevos**: implementar polling fue la decisión pragmática. Considerar WebSockets habría supuesto añadir un broker de mensajes y reescribir toda la capa de comunicación, sin un beneficio claro para el caso de uso (la vista activa de un camarero rara vez está abierta más de 8 horas seguidas).

### Limitaciones conocidas

Reconocer las limitaciones forma parte del rigor del proyecto. Las más relevantes son:

- **Base de datos SQLite**: adecuada para la Fase 1 (un piloto con pocos locales) pero no recomendable para escalar. La migración a PostgreSQL está prevista cuando se supere el primer local productivo.
- **Polling cada 10 segundos**: introduce hasta 10 segundos de latencia en la notificación de un pedido nuevo. Para la Fase 2 contemplamos sustituirlo por Server-Sent Events o WebSockets si los clientes reportan que el retardo es perceptible.
- **Pagos integrados**: la plataforma marca la mesa como "pagada" pero el cobro se realiza por medios externos (TPV físico o efectivo). Integrar pasarelas de pago (Redsys, Stripe) está en la hoja de ruta.
- **Cobertura de tests**: el backend cuenta con factorías de datos pero la suite de tests automatizados es limitada. Antes de pasar a producción para varios clientes hay que escribir tests unitarios y de integración que cubran al menos los flujos críticos (login, creación de pedido, avance de estados).
- **Internacionalización**: la arquitectura permite añadir idiomas, pero la versión actual está solo en castellano. El primer idioma adicional probable sería el inglés para servir a turistas internacionales en establecimientos canarios.

## Trabajo futuro

### Mejoras técnicas a corto plazo

1. **Cobertura de tests**: escribir tests unitarios para los helpers de `orders/views.py` (especialmente `_advance_order`, `_get_active_order_for_table`) y tests de integración para el flujo completo de un pedido.
2. **Migración a PostgreSQL**: preparada para la Fase 2. La estructura del backend ya es agnóstica a la BBDD (no usa funciones específicas de SQLite).
3. **Sustituir polling por SSE o WebSockets** en las vistas de camarero y cocina.
4. **Compresión y CDN para imágenes de producto**: actualmente se sirven sin procesar desde el volumen `media/`. Aplicar redimensionado al subir (con Pillow) y servir desde un CDN reduciría el peso de la carta digital.
5. **Auditoría de cambios**: registrar quién hizo qué (mediante una app `django-simple-history` o similar) para tener trazabilidad de las modificaciones en la carta o el equipo.

### Funcionalidades a medio plazo

1. **Pagos integrados** con Redsys (estándar bancario español) y Stripe (para pagos internacionales).
2. **Sistema de reservas** integrado con las mesas (cliente reserva → mesa marcada como reservada en un rango horario).
3. **Estadísticas y dashboard**: productos más vendidos, ticket medio, hora punta, rotación de mesas... Esta información ya está implícita en los datos, solo hay que exponerla en una vista.
4. **Multi-idioma en el menú público** para servir mejor al turismo internacional, especialmente relevante en Canarias.
5. **Comandas modificables**: hoy un cliente no puede modificar el pedido tras enviarlo (tiene que pedirle al camarero que lo cancele y rehacer). Permitir añadir productos a un pedido ya en marcha sería un caso de uso valioso.
6. **Notificaciones push al móvil del cliente** cuando su pedido está listo para recoger (en restaurantes self-service).

### Funcionalidades a largo plazo

1. **App de gestión nativa para iOS y Android** para el manager y el camarero, aprovechando notificaciones push del sistema y modo offline parcial.
2. **Marketplace de plantillas de cartas** para acelerar el onboarding de nuevos clientes (subir una carta tipo bar de tapas precargada y solo retocarla).
3. **Integración con software de contabilidad** (Holded, Quipu) para exportar tickets automáticamente.
4. **Modo franquicia** para cadenas, con jerarquía de permisos por encima del manager (responsable de zona, central corporativa).
5. **Análisis predictivo**: basándose en el histórico de pedidos, sugerir compras de aprovisionamiento o detectar patrones de demanda.

### Aspectos del modelo de negocio

Más allá del producto, hay frentes abiertos en el lado empresarial:

1. **Validación con clientes reales en Tenerife** durante la Fase 1 (captación directa). El feedback de los primeros 5-10 negocios marcará la hoja de ruta a 12 meses.
2. **Solicitud de inscripción en la Zona Especial Canaria (ZEC)** para acceder al tipo reducido del 4 % en el Impuesto de Sociedades.
3. **Búsqueda de subvenciones** para startups tecnológicas en Canarias (líneas del Cabildo, SODECAN, fondos europeos Next Generation).
4. **Constitución formal de la S.L.** una vez validado el modelo y captados los primeros 10 clientes de pago.
