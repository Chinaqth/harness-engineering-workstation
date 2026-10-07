# Harness Kernel 4.0

内核只负责入口识别、路由、四阶段调度、状态和证据记录。Domain 负责准备、执行、独立评估与总结。无匹配 Domain 立即结束并告知用户；执行问题记录后继续可做的工作，最终集中披露。

使用 `scripts/resolve_route.py` 路由，使用 `scripts/task_runtime.py` 保存和恢复生命周期。阶段 Skill 由宿主 Agent 调用，内核不直接实现业务。流程结束与目标达成分别记录。

完整契约见 `docs/LIFECYCLE.md`，本地校验运行 `./scripts/harness-check.sh`。
