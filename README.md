## Hackactivistas - Proyectos
Somos un movimiento voluntario de activistas de la información al servicio de una sociedad abierta, nuestra base se fundamenta en la transparencia y colaboración a partir de la integración cultural.

Si te sientes identificado únete a nuestro movimiento.

Nuestro objetivo : Impulsar un sistema de Gobernación Abierta, desde la interdisciplinaria entre hackactivistas, el gobierno y la sociedad civil.

![Arquitectura](arquitectura-hackactivista.png)

## PROYECTOS:

### Diagnóstico de COVID19 con IA - COVIDNetPerú 
Asistencia inteligente para el diagnóstico automatizado de COVID19 por radiografía.

### ChatCOVID19 

Orientación a la ciudadanía para el rápido despistaje vía chatbot.

### Kitchay CoronaVida 

Desarrollo de un kit de salvaguarda para la cuarentena.



### Requisitos:
- git
- pip3 
- virtualenv 
- python3.6.8 
- mongodb-4.0
- django2.2

### Instalacion de dependencias en S.O(ubuntu 18.04)

Si no tiene instalado pip y virtualenv
```
sudo apt update && sudo apt install python3-pip	&& sudo pip3 install virtualenv 
```

### Ejecución en modo desarrollo:

```
git@github.com:Hackactivistas/hackactivista.git
```
creación y activación de un entorno virtual
```
virtualenv -p python3 env_hackactivista && source env_hackactivista/bin/activate
```
```
cp hackactivista/config/example_config.json_copy hackactivista/config/develop.json && cd hackactivista
```
```
pip install -r requirements.txt
```
Confgurar su DB, antes de ejecutar las migraciones.. 

Ejecución de migraciones
```
./manage.py makemigrations && ./manage.py migrate
```
Creacion de super usuario
```
./manage.py createsuperuser
```
Ejecuación en modo desarrollo
```
 ./manage.py runserver
```


### Configuración de mongodb, opcional
Nota: El proyecto en desarrollo por defecto está configurado con SqlLite3
en terminal ejecutar
```
 use admin
```
```
 db.createUser( { user: "user_xxx", pwd: "passs_xxx", roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ] } )
```
habilitando autenticación
```
sudo nano /etc/mongod.conf
```

en bindIp: IP_PC_Interna o localhost 
```
security:
  authorization: "enabled" # Para autenticar o no "enabled" o "disabled"
```
```
sudo service mongod restart 
```

por último en config/develop.json, actualizar conexión a DB

### ¿Cómo puedo contribuir? 
Las contribuciones son las que hacen que la comunidad de código abierto sea un lugar increíble para aprender y aportar. Cualquier contribución que haga es muy apreciada.

Este proyecto existe gracias a todas las personas que contribuyen. [[Contribuidores](CONTRIBUTING.md)]


Opcion 1: Contáctenos a [+51983679449](https://api.whatsapp.com/send?phone=51938438089&text=Hola,%20quiero%20ser%20contribuidor%20en%20github%20de%20hackactivistas.!), le daremos acceso como contribuidor para comprometerte libremente.

Opcion 2: Bifurca el proyecto
Crea tu rama de características ( git checkout -b develop)

Compromete tus cambios ( git commit -m 'Add some AmazingFeature')

Empujar a la rama ( git push origin develop)

Abrir una solicitud de extracción

### Referencias:
[referencia COVIDNet](https://github.com/lindawangg/COVID-Net)
