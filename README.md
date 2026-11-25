# Amigo Secreto automatizado en Python

El presente proyecto no es nada más que un script en Python que realiza "El sorteo del amigo secreto" y envía los resultados mediante correo electrónico.

La lógica es bastante sencilla, recibe un json con los correos y nombres de los participantes, luego, toma los correos (puesto que son irrepetibles) y los "desordena" aleatoriamente para crear un nuevo diccionario, el cual tiene como clave el correo de quien regala, y como valor, el correo de quién le sigue en la "lista desordenada", dejando al último "regalador" asignado al primero (es decir, la lógica de regalo es circular una vez se desordena la lista). Dicho algoritmo tiene una complejidad de O(n) en tanto cada estrcutura de datos se recorre una sola vez, al mismo tiempo que la lista rotación circular garantiza que nadie se regale a sí mismo. En el siguiente diagrama se aprecia mejor el funcionamiento

1. Lista Original 2. Lista "Desordenada" 3. Círculo de Regalos
   ┌───────────────┐ ┌───────────────┐  
   │ 1. Ana │ │ 1. Carlos │ [ Carlos ]
   │ 2. Beto │ ──▶ │ 2. Beto │ ──▶ ↗ ↘
   │ 3. Carlos │ │ 3. Ana │ [ Ana ] ◀─── [ Beto ]
   └───────────────┘ └───────────────┘

Si bien este proyecto es reinventar la rueda, el verdadero valor reside en que además de ser auditable, está pensado para ser autoalojado (Self-hosted) por las siguientes razones:

- **Privacidad**: Los correos nunca pasan por servidores de terceros, se envían directamente desde la cuenta de Gmail que elija el usuario para dicho fin, en tanto las direcciones de los participantes no son susceptibles a ser vendidos a empresas de spam.
- **Sin spoilers** El sorteo y el envío ocurren en segundo plano, sin logs para que el organizador no se entere de quién le tocó a quién.
- **Permisos mínimos** Se utiliza únicamente el alcance scope y gmail.send por lo que el código solo tiene acceso a mandar tus correos, mas no a leer ni modificar tu bandeja de entrada.

## Requisitos

1. Tener Python 3.10 en adelante instalado.
2. Una cuenta de Gmail desde la cual enviarás los correos.

## Configuración de credenciales.

1. Ve a [Google Cloud Console](https://console.cloud.google.com/) y crea un proyecto nuevo.
2. En el menú lateral, ve a **APIs y servicios > Biblioteca**, busca **Gmail API** y haz clic en **Habilitar**.
3. Ve a **APIs y servicios > Pantalla de consentimiento de OAuth**:
   - Selecciona tipo **Externo** y completa los campos obligatorios (nombre de la app y tu correo).
   - En **Permisos (Scopes)**, agrega `.../auth/gmail.send`.
   - En **Usuarios de prueba**, agrega tu propia dirección de Gmail.
4. Ve a **APIs y servicios > Credenciales**:
   - Haz clic en **Crear credenciales > ID de cliente de OAuth**.
   - Selecciona **App de escritorio** (_Desktop app_).
   - Descarga el archivo JSON, renómbralo a `credentials.json` y colócalo en la raíz de este proyecto.

## Instalación y uso

### 1. Clona el repositorio

Abre tu terminal y descarga el proyecto en tu computadora:

git clone [https://github.com//.git](https://github.com//.git)
cd amigo-secreto

### 2. Crea un entorno virtual e instala las dependencias.

**Windows:**
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

\*\*macOS/Linux:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 3. Crea el archivo de participantes (nómbralo participantes.json)

{
"ana.garcia@gmail.com": "Ana",
"beto.perez@hotmail.com": "Beto",
"carlos.ruiz@gmail.com": "Carlos",
"diana.lopez@yahoo.com": "Diana"
}

### 4. Ejecuta el sorteo.

python amigo_secreto.py
