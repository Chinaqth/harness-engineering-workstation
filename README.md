# Harness Engineering Workstation

面向个人起步、可扩展到大型组织的 AI 工程工作基站。

本仓库不是一份静态规范，而是团队 AI 工作方式的 **System of Record**：规则、流程、技能、评估、决策与演进记录都在这里版本化，并通过 Pull Request 持续改进。

## 北极星

让 AI 生成的交付具备与成熟工程团队相同的特征：

- 有明确上下文，不依赖聊天历史猜测；
- 有计划、有验收标准、有责任边界；
- 默认最小权限，重要操作可审计、可恢复；
- 质量由自动化证据证明，而不是由“看起来不错”证明；
- 每次交付都会沉淀知识，下一次工作更快、更稳。

## 从这里开始

1. 阅读 [AGENTS.md](AGENTS.md)，了解入口和强制规则。
2. 阅读 [架构](docs/ARCHITECTURE.md) 与 [治理模型](docs/GOVERNANCE.md)。
3. 从 `changes/_template/` 复制一份变更提案，按 `3+1` 流程执行。
4. 运行 `./scripts/harness-check.sh` 检查基站完整性。
5. 使用 `skills/harness-audit` 对接入项目进行成熟度审计。

## 仓库结构

```text
.
├── AGENTS.md                  # AI 入口与渐进式索引
├── docs/                      # 架构、治理、成熟度与参考资料
├── rules/                     # 强制规则与工程护栏
├── workflows/                 # 可复用工作流
├── changes/                   # 进行中和已归档的变更记录
├── skills/                    # 团队领域技能
├── scripts/                   # 确定性检查
└── .github/                   # PR 模板与持续检查
```

## 当前状态

当前为 `v0.1` 基线：先建立可执行的最小闭环，再用真实项目反馈完善。下一阶段重点见 [成熟度模型](docs/MATURITY_MODEL.md)。
