
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.dependencies import get_roles_service
from app.roles.schemas import RoleSchema, RoleCreate
from app.roles.service import RolesService

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
)

# Получить все роли
@router.get("/", response_model=list[RoleSchema])
async def get_roles(
roles_service: Annotated[RolesService, Depends(get_roles_service)],
):
    try:
        roles = await roles_service.get_roles()
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return roles

# Получить одну роль по id
@router.get("/{role_id}", response_model=RoleSchema)
async def read_role(role_id: int, roles_service: Annotated[RolesService, Depends(get_roles_service)],):
    try:
        roles = await roles_service.get_role_by_id(role_id)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return roles

# Создать новую роль
@router.post("/", response_model=RoleSchema, status_code=status.HTTP_201_CREATED)
async def create_role(role: RoleCreate, roles_service: Annotated[RolesService, Depends(get_roles_service)]):
    try:
        roles = await roles_service.create_role(role)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return roles

# Обновить роль
@router.put("/{role_id}", response_model=schemas.Role)
def update_role(role_id: int, role: schemas.RoleUpdate, db: Session = Depends(get_db)):
    HTTPException(status_code=404, detail="Role not found")

# Удалить роль
@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(db_role)
    db.commit()
    return None
