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

### Ejecucion
Correr dev:
```bash
fastapi dev src/main.py
```
