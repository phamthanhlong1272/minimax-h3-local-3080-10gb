#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trợ lý kiểm tra phần cứng & khởi tạo môi trường ComfyUI + MiniMax H3 (8-step)
Tối ưu riêng cho cấu hình: Windows + NVIDIA RTX 3080 (10GB VRAM) + 32GB DDR5 RAM.

Cách dùng:
  python scripts/setup_helper.py check
  python scripts/setup_helper.py install-nodes --comfy-dir "D:\\ComfyUI"
  python scripts/setup_helper.py create-launcher --comfy-dir "D:\\ComfyUI"
"""

import argparse
import ctypes
import os
import shutil
import subprocess
import sys
from pathlib import Path

REQUIRED_NODES = [
    ("ComfyUI-GGUF", "https://github.com/city96/ComfyUI-GGUF.git"),
    ("ComfyUI-ClipProj", "https://github.com/nicolab28/ComfyUI-ClipProj.git"),
    ("ComfyUI-VDN-Minimax-H3", "https://github.com/monnky/ComfyUI-VDN-Minimax-H3.git"),
    ("ComfyUI-MiniMax-H3-Turbo", "https://github.com/larryvrh/ComfyUI-MiniMax-H3-Turbo.git"),
    ("ComfyUI-MiniMaxH3-Easy", "https://github.com/nkxx188/ComfyUI-MiniMaxH3-Easy.git"),
]

MODEL_SUBDIRS = [
    "models/unet",
    "models/diffusion_models",
    "models/text_encoders",
    "models/clip_projections",
    "models/vae",
    "models/loras",
    "models/vdn",
]


class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]


def check_system(target_path: Path) -> None:
    print("=== KIỂM TRA CẤU HÌNH HỆ THỐNG CHO MINIMAX H3 (10GB VRAM) ===")

    # 1. GPU & VRAM check
    nvidia_smi = shutil.which("nvidia-smi")
    if nvidia_smi:
        res = subprocess.run(
            [nvidia_smi, "--query-gpu=name,memory.total,memory.free,driver_version", "--format=csv,noheader"],
            capture_output=True,
            text=True,
        )
        if res.returncode == 0:
            print(f"[OK] GPU phát hiện: {res.stdout.strip()}")
        else:
            print("[WARN] Không đọc được thông tin từ nvidia-smi.")
    else:
        print("[ERROR] Không tìm thấy nvidia-smi trong PATH. Hãy kiểm tra NVIDIA Driver.")

    # 2. RAM & Pagefile check (Windows)
    if os.name == "nt":
        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
        ram_gb = stat.ullTotalPhys / (1024**3)
        commit_gb = stat.ullTotalPageFile / (1024**3)
        pagefile_gb = max(0.0, commit_gb - ram_gb)
        print(f"[INFO] RAM vật lý: {ram_gb:.1f} GB | Tổng Commit (RAM + Pagefile): {commit_gb:.1f} GB (~{pagefile_gb:.1f} GB Pagefile)")
        if commit_gb < 60:
            print(
                "[WARN] Tổng RAM + Pagefile đang dưới 60 GB! "
                "Nên mở rộng Windows Pagefile trên ổ SSD lên 32768 - 65536 MB (32-64 GB) để tránh văng ComfyUI."
            )
        else:
            print("[OK] Dung lượng RAM + Pagefile đạt mức an toàn (>= 60 GB).")

    # 3. Disk space check
    anchor = target_path.resolve().anchor or str(Path.cwd().resolve().anchor)
    usage = shutil.disk_usage(anchor)
    free_gb = usage.free / (1024**3)
    print(f"[INFO] Ổ đĩa ({anchor}) còn trống: {free_gb:.1f} GB")
    if free_gb < 55:
        print("[WARN] Ổ đĩa trống dưới 55 GB. Khuyến nghị dọn trống tối thiểu 60 GB trước khi tải model.")
    else:
        print("[OK] Dung lượng ổ đĩa trống đảm bảo.")


def install_nodes(comfy_dir: Path, python_exe: str | None) -> None:
    if not (comfy_dir / "main.py").exists():
        raise SystemExit(f"[ERROR] Không tìm thấy main.py trong {comfy_dir}. Hãy truyền đúng thư mục gốc ComfyUI.")

    for sub in MODEL_SUBDIRS:
        p = comfy_dir / sub
        p.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Đã tạo/xác nhận các thư mục models chuẩn trong {comfy_dir / 'models'}")

    custom_nodes = comfy_dir / "custom_nodes"
    custom_nodes.mkdir(parents=True, exist_ok=True)

    py = python_exe or sys.executable
    for name, url in REQUIRED_NODES:
        dest = custom_nodes / name
        if dest.exists():
            print(f"[UPDATE] Đang cập nhật {name}...")
            subprocess.run(["git", "-C", str(dest), "pull"], check=False)
        else:
            print(f"[CLONE] Đang tải {name} từ {url}...")
            subprocess.run(["git", "clone", url, str(dest)], check=True)

        req_file = dest / "requirements.txt"
        if req_file.exists():
            print(f"[PIP] Cài đặt requirements cho {name} bằng {py}...")
            subprocess.run([py, "-m", "pip", "install", "-r", str(req_file)], check=False)

    print("\n[HOÀN TẤT] Đã cài đặt xong bộ Custom Nodes tối ưu cho MiniMax H3 10GB VRAM.")


def create_launcher(comfy_dir: Path) -> None:
    portable_py = comfy_dir.parent / "python_embeded" / "python.exe"
    if portable_py.exists():
        launcher_path = comfy_dir.parent / "run_minimax_h3_3080_10gb.bat"
        content = (
            "@echo off\r\n"
            "title ComfyUI - MiniMax H3 (RTX 3080 10GB Optimized)\r\n"
            ".\\python_embeded\\python.exe -s ComfyUI\\main.py --windows-standalone-build --use-sage-attention --reserve-vram 1.0\r\n"
            "pause\r\n"
        )
    else:
        launcher_path = comfy_dir / "run_minimax_h3_3080_10gb.bat"
        content = (
            "@echo off\r\n"
            "title ComfyUI - MiniMax H3 (RTX 3080 10GB Optimized)\r\n"
            "python -s main.py --use-sage-attention --reserve-vram 1.0\r\n"
            "pause\r\n"
        )

    launcher_path.write_text(content, encoding="utf-8")
    print(f"[OK] Đã tạo file khởi chạy tối ưu tại: {launcher_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Setup Helper cho MiniMax H3 trên RTX 3080 10GB")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="Kiểm tra GPU, RAM, Pagefile và dung lượng ổ cứng")
    p_check.add_argument("--path", type=Path, default=Path.cwd(), help="Đường dẫn ổ đĩa dự kiến cài đặt")

    p_nodes = sub.add_parser("install-nodes", help="Tạo cây thư mục models và cài 5 Custom Nodes chuẩn")
    p_nodes.add_argument("--comfy-dir", type=Path, required=True, help="Đường dẫn tới thư mục ComfyUI (chứa main.py)")
    p_nodes.add_argument("--python", type=str, default=None, help="Đường dẫn tới python.exe của ComfyUI (nếu dùng Portable/venv)")

    p_launch = sub.add_parser("create-launcher", help="Tạo file .bat khởi chạy ComfyUI tối ưu cho 3080 10GB")
    p_launch.add_argument("--comfy-dir", type=Path, required=True, help="Đường dẫn tới thư mục ComfyUI (chứa main.py)")

    args = parser.parse_args()
    if args.cmd == "check":
        check_system(args.path)
    elif args.cmd == "install-nodes":
        install_nodes(args.comfy_dir, args.python)
    elif args.cmd == "create-launcher":
        create_launcher(args.comfy_dir)


if __name__ == "__main__":
    main()
