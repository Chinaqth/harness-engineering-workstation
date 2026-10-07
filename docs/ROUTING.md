# Routing 5.0

Route matches exact task_type against active, compatible registered Domain routes.
It reads immutable Git commits or explicitly content-addressed development snapshots.
An optional overlay limits enabled Domains, pins versions and disables capabilities.
Equal-priority routes choose the lexicographically first stable route ID and record a
route_tie issue. Multiple matching Domains are returned in registry order; the host
integrates their professional outputs for each stage into one stage receipt.

Outputs: matched, no_match, source_error. no_match immediately ends the task and tells
the user that no Domain matched and no professional work was executed. source_error
reports broken configuration, version mismatch, invalid metadata or unavailable source;
it must never masquerade as no_match. Neither condition executes Domain lifecycle stages.

A selection contains Domain ID/version, route ID, capability IDs, reason, and explicit
prepare/execute/evaluate/summarize Skill bindings. Missing stage Skills become issues;
there is no Kernel execution fallback. No risk classification or approval state belongs
in routing. Professional uncertainty belongs in Domain preparation/results.

Pass `--domain-root` for checkouts, or set HARNESS_DOMAIN_PACKS_CHECKOUT. Installed
Runtime uses its sibling domains directory. Source SHA-256 covers authoritative Domain
entries; mismatch is diagnosed before any professional invocation.
