#!/usr/bin/env bash
set -u

root="${1:-.}"
failures=0

required=(
  "AGENTS.md"
  "docs/ARCHITECTURE.md"
  "docs/AUTONOMY_POLICY.md"
  "docs/GOVERNANCE.md"
  "docs/MATURITY_MODEL.md"
  "docs/OBSERVABILITY.md"
  "docs/ENTERPRISE_DOMAIN_ARCHITECTURE.md"
  "docs/ROUTING.md"
  "docs/PROTOCOL_VERSIONING.md"
  "docs/PROJECT_ACTIVATION.md"
  "rules/CORE.md"
  "workflows/3-plus-1.md"
  "changes/README.md"
  "config/domain-pack-sources.json"
  "config/protocol-versions.json"
  "config/task-workflows.json"
  "schemas/task-workflow-registry.schema.json"
  "schemas/task-envelope.schema.json"
  "schemas/routing-plan.schema.json"
  "schemas/approval-decisions.schema.json"
  "schemas/project-domain-overlay.schema.json"
  "schemas/domain-pack-source.schema.json"
  "schemas/protocol-versions.schema.json"
  "schemas/project-harness-bridge.schema.json"
  "examples/project-domain-overlay.json"
  "examples/approval-decisions.json"
  "scripts/validate_domain_source.py"
  "scripts/sync_domain_pin.py"
  "scripts/validate_protocol_versions.py"
)

for path in "${required[@]}"; do
  if [[ -f "$root/$path" ]]; then
    printf 'PASS %s\n' "$path"
  else
    printf 'FAIL %s is missing\n' "$path"
    failures=$((failures + 1))
  fi
done

while IFS= read -r secrets_file; do
  printf 'FAIL possible secret filename: %s\n' "$secrets_file"
  failures=$((failures + 1))
done < <(find "$root" -type f \( -name '*.pem' -o -name '*.key' -o -name '.env' \) -not -path '*/.git/*')

while IFS= read -r generated_doc; do
  if perl -CSDA -ne 'exit 1 if /[\p{Han}\p{Hiragana}\p{Katakana}\p{Hangul}]/' "$generated_doc"; then
    continue
  fi
  printf 'FAIL non-English text in generated document: %s\n' "$generated_doc"
  failures=$((failures + 1))
done < <(
  find "$root" -type f \
    \( -name '*.md' -o -name '*.yml' -o -name '*.yaml' \) \
    -not -name 'README-CH.md' \
    -not -name '*.[a-z][a-z]-[A-Z][A-Z].md' \
    -not -path '*/changes/*.md' \
    -not -path '*/changes/*/*.md' \
    -not -path '*/changes/archive/*/*.md' \
    -not -path '*/.git/*'
)

if ! python3 "$root/scripts/validate_change.py" "$root"; then
  failures=$((failures + 1))
fi

if ! python3 "$root/scripts/knowledge-garden.py" "$root"; then
  failures=$((failures + 1))
fi

if ! python3 "$root/scripts/validate_protocol_versions.py" "$root"; then
  failures=$((failures + 1))
fi

if ! python3 "$root/scripts/validate_routing.py" "$root"; then
  failures=$((failures + 1))
fi

domain_checkout="${HARNESS_DOMAIN_PACKS_CHECKOUT:-}"
if [[ -z "$domain_checkout" ]]; then
  sibling_checkout="$(cd "$root/.." && pwd)/harness-domain-packs"
  if [[ -d "$sibling_checkout/.git" ]]; then
    domain_checkout="$sibling_checkout"
  fi
fi
if [[ -n "$domain_checkout" ]]; then
  if ! python3 "$root/scripts/validate_domain_source.py" "$root" \
    --domain-root "$domain_checkout"; then
    failures=$((failures + 1))
  fi
  pin="$(python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["sources"][0]["ref"])' \
    "$root/config/domain-pack-sources.json")"
  remote_head="$(git -C "$domain_checkout" rev-parse --verify --quiet 'refs/remotes/origin/HEAD^{commit}' \
    || git -C "$domain_checkout" rev-parse --verify --quiet 'origin/main^{commit}' || true)"
  if [[ -n "$remote_head" && "$pin" != "$remote_head" ]]; then
    counts="$(git -C "$domain_checkout" rev-list --left-right --count "$pin...$remote_head" 2>/dev/null || printf '?\t?')"
    ahead="${counts%%[[:space:]]*}"
    behind="${counts##*[[:space:]]}"
    if [[ "$behind" != "0" ]]; then
      printf 'WARN Domain pin %.12s is %s commit(s) behind the remote default branch %.12s' \
        "$pin" "$behind" "$remote_head"
      printf ' (local refs may be stale); run scripts/sync_domain_pin.py\n'
    else
      printf 'WARN Domain pin %.12s is not on the recorded remote default branch %.12s' \
        "$pin" "$remote_head"
      printf ' (%s commit(s) ahead; unpushed work or stale local refs)\n' "$ahead"
    fi
  fi
else
  printf 'SKIP cross-repository Domain compatibility: set HARNESS_DOMAIN_PACKS_CHECKOUT to an authorized checkout\n'
fi

if ! python3 -m unittest discover -s "$root/tests"; then
  failures=$((failures + 1))
fi

if (( failures > 0 )); then
  printf '\nHarness check failed with %d issue(s).\n' "$failures"
  exit 1
fi

printf '\nHarness check passed.\n'
