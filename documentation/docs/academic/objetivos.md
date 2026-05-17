---
title: Objetivos
icon: lucide/target
---

# Objetivos del proyecto

## Objetivo general

Desarrollar una plataforma web de gestión integral para el sector de la hostelería que permita a bares, restaurantes y cafeterías digitalizar su carta, automatizar la toma de pedidos y coordinar el trabajo entre sala y cocina en tiempo real, sin necesidad de que el cliente final instale ninguna aplicación.

## Objetivos específicos

### Objetivos funcionales

1. **Permitir al cliente final realizar pedidos desde su propio móvil** escaneando un código QR colocado en la mesa, accediendo a la carta digital directamente desde el navegador y enviando la comanda a cocina sin intervención del camarero.
2. **Ofrecer al manager una herramienta completa de gestión** del establecimiento donde pueda configurar su carta (productos, ingredientes, alérgenos, categorías), administrar las mesas con sus códigos QR e invitar a su equipo a la plataforma.
3. **Proporcionar al camarero una vista de sala en tiempo real** que muestre el estado de cada mesa (libre, pendiente, en preparación, lista para cobrar), notifique los pedidos nuevos al instante y permita gestionar el cobro y cierre de mesa.
4. **Implementar una pantalla KDS (Kitchen Display System) para cocina** optimizada para uso táctil, que muestre los pedidos activos ordenados por antigüedad, permita marcar platos como listos individualmente o el pedido completo en bloque, y avance el estado del pedido de forma automática.
5. **Soportar la gestión simultánea de varios establecimientos** desde una única cuenta de manager.
6. **Implementar un sistema de invitaciones por código QR o enlace** para incorporar personal al equipo de un establecimiento concreto con el rol adecuado (camarero o cocinero).

### Objetivos no funcionales

1. **Seguridad**: implementar autenticación basada en cookies `HttpOnly` para mitigar ataques XSS, validación estricta de roles en cada endpoint del backend y aislamiento multi-tenant para que cada usuario solo pueda acceder a los datos de los establecimientos que le corresponden.
2. **Cumplimiento normativo**: integrar la lista oficial de los 14 alérgenos del **Reglamento UE 1169/2011** sobre información alimentaria al consumidor, así como cumplir con el **RGPD (UE 2016/679)** en el tratamiento de los datos personales.
3. **Multiplataforma sin instalación**: la aplicación debe funcionar correctamente en cualquier navegador moderno (Chrome, Safari, Firefox, Edge) tanto en móvil como en tablet u ordenador, sin requerir descargas ni instalaciones.
4. **Diseño responsive adaptado al rol**: panel del manager pensado para escritorio y tablet, vistas de camarero y cocina optimizadas para tablet, y menú del cliente final optimizado para móvil.
5. **Rendimiento**: tiempos de respuesta inferiores a 300 ms en los listados principales mediante el uso de optimizaciones de base de datos (`select_related`, `prefetch_related`, `bulk_create`) y soporte para varios cientos de pedidos en histórico sin degradación perceptible.
6. **Despliegue reproducible**: el sistema debe poder levantarse en cualquier servidor Linux con Docker en menos de 10 minutos a partir de un único script de despliegue.
7. **Internacionalización lista para crecer**: aunque la versión inicial está en castellano, la arquitectura permite añadir nuevos idiomas más adelante sin reescribir el frontend.

## Objetivos académicos

Como Trabajo de Fin de Ciclo del CFGS en **Desarrollo de Aplicaciones Web (DAW)** del IES Puerto de la Cruz, los objetivos académicos complementarios son:

1. Aplicar de forma integral los conocimientos adquiridos durante el ciclo: programación web (Python, Django, JavaScript, Vue 3), bases de datos relacionales (SQLite/PostgreSQL), diseño de interfaces, seguridad en aplicaciones web y despliegue en entornos de producción.
2. Trabajar de forma colaborativa en un equipo de tres personas usando un flujo Git con ramas por funcionalidad y revisiones de código.
3. Documentar el proyecto a un nivel adecuado para que un desarrollador externo pueda entender la arquitectura y contribuir.
4. Resolver un problema real del sector hostelero canario y validar la solución con potenciales usuarios reales (negocios locales).
