import uuid 
from fastapi_users import schemas

# heredamos los esquemas de usuario utilizando fastapi-users, añadir si queremos mas aca
class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass