# 技能元数据检查记录

检查日期：2026-11-01。基线提交：`26645a568967126cf3f09a259d439ffce6606b70`。
范围：仓库全部 33 份 `skills/**/SKILL.md`，以及名称引用和相关 hook / `_meta.json`。
本次是静态检查，没有在实际 OpenClaw 安装环境中测试加载、配置或调用。

## 发现与修复

- 33 份 frontmatter 均可解析为 YAML mapping，未发现语法错误或显式重复 YAML 键。
- 发现唯一一组重名：`self-improvement` 与 `self-improving-agent` 两个目录都声明
  `name: self-improvement`。只修改后者为 `name: self-improving-agent`。
- `taskflow`、`node-connect`、`minimax-team-rules`、`system-inspection` 的 frontmatter
  结束后残留 `tags`、`compatibility`、`license`、`source`，共 16 个重复字段。
  后三项与有效 frontmatter 值相同；标签取有序并集，保留残留区独有的 8 个标签，
  再删除残留区块。这些残留原本属于 Markdown 正文，并非 YAML 解析错误。
- 全文搜索这些元数据字段，并人工区分 Markdown 示例后，未发现其他同类残留。
- 28 份 `SKILL.md` 完全未改动；其余 5 份的技能指令正文保持不变。
  未修改既有技能脚本、hook、目录、根 README、分类索引或安装说明。

| 技能目录（位于 `skills/`） | 修复前发现 | 处理后 |
| --- | --- | --- |
| agent-builder | 无 | 通过 |
| agent-memory-wisdom | 无，声明名为 `brain` | 保留，通过 |
| agent-swarm | 无 | 通过 |
| agent-team-orchestration | 无 | 通过 |
| ai-image-prompts | 无，声明名为 `ai-image-prompts-skill` | 保留，通过 |
| akshare-stock | 无 | 通过 |
| context-mode | 无 | 通过 |
| daily-news-digest | 无，使用显示式名称 | 保留，通过 |
| dfcf-stock-intraday | 无，声明名为 `eastmoney-intraday` | 保留，通过 |
| git-monitor | 无，使用 `trigger` 扩展字段 | 保留，通过 |
| github-monitor | 无 | 通过 |
| healthcheck | 无 | 通过 |
| memclaw | 无 | 通过 |
| minimax-team-rules | 4 个正文重复字段 | 合并标签、清理，通过 |
| node-connect | 4 个正文重复字段 | 合并标签、清理，通过 |
| oc-full-ops-audit-recipe | 无 | 通过 |
| openclaw-multi-agent-orchestrator | 无 | 通过 |
| openclaw-ops | 无 | 通过 |
| peekaboo | 无 | 通过 |
| personality-switcher | 无 | 通过 |
| rss-feed-digest | 无，声明名为 `rss-digest`，标签为字符串 | 保留，通过 |
| seedance | 无 | 通过 |
| self-improvement | 与下一项重名 | 保留原名称，通过 |
| self-improving-agent | 声明名为 `self-improvement` | 改为 `self-improving-agent`，通过 |
| self-improving | 无，使用显示式名称 | 保留，通过 |
| session-logs | 无，嵌套 YAML 元数据有效 | 保留，通过 |
| skill-vetter | 无 | 通过 |
| system-inspection | 4 个正文重复字段 | 合并标签、清理，通过 |
| taskflow | 4 个正文重复字段 | 合并标签、清理，通过 |
| taskflow-inbox-triage | 无 | 通过 |
| video-prompting-guide | 无 | 通过 |
| weather | 无，嵌套 YAML 元数据有效 | 保留，通过 |
| yinyo-liuyao | 无，多行描述有效 | 保留，通过 |

## 名称兼容性与迁移

两份同名技能的指令正文相同，frontmatter 存在差异；`self-improving-agent` 还包含
脚本、资产和 hook，且 `_meta.json` 的 slug 已为 `self-improving-agent`。
保留 `self-improvement` 目录的原名称，让另一个名称与其既有目录及 slug 一致，
只需修改一个字段，避免删除技能或重构功能。

[OpenClaw 技能文档](https://docs.openclaw.ai/skills) 说明同名技能存在来源优先级；
[配置文档](https://docs.openclaw.ai/tools/skills-config) 说明 `skills.entries` 默认使用
技能 `name`，可由 `metadata.openclaw.skillKey` 覆盖。由此判断：改名可能影响按名称
配置和显式调用。本次未验证同一目录来源下两个重名技能的具体加载结果。

- 使用 `self-improvement` 目录的用户继续使用原名称。
- 使用 `self-improving-agent` 目录的用户，如曾为它设置
  `skills.entries["self-improvement"]`，应先备份配置，再将针对它的配置转到
  `skills.entries["self-improving-agent"]`，包括已有的 `enabled: false`。
  按名称引用它的 allowlist、自动化或显式调用也需同步检查。
- 如果同时使用两份技能，为两者分别保留各自的配置；不要盲目搬走仍属于
  `self-improvement` 的配置。仓库中未发现需要修改的 `skills.entries` 配置。
- 不添加指向旧名的别名或 `skillKey`：两份技能共享旧配置键会继续耦合配置，
  也不能据此保证旧调用能无歧义地指向任意一份技能。
- hook 的 `self-improvement` 标识和启用命令保持原样，它不是本次改名的技能字段。
  目录路径、资源路径、触发描述及 `.learnings/` 数据约定均保持原样。

## 静态校验与复现

```bash
python -m pip install -r scripts/requirements-metadata.txt
python scripts/validate_skill_metadata.py
python -m unittest discover -s tests -p 'test_skill_metadata.py' -v
git diff --check
```

修复后结果：33/33 份文件通过，17 项回归测试通过。将同一个校验器对基线快照运行，
退出码为 1，报告 16 个正文残留字段和 1 个名称重复；修复后退出码为 0。
另以解析后的元数据及指令正文逐项比较，确认 8 个独有标签保留、指令正文未改变。

校验器仅依赖 PyYAML（固定版本），使用安全加载器，并拒绝各层显式重复键。
合法 YAML merge 覆盖、内联 JSON、多行描述、扩展字段以及现有显示式名称均有测试覆盖。
正文残留检查只覆盖 frontmatter 后的无代码围栏元数据前缀；遇到标题、围栏、引用
或普通说明即停止，避免把正文示例误判为元数据。这不是完整 Markdown linter，
不保证发现正文任意位置的残留，也不验证运行环境、URL 可用性或技能功能。

GitHub Actions 在 push、pull_request、workflow_dispatch 时运行相同的测试和全量检查，
只授予 `contents: read`，无需仓库密钥。是否将该检查设为合并必需项由仓库维护者决定。
