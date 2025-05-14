from fastapi import FastAPI, APIRouter, HTTPException
from configurations import collection
from database.model import Todo
from database.schema import all_tasks, individual_data
from bson import ObjectId

app = FastAPI()
router = APIRouter()


@router.get("/")
async def get_all_tasks():
    data = collection.find()
    return all_tasks(data)


@router.post("/")
async def create_task(new_task: Todo):
    task_dict = new_task.dict()
    result = collection.insert_one(task_dict)
    created_task = collection.find_one({"_id": result.inserted_id})
    return individual_data(created_task)


@router.put("/{id}")
async def update_task(id: str, updated_task: Todo):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_task.dict()}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    task = collection.find_one({"_id": ObjectId(id)})
    return individual_data(task)


@router.delete("/{id}")
async def delete_task(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    result = collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}


app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
