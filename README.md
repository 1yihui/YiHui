# YiHui Skills ⭐ 中文技能库

> 让 AI 编程助手真正"会干活"——一套可组合的 Skill 工作法，覆盖上下文压缩、Git 监控、持续改进、系统巡检等核心场景。

[![GitHub Stars](https://img.shields.io/github/stars/1yihui/YiHui?style=flat-square&logo=github)](https://github.com/1yihui/YiHui/stargazers)
[![Skills](https://img.shields.io/badge/skills-13-blue?style=flat-square)](#收录技能)
[![Platform](https://img.shields.io/badge/platform-OpenClaw%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Gemini%20CLI-green?style=flat-square)](#兼容性)
[![License](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)](LICENSE)

---

## 🎯 这个仓库解决什么问题

AI 编程助手"会写代码，但不会干活"。

它拿到需求就开干，从不问你边界条件、有没有现成模块、会不会影响其他功能。简单任务没问题，多文件多步骤就开始跑偏。

**YiHui Skills 就是那套"纪律"**——每个 Skill 都是一个工作方法论的条文，遇到对应场景自动触发，让 AI 按稳定流程走，而不是自己瞎发挥。

---

## ⚡ 快速上手

### 安装（任意一个即可）

```bash
# 方式一：ClawHub（推荐）
openclaw skills install clawhub:@yihui/context-mode

# 方式二：复制 SKILL.md 到 workspace/skills/
# 直接复制 skills/<name>/SKILL.md 到你的 agent skills/ 目录

# 方式三：Git Submodule
git submodule add https://github.com/1yihui/YiHui.git skills/<name>
```

### 必装推荐（新手第一步）

| 优先级 | Skill | 原因 |
|--------|-------|------|
| 🥇 | `context-mode` | Token 节省 65-90%，告别上下文焦虑 |
| 🥈 | `skill-vetter` | 安装任何第三方 Skill 前必跑安全审查 |
| 🥉 | `self-improvement` | 让 Agent 记住你的偏好，越用越聪明 |

---

## 📦 收录技能（13 个）

### 🚀 效率与上下文

| Skill | 功能 | 适用场景 |
|-------|------|----------|
| [`context-mode`](./skills/context-mode/) | **98% 上下文压缩**——工具输出沙箱执行，只把精简结果送进上下文 | Token 账单优化、复杂项目分析、30分钟+长会话 |
| [`taskflow`](./skills/taskflow/) | 跨会话持久化任务编排，子任务链接+状态机 | 多步骤项目、后台任务、复杂工作流 |

### 🔍 监控与追踪

| Skill | 功能 | 适用场景 |
|-------|------|----------|
| [`git-monitor`](./skills/git-monitor/) | Git 仓库监控，更新摘要 | 追踪依赖项目、代码变化通知 |
| [`github-monitor`](./skills/github-monitor/) | GitHub Release/PR/commit 监控 | 关注 OpenClaw 动态、第三方库更新 |
| [`system-inspection`](./skills/system-inspection/) | OpenClaw 系统巡检 SOP | 定时体检、低打扰式诊断 |

### 🛡️ 安全与质量

| Skill | 功能 | 适用场景 |
|-------|------|----------|
| [`skill-vetter`](./skills/skill-vetter/) | **安全审计**——安装第三方 Skill 前必跑，检查权限和可疑代码模式 | 所有第三方 Skill 安装前必跑 |
| [`healthcheck`](./skills/healthcheck/) | 系统巡检 + 安全审计 | 定期体检、问题诊断 |
| [`node-connect`](./skills/node-connect/) | 设备配对诊断 | QR 连接失败、token 失效排查 |

### 🧠 记忆与学习

| Skill | 功能 | 适用场景 |
|-------|------|----------|
| [`self-improvement`](./skills/self-improvement/) | 错误日志 + 持续改进，每次失败后记录，循环优化 | 减少重复犯错、让 Agent 记住你的偏好 |
| [`session-logs`](./skills/session-logs/) | jq 搜索历史会话 | 查旧对话、追溯决策、找回断点 |

### 🤖 Agent 构建与编排

| Skill | 功能 | 适用场景 |
|-------|------|----------|
| [`agent-builder`](./skills/agent-builder/) | 从零设计高表现 Agent | 创建新 Agent、设计 persona+工作流 |
| [`agent-swarm`](./skills/agent-swarm/) | 多 Agent 协作框架，任务路由+状态机 | 多角色协作、大任务分解 |
| [`minimax-team-rules`](./skills/minimax-team-rules/) | 小美/大龙/小语协作规范 | 多 Agent 团队规则同步 |

---

## 🌟 context-mode 专项介绍（Star 13000+）

context-mode 是本仓库最热门的 Skill，解决 AI 编程的"上下文焦虑"：

```
315KB 原始输出 → 5.4KB 精简结果
56KB 网页快照 → 299 字节索引摘要
AI 回复 Token 节省 65-75%
```

**核心四大能力：**
1. **上下文压缩** — 工具输出沙箱执行，只进精简结果
2. **会话连续性** — SQLite 记录每次操作，长会话不"失忆"
3. **用代码思考** — 让 AI 写脚本分析，而不是把大文件读进上下文
4. **输出压缩** — 技术准确性不变，token 大幅减少

已在 [ClawHub](https://clawhub.ai/1yihui/yihui-context-mode) 上架，评分 3.40。

---

## 🤝 兼容性

| 平台 | 状态 |
|------|------|
| ✅ OpenClaw | 完整支持 |
| ✅ Claude Code | 完整支持（支持全部 5 个 Hook） |
| ✅ Cursor | 支持（上下文压缩 98%） |
| ✅ VS Code Copilot | 支持 |
| ✅ Gemini CLI | 支持 |
| ✅ 通用 | 大多数 Skill 平台无关 |

---

## 📋 提交新 Skill

欢迎贡献！参见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

格式要求：
- 每个 Skill 目录必须有 `SKILL.md`
- frontmatter 包含 name、description、triggers、tags、compatibility
- 无安全风险，敏感操作有明确警告

---

## 📄 License

MIT — 可商用，可修改，可分发。

---

_持续更新，欢迎 Star ⭐_
