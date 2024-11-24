from sqlalchemy import Table, ForeignKey
from sqlalchemy import Column
from models.base import Base


role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id",
           ForeignKey("roles.id"),
           primary_key=True
           ),
    Column("permission_id",
           ForeignKey("permissions.id"),
           primary_key=True
           ),
)
