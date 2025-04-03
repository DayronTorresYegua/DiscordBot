# Project details

Jinhsi Bot is a Discord bot designed to collect, unify and present relevant information about a video game from various online sources. The main goal of the project is to provide players with quick and centralised access to data without the need to visit multiple web pages.

The bot will serve as an automated assistant within a Discord server, allowing users to obtain up-to-date information about the game through specific commands. This will facilitate access to statistics, news, events, guides and other relevant data without leaving the Discord platform.

Jinhsi Bot still on developtment so there might be some parts that are not implemented yet.

# Preguntas a Responder

## Ciclo de vida del dato (5b)
1. ¿Cómo se gestionan los datos desde su generación hasta su eliminación en tu proyecto?
   - En mi proyecto, gestiono los datos siguiendo un ciclo donde primero creo manualmente un archivo JSON con la información de los personajes, luego mi bot los procesa al iniciar convirtiéndolos en un diccionario en Python, después los distribuye mediante comandos que los filtran y formatean, y finalmente los muestra en Discord usando embeds con campos organizados; por ahora, no he implementado un sistema automático para eliminar o actualizar los datos.
2. ¿Qué estrategia sigues para garantizar la consistencia e integridad de los datos?
   - Mi estrategia de consistencia se basa en validar los datos al leerlos con manejo de excepciones, usar una estructura coherente y predefinida para cada personaje, permitir búsquedas sin importar mayúsculas o minúsculas, verificar la existencia de los campos antes de acceder a ellos y generar respuestas predeterminadas cuando no se encuentran datos para evitar errores.
3. Si no trabajas con datos, ¿cómo podrías incluir una funcionalidad que los gestione de forma eficiente?
   - No aplica

## Almacenamiento en la nube (5f)
1. Si tu software utiliza almacenamiento en la nube, ¿cómo garantizas la seguridad y disponibilidad de los datos?
   - No usa almacenamiento en la nube
2. ¿Qué alternativas consideraste para almacenar datos y por qué elegiste tu solución actual?
   - Elegí JSON porque se adapta bien a los datos estáticos de los personajes, permite una estructura clara que organiza sus propiedades, no necesita configurar una base de datos, es fácil de leer y modificar manualmente, y se integra de forma natural con Python usando sus bibliotecas estándar.
3. Si no usas la nube, ¿cómo podrías integrarla en futuras versiones?
   - Podría usar almacenamiento en la nube con una base de datos NoSQL como Firebase para sincronización en tiempo real, MongoDB Atlas para escalabilidad, AWS Lambda con DynamoDB para gestión automática, una API REST con autenticación para modificar datos desde fuera o un sistema de versionado en Git para controlar cambios en mis JSON.

## Seguridad y regulación (5i)
1. ¿Qué medidas de seguridad implementaste para proteger los datos o procesos en tu proyecto?
   - He implementado un control de acceso basado en roles para comandos administrativos como >clear, asegurando que solo los usuarios autorizados puedan ejecutarlos y evitando que personas no autorizadas eliminen mensajes del canal. El rol en cuestión es el de 'Admin'.
2. ¿Qué normativas (e.g., GDPR) podrían afectar el uso de tu software y cómo las has tenido en cuenta?
   - Las normativas relevantes incluyen el RGPD si recopilara datos de usuarios europeos, los términos de servicio de Discord para cumplir con las restricciones de la API, las leyes de derechos de autor si usara imágenes o contenido del juego, las políticas de privacidad si almacenara datos de interacción y las regulaciones de protección al consumidor si el bot tuviera fines comerciales.
3. Si no implementaste medidas de seguridad, ¿qué riesgos potenciales identificas y cómo los abordarías en el futuro?
   - Existen medidas

## Implicación de las THD en negocio y planta (2e)
1. ¿Qué impacto tendría tu software en un entorno de negocio o en una planta industrial?
   - No aplica a ese entorno
2. ¿Cómo crees que tu solución podría mejorar procesos operativos o la toma de decisiones?
   - No aplica para ese proposito
3. Si tu proyecto no aplica directamente a negocio o planta, ¿qué otros entornos podrían beneficiarse?
   - Los usuarios de Discord podrían beneficiarse de mi bot al acceder de manera rápida y organizada a información del juego dentro de un servidor, evitando la necesidad de buscar en múltiples fuentes. Con solo usar un comando, podrían obtener detalles sobre personajes, facilitando el intercambio de información dentro de la comunidad.

## Mejoras en IT y OT (2f)
1. ¿Cómo puede tu software facilitar la integración entre entornos IT y OT?
   - No aplica a entorno IT/OT
2. ¿Qué procesos específicos podrían beneficiarse de tu solución en términos de automatización o eficiencia?
   - No aplica
3. Si no aplica a IT u OT, ¿cómo podrías adaptarlo para mejorar procesos tecnológicos concretos?
   - Las adaptaciones posibles incluyen un sistema de alertas que notifique sobre parámetros operativos críticos, una interfaz de consulta para acceder a informes técnicos o manuales detallados, un asistente de mantenimiento predictivo basado en patrones de consulta, un sistema de documentación dinámica que actualice procedimientos según la experiencia, y un canal automatizado de comunicación entre sistemas de monitoreo y equipos de respuesta.

## Tecnologías Habilitadoras Digitales (2g)
1. ¿Qué tecnologías habilitadoras digitales (THD) has utilizado o podrías integrar en tu proyecto?
   - Podria intregar IA en el código para poder hacer recomendaciones en tiempo real en funcion de las necesidades del usuario
2. ¿Cómo mejoran estas tecnologías la funcionalidad o el alcance de tu software?
   - Mejoraría la experiencia de usuario
3. Si no has utilizado THD, ¿cómo podrías implementarlas para enriquecer tu solución?
   - Podría implementar un sistema de procesamiento de lenguaje natural para consultas más libres como "¿Quién es mejor para daño Fusion?", análisis de datos para identificar los personajes más populares y ampliar su información, integración con servicios web para actualizar estadísticas de personajes automáticamente, implementación de webhooks para notificar actualizaciones del juego, y el desarrollo de una interfaz web de administración para gestionar los datos de personajes sin necesidad de editar el archivo JSON directamente.


# Explicación

## Instalación

- Para poder instalar el bot de discord será necesario tener el enlace de invitación de este a un servidor de discord, el enlace es el siguiente:

```
https://discord.com/oauth2/authorize?client_id=1332374346294886470&permissions=0&integration_type=0&scope=bot
```

- Para poder hacer uso de este deberos introducir el token del bot de discord, ya sea dentro del código o dentro de una variable de entorno 

> Lo paso en el archivo txt adjunto a la tarea porque github restringe el pasar el token en el repositorio

- Una vez tenemos nuestro token para ejecutar el bot haremos uso del comando:
>python main.py

o de:
> python3 main.py


- Para hacer uso del bot dentro de el servidor de discord que tenga el bot haremos uso de el prefijo ">" para despues introducir el nombre de el comando 

- EJ: ">help" que es un comando que muestra la informacion de los comandos disponibles en el bot
