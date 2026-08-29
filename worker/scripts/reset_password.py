"""Reset a D1 user's password without putting the password in shell history."""

import argparse
import getpass
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agriflow.security import hash_password


def _sql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def main() -> int:
    parser = argparse.ArgumentParser(description="Reset an AgriFlow D1 user password.")
    parser.add_argument("username")
    parser.add_argument(
        "--remote",
        action="store_true",
        help="Update the production D1 database (the default is the local database).",
    )
    args = parser.parse_args()

    password = getpass.getpass("New password: ")
    confirmation = getpass.getpass("Confirm new password: ")
    if password != confirmation:
        parser.error("passwords do not match")
    if len(password) < 8:
        parser.error("password must be at least 8 characters")

    runner = shutil.which("npx.cmd") or shutil.which("npx")
    if runner is None:
        parser.error("npx was not found")

    password_hash = hash_password(password)
    sql = (
        f"UPDATE users SET password_hash = {_sql_string(password_hash)} "
        f"WHERE username = {_sql_string(args.username)} RETURNING id, username, role"
    )
    command = [runner, "wrangler", "d1", "execute", "agriflow"]
    command.append("--remote" if args.remote else "--local")
    command.extend(["--command", sql])
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
