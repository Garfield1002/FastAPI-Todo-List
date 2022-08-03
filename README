# To-Do List API

This simple project was made to learn how to use [Redis](https://redis.io/), [FastAPI](https://fastapi.tiangolo.com/) and integrate them together.

It was not made to necessarily be extremely efficient, but it was made to be simple and easy to use and understand.

## ✅ Usage

This project relies on docker-compose. To start the containers run:

```bash
docker-compose up -d --build
```

## 📚 Explanation

This project is made up of two docker containers:

- `todo-redis`: A simple redis server
- `todo-api`: A custom FastAPI server

### 🏗 Redis Architecture

There are two special redis keys that are used in this project:

- "todoId": A simple counter that is used to generate unique ids for todo items
- "todoIdsSet": A [set](https://redis.io/docs/manual/data-types/#sets) that contains all the todo ids

The items can then be added by incrementing the `todoId` key and adding the id to the `todoIdsSet` set. Then the contents of the todo item can be stored in a redis hash with the `todo{id}` as the key.

### ⚙ Todo-API

> The API was built without using [Redis OM](https://github.com/redis/redis-om-python) in order to understand the Redis commands, for a serious project I would recommend using it.

The application is split into 4 files:

- `todo-api/schemas.py`: This file contains [Pydantic](https://pydantic-docs.helpmanual.io/) schemas for the API, these are used to validate data, as well as provide quick documentation through the use of examples.

- `todo-api/redis.py`: This file contains a single file responsible for the connection to the redis server and initializing `todoId` if it doesn't exist.

- `todo-api/service.py`: This file contains the logic for the API, it is responsible for creating, updating, and deleting todo items with the appropriate redis commands.

- `todo-api/main.py`: This file FastAPI app, as well as the route handlers for the API.

## License

MIT License
