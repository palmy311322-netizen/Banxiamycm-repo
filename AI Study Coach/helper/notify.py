"""Windows 系统通知"""
import sys
from pathlib import Path


def send_toast(title: str, message: str) -> bool:
    """发送 Windows 系统通知

    尝试顺序：WinRT（零依赖）→ winotify → print 降级
    返回是否成功发送
    """
    if sys.platform != "win32":
        print(f"[通知] {title}: {message}")
        return True

    # 方案 1：winotify（更稳定）
    try:
        from winotify import Notification
        toast = Notification(
            app_id="HelperStudyAssistant",
            title=title,
            msg=message,
            duration="short",
        )
        toast.set_audio("ms-winsoundevent:Notification.Reminder", loop=False)
        toast.show()
        return True
    except Exception:
        pass

    # 方案 2：降级到 print
    print(f"[通知] {title}: {message}")
    return False
