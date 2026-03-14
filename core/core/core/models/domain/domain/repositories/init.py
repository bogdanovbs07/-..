from repositories.image_repository import ImageRepository
from repositories.user_repository import UserRepository

__all__ = ["ImageRepository", "UserRepository"]

from repositories.image_repository import ImageRepository
from repositories.user_repository import UserRepository

__all__ = ["ImageRepository", "UserRepository"]

from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type, Optional, List
from core.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, **kwargs) -> ModelType:
        obj = self.model(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, id: int, **kwargs) -> Optional[ModelType]:
        obj = self.get_by_id(id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            self.db.commit()
            self.db.refresh(obj)
        return obj
    
    def delete(self, id: int) -> bool:
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

  from sqlalchemy.orm import Session
from models.image import Image
from repositories.base_repository import BaseRepository
from typing import Optional, List

class ImageRepository(BaseRepository[Image]):
    def __init__(self, db: Session):
        super().__init__(Image, db)
    
    def get_by_user_id(self, user_id: int) -> List[Image]:
        return self.db.query(Image).filter(Image.user_id == user_id).all()
    
    def get_by_filename(self, filename: str) -> Optional[Image]:
        return self.db.query(Image).filter(Image.filename == filename).first()

  from sqlalchemy.orm import Session
from models.user import User
from repositories.base_repository import BaseRepository
from typing import Optional

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
