from apps.auth.src.common.application.ports.identifier_port import Identifier
import uuid

class UUID_provider(Identifier):
   
    def create_id()->str:
       return str(uuid.uuid4())

