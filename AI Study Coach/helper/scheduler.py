"""Windows 任务计划程序管理"""
import subprocess
import sys
from pathlib import Path

TASK_NAME = "HelperStudyReminder"


def setup_reminder(time: str = "09:00") -> bool:
    """注册每日提醒任务

    Args:
        time: 提醒时间，格式 HH:MM

    Returns:
        是否成功
    """
    if sys.platform != "win32":
        print("仅支持 Windows 系统")
        return False

    script_path = Path(__file__).parent.parent / "main.py"
    python_exe = sys.executable

    # 先删除旧任务（如果存在）
    subprocess.run(
        ["schtasks", "/delete", "/tn", TASK_NAME, "/f"],
        capture_output=True,
    )

    # 创建新任务
    result = subprocess.run(
        [
            "schtasks", "/create",
            "/tn", TASK_NAME,
            "/tr", f'"{python_exe}" "{script_path}" notify send',
            "/sc", "daily",
            "/st", time,
            "/f",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"✓ 已设置每日 {time} 提醒")
        print(f"  任务名称：{TASK_NAME}")
        print(f"  执行命令：{python_exe} {script_path} notify send")
        return True
    else:
        print(f"✗ 设置失败：{result.stderr}")
        return False


def remove_reminder() -> bool:
    """移除提醒任务"""
    if sys.platform != "win32":
        print("仅支持 Windows 系统")
        return False

    result = subprocess.run(
        ["schtasks", "/delete", "/tn", TASK_NAME, "/f"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"✓ 已移除提醒任务：{TASK_NAME}")
        return True
    else:
        print(f"✗ 移除失败：{result.stderr}")
        return False


def check_reminder() -> bool:
    """检查提醒任务是否存在"""
    if sys.platform != "win32":
        return False

    result = subprocess.run(
        ["schtasks", "/query", "/tn", TASK_NAME],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0
