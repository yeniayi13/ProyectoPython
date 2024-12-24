from sqlalchemy.orm import Session

class Base_repository():
    def __init__(self, session: Session):

        self.session = session