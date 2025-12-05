# en caso de ampliar mas rutas relacionadas con usuarios importar todo lo necesario de fastapi

tags = ["auth"]
prefix = "/auth"

auth_router: dict = {"prefix": prefix + "/jwt", "tags": tags}
register_router: dict = {"prefix": prefix + "", "tags": tags}
reset_password_router: dict = {"prefix": prefix + "", "tags": tags}
verify_router: dict = {"prefix": prefix + "", "tags": tags}
