---
name: consensus
description: Consensus Governor / Consensus Flow Manager — routes layer-specific adapters into a transaction-like commit/blocked result. Manages fleet-wide state convergence with authority gates, conflict detection, and confidence thresholds. The vault-native implementation lives at claude/consensus_flow_manager/ in the =notes vault.
---

Goal: Provide a consensus-orchestration skill that routes an Intent through capability-matched adapters organized by layer (L1=local FS, L2=code/vault, L3=external runtime), collects provenance-bearing proposals, blocks incompatible state deltas, enforces minimum confidence thresholds, and commits merged deltas only when all required layers are covered and no conflicts remain. The skill does NOT control fleet runtimes directly (launchd, SOPS, Discord, Matrix, Hermes gateway, k3s) — adapters are read/proposal only until explicit authority gates are implemented and verified.

# /consensus

## Role Definition: Consensus Governor / Consensus Manager

The Consensus Governor is the orchestrator role within the ConsensusFlowManager. It:

1. Receives an Intent — a typed request with a goal description, required layers, input data, and authorized roles.
2. Selects adapters — from submitted ModuleAdapterInterface instances, filtering by capability layer match and authority gate.
3. Routes to matched adapters — executes each adapter's execute() method with the intent's input data and a context snapshot of current global state.
4. Collects proposals — each adapter returns a TransactedOutput with provenance, a state delta, a conflict score (0.0–1.0), and a summary.
5. Detects conflicts — if two proposals produce different values for the same key in state_delta, the cycle is blocked and global state is not mutated.
6. Applies confidence threshold — the cycle's confidence is the minimum conflict score across all proposals. If below min_confidence (default 0.80), the cycle is blocked.
7. Commits or blocks — if no conflicts and confidence threshold is met, merged deltas are applied to global state and the result is committed.

### Authority Gate

Adapters with required_authority set to a non-None value are gated. The Intent must include that role in authorized_roles for the adapter to participate. Without proper authorization, the adapter is rejected with "missing authority: <role>".

Adapters requiring authority:
- ExternalMessagingAdapter — requires EXTERNAL_ACTION role (external messaging, notifications, fleet handoffs).

Read/proposal adapters (no authority gate):
- LocalMemoryAdapter — L1, state update proposals
- SourceCodeReferenceAdapter — L2, read-only source graph/reference
- VaultStateAdapter — L1+L2, read-only vault/git state snapshot

## Modular Dependency Graph

```
Intent
  |
  +-- required_layers: [L1, L2, ...]
  +-- input_data: dict
  +-- authorized_roles: set[str]
  |
  v
ConsensusFlowManager.execute_consensus_cycle(intent)
  |
  +-- _select_adapters(intent)
  |     |
  |     +-- Filter adapters by capability layer match
  |     |   (layer string must appear in adapter capabilities)
  |     |
  |     +-- Authority gate check
  |           +-- If adapter.required_authority is None -> pass
  |           +-- If authority set -> check intent.authorized_roles
  |               +-- Missing role -> reject adapter
  |               +-- Role present -> select adapter
  |
  +-- Coverage check: _missing_required_layers(intent.required_layers, selected)
  |     +-- If any required layer has no matching adapter -> BLOCKED
  |           (rejected_adapters["__coverage__"] = "missing required layers: ...")
  |
  +-- Snapshot: copy.deepcopy(self._global_state)
  |
  +-- Execution: for each selected adapter -> adapter.execute(input_data, snapshot)
  |     +-- On exception -> reject adapter ("execution failed: ...")
  |     +-- Collect TransactedOutput proposals
  |
  +-- Conflict detection: compare state_delta keys across proposals
  |     +-- If same key, different values -> BLOCKED
  |           (conflicts list, global state NOT mutated)
  |
  +-- Confidence check: min(proposal.conflict_score for all proposals)
  |     +-- If confidence < min_confidence (default 0.80) -> BLOCKED
  |
  +-- Commit: self._global_state.update(merged_delta) -> COMMITTED
```

### Adapter Layer Model

| Adapter | Layer(s) | Role | Scope | Authority Required | DataSource |
|---|---|---|---|---|---|
| LocalMemoryAdapter | L1 | Proposer | Local_FS | None | In-memory counters/state |
| SourceCodeReferenceAdapter | L2 | Architect | Read_Only | None (needs READ_SOURCE_CODE for read) | repo-weaver / file system |
| VaultStateAdapter | L1, L2 | Observer | Vault_Git | None (needs WRITE_VAULT/GIT_PUSH for write) | Git repository state |
| ExternalMessagingAdapter | L3 | Orchestrator | External_Action | EXTERNAL_ACTION | Handoff ticket / notification generation |

### Data Types

- Intent — input request (frozen dataclass)
- TransactedOutput — individual adapter proposal (frozen dataclass)
- ConsensusResult — cycle outcome with status/committed flag (frozen dataclass)
- ModuleAdapterInterface — Protocol defining adapter contract

## Required Input Structure

### Intent (input to execute_consensus_cycle)

| Field | Type | Default | Description |
|---|---|---|---|
| goal_description | str | (required) | Human-readable description of what the cycle is trying to achieve |
| required_layers | list[str] | (required) | Layer identifiers (e.g., ["L1", "L2"]) that must be covered by selected adapters |
| input_data | dict[str, Any] | {} | Arbitrary payload forwarded to each adapter's execute() method |
| authorized_roles | set[str] | set() | Roles the issuer is authorized for; gates adapters with required_authority |

### ModuleAdapterInterface (adapter contract)

| Attribute/Method | Type | Description |
|---|---|---|
| required_authority | str \| None | Authority role needed; None means no gate |
| get_capabilities() | -> list[str] | Returns capability strings (must include layer identifiers like "Layer: L1") |
| execute(input_data, context_snapshot) | -> TransactedOutput | Produces a proposal given intent data and current global state |
| needs_authority(required_role) | -> bool | Returns True if the adapter needs that role to execute |

### Global State

- Type: dict[str, Any]
- Deep-copied on each cycle for snapshot isolation
- Updated only on commit via self._global_state.update(merged_delta)
- Never mutated on blocked cycles

## Final Output Artifact

### ConsensusResult

| Field | Type | Description |
|---|---|---|
| status | str | "committed" or "blocked" |
| committed | bool | True if state delta was applied |
| provenance | dict | Manager identity, goal, timestamp, proposal adapter IDs, source state hashes |
| state_delta | dict \| None | Merged delta (on commit) or None (on block) |
| conflict_score | float | Minimum conflict score across proposals (0.0–1.0) |
| summary | str | Human-readable result description |
| proposal_count | int | Number of proposals collected |
| rejected_adapters | dict[str, str] | Adapter IDs -> rejection reason (empty dict if all accepted) |

### Commit Outcome

When committed=True:
- status = "committed"
- state_delta contains the merged, applied delta
- Global state is updated
- No conflicts, confidence meets threshold

When committed=False (blocked):
- status = "blocked"
- state_delta = None
- Global state is NOT mutated
- rejected_adapters explains why (missing layer coverage, missing authority, execution failure, conflicts, or low confidence)

### Provenance

Every result includes a provenance dict with:
- manager: "ConsensusFlowManager"
- goal_description: from the Intent
- run_timestamp: epoch seconds at execution
- proposal_adapters: list of adapter IDs that produced proposals
- source_state_hashes: SHA-256 hashes of each proposal's source state

## Verification

```bash
cd ~/Documents/=notes
.venv/bin/python -m pytest tests/test_consensus_flow_manager.py -v
```

Expected: 5 passed (adapter routing + commit, conflict blocking, layer coverage, authority gate, vault git-state proposal read).

## Runtime

The canonical implementation lives at:
- claude/consensus_flow_manager/core.py — ConsensusFlowManager, Intent, ConsensusResult, ModuleAdapterInterface
- claude/consensus_flow_manager/adapters.py — LocalMemoryAdapter, SourceCodeReferenceAdapter, VaultStateAdapter, ExternalMessagingAdapter
- claude/consensus_flow_manager/__init__.py — public exports
- claude/consensus_flow_manager/README.md — implementation overview
- tests/test_consensus_flow_manager.py — focused pytest coverage

## Authority Boundary

- CFM does NOT own: launchd services, SOPS secret loading, Discord posting, Matrix posting, Hermes gateway control, k3s deployments.
- Runtime layers keep those responsibilities until explicit tested adapter + authority gate work is implemented.
- Adapters should start as read/proposal adapters: inspect runtime state, produce provenance, calculate conflict/risk, propose reversible deltas.
- External messaging is gated by EXTERNAL_ACTION authority — no message is sent without explicit authorization.

## Relationship to /gather

consensus is a separate skill from gather. The /gather skill produces a read-only "where was I?" briefing and has HARD RULES against fabrication. consensus handles orchestration, state convergence, and fleet coordination. They do not overlap:

- /gather reads current state and surfaces it — no writes.
- /consensus routes Intents through adapters — writes only on commit with authority gates.

Use /gather for briefing; use /consensus for state convergence decisions.
