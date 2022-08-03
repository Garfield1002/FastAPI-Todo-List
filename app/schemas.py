from typing import Optional, Tuple
from enum import Enum
from pydantic import BaseModel, Field


class TodoStatus(str, Enum):
    todo = "todo"
    in_progress = "in progress"
    done = "done"


class TodoSchema(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "title": "Buy milk",
                "description": "For the cat.",
                "status": "todo",
            },
        }

    title: str = Field(...)
    description: Optional[str] = None
    status: TodoStatus = Field(TodoStatus.todo)


class IDSchema(BaseModel):
    class Config:
        schema_extra = {
            "example": "todo1",
        }

    id: str = Field(...)


class AllTodosSchema(BaseModel):
    class IDTodoSchema(BaseModel):
        id: str = Field(...)
        todo: TodoSchema = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "todos": [
                    {
                        "id": "todo1",
                        "todo": {
                            "title": "Buy milk",
                            "description": "For the cat.",
                            "status": "todo",
                        },
                    },
                    {
                        "id": "todo2",
                        "todo": {
                            "title": "Buy eggs",
                            "status": "done",
                        },
                    },
                    {
                        "id": "todo3",
                        "todo": {
                            "title": "Create todo app",
                            "status": "in progress",
                        },
                    },
                ],
            }
        }

    todos: list[IDTodoSchema] = Field(...)


class ErrorMessage(BaseModel):
    """
    Model for passing error messages.
    """

    class Config:
        schema_extra = {
            "example": {
                "message": "Todo item not found.",
            },
        }

    message: str = Field(...)
