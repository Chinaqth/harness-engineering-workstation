# 独立评估报告

- Change ID: `20260809-governed-model-fallback`
- Evaluator: 独立 Evaluator（未参与本变更实现）
- Verdict: **pass**
- Evaluated revision: Kernel `9b30a43e32c897f395c52e2f6ffbf43f92121aa0` 加当前未提交变更；Domain Packs `0ca789ced412a5cceb4c247c3dd726fcb10b9882`
- Environment: macOS，本地工作树；Python 3；只读 HmTest 与 Domain Pack；临时测试目录位于 `/tmp` 或 `/private/tmp`
- Evaluated at: 2026-08-09 16:35:25 +0800

## 发现

未发现范围内 P0 或 P1 问题。

### P2/P3

无。

## 关键旅程

### AC-02、AC-03、AC-08：完整专业资产的 HmTest 路由

前置条件：使用旧 HmTest Envelope 作为事实来源，但将 `task_id`、`intent` 和证据要求改为 Evaluator
新输入；固定使用上述 Domain Pack revision；不修改 HmTest 源码。

执行：

```bash
jq '.task_id="eval-hmtest-route-20260809" |
    .intent="独立评估 HmTest 单页状态管理迁移路由，不执行源码修改。" |
    .required_evidence += ["独立 Routing Plan Schema 校验"]' \
  changes/20260809-hmtest-v1-v2-migration/task-envelope.json \
  > /tmp/harness-evaluator.4eAEYI/hmtest-envelope.json
python3 scripts/resolve_route.py \
  /tmp/harness-evaluator.4eAEYI/hmtest-envelope.json \
  --root . \
  --domain-root /Users/minikukala/harness-domain-packs \
  -o /tmp/harness-evaluator.4eAEYI/hmtest-plan.json
```

预期：选择 HarmonyOS 状态管理迁移 Capability 及三个 Skill；未选依赖只形成软 fallback；保留实现审批门。

实际：`execution_mode=domain_augmented`、`status=needs_approval`；选择
`engineering.harmonyos/arkui-state-management-v1-to-v2-migration`，加载
`harmonyos-engineering`、`hmos-arkui-statemgt-migration`、`hmos-arkui-knowledge-retriever`；
三个未选 Capability 依赖记为 soft fallback；一个 implementation gate 为 `pending`；
`conflicts=[]`、`missing_inputs=[]`。Routing Plan 3.0 Schema 为 0 error，状态不变量为 0 error。

### AC-01、AC-02、AC-03、AC-08：零 Domain 的模型原生兜底

前置条件：Evaluator 新建 `refactoring/local-config-normalization` Envelope；`operation=modify`，没有
注册的匹配 Domain、Capability 或 Skill。

执行：

```bash
python3 scripts/resolve_route.py \
  /tmp/harness-evaluator.4eAEYI/fallback-envelope.json \
  --root . \
  --domain-root /Users/minikukala/harness-domain-packs \
  -o /tmp/harness-evaluator.4eAEYI/fallback-plan.json
```

预期：不伪造专业资产；继续 Kernel 治理并保留修改审批门。

实际：`execution_mode=model_native`、`status=needs_approval`、`selections=[]`；fallback 明确记录无
active enabled Domain capability；一个 implementation gate 为 `pending`；`conflicts=[]`、
`missing_inputs=[]`。Routing Plan 3.0 Schema 为 0 error，状态不变量为 0 error。

### AC-03、AC-08：真正硬性条件缺失时阻断

前置条件：Evaluator 新建 `defect/web-change` Envelope，但刻意不提供 `expected_behavior`。

执行：

```bash
python3 scripts/resolve_route.py \
  /tmp/harness-evaluator.4eAEYI/hard-block-envelope.json \
  --root . \
  --domain-root /Users/minikukala/harness-domain-packs \
  -o /tmp/harness-evaluator.4eAEYI/hard-block-plan.json
```

预期：缺少定义偏差所必需的预期行为时 fail closed，不生成可执行审批门。

实际：`status=needs_input`、`approval_gates=[]`、`selections=[]`；`missing_inputs` 明确指出
`expected_behavior` 是 defect remediation 的必要输入。Routing Plan 3.0 Schema 为 0 error，状态不变量为 0 error。

### AC-04：非 Git 项目的 change 根目录

执行：

```bash
project_dir=$(mktemp -d /tmp/non-git-project.XXXXXX)
python3 scripts/init_change.py 20260809-evaluator-non-git \
  --project-root "$project_dir" --kernel-root .
test ! -e "$project_dir/.git"
# 填入模板要求的最小 ID、Owner、Risk、Review-By 和 acceptance change_id 后：
python3 scripts/validate_change.py "$project_dir"
```

实际：记录创建在显式的
`<project-root>/changes/20260809-evaluator-non-git/`，项目没有 `.git`；六个 G2 模板文件均存在；
填入最小有效元数据后输出 `PASS validated 1 change record(s).`。未移动或删除任何旧记录。

### AC-05：语言政策边界

新建 change 的五份人类可读 Markdown 模板均包含中文；`acceptance.json` 的机器字段保持英文
（`change_id,criteria,risk,schema_version,status`）。完整 Harness 检查同时验证 changes 例外和其他
生成文档的英文要求，没有把中文默认扩大到 Schema、代码标识符或所有技术文档。

## 验收对账

| 标准 | 结论 | 独立证据 |
| --- | --- | --- |
| AC-01 | passing | 零 Domain/Skill 新输入仍进入受治理审批；硬条件缺失另行阻断 |
| AC-02 | passing | HmTest `domain_augmented` 与零 Domain `model_native` 均生成有效 Routing Plan 3.0 |
| AC-03 | passing | soft fallback 为 `needs_approval`；缺 `expected_behavior` 为 `needs_input` 且无 gate |
| AC-04 | passing | 无 `.git` 临时项目完成显式根目录初始化和 change 校验 |
| AC-05 | passing | 中文 Markdown、英文机器字段边界与完整检查一致 |
| AC-06 | passing | `migration.md` 保留复制、哈希核对、源记录指针和回滚步骤；本评估未修改 HmTest |
| AC-07 | passing | 44 项定向测试、61 项完整测试、协议/Schema/路由/跨仓库检查全部通过 |
| AC-08 | passing | 本报告独立复现三类关键路由并给出最终 pass 结论 |

## 完整验证证据

```text
$ python3 -m unittest tests.test_resolve_route tests.test_routing_validation tests.test_protocol_versions tests.test_init_change
Ran 44 tests in 3.260s
OK

$ bash scripts/harness-check.sh
PASS validated 12 change record(s).
Protocol version manifest validation passed.
Routing contract validation passed.
Cross-repository Domain compatibility validation passed.
Ran 61 tests in 6.837s
OK
Harness check passed.

$ git -C /Users/minikukala/harness-domain-packs rev-parse HEAD
0ca789ced412a5cceb4c247c3dd726fcb10b9882
```

## 安全、权限、兼容与回滚观察

- 零 Domain 不会移除 Kernel implementation gate；外部副作用的附加门由完整测试覆盖。
- 缺必要输入时不会产生 gate 或可继续状态；未知 Kernel task class 在输入边界拒绝，由完整测试覆盖。
- Domain Pack 固定 revision 与配置一致，跨仓库兼容检查通过且工作树干净。
- 旧 Routing Plan 兼容、3.0 迁移矩阵和协议版本由完整检查验证。
- 回滚方案覆盖协议、Schema、Resolver、校验器、模板、文档、示例和测试的原子恢复；外部记录未移动，
  因此不需要外部数据恢复。

## 限制与残余风险

- 本评估验证的是 Router/Resolver 的可观察输出，不执行 HmTest 源码迁移、构建或设备运行；这些属于
  已暂停的后续变更，而非本 G2 范围。
- 三份独立计划和非 Git fixture 位于临时目录，可能被系统清理；本报告保留完整命令、输入变换、关键
  输出与状态断言，可重复生成。
- Kernel 变更尚未提交，因此 evaluated revision 由 `HEAD` 加当前工作树共同定义；提交前应再次运行
  `bash scripts/harness-check.sh`，防止工作树继续变化造成证据漂移。

## 最终结论

**pass**。所有关键验收标准均被独立证据证明，未发现范围内 P0/P1。最小后续动作是在实际提交前
重新运行完整 Harness 检查；本评估不授权提交、推送、发布、HmTest 迁移或旧记录移动。
