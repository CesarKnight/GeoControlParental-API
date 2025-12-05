### Dependencias
1. Primero debes instalar uv, un package manager, de manera global
```bash
pip install uv
```

2. Una vez en el proyecto crear tu ambiente virtual con :
```bash
uv venv
```

3. Puedes asegurarte de activar tu ambiente virtual con:
```bash
.venv/Scripts/activate.ps1
```
4. instalar las dependencias con:
```bash
uv sync
```
5. Crear un archivo de variables de ambiente para los datos de DB y Secret para autenticacion (copia del ejemplo), en caos que no se tenga un secret se generará uno
6. Para usar DB de pruebas con docker levantar el contenedor con
```bash
docker compose up
```

### Ejecucion
Correr dev:
```bash
fastapi dev src/main.py
```
