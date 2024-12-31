from enum import Enum

class Roles(Enum):
    SUPERADMIN = 'SUPERADMIN'
    MANAGER = 'MANAGER'
    CLIENT = 'CLIENT'

    @classmethod
    def list(cls):
        """Devuelve una lista de todos los roles."""
        return [role.value for role in cls]
