# 独立评估记录

- Evaluator: `/root/g2_evaluator`（独立、只读上下文）
- Date: 2026-09-02
- Verdict: **FAIL**

## 发现

1. `P1`：旧版 decisions record 仅要求非空字符串，代理自报“已展示/已批准”即可绕过 AC-03 与 AC-05。
2. `P1`：CLI Bundle 仍是旧协议；生成器以 Git HEAD 标记来源却复制脏工作树，可能制造不可追溯 Bundle。
3. `P2`：Domain `domain-check.sh` 因语言扫描 SIGPIPE 与默认 Python 缺少 `tomllib` 未能完整通过。
4. `P2`：变更记录的 phase 状态不一致。

## 已触发的修复

- 新增 Approval Decisions 2.0 结构化凭证契约，展示证据绑定计划 digest，用户决定绑定 scope fingerprint、
  durable message reference 与 gate required role；拒绝自由文本和代理自报。
- CLI Bundle 生成器在读取 revision 与复制文件前拒绝 Kernel 或 Domain 脏工作树。
- Domain 检查支持显式 `HARNESS_PYTHON`，消除 SIGPIPE，并对既有、明确隔离的中文资料路径使用显式豁免。
- 统一 change phase 状态，修复后重新进入独立评估。

该 FAIL 结论不会被生成者覆盖；后续通过结论必须由独立 Evaluator 重新签发。

## 修复后复评

- Verdict: **BLOCKED**
- 已独立确认 AC-01 至 AC-09、Domain 完整检查以及 CLI 脏源码失败关闭。
- 唯一前置阻塞为 AC-11：需要先创建不可变 Domain revision、匹配的 Kernel pin/revision，才能正向生成
  并验证 CLI Bundle。该结论不是新的实现失败。

## 最终独立验收

- Verdict: **PASS**
- Domain revision `3365343ee3025759160461a69613110185c92674` 与 Kernel pin 精确匹配，两个源码树干净。
- 独立临时 CLI 副本从 clean revisions 正向生成并验证 874 个 Runtime 文件；其 manifest 与候选 Bundle
  字节一致。
- Bundle 包含 Kernel protocol 3.0、Routing Plan 4.0、Approval Decisions 2.0、HarmonyOS 6.0.0 与
  Web 1.0.0；active 状态一致。
- CLI `npm run check` 21/21 tests 通过，无 P0/P1 发现。
