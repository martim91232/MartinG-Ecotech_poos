# EcoTech POOS

Aplicacion de consola en Python para administrar empleados. Permite registrar, listar, buscar, actualizar y eliminar empleados mediante un menu interactivo. El proyecto tambien contiene modelos de dominio para departamentos, proyectos y registros de tiempo.

## Estructura
- `src/presentacion`: distintos menus
- `src/main.py`: punto de entrada  para los menus de la aplicacion.
- `src/dominio/`: modelos de empleado, departamento, proyecto y registro de tiempo.
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

Sin configuracion adicional se usa SQLite y se crea `ecotech.db` en la carpeta desde la que se ejecuta la aplicacion. Al iniciar, la aplicacion crea la tabla de empleados si no existe.

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

Después de iniciar sesión, selecciona `3` para abrir el menú principal. Para crear
otra cuenta, selecciona `2` antes de iniciar sesión e indica el ID de un empleado
que todavía no tenga usuario.

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
