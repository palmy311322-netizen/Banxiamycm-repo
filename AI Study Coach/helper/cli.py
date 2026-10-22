"""CLI 入口：argparse 子命令"""
import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from . import db, ai, notify, scheduler

console = Console()


def cmd_goal(args):
    """目标管理子命令"""
    if args.goal_action == "add":
        gid = db.add_goal(args.name, args.desc)
        console.print(f"[green]✓[/green] 已添加目标 #{gid}: {args.name}")

    elif args.goal_action == "list":
        goals = db.list_goals(active_only=not args.all)
        if not goals:
            console.print("[dim]暂无目标。用 `goal add` 添加一个吧！[/dim]")
            return
        table = Table(title="学习目标")
        table.add_column("ID", style="cyan", width=4)
        table.add_column("名称", style="bold")
        table.add_column("描述")
        table.add_column("状态", width=6)
        for g in goals:
            status = "[green]活跃[/green]" if g["active"] else "[dim]已归档[/dim]"
            table.add_row(str(g["id"]), g["name"], g["description"] or "", status)
        console.print(table)

    elif args.goal_action == "archive":
        if db.archive_goal(args.id):
            console.print(f"[green]✓[/green] 已归档目标 #{args.id}")
        else:
            console.print(f"[red]✗[/red] 目标 #{args.id} 不存在")


def cmd_task(args):
    """任务管理子命令"""
    if args.task_action == "add":
        goal = db.get_goal(args.goal_id)
        if not goal:
            console.print(f"[red]✗[/red] 目标 #{args.goal_id} 不存在")
            return
        tid = db.add_task(args.goal_id, args.title)
        console.print(f"[green]✓[/green] 已添加任务 #{tid}: {args.title} (目标: {goal['name']})")

    elif args.task_action == "list":
        tasks = db.list_tasks(goal_id=args.goal)
        if not tasks:
            console.print("[dim]暂无任务。用 `task add` 添加吧！[/dim]")
            return
        table = Table(title="任务清单")
        table.add_column("ID", style="cyan", width=4)
        table.add_column("所属目标", style="magenta")
        table.add_column("任务", style="bold")
        table.add_column("频率", width=6)
        table.add_column("已完成", style="green", width=6)
        for t in tasks:
            table.add_row(
                str(t["id"]), t["goal_name"], t["title"],
                t["frequency"], str(t["completed_count"])
            )
        console.print(table)


def cmd_plan(args):
    """每日计划子命令"""
    if args.plan_action == "today":
        _generate_today_plan()

    elif args.plan_action == "show":
        d = args.date or date.today().isoformat()
        plan = db.get_daily_plan(d)
        if not plan:
            console.print(f"[dim]{d} 没有计划。用 `plan today` 生成一个。[/dim]")
            return
        _show_plan(plan)

    elif args.plan_action == "edit":
        console.print("[yellow]交互式编辑暂未实现，请直接编辑 data.db[/yellow]")


def _generate_today_plan():
    """生成今日计划（调用 AI）"""
    today = date.today().isoformat()
    existing = db.get_daily_plan(today)
    if existing:
        console.print(f"[yellow]今日计划已存在，覆盖生成中...[/yellow]")

    goals = db.list_goals()
    tasks = db.list_tasks()
    history = db.get_recent_checkins(7)

    if not goals or not tasks:
        console.print("[red]✗[/red] 请先添加目标和任务：")
        console.print("  python main.py goal add \"目标名\"")
        console.print("  python main.py task add <goal_id> \"任务名\"")
        return

    console.print("[dim]正在调用 AI 生成今日计划...[/dim]")
    try:
        result = ai.generate_daily_plan(goals, tasks, history)
    except Exception as e:
        console.print(f"[red]✗ AI 调用失败：{e}[/red]")
        return

    # 保存计划
    tasks_list = result.get("tasks", [])
    motivation = result.get("motivation", "")
    db.save_daily_plan(today, tasks_list, motivation)

    plan = db.get_daily_plan(today)
    _show_plan(plan)


def _show_plan(plan: dict):
    """展示每日计划"""
    console.print()
    console.print(Panel(
        plan.get("ai_suggestion", "") or "今天也要加油哦！",
        title=f"📅 {plan['plan_date']} 每日计划",
        border_style="green",
    ))

    table = Table()
    table.add_column("任务 ID", style="cyan", width=8)
    table.add_column("说明", style="bold")
    table.add_column("已打卡", style="green", width=6)

    today_checkins = db.get_checkins_for_date(plan["plan_date"])
    done_task_ids = {c["task_id"] for c in today_checkins}

    for t in plan["tasks_json"]:
        tid = t.get("task_id", "?")
        desc = t.get("description", "")
        done = "✓" if tid in done_task_ids else ""
        table.add_row(str(tid), desc, done)

    console.print(table)
    console.print()


def cmd_checkin(args):
    """打卡子命令"""
    if args.checkin_action == "quick":
        # 快速打卡：标记今日计划中所有任务为已完成
        plan = db.get_daily_plan()
        if not plan:
            console.print("[red]✗ 今日没有计划，先用 `plan today` 生成一个[/red]")
            return
        count = 0
        for t in plan["tasks_json"]:
            tid = t.get("task_id")
            if tid:
                db.add_checkin(tid, note="快速打卡", plan_date=plan["plan_date"])
                count += 1
        console.print(f"[green]✓[/green] 快速打卡完成！已标记 {count} 个任务")
        return

    # 单个任务打卡
    task = db.get_task(args.task_id)
    if not task:
        console.print(f"[red]✗[/red] 任务 #{args.task_id} 不存在")
        return

    cid = db.add_checkin(
        task_id=args.task_id,
        note=args.note,
        duration_minutes=args.duration,
    )
    console.print(f"[green]✓[/green] 打卡成功！任务: {task['title']} (#{args.task_id})")
    if args.note:
        console.print(f"  笔记: {args.note}")
    if args.duration:
        console.print(f"  时长: {args.duration} 分钟")


def cmd_status(args):
    """状态统计"""
    today = date.today().isoformat()
    checkins = db.get_checkins_for_date(today)
    plan = db.get_daily_plan(today)
    overall_streak = db.get_overall_streak()

    console.print()
    console.print(Panel(
        f"🔥 连续打卡 [bold yellow]{overall_streak}[/bold yellow] 天",
        title="今日状态",
        border_style="cyan",
    ))

    if plan:
        total = len(plan["tasks_json"])
        done = len(checkins)
        console.print(f"  今日进度: {done}/{total} 个任务")
    else:
        console.print("  [dim]今日还没有计划，用 `plan today` 生成一个[/dim]")

    if checkins:
        console.print()
        table = Table(title="今日打卡记录")
        table.add_column("时间", style="dim")
        table.add_column("目标", style="magenta")
        table.add_column("任务", style="bold")
        table.add_column("笔记")
        table.add_column("时长", style="green")
        for c in checkins:
            t = c["checked_at"][11:16]
            table.add_row(
                t, c["goal_name"], c["task_title"],
                c["note"] or "", f"{c['duration_minutes'] or '-'} 分"
            )
        console.print(table)

    # 各目标 streak
    goals = db.list_goals()
    if goals:
        console.print()
        table = Table(title="各目标连续打卡")
        table.add_column("目标", style="magenta")
        table.add_column("连续天数", style="bold yellow")
        for g in goals:
            streak = db.get_streak_for_goal(g["id"])
            table.add_row(g["name"], str(streak))
        console.print(table)
    console.print()


def cmd_report(args):
    """学习报告"""
    days = args.days or 7
    goals = db.list_goals()
    checkins = db.get_recent_checkins(days)

    if not checkins:
        console.print(f"[dim]过去 {days} 天没有打卡记录[/dim]")
        return

    console.print(f"[dim]正在生成过去 {days} 天的学习报告...[/dim]")
    try:
        report = ai.generate_report(checkins, goals, days)
    except Exception as e:
        console.print(f"[red]✗ AI 调用失败：{e}[/red]")
        return

    console.print()
    console.print(Markdown(report))
    console.print()


def cmd_notify(args):
    """通知管理"""
    if args.notify_action == "test":
        notify.send_toast("学习督促助手", "测试通知：该学习了！📚")
        console.print("[green]✓[/green] 已发送测试通知")

    elif args.notify_action == "setup":
        config = ai.load_config()
        time = config.get("reminder", {}).get("time", "09:00")
        scheduler.setup_reminder(time)

    elif args.notify_action == "remove":
        scheduler.remove_reminder()

    elif args.notify_action == "send":
        # 由任务计划程序调用：发送今日提醒
        _send_daily_reminder()


def _send_daily_reminder():
    """发送每日提醒（由 schtasks 触发）"""
    today = date.today().isoformat()
    plan = db.get_daily_plan(today)
    checkins = db.get_checkins_for_date(today)
    overall_streak = db.get_overall_streak()

    if plan:
        total = len(plan["tasks_json"])
        done = len(checkins)
        remaining = total - done
        if remaining <= 0:
            msg = f"今天的任务都完成啦！连续打卡 {overall_streak} 天，厉害！"
        else:
            try:
                msg = ai.generate_motivation(overall_streak, done, total)
            except Exception:
                msg = f"今天还有 {remaining} 个任务没完成，连续打卡 {overall_streak} 天，别断啦！"
    else:
        msg = "今天还没有学习计划，打开终端运行 `python main.py plan today` 吧！"

    notify.send_toast("📚 学习督促", msg)


def cmd_config(args):
    """配置管理"""
    if args.config_action == "show":
        try:
            config = ai.load_config()
        except FileNotFoundError as e:
            console.print(f"[red]✗[/red] {e}")
            return
        console.print(Panel(
            json.dumps(config, indent=2, ensure_ascii=False),
            title="当前配置",
            border_style="blue",
        ))

    elif args.config_action == "set":
        config_path = Path(__file__).parent.parent / "config.toml"
        if not config_path.exists():
            console.print("[red]✗[/red] config.toml 不存在，请先从 config.toml.example 复制")
            return

        import tomllib
        content = config_path.read_text(encoding="utf-8")
        # 简单替换：只支持顶层 key
        key, value = args.key, args.value
        lines = content.splitlines()
        found = False
        for i, line in enumerate(lines):
            if line.strip().startswith(f"{key} ="):
                # 保留引号格式
                if value.isdigit():
                    lines[i] = f'{key} = {value}'
                else:
                    lines[i] = f'{key} = "{value}"'
                found = True
                break

        if found:
            config_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            console.print(f"[green]✓[/green] 已设置 {key} = {value}")
        else:
            console.print(f"[red]✗[/red] 未找到配置项: {key}")


def build_parser() -> argparse.ArgumentParser:
    """构建命令行解析器"""
    parser = argparse.ArgumentParser(
        prog="helper",
        description="📚 每日学习督促助手 — 让 AI 监督你学习",
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    # goal
    p_goal = sub.add_parser("goal", help="学习目标管理")
    goal_sub = p_goal.add_subparsers(dest="goal_action")

    g_add = goal_sub.add_parser("add", help="添加目标")
    g_add.add_argument("name", help="目标名称")
    g_add.add_argument("--desc", help="目标描述")

    g_list = goal_sub.add_parser("list", help="列出目标")
    g_list.add_argument("--all", action="store_true", help="包含已归档目标")

    g_arch = goal_sub.add_parser("archive", help="归档目标")
    g_arch.add_argument("id", type=int, help="目标 ID")

    # task
    p_task = sub.add_parser("task", help="任务管理")
    task_sub = p_task.add_subparsers(dest="task_action")

    t_add = task_sub.add_parser("add", help="添加任务")
    t_add.add_argument("goal_id", type=int, help="目标 ID")
    t_add.add_argument("title", help="任务名称")

    t_list = task_sub.add_parser("list", help="列出任务")
    t_list.add_argument("--goal", type=int, help="按目标筛选")

    # plan
    p_plan = sub.add_parser("plan", help="每日计划")
    plan_sub = p_plan.add_subparsers(dest="plan_action")

    plan_sub.add_parser("today", help="生成今日计划（AI）")

    p_show = plan_sub.add_parser("show", help="查看计划")
    p_show.add_argument("date", nargs="?", help="日期 YYYY-MM-DD（默认今天）")

    plan_sub.add_parser("edit", help="编辑今日计划")

    # checkin
    p_ci = sub.add_parser("checkin", help="打卡")
    ci_sub = p_ci.add_subparsers(dest="checkin_action")

    ci_quick = ci_sub.add_parser("quick", help="快速打卡（标记所有任务完成）")

    c_single = ci_sub.add_parser("single", help="单个任务打卡")
    c_single.add_argument("task_id", type=int, help="任务 ID")
    c_single.add_argument("--note", help="学习笔记")
    c_single.add_argument("--duration", type=int, help="学习时长（分钟）")

    # 也支持直接 checkin <task_id>
    c_direct = ci_sub.add_parser("direct", help=argparse.SUPPRESS)
    c_direct.add_argument("task_id", type=int)
    c_direct.add_argument("--note")
    c_direct.add_argument("--duration", type=int)

    # status
    sub.add_parser("status", help="查看今日状态和统计")

    # report
    p_report = sub.add_parser("report", help="生成学习报告（AI）")
    p_report.add_argument("days", nargs="?", type=int, help="报告天数（默认 7）")

    # notify
    p_notify = sub.add_parser("notify", help="通知管理")
    notify_sub = p_notify.add_subparsers(dest="notify_action")
    notify_sub.add_parser("test", help="发送测试通知")
    notify_sub.add_parser("setup", help="注册每日提醒")
    notify_sub.add_parser("remove", help="移除提醒")
    notify_sub.add_parser("send", help=argparse.SUPPRESS)  # 由 schtasks 调用

    # config
    p_config = sub.add_parser("config", help="配置管理")
    config_sub = p_config.add_subparsers(dest="config_action")
    config_sub.add_parser("show", help="显示配置")

    c_set = config_sub.add_parser("set", help="设置配置项")
    c_set.add_argument("key", help="配置键")
    c_set.add_argument("value", help="配置值")

    return parser


def main(argv=None):
    """CLI 主入口"""
    db.init_db()

    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return

    # 特殊处理：checkin <task_id> 直接打卡
    if args.command == "checkin" and not getattr(args, "checkin_action", None):
        # 尝试解析为直接打卡
        parser.parse_args(["checkin", "single"] + (argv[1:] if argv else []), args)
        args.checkin_action = "single"

    dispatch = {
        "goal": cmd_goal,
        "task": cmd_task,
        "plan": cmd_plan,
        "checkin": cmd_checkin,
        "status": cmd_status,
        "report": cmd_report,
        "notify": cmd_notify,
        "config": cmd_config,
    }

    handler = dispatch.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
