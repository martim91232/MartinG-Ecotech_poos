# EcoTech POOS

Aplicacion de consola en Python para administrar empleados. Permite registrar, listar, buscar, actualizar y eliminar empleados mediante un menu interactivo. El proyecto tambien contiene modelos de dominio para departamentos, proyectos y registros de tiempo....

## Estructura
- `src/presentacion`: distintos menus
- `main.py`: punto de entrada  para los menus de la aplicacion.
- `src/dominio/`: modelos de empleado, departamento, proyecto y registro de tiempo.
- 'src/servicios': autenticacion para usuario
- `src/persistencia/`: conexion a la base de datos, creacion de tablas y objetos de acceso a datos.
- `requirements.txt`: dependencias de Python.

## Requisitos

- Python 3 instalado y disponible como `python` en Git Bash.
- Git Bash en Windows.

La aplicacion usa SQLite por defecto, por lo que no hace falta instalar ni iniciar un servidor de base de datos. Tambien admite MySQL.

## Preparar el entorno en Git Bash

Ejecuta estos comandos desde la carpeta raiz del repositorio:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

Para salir del entorno virtual:

```bash
deactivate
```

## Configuracion de la base de datos

Sin configuracion adicional se usa SQLite y se crea `ecotech.db` dentro de la carpeta raiz del proyecto. La ruta no depende de la carpeta desde la que se ejecute la aplicacion. Al iniciar, la aplicacion crea la tabla de empleados si no existe.

Para configurar valores propios, copia `src/.env.example` como `src/.env` y edita sus variables. El motor predeterminado es SQLite (`DB_ENGINE=sqlite`). Para usar MySQL, configura `DB_ENGINE=mysql`, `DB_NAME`, `DB_HOST`, `DB_PORT`, `DB_USER` y `DB_PASSWORD`; la base de datos debe existir previamente. No publiques `src/.env` ni credenciales reales.

## Ejecutar

Con el entorno virtual activo y desde la raiz del repositorio:

```bash
python src/main.py
```

El menu principal permite entrar al menu de empleados, menu de departamentos, menu de proyectos y menus de registro de tiempo.

## Inicio de sesión

Al iniciar por primera vez se crea la cuenta administrativa:

```text
Usuario: admin
Contraseña: Admin123*
```

Después de iniciar sesión, una cuenta administradora selecciona `4` para abrir el menú principal. Para crear
Al registrar un empleado desde `Gestionar sistema`, también se crea
automáticamente su cuenta. Después, el empleado inicia sesión usando su correo
y la contraseña inicial `Empleado123*`.

Las cuentas iniciales de los empleados se crean automáticamente al iniciar la
aplicación. La contraseña inicial es `Empleado123*` y se puede usar con el
correo registrado del empleado, por ejemplo `fernanda.tapia@ecotech.cl`.

El menú autenticado muestra la ficha, los registros propios y la consulta de la
API e historial de indicadores para cualquier usuario. Si la API no responde,
se utiliza el último indicador guardado en la base local y se muestra claramente
su origen. Las cuentas con rol `admin` también pueden abrir el
menú de administración para gestionar departamentos, empleados, proyectos,
registros de tiempo, cuentas, gerentes y asignaciones de proyectos. Los
empleados pueden consultar y actualizar su ficha, consultar sus registros, ver
sus proyectos asignados y registrar horas únicamente en esos proyectos.

## Guardar cambios en GitHub

Ejecuta estos comandos desde la carpeta raiz del repositorio:

1. Revisar que archivos cambiaron:

```bash
git status
```

2. Preparar los cambios para guardarlos:

```bash
git add .
```

3. Crear un commit con un mensaje:

```bash
git commit -m "Describe aqui tus cambios"
```

4. Subir el commit a GitHub:

```bash
git push
```

El comando `git push` solo sube los cambios que ya fueron incluidos en un
commit. La base de datos `ecotech.db` se crea localmente al ejecutar
`python src/main.py` y no es necesario subirla a GitHub.
