# Prueba Técnica para Emtelco

## Instrucciones de Instalación

### Ejecutar la API Localmente

La forma más sencilla de ejecutar la API es utilizando Docker. Sigue los pasos a continuación para construir y correr la imagen de Docker:

#### Construir la imagen Docker:
   
   docker build -t arodriguem/docker-django .

#### Correr el contenedor de Docker:

   docker run -p 8000:8000 arodriguem/docker-django

### Endpoints Disponibles Localmente

Una vez que la API esté corriendo, puedes acceder a los siguientes endpoints:

**Obtener la lista de vulnerabilidades del NIST:**

   URL: http://localhost:8000/api/

**Obtener la lista de vulnerabilidades de la API:**

   URL: http://localhost:8000/api/get/

**Marcar una vulnerabilidad como "fixeada":**

   URL: http://localhost:8000/api/fixed/

**Obtener la lista de vulnerabilidades no "fixeadas":**

   URL: http://localhost:8000/api/filtered/

**Obtener un resumen de las vulnerabilidades:**

   URL: http://localhost:8000/api/summary/

**Ver el reporte de cobertura de pruebas:**

   URL: http://localhost:8000/static/index.html

**Obtener una copia de los logs:**

   URL: http://localhost:8000/static/app.log

## Realizado por Alejandro Rodriguez 
