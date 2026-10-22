"""AI 集成：Anthropic 兼容 API 调用"""
import json
import os
import re
from datetime import date
from pathlib import Path
from typing import Optional

import anthropic

CONFIG_PATH = Path(__file__).parent.parent / "config.toml"


def load_config() -> dict:
    """加载配置文件"""
    import tomllib
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"配置文件不存在：{CONFIG_PATH}\n"
            "请复制 config.toml.example 为 config.toml 并填入你的 API 配置"
        )
    return tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def get_client() -> anthropic.Anthropic:
    """从 config.toml 或环境变量创建 Anthropic 客户端"""
    config = load_config()
    api_cfg = config.get("api", {})

    api_key = api_cfg.get("api_key") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "未配置 API 密钥。请在 config.toml 的 [api] 中设置 api_key，"
            "或设置环境变量 ANTHROPIC_API_KEY"
        )

    kwargs = {"api_key": api_key, "timeout": 60.0}
    base_url = api_cfg.get("base_url")
    if base_url:
        kwargs["base_url"] = base_url

    return anthropic.Anthropic(**kwargs)


def get_model() -> str:
    """获取配置的模型名称"""
    config = load_config()
    model = config.get("api", {}).get("model")
    if not model:
        raise ValueError("未在 config.toml 中配置 model")
    return model


def _extract_json(text: str) -> dict:
    """从 AI 响应中提取 JSON（兼容 markdown 代码块和裸 JSON）"""
    # 尝试提取 ```json ... ``` 代码块
    m = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if m:
        text = m.group(1)
    # 尝试提取 { ... } 块
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        text = m.group(0)
    return json.loads(text)


def generate_daily_plan(goals: list[dict], tasks: list[dict], history: list[dict]) -> dict:
    """根据目标、任务清单、历史打卡生成今日计划

    返回 {"tasks": [...], "motivation": "..."}
    """
    client = get_client()
    model = get_model()

    system_prompt = """你是一个幽默吐槽型的学习督促助手。
用户设定了多个学习目标，每个目标下有若干任务。
你的任务：
1. 根据用户的历史打卡记录和当前 streak，生成今天的个性化学习计划
2. 用幽默吐槽的语气写一段督促语（比如"昨天背了 5 个词就敢说自己努力了？今天至少 30 个！"）
3. 输出 JSON 格式：{"tasks": [{"task_id": 数字, "description": "今天具体要做什么"}], "motivation": "督促语"}

规则：
- tasks 列表中的 task_id 必须来自用户提供的任务清单
- 如果用户连续打卡，语气鼓励但带点调侃
- 如果用户断 streak，语气更犀利但不伤人
- 任务优先级根据历史完成情况动态调整（完成少的优先）
- 保持简洁，督促语不超过 100 字
- 只输出 JSON，不要其他内容"""

    user_message = (
        f"目标列表：{json.dumps(goals, ensure_ascii=False)}\n"
        f"任务清单：{json.dumps(tasks, ensure_ascii=False)}\n"
        f"最近 7 天打卡记录：{json.dumps(history, ensure_ascii=False)}\n"
        f"今天是：{date.today().isoformat()}\n\n"
        f"请生成今日计划。"
    )

    response = client.messages.create(
        model=model,
        max_tokens=4000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    text = next((b.text for b in response.content if b.type == "text"), "")
    return _extract_json(text)


def generate_motivation(streak_days: int, today_done: int, today_total: int) -> str:
    """根据 streak 生成幽默督促语（用于通知弹窗，轻量调用）"""
    client = get_client()
    model = get_model()

    system_prompt = """你是一个幽默吐槽型的学习督促助手。
根据用户的学习状态，用一句话吐槽或鼓励他。
要求：
- 不超过 50 字
- 如果连续打卡，调侃式鼓励
- 如果断 streak，犀利但不伤人
- 只输出一句话，不要引号或其他内容"""

    user_message = (
        f"连续打卡 {streak_days} 天，"
        f"今天已完成 {today_done}/{today_total} 个任务。"
        f"请用一句话督促我。"
    )

    response = client.messages.create(
        model=model,
        max_tokens=200,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    return next((b.text.strip() for b in response.content if b.type == "text"), "该学习了！")


def generate_report(checkins: list[dict], goals: list[dict], days: int = 7) -> str:
    """生成学习报告"""
    client = get_client()
    model = get_model()

    system_prompt = """你是一个幽默吐槽型的学习督促助手。
根据用户的学习数据，生成一份简短的学习报告。
要求：
- 总结过去 N 天的学习情况
- 指出亮点和不足
- 给出下一步建议
- 语气幽默吐槽
- 使用 markdown 格式"""

    user_message = (
        f"目标列表：{json.dumps(goals, ensure_ascii=False)}\n"
        f"过去 {days} 天打卡记录：{json.dumps(checkins, ensure_ascii=False)}\n\n"
        f"请生成学习报告。"
    )

    response = client.messages.create(
        model=model,
        max_tokens=4000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    return next((b.text for b in response.content if b.type == "text"), "")
