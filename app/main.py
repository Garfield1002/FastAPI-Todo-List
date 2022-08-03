from fastapi import APIRouter, Body, FastAPI, HTTPException, Path, Query

from app.redis import init_redis_pool
from app.service import TodoStore
from app.schemas import AllTodosSchema, IDSchema, ErrorMessage, TodoSchema


app = FastAPI()


@app.on_event("startup")
async def startup():
    print("Starting up...")
    app.state.redis = await init_redis_pool()
    app.state.todoStore = TodoStore(app.state.redis)


@app.on_event("shutdown")
async def shutdown():
    print("Shutting down...")
    await app.state.redis.close()


todo_router = APIRouter(prefix="/todo")


@app.get("/all", tags=["todo"])
async def get_todos():
    """
    Retrieve every todo item and return them, with their id.
    """
    todos = await app.state.todoStore.get_all()
    return {
        "todos": list(
            map(
                lambda id, todo: {"id": id, "todo": todo},
                todos,
                [await app.state.todoStore.get_item(todo) for todo in todos],
            )
        )
    }


@app.post(
    "/add",
    tags=["todo"],
    response_model=IDSchema,
    response_description="The id of the newly added todo item.",
)
async def add_todo(todo: TodoSchema):
    """
    Add a new todo item.
    """
    todo_id = await app.state.todoStore.add_item(todo.dict())
    return {"id": todo_id}


@app.post(
    "/update/{id}",
    tags=["todo"],
    response_model=IDSchema,
    response_description="The id of modified todo item.",
    responses={404: {"model": ErrorMessage, "description": "Todo item not found."}},
)
async def update_todo(
    id: str = Path(
        ...,
        regex=r"^todo\d+$",
        example="todo1",
        description="The id of the todo item to delete.",
    ),
    todo: TodoSchema = Body(),
):
    """
    Stores the given todo item in the store at the given id, replacing the previous one.
    """
    if await app.state.todoStore.does_item_exist(id):
        await app.state.todoStore.update_item(id, todo.dict())
        return {"id": id}
    else:
        raise HTTPException(
            status_code=404, content={"message": "Todo item not found."}
        )


@app.delete(
    "/delete/{id}",
    tags=["todo"],
    response_model=IDSchema,
    response_description="The id of the deleted todo item.",
    responses={404: {"model": ErrorMessage, "description": "Todo item not found."}},
)
async def delete_todo(
    id: str = Path(
        ...,
        regex=r"^todo\d+$",
        example="todo1",
        description="The id of the todo item to delete.",
    )
):
    """
    Delete the todo item with the given id.
    """
    if await app.state.todoStore.does_item_exist(id):
        await app.state.todoStore.delete_item(id)
        return {"id": id}
    else:
        raise HTTPException(
            status_code=404, content={"message": "Todo item not found."}
        )
