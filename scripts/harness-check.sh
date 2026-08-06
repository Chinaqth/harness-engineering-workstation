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
  "rules/CORE.md"
  "workflows/3-plus-1.md"
  "changes/README.md"
  "config/domain-pack-sources.json"
  "config/protocol-versions.json"
  "config/task-workflows.json"
  "schemas/task-workflow-registry.schema.json"
  "schemas/task-envelope.schema.json"
  "schemas/routing-plan.schema.json"
  "schemas/project-domain-overlay.schema.json"
  "schemas/domain-pack-source.schema.json"
  "schemas/protocol-versions.schema.json"
  "examples/project-domain-overlay.json"
  "scripts/validate_domain_source.py"
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
