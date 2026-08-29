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


async def list_users(env):
    result = await (
        env.DB.prepare(
            "SELECT id, username, role, created_at FROM users "
            "ORDER BY CASE WHEN role = 'master' THEN 0 ELSE 1 END, created_at DESC"
        ).all()
    )
    return result.results


async def get_user_summary(env, user_id: int):
    return (
        await env.DB.prepare(
            "SELECT id, username, role, created_at FROM users WHERE id = ?"
        )
        .bind(user_id)
        .first()
    )


async def update_user_password(env, user_id: int, password_hash: str):
    await (
        env.DB.prepare("UPDATE users SET password_hash = ? WHERE id = ?")
        .bind(password_hash, user_id)
        .run()
    )


async def update_user_role(env, user_id: int, role: str):
    await (
        env.DB.prepare("UPDATE users SET role = ? WHERE id = ?")
        .bind(role, user_id)
        .run()
    )
