"""Generate final Markdown prompt documents from pipeline outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable


class MarkdownGenerator:
    def __init__(self, state: Dict[str, Any], config: Dict[str, Any]):
        self.state = state
        self.config = config

    def generate(self) -> str:
        ip = self.state["IP_UNDERSTANDING"]["ip_profile"]
        rules = self.state["IP_UNDERSTANDING"]["fixed_rules"]
        story = self.state["STORY_CREATION"]
        visual = self.state["VISUAL_DESIGN"]
        cine = self.state["CINEMATOGRAPHY"]
        prompts = self.state["PROMPT_GENERATION"]
        compiler = self.state["INPUT_COMPILER"]
        ip_bible = self.state["IP_BIBLE_BUILDER"]
        compliance = self.state["COMPLIANCE_REVIEW"]
        ledger = self.state["ASSET_LEDGER"]
        storyboard = self.state["STORYBOARD_CONTRACT"]
        validator = self.state["PROMPT_VALIDATOR"]
        qa = self.state["QA_REPAIR_EXPORT"]
        research_plan = self.state["RESEARCH_PLANNER"]["research_plan"]
        design_research = self.state["DESIGN_RESEARCH"]["design_research"]
        design_strategy = self.state["RESEARCH_SYNTHESIS"]["design_strategy"]
        channel_plan = self.state["CHANNEL_PLANNER"]["channel_plan"]
        campaign = self.state["CAMPAIGN_CALENDAR"]["campaign_focus"]
        wechat = self.state["WECHAT_CONTENT"]
        poster = self.state["POSTER_DESIGN"]
        client = self.state["CLIENT_CASE_PLAN"]

        lines = [
            f"# {ip['name']} {ip['duration']} AIGC 短片提示词文档",
            "",
            f"- 模板 (Style Template): `{self.state['template_id']}`",
            f"- 平台 (Platform): {ip.get('platform', 'Seedance')}",
            f"- 受众 (Audience): {ip.get('audience', '')}",
            f"- 产品/道具 (Product): {ip.get('product', '')}",
            f"- 生产状态 (Production Status): {qa['status']}",
            "",
            "## 0. 设计调研与生产策略",
            "",
            f"- 调研模式: {research_plan['mode']}",
            f"- 调研画像: {research_plan['domain_profile_id']}",
            f"- 匹配词: {', '.join(research_plan.get('matched_terms', [])) or '无'}",
            f"- 推荐模板: {design_strategy['style_template_recommendation']}",
            f"- 受众洞察: {design_strategy['audience_taste']}",
            f"- 情绪定位: {design_strategy['emotional_positioning']}",
            f"- 视觉方向: {design_strategy['visual_direction']}",
            f"- 叙事机会: {design_strategy['story_direction']}",
            f"- 参考关键词: {', '.join(design_strategy['reference_keywords'])}",
                f"- 禁止调性: {', '.join(design_strategy['forbidden_tones'])}",
                f"- 宣传渠道: {', '.join(channel_plan['requested_channels'])}",
                f"- 当前节点: {campaign['occasion']}",
                "",
            "### 甲方全案方案摘要",
            "",
            f"- 核心调性: {client['research_tone_summary']['core_tone']}",
            f"- 传播主张: {client['case_plan']['communication_proposition']}",
            f"- 首轮交付: {'；'.join(item['output'] for item in client['case_plan']['first_round_delivery'])}",
            "",
            "### 调研限制",
            "",
        ]
        lines.extend(self._bullet_list(design_research.get("research_limitations", [])))
        lines.extend(
            [
                "",
            "## 1. 使用说明 (Step by Step)",
            "",
            ]
        )
        lines.extend(f"{index}. {step}" for index, step in enumerate(prompts["usage_steps"], start=1))
        lines.extend(
            [
                "",
                "## 2. IP 档案与固定规则",
                "",
                f"- IP: {ip['name']}",
                f"- 类型: {ip.get('type', '')}",
                f"- 描述: {ip.get('description', '')}",
                f"- 观众承诺: {self.state['IP_UNDERSTANDING']['audience_promise']}",
                f"- 固定轮廓: {rules.get('silhouette', '')}",
                f"- 输入编译状态: {compiler['signoff']['status']}",
                "",
                "### 合规与品牌边界",
                "",
            ]
        )
        lines.extend(self._bullet_list(compliance.get("hard_rules", [])))
        lines.extend(
            [
                "",
                "### IP Bible 锁定项",
                "",
                f"- 必须保留: {', '.join(ip_bible['ip_bible']['visual_lock']['must_keep'])}",
                f"- 禁止变化: {'；'.join(ip_bible['ip_bible']['forbidden_variation'])}",
                f"- 连续性钩子: {'；'.join(ip_bible['ip_bible']['continuity_hooks'])}",
            ]
        )
        lines.extend(
            [
                "",
                "## 3. 故事结构",
                "",
                f"- 故事语法: {story.get('archetype', '')}",
                f"- 主题: {story['theme']}",
                f"- 情绪曲线: {story.get('emotional_curve', '')}",
                f"- 中文一句话: {story['logline_cn']}",
                f"- English logline: {story['logline_en']}",
                f"- 调研叙事方向: {story.get('research_story_direction', '')}",
                "",
                "| Time | Beat | Purpose | 中文动作 | English Action |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for beat in story["story_beats"]:
            lines.append(f"| {beat['time']} | {beat['beat']} | {beat.get('purpose', '')} | {beat['cn']} | {beat['en']} |")

        lines.extend(
            [
                "",
                "## 4. 图片提示词 (Image Prompts)",
                "",
                "### Visual Prompt Blocks",
                "",
            ]
        )
        for key, value in visual.get("prompt_blocks", {}).items():
            lines.append(f"- `{key}`: {value}")
        lines.extend(["", "### Asset Spec Contract", ""])
        for asset_name, spec in visual.get("asset_specs", {}).items():
            panels = ", ".join(spec.get("required_panels", []))
            constraints = ", ".join(spec.get("hard_constraints", []))
            lines.append(f"- `{asset_name}` panels: {panels}; constraints: {constraints}")
        lines.append("")
        for key, value in visual["image_prompts"].items():
            lines.extend([f"### {key}", "", value, ""])

        lines.extend(
            [
                "## 5. 资产台账与参考职责",
                "",
                "| Asset ID | Duty | Name | Priority | Status |",
                "| --- | --- | --- | ---: | --- |",
            ]
        )
        for asset in ledger["asset_ledger"]:
            lines.append(
                f"| {asset['asset_id']} | {asset['duty']} | {asset['name']} | {asset['priority']} | {asset['status']} |"
            )
        lines.extend(
            [
                "",
                f"- 身份参考: {ledger['reference_duty'].get('identity_lock', [])}",
                f"- 执行态参考: {ledger['reference_duty'].get('execution_state', [])}",
                f"- Source Board Exclusion: {'；'.join(ledger['source_board_exclusion'])}",
                "",
                "## 6. 分镜与摄影",
                "",
                "| Shot | Time | Beat | Action | Camera | Transition |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )

        for shot in cine["shots"]:
            lines.append(
                f"| {shot['shot']} | {shot['time']} | {shot['beat']} | {shot['action_cn']} | {shot['camera']} | {shot['transition']} |"
            )

        lines.extend(
            [
                "",
                "### Storyboard Contract 摘要",
                "",
                f"- 状态: {storyboard['storyboard_signoff']['status']}",
                f"- 必要资产: {storyboard['storyboard_signoff']['required_assets']}",
                f"- Shot 数量: {storyboard['storyboard_signoff']['shot_count']}",
                f"- 总时长: {storyboard['storyboard_signoff']['total_duration_seconds']}s",
                "",
                "### 单镜头 Prompt 摘要",
                "",
            ]
        )
        for shot_id, prompt in storyboard.get("shot_prompt_pack", {}).items():
            lines.extend([f"#### {shot_id}", "", prompt, ""])

        lines.extend(
            [
                "",
                "## 7. Seedance 2.0 · 15 秒视频提示词",
                "",
                prompts["seedance_20_15s"],
                "",
                "## 8. Seedance 2.5 · 30 秒视频提示词",
                "",
                prompts["seedance_25_30s"],
                "",
                "## 9. Seedance 2.5 · 60 秒 IP 故事视频提示词",
                "",
                prompts["seedance_25_60s"],
                "",
                "## 10. 音乐 / 音效参考提示",
                "",
                prompts["audio_prompt"],
                "",
                "## 11. 负面提示与校验",
                "",
                validator["negative_prompt"],
                "",
                f"- Prompt Validator: {validator['status']}",
                f"- 修复建议: {validator['repair_instructions'] or '无'}",
                "",
                "## 12. 公众号内容包",
                "",
                "### 标题备选",
                "",
            ]
        )
        lines.extend(f"- {title}" for title in wechat["article_draft"]["title_options"])
        lines.extend(
            [
                "",
                "### 正文草案",
                "",
                wechat["article_draft"]["opening"],
                "",
            ]
        )
        for section in wechat["article_draft"]["sections"]:
            lines.extend([f"#### {section['heading']}", "", section["body"], ""])
        lines.extend(
            [
                "### 公众号配图提示词",
                "",
            ]
        )
        for slot, prompt in wechat["image_prompts"].items():
            lines.extend([f"#### {slot}", "", prompt, ""])
        lines.extend(
            [
                "## 13. 平面海报提示词",
                "",
            ]
        )
        for key, item in poster["poster_prompts"].items():
            lines.extend(
                [
                    f"### {key}",
                    "",
                    f"- 比例: {item['ratio']}",
                    f"- 用途: {item['usage']}",
                    f"- 标题方向: {item['headline_direction']}",
                    f"- 微博配文: {item.get('weibo_caption', '')}",
                    "",
                    item["prompt_cn"],
                    "",
                ]
            )
        lines.extend(
            [
                "## 14. 甲方全案方案与验证矩阵",
                "",
                "### 年度节点策略",
                "",
            ]
        )
        for item in client["case_plan"].get("annual_node_strategy", []):
            lines.append(f"- {item['node']} ({item['date_rule']}): {item['angle']}")
        lines.extend(["", "### 验证矩阵", ""])
        for item in client["verification_matrix"]:
            lines.extend(
                [
                    f"#### {item['channel']}",
                    "",
                    f"- 交付物: {item['artifact']}",
                    f"- 证据样例: {item['sample_evidence']}",
                    f"- 检查项: {'；'.join(item['checks'])}",
                    "",
                ]
            )
        lines.extend(
            [
                "## 15. 评分记录",
                "",
                "| Pipeline | Score | Attempt | Missing |",
                "| --- | ---: | ---: | --- |",
            ]
        )
        for key in (
            "RESEARCH_PLANNER",
            "DESIGN_RESEARCH",
            "RESEARCH_SYNTHESIS",
            "INPUT_COMPILER",
            "IP_UNDERSTANDING",
            "IP_BIBLE_BUILDER",
            "STORY_CREATION",
            "COMPLIANCE_REVIEW",
            "VISUAL_DESIGN",
            "ASSET_LEDGER",
            "CINEMATOGRAPHY",
            "STORYBOARD_CONTRACT",
            "PROMPT_GENERATION",
            "PROMPT_VALIDATOR",
            "QA_REPAIR_EXPORT",
            "CHANNEL_PLANNER",
            "CAMPAIGN_CALENDAR",
            "WECHAT_CONTENT",
            "POSTER_DESIGN",
            "CLIENT_CASE_PLAN",
        ):
            item = self.state[key]
            missing = ", ".join(item.get("_missing", [])) or "-"
            lines.append(f"| {key} | {item.get('_score', 0)} | {item.get('_attempt', 1)} | {missing} |")

        lines.append("")
        return "\n".join(lines)

    def save(self, path: str, content: str | None = None) -> str:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content if content is not None else self.generate(), encoding="utf-8")
        return str(output_path)

    @staticmethod
    def _bullet_list(items: Iterable[str]) -> Iterable[str]:
        values = list(items)
        if not values:
            return ["- 无"]
        return [f"- {item}" for item in values]
