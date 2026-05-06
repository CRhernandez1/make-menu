---
title: Documentación técnica
icon: lucide/code
---

# Documentación técnica

Esta sección está dirigida a desarrolladores que quieran entender, contribuir o desplegar la plataforma MakeMenu. Aquí se describe la arquitectura general del sistema, las tecnologías utilizadas y cómo están organizadas las diferentes capas de la aplicación.

## Stack tecnológico

MakeMenu está construido con tecnologías modernas, bien documentadas y ampliamente adoptadas en el sector:

| Capa          | Tecnología      |
| ------------- | --------------- |
| Backend       | Django (Python) |
| Frontend      | Vue.js          |
| Estilos       | Tailwind CSS    |
| Base de datos | SQLite          |
| Servidor web  | Nginx           |
| Contenedores  | Docker          |

## Backend (Django)

El backend está desarrollado con Django, un framework web de Python que sigue el patrón MVC. Se encarga de toda la lógica de negocio, la gestión de usuarios y roles, y expone una API REST que consume el frontend.

Entre sus responsabilidades principales están la autenticación y autorización por roles (manager, camarero, cocinero), la gestión de establecimientos, mesas, productos, ingredientes y pedidos, y la generación de los códigos QR por mesa.

Consulta el apartado [Backend](backend.md) para ver la estructura del proyecto, los endpoints disponibles y los modelos de datos.

## Frontend (Vue.js + Tailwind CSS)

La interfaz de usuario está construida con Vue.js, un framework JavaScript progresivo orientado a componentes. Los estilos se gestionan con Tailwind CSS, un framework de utilidades que permite construir interfaces consistentes y responsivas sin escribir CSS personalizado.

El frontend se comunica con el backend a través de la API REST y gestiona las vistas de cada rol: el panel de administración del manager, la vista de pedidos del camarero, la pantalla de cocina del cocinero y la carta digital del cliente.

Consulta el apartado [Frontend](frontend.md) para ver la estructura de componentes y las vistas disponibles.

## Base de datos (SQLite)

MakeMenu utiliza SQLite como base de datos. Es una solución ligera, sin necesidad de servidor separado, que se integra de forma nativa con Django y es suficiente para la fase actual del proyecto.

El esquema de la base de datos incluye las entidades principales: usuarios, establecimientos, mesas, productos, ingredientes, categorías y pedidos.

## Despliegue (Docker + Nginx)

La aplicación se despliega mediante Docker, lo que garantiza que el entorno de producción sea reproducible e independiente del sistema operativo del servidor. Nginx actúa como servidor web y proxy inverso, gestionando las peticiones entrantes y sirviendo los archivos estáticos del frontend.

Consulta el apartado [Despliegue](deploy.md) para ver el proceso completo de puesta en producción.
