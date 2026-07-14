#!/usr/bin/env python3
"""一键启动南京墙公网服务。

启动后会在后台运行：
  1. waitress (生产级 WSGI 服务器, DEBUG=False)
  2. cloudflared Quick Tunnel (公网隧道)

按 Ctrl+C 停止所有服务。
"""

import os
import re
import subprocess
import sys
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
VENV_PYTHON = PROJECT_DIR / "venv" / "Scripts" / "python.exe"
CLOUDFLARED = Path(os.environ.get("LOCALAPPDATA", "")) / ".." / "bin" / "cloudflared.exe"
CLOUDFLARED_ALT = Path("C:/Users/mj/bin/cloudflared.exe")
PORT = 8000
URL_PATTERN = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")


def find_cloudflared():
    for p in [CLOUDFLARED, CLOUDFLARED_ALT]:
        if p.exists():
            return str(p)
    result = shutil_which("cloudflared")
    if result:
        return result
    return None


def shutil_which(name):
    import shutil
    return shutil.which(name)


def main():
    cloudflared = find_cloudflared()
    if not cloudflared:
        print("[ERROR] cloudflared not found. Install it first.")
        return 1

    env = os.environ.copy()
    env["DEBUG"] = "False"

    print("[1/3] Starting waitress on port %d (DEBUG=False)..." % PORT)
    waitress = subprocess.Popen(
        [str(VENV_PYTHON), "-m", "waitress",
         "--listen=0.0.0.0:%d" % PORT,
         "nanjing_wall_project.wsgi:application"],
        cwd=str(PROJECT_DIR),
        env=env,
    )
    time.sleep(2)

    config_file = PROJECT_DIR / ".cloudflare-tunnel" / "cloudflared-empty.yml"
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text("", encoding="utf-8")

    print("[2/3] Starting cloudflared Quick Tunnel...")
    tunnel = subprocess.Popen(
        [cloudflared, "--config", str(config_file),
         "tunnel", "--no-autoupdate", "--protocol", "http2",
         "--url", "http://localhost:%d" % PORT],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    public_url = None
    print("[3/3] Waiting for public URL...")
    deadline = time.time() + 120
    while time.time() < deadline:
        line = tunnel.stdout.readline()
        if not line:
            if tunnel.poll() is not None:
                print("[ERROR] cloudflared exited early")
                waitress.terminate()
                return 1
            time.sleep(0.2)
            continue
        line = line.strip()
        if line:
            print("  ", line)
        match = URL_PATTERN.search(line)
        if match:
            public_url = match.group(0)
        if "Registered tunnel connection" in line and public_url:
            break

    if not public_url:
        print("[ERROR] Did not get a public URL")
        waitress.terminate()
        tunnel.terminate()
        return 1

    print()
    print("=" * 60)
    print("  PUBLIC URL: %s" % public_url)
    print("  LOCAL URL:  http://localhost:%d" % PORT)
    print("  MODE:       DEBUG=False (production)")
    print("  Stop:       Press Ctrl+C")
    print("=" * 60)
    print()
    print("This URL works as long as this script is running.")
    print("URL will change if you restart this script.")
    print()

    try:
        while True:
            time.sleep(1)
            if waitress.poll() is not None:
                print("[WARN] waitress exited")
                break
            if tunnel.poll() is not None:
                print("[WARN] cloudflared exited")
                break
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        waitress.terminate()
        tunnel.terminate()
        try:
            waitress.wait(timeout=5)
        except subprocess.TimeoutExpired:
            waitress.kill()
        try:
            tunnel.wait(timeout=5)
        except subprocess.TimeoutExpired:
            tunnel.kill()
        print("Stopped.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
