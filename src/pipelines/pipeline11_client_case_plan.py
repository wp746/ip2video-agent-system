"""Pipeline 11: Build a client-facing full case plan and validation matrix."""

from __future__ import annotations

from typing import Any, Dict, List


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    brief = state["INPUT_COMPILER"]["compiled_brief"]
    research = state["RESEARCH_SYNTHESIS"]["design_strategy"]
    design_research = state["DESIGN_RESEARCH"]["design_research"]
    channel_plan = state["CHANNEL_PLANNER"]["channel_plan"]
    campaign = state["CAMPAIGN_CALENDAR"]["campaign_focus"]
    annual_calendar = state["CAMPAIGN_CALENDAR"]["annual_calendar"]
    wechat = state["WECHAT_CONTENT"]["article_draft"]
    poster = state["POSTER_DESIGN"]["poster_prompts"]
    story = state["STORY_CREATION"]

    profile_id = brief.get("research_profile_id", "")
    case_plan = _case_plan(brief, research, design_research, channel_plan, campaign, annual_calendar, story)
    verification_matrix = _verification_matrix(brief, profile_id, wechat, poster, story)

    return {
        "pipeline": "CLIENT_CASE_PLAN",
        "research_tone_summary": _tone_summary(brief, research, design_research),
        "case_plan": case_plan,
        "verification_matrix": verification_matrix,
        "prompt_usage": "Use this before generating final channel assets; validate each channel against the matrix.",
    }


def _tone_summary(brief: Dict[str, Any], research: Dict[str, Any], design_research: Dict[str, Any]) -> Dict[str, Any]:
    if brief.get("research_profile_id") == "engineering_maritime":
        return {
            "core_tone": "央企工程传播：宏大但不空，专业但不冷，温暖但不低幼。",
            "adoptable_expression": [
                "先给真实岗位和工程场景，再给节日祝福。",
                "用一线动作承接宏大主题：巡检、对讲、看图纸、掌舵、挥手送航、设备确认。",
                "IP 的可爱感只能降低阅读门槛，不能替代行业可信度。",
                "标题和画面要能被官方号直接判断为中国交建语境，而不是通用节日模板。",
            ],
            "local_reference_reading": [
                "参考海报集中使用驾驶舱、甲板、海图、对讲机、港口、船舶和归港动作。",
                "有效画面都把人物/IP 放在岗位任务里，而不是单纯摆拍。",
                "标题多采用四字/七字式工程口号和温暖收束，适合微博配图与公众号头图。",
            ],
            "forbidden_tones": _dedupe(design_research.get("forbidden_tones", []) + research.get("forbidden_tones", [])),
        }
    return {
        "core_tone": "行业编辑式传播：具体、有温度、有边界。",
        "adoptable_expression": [
            "从用户真实场景切入。",
            "让 IP 承担解释和陪伴功能。",
            "减少万能口号，增加可见动作。",
        ],
        "local_reference_reading": ["用户参考图仅作为风格和边界输入，不等同于最终创意方向。"],
        "forbidden_tones": _dedupe(design_research.get("forbidden_tones", []) + research.get("forbidden_tones", [])),
    }


def _dedupe(items: List[str]) -> List[str]:
    return list(dict.fromkeys(items))


def _case_plan(
    brief: Dict[str, Any],
    research: Dict[str, Any],
    design_research: Dict[str, Any],
    channel_plan: Dict[str, Any],
    campaign: Dict[str, Any],
    annual_calendar: Dict[str, Any],
    story: Dict[str, Any],
) -> Dict[str, Any]:
    ip_name = brief["ip_name"]
    requested_channels = channel_plan.get("requested_channels", [])
    occasion = campaign.get("occasion") or "首轮测试节点"
    profile_id = brief.get("research_profile_id", "")

    if profile_id == "engineering_maritime":
        proposition = (
            f"用{ip_name}把中国交建的宏大工程、航运服务和安全责任，"
            "翻译成官方号愿意采用的一线岗位动作。"
        )
        strategy_axis = [
            "行业坐标：交通强国、向海图强、重大工程、平安航程。",
            "人物坐标：海员、工程师、项目一线、港口值守人员。",
            "IP 坐标：蓝白工装、安全帽标识、可信动作、温暖收束。",
            "平台坐标：微博要一眼成立，公众号要能展开成故事，短视频要有岗位动作节奏。",
        ]
    else:
        proposition = f"用{ip_name}把模糊需求翻译成多渠道、可执行、可审核的 AIGC 宣发内容。"
        strategy_axis = [
            "行业坐标：先确认用户和场景。",
            "人物坐标：让 IP 承担解释、陪伴或引导功能。",
            "平台坐标：按视频、公众号、海报分别收束。",
        ]

    return {
        "client_goal": brief.get("goal", ""),
        "planning_status": "research_to_full_case_plan",
        "current_test_node": occasion,
        "communication_proposition": proposition,
        "strategic_axis": strategy_axis,
        "research_basis": {
            "profile_id": profile_id,
            "audience_taste": research.get("audience_taste", ""),
            "visual_direction": research.get("visual_direction", ""),
            "story_direction": research.get("story_direction", ""),
            "limitations": design_research.get("research_limitations", []),
        },
        "channel_architecture": _channel_architecture(requested_channels, occasion, story),
        "annual_node_strategy": _annual_node_strategy(annual_calendar, profile_id),
        "first_round_delivery": _first_round_delivery(occasion, requested_channels),
        "client_review_order": [
            "先确认行业调性和官方号采纳标准。",
            "再确认年度节点矩阵和本次测试节点。",
            "再确认公众号标题/结构、海报方向、短视频分镜是否同源。",
            "最后进入图像生成、视频生成和平台文案微调。",
        ],
    }


def _channel_architecture(channels: List[str], occasion: str, story: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    architecture: Dict[str, Dict[str, Any]] = {}
    if "wechat" in channels:
        architecture["wechat"] = {
            "role": "深度解释与组织叙事",
            "first_test": f"围绕{occasion}写一篇不 AI 腔的官方号稿件：从岗位动作切入，延展到行业精神。",
            "must_have": ["真实岗位动作", "行业语境", "IP 自然植入", "结尾品牌收束"],
        }
    if "poster" in channels:
        architecture["poster"] = {
            "role": "微博/朋友圈/公众号头图的一眼传播",
            "first_test": f"围绕{occasion}产出 3 个版式方向：横向社交图、公众号封面、9:16 竖版。",
            "must_have": ["IP 身份锚点", "节点符号", "工程/行业场景", "标题留白", "品牌署名区"],
        }
    if "video" in channels:
        architecture["video"] = {
            "role": "视频号/抖音的岗位动作短片",
            "first_test": story.get("logline_cn", ""),
            "must_have": ["开场场景钩子", "中段岗位动作", "结尾品牌/节点情绪", "镜头可执行"],
        }
    return architecture


def _annual_node_strategy(annual_calendar: Dict[str, Any], profile_id: str) -> List[Dict[str, str]]:
    priority = [
        "春节",
        "劳动节",
        "端午节",
        "父亲节",
        "世界海员日",
        "中国航海日",
        "安全生产月",
        "国庆节",
        "中秋节",
    ]
    result = []
    for name in priority:
        spec = annual_calendar.get(name)
        if not spec:
            continue
        angle = spec.get("campaign_angle", "")
        if profile_id == "engineering_maritime":
            angle = _engineering_node_angle(name, angle)
        result.append(
            {
                "node": name,
                "date_rule": spec.get("date_rule", ""),
                "role": _node_role(name),
                "angle": angle,
            }
        )
    return result


def _engineering_node_angle(name: str, fallback: str) -> str:
    mapping = {
        "春节": "归家与坚守并置：有人返乡团圆，也有人守在港口、项目和航线，IP 负责把祝福送到一线。",
        "劳动节": "致敬一线建设者：安全帽、图纸、设备和港口现场是主视觉，避免空喊致敬。",
        "端午节": "端午安康与平安航程结合：粽叶/龙舟只做节日锚点，核心仍是巡检、守航和港口安全。",
        "父亲节": "把父亲的可靠感转译成工程岗位的支撑感：沉默守护、稳稳托举、按规范把每一步做好。",
        "世界海员日": "从驾驶舱、海图、对讲机和归港动作切入，致敬远航中的专业、平安与坚守。",
        "中国航海日": "向海图强与交通强国叙事：船舶、港口、桥梁和航线共同构成中国交建的行业坐标。",
        "安全生产月": "把安全规范可视化：检查表、警示线、安全帽、对讲确认和设备巡检是内容主角。",
        "国庆节": "国家工程与交通动脉叙事：桥、路、港、船共同服务流动中国，画面庄重克制。",
        "中秋节": "远方与团圆并置：海上明月、归港灯光、项目值守和家国同圆。",
    }
    return mapping.get(name, fallback)


def _node_role(name: str) -> str:
    if name in {"世界海员日", "中国航海日", "安全生产月"}:
        return "行业节点"
    if name in {"春节", "国庆节", "中秋节", "端午节"}:
        return "全民节日"
    return "社会情绪节点"


def _first_round_delivery(occasion: str, channels: List[str]) -> List[Dict[str, str]]:
    delivery = []
    if "poster" in channels:
        delivery.append({"item": "微博海报方向", "output": f"{occasion} 3 张海报提示词 + 微博配文方向"})
    if "wechat" in channels:
        delivery.append({"item": "公众号方向", "output": f"{occasion} 标题备选 + 正文结构 + 配图提示词"})
    if "video" in channels:
        delivery.append({"item": "短视频方向", "output": f"{occasion} 30 秒 Seedance 提示词 + 分镜包"})
    return delivery


def _verification_matrix(
    brief: Dict[str, Any],
    profile_id: str,
    wechat: Dict[str, Any],
    poster: Dict[str, Dict[str, str]],
    story: Dict[str, Any],
) -> List[Dict[str, Any]]:
    common = [
        "IP 身份锚点是否保留",
        "行业场景是否真实具体",
        "是否避免通用节日模板",
        "是否适合甲方提交给上级官方号审核",
    ]
    if profile_id == "engineering_maritime":
        common.extend(["是否体现安全规范", "是否有中国交建蓝白识别", "是否把宏大叙事落到一线动作"])

    return [
        {
            "channel": "调研/全案",
            "artifact": "client_case_plan.md",
            "checks": common + ["是否先调性后生产", "是否给出年度节点矩阵"],
            "sample_evidence": brief.get("research_profile_id", ""),
        },
        {
            "channel": "公众号",
            "artifact": "wechat_content.md",
            "checks": common + ["标题是否像行业编辑", "正文是否有岗位动作和段落推进", "配图是否围绕 IP 原型"],
            "sample_evidence": "；".join(wechat.get("title_options", [])[:2]),
        },
        {
            "channel": "海报",
            "artifact": "poster_prompts.md",
            "checks": common + ["是否有明确比例", "是否预留标题/署名区", "是否给出负面约束"],
            "sample_evidence": "；".join(item.get("headline_direction", "") for item in poster.values()),
        },
        {
            "channel": "短视频",
            "artifact": "seedance_2_5_30s.txt",
            "checks": common + ["是否有开中结节奏", "镜头动作是否可生成", "结尾是否能服务节点传播"],
            "sample_evidence": story.get("logline_cn", ""),
        },
    ]
