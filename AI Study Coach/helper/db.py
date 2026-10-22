"""数据库层：SQLite 模型与操作"""
import sqlite3
from pathlib import Path
from datetime import datetime, date
from typing import Optional
import json

DB_PATH = Path(__file__).parent.parent / "data.db"


def get_conn() -> sqlite3.Connection:
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """初始化数据库表结构"""
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            active INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            goal_id INTEGER NOT NULL REFERENCES goals(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            frequency TEXT DEFAULT 'daily',
            completed_count INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS daily_plans (
            id INTEGER PRIMARY KEY,
            plan_date TEXT NOT NULL UNIQUE,
            tasks_json TEXT NOT NULL,
            ai_suggestion TEXT,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY,
            plan_date TEXT NOT NULL,
            task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
            note TEXT,
            duration_minutes INTEGER,
            checked_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_checkins_date ON checkins(plan_date);
        CREATE INDEX IF NOT EXISTS idx_checkins_task ON checkins(task_id);
        CREATE INDEX IF NOT EXISTS idx_daily_plans_date ON daily_plans(plan_date);
    """)
    conn.commit()
    conn.close()


# ===== Goals =====

def add_goal(name: str, description: Optional[str] = None) -> int:
    """添加学习目标，返回 goal_id"""
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO goals (name, description, created_at) VALUES (?, ?, ?)",
        (name, description, datetime.now().isoformat())
    )
    conn.commit()
    goal_id = cur.lastrowid
    conn.close()
    return goal_id


def list_goals(active_only: bool = True) -> list[dict]:
    """列出所有目标"""
    conn = get_conn()
    if active_only:
        rows = conn.execute("SELECT * FROM goals WHERE active = 1 ORDER BY id").fetchall()
    else:
        rows = conn.execute("SELECT * FROM goals ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def archive_goal(goal_id: int) -> bool:
    """归档目标"""
    conn = get_conn()
    cur = conn.execute("UPDATE goals SET active = 0 WHERE id = ?", (goal_id,))
    conn.commit()
    conn.close()
    return cur.rowcount > 0


def get_goal(goal_id: int) -> Optional[dict]:
    """获取单个目标"""
    conn = get_conn()
    row = conn.execute("SELECT * FROM goals WHERE id = ?", (goal_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ===== Tasks =====

def add_task(goal_id: int, title: str, frequency: str = "daily") -> int:
    """添加任务，返回 task_id"""
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO tasks (goal_id, title, frequency, created_at) VALUES (?, ?, ?, ?)",
        (goal_id, title, frequency, datetime.now().isoformat())
    )
    conn.commit()
    task_id = cur.lastrowid
    conn.close()
    return task_id


def list_tasks(goal_id: Optional[int] = None) -> list[dict]:
    """列出任务"""
    conn = get_conn()
    if goal_id:
        rows = conn.execute(
            "SELECT t.*, g.name as goal_name FROM tasks t JOIN goals g ON t.goal_id = g.id WHERE t.goal_id = ? ORDER BY t.id",
            (goal_id,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT t.*, g.name as goal_name FROM tasks t JOIN goals g ON t.goal_id = g.id ORDER BY t.id"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_task(task_id: int) -> Optional[dict]:
    """获取单个任务"""
    conn = get_conn()
    row = conn.execute(
        "SELECT t.*, g.name as goal_name FROM tasks t JOIN goals g ON t.goal_id = g.id WHERE t.id = ?",
        (task_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ===== Daily Plans =====

def save_daily_plan(plan_date: str, tasks_json: list, ai_suggestion: Optional[str] = None):
    """保存每日计划"""
    conn = get_conn()
    conn.execute(
        """INSERT INTO daily_plans (plan_date, tasks_json, ai_suggestion, created_at)
           VALUES (?, ?, ?, ?)
           ON CONFLICT(plan_date) DO UPDATE SET
               tasks_json = excluded.tasks_json,
               ai_suggestion = excluded.ai_suggestion""",
        (plan_date, json.dumps(tasks_json, ensure_ascii=False), ai_suggestion, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_daily_plan(plan_date: Optional[str] = None) -> Optional[dict]:
    """获取每日计划"""
    if plan_date is None:
        plan_date = date.today().isoformat()
    conn = get_conn()
    row = conn.execute("SELECT * FROM daily_plans WHERE plan_date = ?", (plan_date,)).fetchone()
    conn.close()
    if row:
        d = dict(row)
        d["tasks_json"] = json.loads(d["tasks_json"])
        return d
    return None


# ===== Checkins =====

def add_checkin(task_id: int, note: Optional[str] = None, duration_minutes: Optional[int] = None, plan_date: Optional[str] = None) -> int:
    """添加打卡记录"""
    if plan_date is None:
        plan_date = date.today().isoformat()
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO checkins (plan_date, task_id, note, duration_minutes, checked_at) VALUES (?, ?, ?, ?, ?)",
        (plan_date, task_id, note, duration_minutes, datetime.now().isoformat())
    )
    # 更新任务完成次数
    conn.execute("UPDATE tasks SET completed_count = completed_count + 1 WHERE id = ?", (task_id,))
    conn.commit()
    checkin_id = cur.lastrowid
    conn.close()
    return checkin_id


def get_checkins_for_date(plan_date: Optional[str] = None) -> list[dict]:
    """获取某天的打卡记录"""
    if plan_date is None:
        plan_date = date.today().isoformat()
    conn = get_conn()
    rows = conn.execute(
        """SELECT c.*, t.title as task_title, g.name as goal_name
           FROM checkins c
           JOIN tasks t ON c.task_id = t.id
           JOIN goals g ON t.goal_id = g.id
           WHERE c.plan_date = ?
           ORDER BY c.checked_at""",
        (plan_date,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_recent_checkins(days: int = 7) -> list[dict]:
    """获取最近 N 天的打卡记录"""
    conn = get_conn()
    rows = conn.execute(
        """SELECT c.*, t.title as task_title, g.name as goal_name
           FROM checkins c
           JOIN tasks t ON c.task_id = t.id
           JOIN goals g ON t.goal_id = g.id
           WHERE c.plan_date >= date('now', ?)
           ORDER BY c.plan_date DESC, c.checked_at""",
        (f"-{days} days",)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_streak_for_goal(goal_id: int) -> int:
    """计算某个目标的连续打卡天数"""
    conn = get_conn()
    # 获取该目标下所有任务的打卡日期
    rows = conn.execute(
        """SELECT DISTINCT c.plan_date
           FROM checkins c
           JOIN tasks t ON c.task_id = t.id
           WHERE t.goal_id = ?
           ORDER BY c.plan_date DESC""",
        (goal_id,)
    ).fetchall()
    conn.close()

    if not rows:
        return 0

    dates = [r["plan_date"] for r in rows]
    today = date.today()
    streak = 0

    for i, d in enumerate(dates):
        check_date = date.fromisoformat(d)
        expected = today - __import__("datetime").timedelta(days=i)
        if check_date == expected:
            streak += 1
        else:
            break

    return streak


def get_overall_streak() -> int:
    """计算总体连续打卡天数（任意任务打卡即算）"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT DISTINCT plan_date FROM checkins ORDER BY plan_date DESC"
    ).fetchall()
    conn.close()

    if not rows:
        return 0

    dates = [r["plan_date"] for r in rows]
    today = date.today()
    streak = 0

    for i, d in enumerate(dates):
        check_date = date.fromisoformat(d)
        expected = today - __import__("datetime").timedelta(days=i)
        if check_date == expected:
            streak += 1
        else:
            break

    return streak
