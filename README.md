# Ciclo Request - Response

## Contexto de aplicación en Flask

- Los contextos se utilizan para realizar un seguimiento de los datos necesarios para ejecutar una operación de software. Los `contextos en Flask son un mecanismo que nos permite acceder a ciertas variables globalmente`.
- Proporcionan los datos necesarios durante el procesamiento de solicitudes y comandos CLI.

Flask __no acepta solicitud__ como primer argumento (objeto global), pero accedemos a la petición así:

        from flask import Flask, request

        app = Flask(__name__)
        @app.route('´/')
        def requesta_data():
            return f"Hola, Estás usando {request.user.agent}"

Flask usa contextos para hacer ciertas variables actúen como variables globales y cuando accedes a ellas obtienes acceso al objeto para el hilo actual. Estas variables se denominan thread-locals.

![](https://media.licdn.com/dms/image/C5612AQEzLoL_NayoMg/article-inline_image-shrink_1500_2232/0/1633089725586?e=1677715200&v=beta&t=foQ6FSCZ3Gkgl4NTCSQbo9bf347IWQ9Zokl2XrzGz4A)

- Cada vez que se recibe una solicitud en la aplicacion Flask, se generan 2 contextos:

1. __Contexto de Aplicación__: `Realiza el seguimiento de los datos a nivel de la aplicación`, como variables de configuración de la base de datos, información del registrador, etc.
Contiene objetos como __current_app y g.__ Los __current_app__ se refiere a la instancia que maneja la solicitud y `g` se usa para almacenar datos temporalmente durante la solicitud.
Una vez que se establece el valor, se puede acceder a el dentro de cualquier funcion de vista. Los datos almacenados en `g` se reestablecen despues de cada solicitud.

2. __Contexto de Solicitud__: realiza un seguimiento de los datos de nivel de solicitud como URL, métodos HTTP, encabezados de solicitud, datos de solicitud, sesión, etc.  Estos se exponen de manera similar a cómo el contexto de la aplicación expone current_app y g.
- El objeto de solicitud contiene la información sobre la solicitud actual y una sesión es un objeto similar a un diccionario que se usa para almacenar valores que persisten entre solicitudes.

## Manejo de Solicitudes - descripcion general

![](https://media.licdn.com/dms/image/C5612AQGLiWS5W6gTtQ/article-inline_image-shrink_1500_2232/0/1633091740616?e=1677715200&v=beta&t=2_-F03m9SnvQPmgYOiIIatJunwozoCzKI-gHGAbLu9Y)

- El `contexto de aplicacion y el contexto de solicitud se activan cuando el servidor de flask recibe una solicitud`.
- Cuando se inserta el contexto de aplicacion, todas las variables quedan expuestas al estad disponibles para el subproceso. 
- Y cuando se envía un contexto de solicitud, todas las variables expuestas quedan disponibles para el subproceso.
Así, dentro de las funciones de vistas, tendremos acceso a todos los objetos expuestos por aplicación y contexto de solicitud.

## Paso 1: 
- Comienza cuando el servidor recibe una solicitud

![](https://testdriven.io/static/images/blog/flask/flask-contexts/flask_request_processing_step1.png)

- El trabajo del servidor web es enrutar las solicitudes HTTP entrantes a un servidor  WSGI.

## Paso 2_
- Para procesar la solicitud, el servidor WSGI `genera una trabajador` para manejar la solicitud.
Así los worker son responsables de manejar esa única solicitud.

![](https://testdriven.io/static/images/blog/flask/flask-contexts/flask_request_processing_step2.png)

- El `trabajador (worker)` puede ser un subproceso o una rutina. 
ejm: Los trabajadores serían subprocesos si está utilizando el servidor de desarrollo de Flask con su configuracion predeterminada.


## Paso 3: Contextos.
- Una vez que la ejecución cambia a la aplicacion Flask, Flask crea los contextos de aplicacion y solicitud y los inserta en sus respectivas pilas.

![](https://testdriven.io/static/images/blog/flask/flask-contexts/flask_request_processing_step3.png)

- Para repasar, el contexto de aplicación almacena datis de nivel de la aplicacion, como las variables de configuración, la conexion a la base de datos y el registrador. Mientras que el contexxto de solicitud almacena datos específicos de la solicitud para generar una respuesta.
Ambas pilas se implementan como objetos globales(se aclara en el paso 4) 

## Paso 4:  Proxies
- En este paso, la aplicación Flask está lista para procesar los datos (en la funcion vista) y los datos están listos en la pilas de aplicacion y solicitud de contextos. Se necesita una forma de conectar estas 2 piezas, aquí entran los `proxies`.

![](https://testdriven.io/static/images/blog/flask/flask-contexts/flask_request_processing_step4.png)

- `Las funciones de visualización utilizan proxies para acceder` a la aplicación (almacenada en la pila de contexto de la aplicacion) y a los contextos de solicitud (almacenados en la pila de contexto de solicitud).

* `current_app`: proxy que accede al contexto de aplicacion para el worker
* `request`: proxy que accede al contexto de solicitud para el worker

Ambas pilas (contextos de aplicacion y contexto de solicitud) se implementan como `objetos locales`.

## Contextos Locales (Context Locals)
- Python maneja un concepto de `datos locales de subprocesos`; para almacenar datos especificos de un subproceso, que es a la vez seguro para subprocesos y exclusivo de subprocesos. Cada subproceso podrá acceder a los datos de manera segura y los datos siempre son únicos para el subproceso específico. 

- Flask implementa un comportamiento similar (__locales de contexto__), pero de una manera más genérica para `permitir que los worker sean subprocesos, procesos o rutinas`.
- Estos contextos locales se almacenan en `Werkzeug`.
. Cuando los datos se almacenan en un objeto local de contexto, los datos se almacenan de una manera que `solo un worker puede recuperar`. Si dos worker acceden a un objeto local de contexto, cada uno obtendrá sus propios datos específicos que únicos para cada worker.
 
- Para resumir, los proxies `current_app y request` están disponibles en cada función  de vista y se utilizan para acceder a los contextos desde sus respectivas pilas, que se almacenan como objetos locales de contexto.

## Beneficio de los proxies en Flask

        @app.route('/add_item', methods=['GET', 'POST'])
        def add_item(application_context, request_context):  # contexts passed in!
            if request_context.method == 'POST':
            # Save the form data to the database
            ...
            application_context.logger.info(f"Added new item ({ request_context.form['item_name'] })!")
 
- Flask proporciona proxies `current_app` y `request` que terminan pareciéndose a variables globales para una función de vista.

        from flask import current_app, request

        @app.route('/add_item', methods=['GET', 'POST'])
        def add_item():
            if request.method == 'POST':
            # Save the form data to the database
            ...
            current_app.logger.info(f"Added new item ({ request.form['item_name'] })!")

Al usar este enfoque, la función de vista no necesita que los contextos se pasen como argumentos.
- RECUERDA: Los proxies current_app y request sno son varaibles globales, apuntan a objetos globales que se implementan como locales de contexto.


## Paso 5: Limpiar
- Después de que se generan las respuestas, los contextos de solicitud y aplicación se extraen de sus respectivas pilas.

![](https://testdriven.io/static/images/blog/flask/flask-contexts/flask_request_processing_step5.png)

- __Este paso limpia las pilas__
- Luego las respuestas se envían al navegador web, que completa el manejo de esta solicitud.


