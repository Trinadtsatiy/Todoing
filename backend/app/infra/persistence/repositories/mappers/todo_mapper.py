from backend.app.domain.todos.todo import Todo, TodoContent, TodoId, TodoTitle
from backend.app.domain.users.user import UserId


def todo_from_dict_to_entity(adict: dict) -> Todo:
    return Todo(
        id=TodoId(adict["id"]),
        title=TodoTitle(adict["title"]),
        content=TodoContent(adict["content"]),
        owner_id=UserId(adict["owner_id"]),
        created_at=adict["created_at"],
        updated_at=adict["updated_at"],
    )
