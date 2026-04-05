from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserProfileUpdate(BaseModel):
    height: Optional[float] = None
    weight: Optional[float] = None
    age: Optional[int] = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    height: Optional[float] = None
    weight: Optional[float] = None
    age: Optional[int] = None

class Login(BaseModel):
    email: EmailStr
    password: str

class ExerciseAdd(BaseModel):
    workout_id: str
    name: str
    sets: int
    reps: int
    weight: Optional[float] = None

class ExerciseResponse(BaseModel):
    id: str
    workout_id: str
    name: str
    sets: int
    reps: int
    weight: Optional[float] = None

class WorkoutNoteUpdate(BaseModel):
    notes: str

class WorkoutResponse(BaseModel):
    id: str
    user_id: str
    date: datetime
    notes: Optional[str] = None
    exercises: List[ExerciseResponse] = []

class GoalAdd(BaseModel):
    title: str
    target_date: Optional[datetime] = None

class GoalResponse(BaseModel):
    id: str
    user_id: str
    title: str
    target_date: Optional[datetime] = None
    is_completed: bool = False

class WeightMetric(BaseModel):
    weight: float
    date: datetime = Field(default_factory=datetime.utcnow)


