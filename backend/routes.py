from fastapi import APIRouter, HTTPException, Depends
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from models import (UserCreate, UserResponse, UserProfileUpdate, 
                    ExerciseAdd, ExerciseResponse, WorkoutNoteUpdate, WorkoutResponse,
                    GoalAdd, GoalResponse, WeightMetric)
from database import get_db
from bson import ObjectId
import datetime
import bcrypt
from auth import get_current_user, create_access_token

router = APIRouter()

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hash_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password=password_bytes, hashed_password=hash_bytes)

def fix_id(doc):
    if doc:
        doc["id"] = str(doc.pop("_id"))
    return doc

# 1. Kullanıcı Kaydı
@router.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    db = get_db()
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "height": None,
        "weight": None,
        "age": None
    }
    result = await db.users.insert_one(new_user)
    created_user = await db.users.find_one({"_id": result.inserted_id})
    return fix_id(created_user)

# 2. Kullanıcı Girişi
@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_db()
    # OAuth2 uses "username" field, which we map to email conceptually.
    user = await db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token(data={"sub": str(user["_id"])})
    return {"access_token": token, "token_type": "bearer", "user_id": str(user["_id"])}

# 3. Egzersiz Ekleme
@router.post("/workouts/exercises", response_model=ExerciseResponse)
async def add_exercise(exercise: ExerciseAdd, current_user: dict = Depends(get_current_user)):
    db = get_db()
    if not ObjectId.is_valid(exercise.workout_id):
        raise HTTPException(status_code=400, detail="Invalid Workout ID format. Please provide a valid 24-character MongoDB hex ID.")
    
    # Ensure there's a workout entry representing this workout_id owned by this user
    await db.workouts.update_one(
        {"_id": ObjectId(exercise.workout_id), "user_id": current_user["id"]},
        {"$setOnInsert": {"date": datetime.datetime.utcnow(), "notes": ""}},
        upsert=True
    )
    
    new_exercise = exercise.dict()
    result = await db.exercises.insert_one(new_exercise)
    created_ex = await db.exercises.find_one({"_id": result.inserted_id})
    return fix_id(created_ex)

# 4. Antrenman Listeleme (Only Current User)
@router.get("/workouts", response_model=List[WorkoutResponse])
async def list_workouts(current_user: dict = Depends(get_current_user)):
    db = get_db()
    workouts_cursor = db.workouts.find({"user_id": current_user["id"]})
    workouts = []
    async for w in workouts_cursor:
        w_id = str(w["_id"])
        exercises_cursor = db.exercises.find({"workout_id": w_id})
        exs = []
        async for ex in exercises_cursor:
            exs.append(fix_id(ex))
        
        w["id"] = w_id
        w.pop("_id")
        w["exercises"] = exs
        workouts.append(w)
    return workouts

# 5. Egzersiz Detaylarını Gör
@router.get("/exercises/{id}", response_model=ExerciseResponse)
async def get_exercise(id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    ex = await db.exercises.find_one({"_id": ObjectId(id)})
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    # Restrict viewing if workout doesn't belong to them
    workout = await db.workouts.find_one({"_id": ObjectId(ex["workout_id"]), "user_id": current_user["id"]})
    if not workout:
        raise HTTPException(status_code=403, detail="Not authorized to view this exercise")

    return fix_id(ex)

# 6. Profil Bilgisi Güncelleme
@router.put("/users/profile")
async def update_profile(profile: UserProfileUpdate, current_user: dict = Depends(get_current_user)):
    db = get_db()
    update_data = {k: v for k, v in profile.dict().items() if v is not None}
    if not update_data:
        return {"message": "No data provided to update"}
        
    await db.users.update_one({"_id": ObjectId(current_user["id"])}, {"$set": update_data})
    return {"message": "Profile updated successfully"}

# GET Profil Bilgisi
@router.get("/users/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    db = get_db()
    user = await db.users.find_one({"_id": ObjectId(current_user["id"])})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["id"] = str(user["_id"])
    del user["_id"]
    if "password" in user:
        del user["password"]
    return user

# 7. Antrenman Notu Düzenleme
@router.put("/workouts/{id}/notes")
async def update_workout_notes(id: str, note_data: WorkoutNoteUpdate, current_user: dict = Depends(get_current_user)):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid Workout ID")
        
    result = await db.workouts.update_one(
        {"_id": ObjectId(id), "user_id": current_user["id"]}, 
        {"$set": {"notes": note_data.notes}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Workout not found or not owned by user")
    return {"message": "Notes updated successfully"}

# 8. Egzersiz Kaydını Silme
@router.delete("/exercises/{id}")
async def delete_exercise(id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid Exercise ID")
    
    ex = await db.exercises.find_one({"_id": ObjectId(id)})
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")

    workout = await db.workouts.find_one({"_id": ObjectId(ex["workout_id"]), "user_id": current_user["id"]})
    if not workout:
        raise HTTPException(status_code=403, detail="Not authorized to delete this exercise")

    await db.exercises.delete_one({"_id": ObjectId(id)})
    return {"message": "Exercise deleted successfully"}

# 9. Hedef Ekleme
@router.post("/goals", response_model=GoalResponse)
async def add_goal(goal: GoalAdd, current_user: dict = Depends(get_current_user)):
    db = get_db()
    new_goal = goal.dict()
    new_goal["user_id"] = current_user["id"]
    new_goal["is_completed"] = False
    result = await db.goals.insert_one(new_goal)
    created_goal = await db.goals.find_one({"_id": result.inserted_id})
    return fix_id(created_goal)

# GET Hedefleri Listeleme
@router.get("/goals", response_model=List[GoalResponse])
async def get_goals(current_user: dict = Depends(get_current_user)):
    db = get_db()
    cursor = db.goals.find({"user_id": current_user["id"]})
    goals = await cursor.to_list(length=100)
    return [fix_id(g) for g in goals]

# PUT Hedef Tamamlanma Durumu (Toggle)
@router.put("/goals/{id}/toggle")
async def toggle_goal(id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid Goal ID")
    goal = await db.goals.find_one({"_id": ObjectId(id), "user_id": current_user["id"]})
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    new_status = not goal.get("is_completed", False)
    await db.goals.update_one({"_id": ObjectId(id)}, {"$set": {"is_completed": new_status}})
    return {"message": "Goal toggled"}

# 10. Hedef Silme
@router.delete("/goals/{id}")
async def delete_goal(id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid Goal ID")
    result = await db.goals.delete_one({"_id": ObjectId(id), "user_id": current_user["id"]})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found or not authorized")
    return {"message": "Goal deleted successfully"}

# 11. Ağırlık Takibi
@router.post("/metrics/weight")
async def track_weight(metric: WeightMetric, current_user: dict = Depends(get_current_user)):
    db = get_db()
    new_metric = metric.dict()
    new_metric["user_id"] = current_user["id"]
    result = await db.metrics.insert_one(new_metric)
    return {"message": "Weight recorded successfully", "id": str(result.inserted_id)}

# GET Ağırlık Takibi Geçmişi
@router.get("/metrics/weight")
async def get_weight_history(current_user: dict = Depends(get_current_user)):
    db = get_db()
    cursor = db.metrics.find({"user_id": current_user["id"]}).sort("date", 1)
    metrics = await cursor.to_list(length=100)
    for m in metrics:
        m["id"] = str(m["_id"])
        del m["_id"]
    return metrics

# 13. Antrenman Silme
@router.delete("/workouts/{id}")
async def delete_workout(id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid Workout ID format")
    workout = await db.workouts.find_one({"_id": ObjectId(id), "user_id": current_user["id"]})
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found or not authorized")
    await db.workouts.delete_one({"_id": ObjectId(id)})
    await db.exercises.delete_many({"workout_id": id})
    return {"message": "Workout and associated exercises deleted successfully"}

