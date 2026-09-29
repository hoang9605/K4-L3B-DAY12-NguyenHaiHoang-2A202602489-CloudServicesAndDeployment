"""Khởi động Compose với AGENT_API_KEY lấy từ .env của repo."""

import os
import shutil
import subprocess
from pathlib import Path

from dotenv import dotenv_values


repo_root = Path(__file__).resolve().parents[1]
api_key = dotenv_values(repo_root / ".env").get("AGENT_API_KEY")
if not api_key:
    raise SystemExit("Thiếu AGENT_API_KEY trong .env")

# Biến của shell ưu tiên hơn .env trong Compose; đặt lại key cho tiến trình này.
env = os.environ.copy()
env["AGENT_API_KEY"] = api_key
docker = shutil.which("docker")
if docker is None and os.name == "nt":
    docker = str(Path.home() / "AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe")
subprocess.run([docker or "docker", "compose", "up", "-d", "--build"], cwd=repo_root, env=env, check=True)
