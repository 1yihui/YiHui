# YiHui Skills

OpenClaw / Claude Code / Cursor 技能集合。拿来即用，持续更新。

## 收录技能

| Skill | 功能 | 适用场景 |
|-------|------|----------|
| [context-mode](./skills/context-mode/) | 98% 上下文压缩，工具输出沙箱 | Token 账单优化、复杂项目分析 |
| [git-monitor](./skills/git-monitor/) | Git 仓库监控，更新摘要 | 追踪依赖项目、代码变化通知 |
| [github-monitor](./skills/github-monitor/) | GitHub Release/PR/commit 监控 | 关注 OpenClaw 动态、第三方库更新 |
| [skill-vetter](./skills/skill-vetter/) | Skill 安全审查 | 安装第三方 skill 前必跑 |
| [self-improvement](./skills/self-improvement/) | 错误日志 + 持续改进 | 每次失败后记录，循环优化 |
| [agent-builder](./skills/agent-builder/) | 构建高表现 Agent | 从零设计新 Agent |
| [healthcheck](./skills/healthcheck/) | 系统巡检 + 安全审计 | 定期体检、问题诊断 |

## 安装方式

### 方式一：复制 SKILL.md
直接复制对应 `skills/<name>/SKILL.md` 到你的 agent workspace 的 `skills/` 目录。

### 方式二：ClawHub（推荐）
```bash
openclaw skills install clawhub:@yihui/<skill-name>
```

### 方式三：Git Submodule
```bash
git submodule add https://github.com/1yihui/YiHui.git skills/<name>
```

## 提交新 Skill

参见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 兼容性

- ✅ OpenClaw
- ✅ Claude Code
- ✅ Cursor
- ✅ VS Code Copilot
- ✅ Gemini CLI
- ✅ 通用（大多数 skill 平台无关）
