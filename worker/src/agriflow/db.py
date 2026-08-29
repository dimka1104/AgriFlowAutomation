async def get_user_by_username(env, username: str):
    return (
        await env.DB.prepare("SELECT * FROM users WHERE username = ?")
        .bind(username)
        .first()
    )


async def get_user_by_id(env, user_id: int):
    return (
        await env.DB.prepare("SELECT * FROM users WHERE id = ?")
        .bind(user_id)
        .first()
    )


async def create_user(env, username: str, password_hash: str, role: str):
    await (
        env.DB.prepare(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)"
        )
        .bind(username, password_hash, role)
        .run()
    )
    return await get_user_by_username(env, username)
