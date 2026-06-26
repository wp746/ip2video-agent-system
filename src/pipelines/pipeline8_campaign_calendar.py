"""Pipeline 8: Build annual festival/node campaign plan."""

from __future__ import annotations

from typing import Any, Dict


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    nodes = state.get("campaign_calendar", {}).get("annual_nodes", {})
    channel_plan = state["CHANNEL_PLANNER"]["channel_plan"]
    occasion = channel_plan.get("occasion", "")
    brief = state["INPUT_COMPILER"]["compiled_brief"]
    research = state["RESEARCH_SYNTHESIS"]["design_strategy"]

    matched = nodes.get(occasion, {}) if occasion else {}
    matched = _profile_node_overlay(brief, occasion, matched)
    annual_calendar = {_name: _annual_calendar_item(_name, spec, brief, research) for _name, spec in nodes.items()}

    campaign_focus = {
        "occasion": occasion or "全年节点规划",
        "matched": bool(matched),
        "date_rule": matched.get("date_rule", ""),
        "audience_emotion": matched.get("audience_emotion", ""),
        "visual_symbols": matched.get("visual_symbols", []),
        "content_angles": matched.get("content_angles", []),
        "poster_motifs": matched.get("poster_motifs", []),
        "forbidden_tones": matched.get("forbidden_tones", []),
        "industry_integration": _industry_integration(brief, research, matched),
    }

    return {
        "pipeline": "CAMPAIGN_CALENDAR",
        "annual_calendar": annual_calendar,
        "campaign_focus": campaign_focus,
        "prompt_usage": "Use campaign_focus for a current festival/event; use annual_calendar for yearly content planning.",
    }


def _campaign_angle(name: str, spec: Dict[str, Any], brief: Dict[str, Any], research: Dict[str, Any]) -> str:
    angles = spec.get("content_angles", [])
    base = angles[0] if angles else "节点关怀"
    return f"{name}: 用 {brief['ip_name']} 表达「{base}」，结合行业方向：{research.get('story_direction', '')}"


def _annual_calendar_item(name: str, spec: Dict[str, Any], brief: Dict[str, Any], research: Dict[str, Any]) -> Dict[str, Any]:
    node = _profile_node_overlay(brief, name, spec)
    return {
        "date_rule": node.get("date_rule", ""),
        "category": node.get("category", ""),
        "campaign_angle": _campaign_angle(name, node, brief, research),
        "poster_motifs": node.get("poster_motifs", []),
        "content_angles": node.get("content_angles", []),
        "forbidden_tones": node.get("forbidden_tones", []),
    }


def _industry_integration(brief: Dict[str, Any], research: Dict[str, Any], matched: Dict[str, Any]) -> str:
    if not matched:
        return f"围绕 {brief['ip_name']} 的行业语境，规划全年节点内容。"
    if brief.get("research_profile_id") == "engineering_maritime":
        return (
            f"把「{matched.get('audience_emotion', '')}」落到工程、航运和安全岗位动作；"
            "IP 负责降低传播门槛，真实场景负责建立中国交建语境。"
        )
    return (
        f"把「{matched.get('audience_emotion', '')}」和行业关怀结合；"
        f"IP 负责承载情绪，产品/服务负责给出具体行动。"
    )


def _profile_node_overlay(brief: Dict[str, Any], name: str, spec: Dict[str, Any]) -> Dict[str, Any]:
    if brief.get("research_profile_id") != "engineering_maritime" or not spec:
        return spec
    overlay = _engineering_maritime_overlay(name)
    if not overlay:
        return spec
    merged = dict(spec)
    merged.update({key: value for key, value in overlay.items() if value})
    merged["forbidden_tones"] = list(dict.fromkeys(spec.get("forbidden_tones", []) + overlay.get("forbidden_tones", [])))
    return merged


def _engineering_maritime_overlay(name: str) -> Dict[str, Any]:
    name = str(name)
    overlays = {
        "元旦": {
            "audience_emotion": "新程、开局、计划、抵达",
            "visual_symbols": ["新年数字", "航线图", "港口晨光", "桥梁", "项目计划表"],
            "content_angles": ["新年新程", "开局即出发", "年度工程计划", "把蓝图变成通途"],
            "poster_motifs": ["IP 在港口晨光中展开新年航线图", "新年数字与桥梁剪影结合", "IP 在项目计划表前开启新程"],
            "forbidden_tones": ["空泛口号", "过度鸡血", "脱离工程现场"],
        },
        "春节": {
            "audience_emotion": "团圆、坚守、平安、归航",
            "visual_symbols": ["港口灯光", "归航船舶", "春联", "安全帽", "值守岗亭"],
            "content_angles": ["归家与坚守", "平安春运", "一线值守", "新春工程祝福"],
            "poster_motifs": ["IP 在港口灯光中送上新春祝福", "IP 与归航船舶同框", "IP 给值守岗位递上春联"],
            "forbidden_tones": ["廉价红金堆砌", "忽略一线值守"],
        },
        "劳动节": {
            "audience_emotion": "致敬、专业、踏实、安全",
            "visual_symbols": ["安全帽", "图纸", "工具", "桥梁", "港口机械"],
            "content_angles": ["致敬一线建设者", "专业背后的规范", "劳动创造交通动脉"],
            "poster_motifs": ["IP 站在桥梁工地看图纸", "IP 在港口机械前完成安全确认", "IP 向一线建设者致敬"],
            "forbidden_tones": ["空喊致敬", "危险施工动作"],
        },
        "元宵节": {
            "audience_emotion": "灯火、团圆、复工、守望",
            "visual_symbols": ["花灯", "港口灯火", "桥梁夜景", "汤圆", "值守岗亭"],
            "content_angles": ["灯火里的项目值守", "团圆之后继续出发", "元宵灯火照亮通途"],
            "poster_motifs": ["IP 提花灯站在港口灯火前", "汤圆与桥梁夜景形成温暖主视觉", "IP 在值守岗亭送上元宵祝福"],
            "forbidden_tones": ["视觉过满", "民俗符号错用", "脱离工程现场"],
        },
        "妇女节": {
            "audience_emotion": "看见、专业、力量、尊重",
            "visual_symbols": ["安全帽", "图纸", "港口晨光", "花束", "工程现场"],
            "content_angles": ["看见她在一线的专业", "工程岗位里的女性力量", "尊重每一份建设者担当"],
            "poster_motifs": ["女 IP 与女性工程师在图纸前讨论方案", "安全帽与花束克制同框", "港口晨光里女性建设者背影"],
            "forbidden_tones": ["消费主义套路", "刻板女性形象", "只送花不见岗位"],
        },
        "清明节": {
            "audience_emotion": "清朗、追思、春日复工、安全",
            "visual_symbols": ["柳枝", "细雨", "桥梁", "工地围挡", "安全帽", "清朗天空"],
            "content_angles": ["清朗工程现场", "春日复工安全", "慎终追远与建设前行"],
            "poster_motifs": ["IP 在清朗春雨中检查桥梁图纸", "柳枝与中国交建蓝形成克制主视觉", "IP 在项目现场提示复工安全"],
            "forbidden_tones": ["嬉闹营销", "过度商业化"],
        },
        "母亲节": {
            "audience_emotion": "牵挂、平安、归家、温柔支撑",
            "visual_symbols": ["港口灯光", "家书", "安全帽", "康乃馨", "归航船舶"],
            "content_angles": ["把平安带回家", "一线岗位背后的牵挂", "给远方家人的安心答复"],
            "poster_motifs": ["IP 把康乃馨与安全帽放在港口晨光中", "IP 展开一封写给家人的平安家书", "归航船舶与温柔灯光同框"],
            "forbidden_tones": ["催泪过度", "道德绑架", "纯家庭模板"],
        },
        "520": {
            "audience_emotion": "表达、承诺、陪伴、抵达",
            "visual_symbols": ["航线", "便签", "桥梁", "港口灯光", "中国交建蓝"],
            "content_angles": ["把爱写成一条抵达的路", "长期陪伴与工程承诺", "让距离被交通连接"],
            "poster_motifs": ["IP 在航线图上贴下一张蓝色便签", "桥梁和港口灯光组成连接承诺画面", "IP 把心形符号做成航标"],
            "forbidden_tones": ["土味情话", "过度粉色", "脱离行业"],
        },
        "儿童节": {
            "audience_emotion": "成长、未来、安全、好奇",
            "visual_symbols": ["安全帽", "儿童画", "桥梁模型", "工程车模型", "蓝天"],
            "content_angles": ["给未来建设者的想象", "安全启蒙", "把大工程讲给孩子听"],
            "poster_motifs": ["IP 和孩子画下一座未来大桥", "IP 带孩子看安全帽和工程模型", "儿童画风线稿叠加真实桥梁剪影"],
            "forbidden_tones": ["低幼化冒犯", "危险模仿", "把施工场景玩具化过度"],
        },
        "端午节": {
            "audience_emotion": "安康、守护、远航、传统",
            "visual_symbols": ["粽子", "龙舟", "艾草", "港口", "船舶", "安全检查表"],
            "content_angles": ["端午安康与平安航程", "传统节日里的安全守护", "龙舟精神与向海图强"],
            "poster_motifs": ["IP 把粽叶化作航线图", "IP 在港口拿安全检查表送端午安康", "龙舟与工程船远近呼应"],
            "forbidden_tones": ["只堆粽子不见行业", "民俗符号乱用"],
        },
        "父亲节": {
            "audience_emotion": "可靠、支撑、沉默守护、担当",
            "visual_symbols": ["安全帽", "背影", "图纸", "桥墩", "港口晨光", "工具箱"],
            "content_angles": ["像父亲一样可靠的工程支撑", "沉默守护与一线担当", "把每一步做稳"],
            "poster_motifs": ["IP 与一线建设者背影并肩看向大桥", "IP 递上安全帽表达可靠守护", "港口晨光里 IP 检查图纸"],
            "forbidden_tones": ["苦情过度", "父爱刻板化", "把父亲节做成家庭模板"],
        },
        "七夕": {
            "audience_emotion": "连接、守候、远方、承诺",
            "visual_symbols": ["鹊桥", "星河", "桥梁", "航线", "港口灯光"],
            "content_angles": ["桥梁连接远方", "长久陪伴与工程承诺", "把浪漫落到抵达"],
            "poster_motifs": ["IP 把鹊桥转译成真实桥梁剪影", "星河航线与港口灯光相连", "IP 在桥梁下方守望远方"],
            "forbidden_tones": ["土味浪漫", "过度商业催促", "脱离交通连接主题"],
        },
        "教师节": {
            "audience_emotion": "传承、引路、专业、成长",
            "visual_symbols": ["图纸", "讲台", "安全帽", "桥梁剖面图", "书本"],
            "content_angles": ["工程知识的传承", "谢谢一线师傅和引路人", "把专业经验交给下一班人"],
            "poster_motifs": ["IP 在图纸前向青年员工讲解桥梁结构", "安全帽与书本组成主视觉", "一线师傅背影与项目现场同框"],
            "forbidden_tones": ["空泛感谢", "教师工具人化"],
        },
        "中秋节": {
            "audience_emotion": "团圆、远方、牵挂、值守",
            "visual_symbols": ["明月", "港口灯光", "归航船舶", "月饼", "桥梁"],
            "content_angles": ["海上明月与工程值守", "远方也有团圆", "家国同圆"],
            "poster_motifs": ["IP 在港口月光下望向归航船", "明月与大桥形成主视觉", "IP 把月饼放在值守岗亭"],
            "forbidden_tones": ["廉价月亮背景", "过度煽情"],
        },
        "国庆节": {
            "audience_emotion": "自豪、流动中国、家国、秩序",
            "visual_symbols": ["国旗红", "桥梁", "港口", "船舶", "城市天际线", "晴空"],
            "content_angles": ["交通强国与流动中国", "重大工程服务家国出行", "中国交建蓝里的国庆祝福"],
            "poster_motifs": ["IP 站在桥梁与港口交汇的城市天际线前", "工程船与国庆晴空同框", "IP 展开交通动脉路线图"],
            "forbidden_tones": ["不规范国旗使用", "过度娱乐化"],
        },
        "重阳节": {
            "audience_emotion": "敬老、陪伴、登高、平安出行",
            "visual_symbols": ["菊花", "登高", "桥梁步道", "港口远景", "暖茶"],
            "content_angles": ["平安出行陪长辈", "登高望远看交通变迁", "把陪伴落到一段路"],
            "poster_motifs": ["IP 陪长辈在桥梁步道远望城市", "菊花暖茶与港口远景结合", "IP 展开平安出行提示卡"],
            "forbidden_tones": ["年龄焦虑", "保健品式夸大", "脱离交通出行"],
        },
        "双十一": {
            "audience_emotion": "物流、效率、选择、连接",
            "visual_symbols": ["港口集装箱", "物流路线", "包裹", "桥梁", "数据看板"],
            "content_angles": ["物流背后的交通基础设施", "让每一次抵达更高效", "理性消费与通达网络"],
            "poster_motifs": ["IP 站在集装箱港口前看物流路线", "包裹路线穿过桥梁港口城市", "IP 整理一张通达网络清单"],
            "forbidden_tones": ["低价轰炸", "虚假紧迫感", "脱离基础设施"],
        },
        "冬至": {
            "audience_emotion": "温暖、值守、寒潮、保障",
            "visual_symbols": ["港口暖灯", "热气", "安全帽", "围巾", "寒潮现场", "值守岗亭"],
            "content_angles": ["寒冬里的工程值守", "把温暖送到一线", "冬日保障与平安航程"],
            "poster_motifs": ["IP 在港口暖灯下给值守人员递上热汤", "安全帽与围巾形成冬至主视觉", "寒潮现场 IP 完成设备确认"],
            "forbidden_tones": ["过度养生焦虑", "忽视低温作业安全"],
        },
    }
    return overlays.get(name, {})
