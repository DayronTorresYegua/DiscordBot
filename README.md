# Detalles del proyecto

Jinhsi Bot es un bot de Discord diseñado para recopilar, unificar y presentar información relevante sobre un videojuego desde diversas fuentes en línea. El objetivo principal del proyecto es proporcionar a los jugadores acceso rápido y centralizado a datos sin necesidad de visitar múltiples páginas web.

El bot servirá como un asistente automatizado dentro de un servidor de Discord, permitiendo a los usuarios obtener información actualizada sobre el juego mediante comandos específicos. Esto facilitará el acceso a estadísticas, noticias, eventos, guías y otros datos relevantes sin salir de la plataforma de Discor

# Preguntas a Responder

## Ciclo de vida del dato (5b)
1. ¿Cómo se gestionan los datos desde su generación hasta su eliminación en tu proyecto?
   - En mi proyecto, gestiono los datos siguiendo un ciclo donde primero creo manualmente un archivo JSON con la información de los personajes, luego mi bot los procesa al iniciar convirtiéndolos en un diccionario en Python, después los distribuye mediante comandos que los filtran y formatean, y finalmente los muestra en Discord usando embeds con campos organizados; por ahora, no he implementado un sistema automático para eliminar o actualizar los datos.
2. ¿Qué estrategia sigues para garantizar la consistencia e integridad de los datos?
   - Mi estrategia de consistencia se basa en validar los datos al leerlos con manejo de excepciones, usar una estructura coherente y predefinida para cada personaje, permitir búsquedas sin importar mayúsculas o minúsculas, verificar la existencia de los campos antes de acceder a ellos y generar respuestas predeterminadas cuando no se encuentran datos para evitar errores.
3. Si no trabajas con datos, ¿cómo podrías incluir una funcionalidad que los gestione de forma eficiente?

## Almacenamiento en la nube (5f)
1. Si tu software utiliza almacenamiento en la nube, ¿cómo garantizas la seguridad y disponibilidad de los datos?
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

## Implicación de las THD en negocio y planta (2e)
1. ¿Qué impacto tendría tu software en un entorno de negocio o en una planta industrial?
2. ¿Cómo crees que tu solución podría mejorar procesos operativos o la toma de decisiones?
3. Si tu proyecto no aplica directamente a negocio o planta, ¿qué otros entornos podrían beneficiarse?
   - Los usuarios de Discord podrían beneficiarse de mi bot al acceder de manera rápida y organizada a información del juego dentro de un servidor, evitando la necesidad de buscar en múltiples fuentes. Con solo usar un comando, podrían obtener detalles sobre personajes, facilitando el intercambio de información dentro de la comunidad.

## Mejoras en IT y OT (2f)
1. ¿Cómo puede tu software facilitar la integración entre entornos IT y OT?
2. ¿Qué procesos específicos podrían beneficiarse de tu solución en términos de automatización o eficiencia?
3. Si no aplica a IT u OT, ¿cómo podrías adaptarlo para mejorar procesos tecnológicos concretos?
   - Las adaptaciones posibles incluyen un sistema de alertas que notifique sobre parámetros operativos críticos, una interfaz de consulta para acceder a informes técnicos o manuales detallados, un asistente de mantenimiento predictivo basado en patrones de consulta, un sistema de documentación dinámica que actualice procedimientos según la experiencia, y un canal automatizado de comunicación entre sistemas de monitoreo y equipos de respuesta.

## Tecnologías Habilitadoras Digitales (2g)
1. ¿Qué tecnologías habilitadoras digitales (THD) has utilizado o podrías integrar en tu proyecto?
2. ¿Cómo mejoran estas tecnologías la funcionalidad o el alcance de tu software?
3. Si no has utilizado THD, ¿cómo podrías implementarlas para enriquecer tu solución?
   - Podría implementar un sistema de procesamiento de lenguaje natural para consultas más libres como "¿Quién es mejor para daño Fusion?", análisis de datos para identificar los personajes más populares y ampliar su información, integración con servicios web para actualizar estadísticas de personajes automáticamente, implementación de webhooks para notificar actualizaciones del juego, y el desarrollo de una interfaz web de administración para gestionar los datos de personajes sin necesidad de editar el archivo JSON directamente.