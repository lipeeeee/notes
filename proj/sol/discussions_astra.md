# Sol — Complete Project Summary

**As of:** 4 November 2026. **Scope:** the available Sol/Saint project conversations, original research plan, and both architecture reviews; includes directly relevant drafting/coaching discussions. Repeated explanations are consolidated. This is a project handover, not a claim that every proposal is implemented or experimentally validated. No repository or dataset was re-audited for this summary.

**Status vocabulary:** **Current** = explicit project direction or latest reported implementation; **Proposed** = a recommendation/experiment; **Open** = unresolved; **Historical** = earlier work retained for context. Later user choices take precedence over the original plan.

## 1. Project identity and current direction

| Topic | Consolidated position |
| --- | --- |
| Name | **Sol**, previously **Saint**. An opposite philosophy, **Sinner/Lua**, has been discussed and deferred. |
| Goal | A professional League of Legends draft evaluator and opinionated pick/ban agent. |
| Stack | Python/PyTorch; develop through small, reproducible iterations. |
| Core distinction | Historical win prediction, strategic preference, and sequential decision value are different targets. |
| Main data | Oracle’s Elixir professional games; expert judgments supply the intended philosophy. |
| Core inference | Draft-visible information; exclude team/player identities, betting odds, and current-game post-draft statistics. |
| Latest minimal model | Additive champion-role strengths, with a bias and potentially first-pick context. |
| Planned preference training | Full-draft expert preference first; partial-draft value learned from full-draft preference under a defined continuation process. |
| Search direction | Preference-led MCTS/PUCT; begin with a tiny implementation to learn the mechanics. Outcome prediction remains separate. |
| Hardware | Laptop RTX 3050, 4 GB VRAM; small models and batched evaluation are the intended starting point. |
| Latest additions | Draft health/fragility and a separate representation of observed meta behavior. Neither has a finalized implementation. |

Sol is intended to question habitual professional drafting, not simply reproduce pick frequency. Winner labels alone cannot establish that professional choices are strategically wrong: outcomes also reflect team strength, mastery, preparation, and execution. There is no accurate cheap League simulator that makes this ordinary AlphaZero self-play.

## 2. Drafting philosophy

The intended philosophy is LS-inspired, explicitly contextual, and independently defined—not a claim of LS endorsement or authenticated judgments on every champion.

- Prefer coherent win conditions, repeatable damage, protection, range/space control, waveclear, resource efficiency, recoverability, and scaling that can actually be reached and used.
- Evaluate answers to enemy threats, target access, setup requirements, cooldown dependence, and the burden of execution on both teams.
- Favor multiple playable states and useful redundancy; avoid depending on one fragile answer or demanding gold/XP for every position simultaneously.
- Preserve flexes, blind-pick stability, counterpick options, and information advantage during the draft.
- Resist handshakes, unexplained meta priority, local counters that damage the composition, and unsupported novelty rewarded by model error.
- “Scaling wins,” “disengage beats engage,” “BOT requires a marksman,” and “early thematic picks are bad” are not universal rules.
- Separate analytical evaluation under stated competence assumptions from optional practical roster pools, mastery, and execution constraints.

**Sinner/Lua:** a possible later aggressive early/mid-game, snowball-oriented preference model. It could reuse data, factual representations, and search with different preference supervision. Its name, implementation, and style conditioning remain open.

## 3. How the plan evolved

| Stage | Main development |
| --- | --- |
| LDANet | Outcome prediction with champion embeddings, bans, synergy/counter statistics, patch features, and deeper networks. Reported validation accuracy reached roughly 61–63%. |
| August Saint plan | Broad research design: separate outcome/preference outputs, ontology, weak supervision, temporal benchmarks, then search. |
| September reviews | Corrected uncertainty signs, role-information leakage, comparison anchoring, counter direction, weighting, and symmetry. Reduced the proposed first experiment set. |
| Late September | Chosen per-iteration modules plus an additive, backward-compatible `SolDataset` API; emphasis on iterative research and clean temporal evaluation. |
| October | Smaller baseline after overfitting; inference and memory discussions; full/partial preference heads; preference-first tiny MCTS/PUCT; role-completion concerns. |
| Late October–November | Draft health, proactive tools in defensive compositions, and encoding meta without treating popularity as quality. |

The original plan’s large baseline ladder and complete-ontology gate are a **backlog**, not prerequisites to the first preference experiment. Its default mixed outcome/preference utility was superseded by preference-first search. Its Blue-oriented uncertainty penalty was mathematically incorrect and must not be reused.

## 4. Output meanings and information contracts

| Output/component | Meaning | Supervision or source |
| --- | --- | --- |
| `p_hist` | Historical pro win probability conditional on allowed inputs | Real match results; calibration on appropriate held-out data |
| `q_sol` | Strategic advantage under Sol’s stated philosophy | Expert comparisons and anchors; optional audited weak labels |
| `V_partial` | Value of an unfinished draft under specified future choices | Full-draft preference evaluations, legal completions, or search targets |
| Policy/opponent model | Which legal actions are plausible or likely | Public draft histories and observed behavior |
| Concepts | Capabilities and contextual properties | Curated attributes or independently annotated concepts |
| Uncertainty/support | Where the evaluator lacks dependable evidence | Model disagreement and explicit support diagnostics |
| Search utility | The configured decision objective | Preference, requester perspective, uncertainty, and enabled practical costs |

`q_sol`, partial value, and search utility are **not match-win probabilities**. A sigmoid of a preference difference models a comparison under its training convention; it does not convert that preference into factual win probability.

Completed assigned drafts may use final roles. Public partial states may use only picks/bans and information available at that turn. Future picks, final enemy flex assignments, and realized in-game lane swaps must not leak into prefix inputs.

## 5. Data source, schema, and ingestion

- **[Oracle’s Elixir](https://oracleselixir.com/tools/downloads)** is preferred over gol.gg as the main factual source. Supplemental sources such as gol.gg/Leaguepedia are for genuinely missing series/format metadata; Riot Data Dragon/CommunityDragon can supply champion and patch facts.
- Historical working scales were approximately **50,000 games**, later approximately **100,000 samples** for an initial iteration. These are discussion figures, not a newly verified usable-game count.
- The original audit reported a particular **2025 snapshot with 9,237 games and 164 columns**, normally **12 rows/game**: five players and one team row per side. Recheck each actual snapshot and year.
- Preserve original downloads immutably with URL, retrieval time, hash, size, row count, columns, coverage, and ingestion version.

A canonical game record needs:

```python
game = {
    "game_id": ..., "date": ..., "patch": ..., "league": ...,
    "split": ..., "series_id": ..., "game_number": ...,
    "ruleset_id": ..., "first_pick_side": ..., "fearless_history": ...,
    "blue": {"picks_in_order": ..., "bans_in_order": ..., "roles": ...},
    "red":  {"picks_in_order": ..., "bans_in_order": ..., "roles": ...},
    "blue_win": ..., "quality_flags": ..., "source_manifest": ...,
}
```

Retain team/player identifiers for grouping and separate diagnostics, not core model inputs. Store physical map side separately from first/second-pick selection. The 2026 format discussion motivated `blue_fp`; current source fields and exact tournament chronology still require validation.

Validate complementary outcomes, exactly two teams, champion/role counts, player-row versus team-row picks, duplicate champions, patch availability, draft counts, and series restrictions. Missing/ambiguous chronology must be flagged. A gameplay-stat “partial” record is not automatically unusable if its draft and result are valid.

For CSV processing, Python `csv` and `itertools.islice` can read bounded chunks; pandas is optional. Do not blindly assume arbitrary 12-row chunks are valid games. Checking the first and last `gameid` is O(1) but does not verify all middle rows.

## 6. Temporal splits and leakage

**Required ordering:** older training data → later validation/development data → still-later locked test data. Validation and test are distinct future periods. No fixed final percentage split is established in the available later discussion; the old LDANet 80/20 setup is historical.

- Keep whole series, duplicates, mirrored examples, and each base draft’s synthetic variants in one split.
- Do not create training bridge comparisons involving held-out families.
- Fit empirical champion rates, synergies, counters, role support, meta priors, preprocessing, label aggregation, and calibration without final-test information. Respect prediction-time cutoffs for time-varying features.
- Use rolling-origin evaluation and slices for regions/leagues, formats, Fearless, rare roles, low support, and new/reworked champions.
- Random splits are diagnostic comparisons, not evidence of future-patch generalization.
- Curated knowledge can leak too: distinguish when an attribute was valid from when the project learned or annotated it. Later strategic insight cannot silently support a claim of earlier meta discovery.
- Build an explicit inference allowlist. Current-game gold, kills, items, XP, objectives, duration, and performance are excluded.

**Post-game auxiliary learning:** discussed as a possible training aid. Such information may supply an auxiliary target or a separate teacher, but draft-time inference must operate from available inputs. Feeding post-game features into the deployed predictor and removing them later is not a valid solution; the precise auxiliary design remains open.

## 7. Dataset API and reproducibility

**Chosen direction:** each iteration, e.g. `sol_1.py`, owns its architecture, required inputs, outputs, and training configuration. Iteration modules should expose importable objects such as `model` and `training_params`.

`SolDataset` evolves additively:

```python
data.champs      # Existing iterations continue using this contract.
data.firstPick
data.results
data.synergies   # Later additions need not affect older iterations.
data.gold       # Availability in the data API is not inference permission.
```

Preserve field meanings, shapes, dtypes, side/role ordering, champion mapping, and missing-value conventions. A changed representation gets a new name/version. A later proposed design made `SolDataset` a data container with lazy cached tensors, with each iteration constructing its own `TensorDataset`/`DataLoader`; it need not itself implement PyTorch’s sample-indexing interface.

**Memory discussion:** laziness avoids computing unused features; caching avoids recomputation but consumes memory. Re-reading raw CSVs independently for every property is also wasteful. Options discussed were a canonical parsing layer, compact CPU tensors cached with `@cached_property`, batch-only GPU transfer, and memmap/custom streaming for larger features. Fully cached tensors and true bounded-memory streaming are different trade-offs; no single final implementation was established for every scale.

Champion IDs are maintained in `metadata/champion_ids.py`, with real IDs intended as `1..N` and an explicit padding convention. Use `max(CHAMPION_IDS.values()) + 1` for table allocation where applicable. Python mapping versus YAML was discussed; preserve stable mappings independently of format. The champion universe was roughly 170, with 174-entry examples; do not freeze that as an eternal count.

**Environment:** `uv` was recommended for lightweight cross-platform Python/package pinning across Ubuntu, Windows, and NixOS. Track `.python-version`, `pyproject.toml`, and `uv.lock`; reproduce with `uv sync --locked`. NixOS `nix-ld` was suggested, not a finalized configuration. Data `.gitignore` rules, including CSV exceptions, were discussed; final tracking policy is not recorded.

Record each run’s code commit/dirty state, config, seed, data/split/ontology hashes, mapping, environment, device, parameter count, metrics, predictions, calibrator, and checkpoint. Prefer simple CLI entry points for prepare/train/evaluate/annotate/search; notebooks remain exploratory. The broad proposed module boundaries were data, features, ontology, models, supervision, training, evaluation, search, and explanations.

## 8. Models and experiments already discussed

### Historical LDANet

- Picks/bans, shared and role-specific champion embeddings, role-pair synergies, counters, and numeric patch features; attention/residuals, dropout, LeakyReLU, and a deep MLP were explored.
- Embedding sizes **6 → 12** and simpler models were discussed; validation accuracy reportedly moved from the mid-50s toward **61–63%**. These were historical results under earlier evaluation conditions.
- Role-pair features included Top–Jungle, Jungle–Mid, ADC–Support and eventually the ten within-team role pairs; role-specific opponent counters were also used.
- Historical smoothing: `(wins + 1) / (games + 2)`, rounded to three decimals. Recompute statistics using only permitted training history.
- One older run used 13 epochs, an 80/20 split, seed 42, batch 12, Adam `lr=0.001`, weight decay `0.0001`, BCELoss, and StepLR every three epochs with `gamma=0.1`. Older balancing removed excess outcomes; that is not the current probability-model recommendation.
- Earlier class counts were **23,318 positives / 26,579 negatives**. Accuracy, class balancing, and patch-as-number choices require reassessment under clean temporal evaluation.

### Earlier dense Sol attempt

`Embedding(174, 32)` → flatten ten tokens + first-pick feature → `Linear(321, 256)` → `Linear(256, 1)`, with GELU, dropout `0.2`, and sigmoid. Reported size: **88,257 parameters**. Overfitting also appeared around **15,000 parameters**: training improved while validation stagnated. Batch size discussed for Sol: **64**.

### Latest minimal additive Sol_1

The intended baseline is a generalized additive model of champion-role strengths:

```python
# Shared role strengths: each table entry is a learned scalar coefficient.
strength = nn.Embedding(max(CHAMPION_IDS.values()) + 1, 5)
nn.init.zeros_(strength.weight)
bias = nn.Parameter(torch.zeros(()))
# roles: a registered buffer [0,1,2,3,4,0,1,2,3,4]

slot_scores = ...  # Select strength[champion, role] for each of ten slots.
logit = bias + slot_scores[:, :5].sum(1) - slot_scores[:, 5:].sum(1)
```

- **Five columns:** shared Top/Jungle/Mid/Bot/Support coefficients across sides. **Ten columns:** side-specific role coefficients, with scoring/sign convention explicitly defined.
- Here `embedding_dim=5/10` selects role coefficients; it is not a 5/10-dimensional hidden representation passed to a large head.
- Initialize strengths and bias to zero; store role indices as a buffer. An optional zero-initialized `nn.Linear(1, 1)` can model first-pick context; it is not inherent to the champion-only formula.
- Discussed training settings: Adam `lr=1e-3`, `weight_decay=0.0`, batch 64, CUDA, FP32.
- At 174 rows and five columns plus bias, parameters occupy about **3.5 KB in FP32**; checkpoint metadata, buffers, optimizer state, and optional context add overhead.
- This deliberately cannot learn champion synergy or opponent-specific counters. Its purpose is a clear baseline for whether later interactions earn their complexity.

**Inference:** reconstruct the matching iteration, load its `state_dict` with the intended device, call `eval()` and `torch.inference_mode()`, and use a batch dimension even for one draft. Discussed loading: `torch.load(..., map_location=device, weights_only=True)`. Avoid a hard-coded device inside `forward`; use input/buffer devices. With BCEWithLogitsLoss, return logits and apply sigmoid only when a probability is needed.

**Compute:** early and possibly later compact Sol iterations can plausibly fit/train on the 4 GB GPU. There is no final-size guarantee: activations, batch size, optimizer state, relational intermediates, ensembles, and search throughput matter. A second scalar head is cheap; multiple encoders or ensemble copies are the larger multipliers.

## 9. Candidate richer architecture

**Proposed, not locked:** a small role-aware, opponent-conditioned encoder. Compare a fixed role-ordered MLP against Deep Sets and a relational/set-attention model before choosing.

```python
token = token_mlp(cat(champion_embedding, role_embedding,
                     capabilities, missing_flags, patch_features))
# Preserve identity while modeling ally and enemy relations.
tokens = relational_blocks(token)
ours, theirs = pool_by_team(tokens)
outcome, preference = matchup_heads(ours, theirs, allowed_context)
```

Required representational distinctions:

- **Champion-role binding:** immediately summing `champ_emb + role_emb` across a team loses which champion has which role. Use a nonlinear interaction before pooling, or fixed role slots.
- **Opponent dependence:** independent scalar `strength(ours) - strength(theirs)` cannot represent a counter cycle A>B>C>A. A joint matchup function can.
- **Counter direction:** `dot(E[a], E[b])` with the same embeddings is symmetric. Ordered pair MLPs, distinct attacker/defender projections, or a skew-symmetric interaction can express direction.
- **Context beyond pairs:** additive pair scores may spend one defensive tool against several simultaneous threats. Preserve nonlinear contextual processing rather than treating each counter independently.
- **Role is not class:** mage, utility, tank BOT, off-role marksmen, and viable enchanter flexes must remain representable.

The September implementation candidate used champion embeddings **24**, role embeddings **8**, token width **64**, two typed ally/enemy message rounds, mean+max team pooling to **128**, and an ordered matchup MLP with two scalar outputs. Ten tokens yield **20 unordered ally pairs + 25 cross-team pairs**, or **40 + 50 directed edges**. This was an example around a few hundred thousand parameters, not an optimized or trained result.

**Symmetry:** distinguish reversing the observer from physically moving compositions between map sides. A perspective-consistent construction is:

```python
q(D) = 0.5 * (raw_score(D) - raw_score(reverse_view(D)))
```

`reverse_view` moves each team’s roles and physical map-side context with that team. The same game viewed from the other side has opposite advantage; physically exchanging Blue/Red compositions need not produce complementary probabilities because map-side effects remain. A side-neutral preference target should exclude map-side effects explicitly. The older alternative decomposition used an antisymmetric draft term plus side bias and an optional symmetric composition-dependent side term.

## 10. Preference supervision and losses

The user’s intended two-stage preference route is: **learn full-draft judgments → learn partial-draft values from those judgments**. Roughly **1,000 manual labels** was discussed as a possible target, with annotation time a major concern. Reviews proposed a **100–300 comparison pilot**, not a claim that this is sufficient for a reliable final evaluator.

The annotation contract specifies patch, final roles, perspective, player competence, side treatment, and practical constraints. Preserve `A`, `B`, `TIE`, and `ABSTAIN` separately, with family ID, change type, confidence, reason codes, annotator, guideline version, and time.

```python
pair_logit = perspective_sign * (q(draft_a) - q(draft_b))
pair_loss = BCEWithLogitsLoss()(pair_logit, preference_target)
# TIE may use 0.5; ABSTAIN contributes no supervised loss.
```

This is RankNet/Bradley–Terry-style comparison learning. Apply sigmoid to the **score difference**, not separately to each score before subtraction. For BCE, `loss = softplus(logit) - target * logit`; its derivative is `sigmoid(logit) - target`.

**Local improvements need anchors:** one-champion swaps teach “better than this alternative,” not necessarily “favorable overall.” Disconnected families can shift their score levels without changing local comparisons. Add side-preference anchors on complete matchups and some cross-family comparisons from the same perspective. Anchors establish a zero boundary; they do not automatically calibrate cardinal utility. Initially fix/regularize comparison scales and temperatures.

High-value comparison families:

1. **Single swaps:** preserve legality and evaluate full-matchup consequences; never copy the original winner label to the synthetic draft.
2. **Context reversals:** keep our candidate change fixed, alter the enemy threat, and ask whether its usefulness changes. Do not manufacture a reversal by heuristic.
3. **Two-champion packages:** compare original, change A, change B, and A+B. The combined package may work when either isolated change does not.
4. **Role changes, resource conflicts, and heuristic exceptions:** include ties, uncertainty, ordinary difficult decisions, and repeated/reversed items to assess consistency.

Package diagnostic: `q(AB) - q(A) - q(B) + q(original)`. Experts need not invent numeric interaction scores; ordinary comparisons and reason codes suffice. A proposed **20–40 quartet pilot** was illustrative, not a settled budget.

Active learning should mix representative examples with decisions that credible models rank differently, impactful swaps, search recommendations, and known failure cases. Compare annotation strategies at equal human time, not merely equal row counts. A sole annotator’s benchmark primarily measures fidelity to that person’s rubric.

## 11. Shared heads, optimization, and calibration

- A full-draft outcome head learns real outcomes; preference learns expert judgments. Sharing may help or contaminate the representation—measure both tasks separately.
- Candidate progression: outcome pretraining plus an early gold pilot; frozen preference-head baseline; partial unfreezing/adapter with outcome replay; joint training or independent encoders if needed. None is a guaranteed winner or mandatory schedule.
- Normalize task losses separately and control task sampling so a few hundred gold labels are not overwhelmed by outcome/weak-label volume.
- Repeated gold sampling increases optimization weight, not independent information. Sample/normalize by family so 100 synthetic swaps do not accidentally outweigh another family 100-fold.
- Do not apply the same recency weights in both the sampler and loss: that effectively squares their influence.
- Use natural-distribution BCE for probabilities unless a different objective is intentional. Constant positive-class weight `w` changes the optimum to `w*p / (w*p + 1-p)`; subtracting `log(w)` corrects that idealized logit shift, not all calibration errors.
- Fit outcome calibration after model selection on temporally appropriate held-out development data. Temperature scaling does not generally undo an additive class-prior shift and does not calibrate preference as game probability.
- Use regularization, early stopping, multiple seeds, and learning curves. Separable preference labels can inflate score magnitudes indefinitely. Specialized gradient surgery is optional only after sharing conflict is demonstrated.

## 12. Ontology, concepts, and weak supervision

**Purpose:** supply capability ingredients that limited pro outcomes may fail to teach; retain champion-ID information and missingness flags. Begin with a small reliable vocabulary, not exhaustive subjective precision.

| Capability family | Candidate attributes discussed |
| --- | --- |
| Damage | Physical/magic/true, burst/sustained, AoE/single-target, tank killing, resets, reliability, effective range, target access |
| Control/protection | Engage/follow-up, disengage, peel, anti-dive, hard/soft CC, displacement, zones, terrain dependence |
| Lane/map | Waveclear, siege/anti-siege, side pressure, roam/global reach, objective damage/setup, vision access, face-check safety, blind stability |
| Durability | Frontline, sustain, healing/shielding, resistance to poke/burst/extended fights |
| Economy/timing | Gold/XP demand, early/mid/late profile, spikes, cooldown dependence, snowball reliance, usefulness from behind |
| Flex/execution | Viable positions, functional jobs, mechanics/coordination burden, setup, punishability, alternative fight patterns |

Attributes may depend on patch, role, resources, and matchup; missing is not zero. Store validity dates/patches, confidence, provenance, `recorded_at`, and `evidence_available_at`. Team identities are continuous and multi-label, not mutually exclusive archetypes.

**Learned versus computed preference:** a hybrid—computed capabilities such as scaling/early strength feeding a small learned model—was discussed. The final score should learn contextual trade-offs; a deterministic sum of universal champion ratings does not capture the intended judgment. Exact features and scales remain open.

**Weak supervision/data programming:** proposed after a gold-only baseline. Labeling functions vote A/B/tie/abstain on near-neighbor drafts, using range/access, waveclear, answer coverage, protection, resource stress, damage, scaling feasibility, recovery, or sequential option preservation. They must not read match winner to manufacture philosophy labels.

Group dependent rules, audit coverage/overlap/conflict/gold accuracy, cap redundant evidence, compare grouped voting with a gold-supervised aggregator, and consider LF dropout/family ablations. The standard Snorkel LabelModel discussed in the review assumes conditional independence; it does not automatically learn away arbitrary correlated rules. Weak labels remain optional if they fail to improve held-out expert decisions.

Features also used to generate labels can become shortcuts. Keep adversarial gold exceptions and document dual use. Analyst reviews may become original structured labels with provenance; repeated rhetoric is not independent evidence.

**Explanations:** concept predictions outside the decision path do not prove why a score was produced. Copying input traits into an auxiliary head is weak evidence. A concept bottleneck makes a stronger computational claim but may omit important information; residual routes improve flexibility while limiting complete explanation claims. Prefer verified swap/role-change deltas and supported reasons over raw attention weights.

## 13. Patch changes and meta

**Patch identity:** store `"15.10"` or `(15, 10)`, not float `15.1`. A numeric date/patch encoding does not explain mechanics, and time encoding is different from recency weighting. Initial minimal iterations can rely on temporal splits while patch-aware representations are later ablations.

Candidates: stable champion identity plus versioned capabilities; known-patch context; recent fine-tuning/recalibration; structured change adapters trained on previous transitions. An unseen categorical vector or untrained patch-note embedding has no learned interpretation. Major reworks/items/map changes require explicit support handling. Distinguish cold-patch prediction from adaptation after new-patch games.

```python
weight = 2 ** (-age_days / half_life_days)
effective_n = sum(weights)**2 / sum(w*w for w in weights)
```

Tune half-life on development windows and compare uniform weighting. Effective sample size reveals concentration, not independence between games. A proposed relational benefit is indirect adaptation: changing a threat’s capabilities might change an unchanged answer’s value; this requires a held-out transition experiment.

**November meta discussion:** the user disputes professional priority but recognizes that it affects drafting. The proposed response separates:

| Question | Proposed treatment |
| --- | --- |
| What is actually strong after balance changes? | Patch-valid mechanics/features, outcome/preference learning, adaptation |
| What do opponents prioritize? | Separate behavior model using recent role-specific pick/ban rates, early-pick rates, trend/change, and sample support |
| Can this pick wait, or will it disappear? | Availability and likely opponent actions inside sequential search |
| What should Sol prefer? | Independent strategic evaluation; popularity is not a quality label |

Compute meta statistics strictly from preceding information and smooth sparse estimates. A meta-conditioned continuation changes partial value. Merely inserting a policy prior into adversarial PUCT does **not** turn it into expected-opponent search: likely-response behavior must affect sampling/expectation at opponent turns. Preserve exploration of uncommon counters. These were proposals; no final meta encoding was accepted in the available exchange.

## 14. Draft health and practical drafting lessons

**Draft HP:** the user proposed that fragile or highly conditional picks—examples **Kassadin** and **Yuumi**—consume draft health. The intended intuition is negative-only operations: capture burdens and failure conditions rather than give arbitrary positive HP for picking an apparently stable champion. **Nautilus** was the example questioning whether a champion should add HP when it can itself become useless in a bad state.

This is an unresolved modeling concept, not a calibrated metric. The open issues are how burdens combine, whether support mitigates a penalty, which conditions trigger it, and how to supervise it. It relates to early vulnerability, delayed resources, recoverability, execution burden, and compounded dependencies; it should not silently become another name for outcome uncertainty or a fixed champion blacklist.

**Scenario proposal:** later labels could evaluate an explicitly stipulated failed early plan, delayed carry resources, or roughly even game. These are hypothetical input assumptions with new annotation contracts—not observed post-game gold fed into draft prediction. Keep scenario profiles separate until a weighting policy is defined.

**Defensive compositions:** the user repeatedly drafted answers without reliable initiation and questioned whether players at the team’s level can execute pure reactive attrition. The concrete example was:

| Role | Our composition | Opponent |
| --- | --- | --- |
| Top | Sion | Gnar |
| Jungle | Poppy | Vi |
| Mid | Viktor | Galio |
| Bot | Zeri | Caitlyn |
| Support | Lulu | Alistar |

The modeling implication is to distinguish “can answer an enemy entry” from “can create progress when the opponent does not cooperate.” Forcing tools, range, wave/map control, side pressure, and objective setup are contextual alternatives; no universal mandatory-engage rule was settled.

The team’s primary direction is **protect the puppy**: viable weakside/agency top, agency jungle, control/supportive mid, hypercarry, enchanter. **Jungle carry is secondary**: Brand/Jayce jungle would come with a melee agency support and corresponding draft adaptation; do not evaluate that branch as Sejuani carry or require equal depth to the main style. Pool recommendations are flexible, not mandatory tier lists, and analytical comparisons assume stated proficiency. Coaching notes need concise Markdown organization; the user prefers direct Vim-friendly tools over Obsidian-style overhead.

**Specific interactions:** Poppy removing an ulting Swain was raised as a test of whether champion mechanics can be learned indirectly. Historical associations may be learned without understanding the mechanism. Capability ingredients, directional relations, and context-reversal labels are proposed ways to test this; the full matchup and patch mechanics determine whether the interaction matters.

**Answer overload:** one spell may answer multiple threats individually but not simultaneously. Candidate reason codes include “single answer overloaded,” “independent second answer,” and “cannot reach target.” Start with challenge examples before a spell-capacity model or combat simulator.

## 15. Partial-draft value

The user’s current intended target is expected **full-draft preference**, not expected match outcome:

```python
# Conceptual target; completion_policy must be explicitly defined.
V_partial(state) = average(q_sol(d) for d in legal_completions(state))
```

The crucial unresolved part is what generates and weights completions: historical continuations, a particular rollout policy, likely opponents, minimax, or teacher search produce different values. An early pick must be evaluated with later choices allowed to adapt.

- Masking a real full draft and retaining its winner estimates a historical-continuation outcome quantity, not intelligent preference completion.
- Masking and using its full-draft preference similarly inherits the continuation distribution of those examples.
- Feeding blanks into a full-draft-only network does not automatically make it a partial evaluator.
- A partial model can favor prefixes with impossible role completions; legality and matching remain hard external checks.
- Reviews proposed legal rollouts first, then distilling externally credible search for speed. This is an implementation option alongside the user’s chosen partial-head direction, not a requirement to abandon it.
- Version generated targets by terminal evaluator, continuation/opponent policy, utility scale, and search budget. Distillation supplies faster predictions of the teacher procedure, not new evidence about actual games.

## 16. State, rules, and role feasibility

The user’s starting state sketch was:

```python
class State:
    picks: dict[str, list[int]]  # {"red": [...], "blue": [...]}
    bans: dict[str, list[int]]
    turn: int
    blue_fp: bool

    def legal_actions(self): ...
    def apply_action(self): ...
    def is_complete(self): ...
```

Readable dictionaries versus compact lists was a performance concern, not an established bottleneck. Keep the interface simple and profile before changing representation. The range check discussed is `0 <= n <= 5`, with invalid counts `not (0 <= n <= 5)`; `0 > n > 5` cannot hold.

A mature state/rules layer also needs patch, ruleset, actor, future pick/ban schedule, remaining pool, feasible assignments, reveal assumptions, series/Fearless restrictions, and optional roster constraints. Rule tables determine who acts; physical Blue side does not universally determine first pick. The same side can have consecutive actions.

**Roles:** maintain candidate champion-to-position assignments rather than fixing a flex immediately. A matching must exist for the whole team; independent per-champion checks are insufficient. Also check that the remaining available pool can fill the unoccupied roles. At most **5! = 120** raw assignments/team and **14,400** assignment pairs exist for a full draft before pruning; cache viable results.

Separate game legality from **strict supported professional roles** and **exploratory roles**. Frequency alone must not permanently forbid novel but plausible assignments. Exploration needs evidence/support handling, not an unconditional bonus for rarity.

**Information order matters:** choosing our role assignment after secretly observing the enemy’s final assignment gives an illegal advantage. These are different assumptions:

```python
mean(max(score(ours, enemy) for ours in our_roles) for enemy in enemy_roles)
max(mean(score(ours, enemy) for enemy in enemy_roles) for ours in our_roles)
```

Use a stated commitment/reveal model or a simultaneous-game model where appropriate. Averaging role embeddings before a nonlinear evaluator is not equivalent to averaging evaluations of legal assignments. Flex value comes from feasible options and information, not just counting allowed roles.

**Bans and pick order:** preserve both for sequential tasks. Intrinsic terminal preference for the same assigned matchup excludes ban bonuses and chronological effects. An optional historical predictor may use bans diagnostically because they reveal preparation/team context. Fearless history controls current legality; optimizing a whole series additionally needs series state and a separate objective.

## 17. MCTS/PUCT and the tiny search

The user chose to learn by implementing a small search, then expand. Earlier proposals included one-step ranking, shallow beam/minimax, iterative deepening, best-first adversarial search, and PUCT/MCTS; compare mature alternatives under equal compute rather than assume a winner.

**Node versus state:** state describes the draft; search nodes/edges hold visits, accumulated value, mean value, priors, and children. A search leaf is an unexpanded/budget-cut node, not necessarily a completed draft. It needs a trained partial value or legal rollout; terminal nodes use full-draft evaluation.

```python
# A simple PUCT convention; exact initialization/ties must be specified.
Q = value_sum / visits if visits else initial_value
exploration = c_puct * prior * sqrt(parent_visits) / (1 + visits)
selection_score = actor_sign * Q + exploration
# actor_sign = +1 for the requester, -1 for the opponent,
# when Q is always stored in the fixed requester perspective.
```

- `Q` favors evaluated actions; the exploration term favors plausible, insufficiently visited alternatives.
- `prior` can be uniform initially or supplied by a behavior/policy model. `c_puct` controls exploration; it is a search setting, not evidence of strategic quality.
- The square root increases the exploration budget as the parent is visited; the denominator reduces repeated exploration of an already visited child.
- UCT commonly has a logarithmic parent-visitation term; PUCT uses a prior-guided term. They should not be conflated.
- Backpropagate under one consistent perspective. Never blindly negate after every pick: consecutive actions may belong to the same team.
- Visits can provide a later policy-training target. AlphaZero’s value target was actual game results; Sol’s preference-derived/search-derived targets have different semantics.

The practical decomposition is: **rules/state → legal actions → apply action → terminal test → evaluator → node bookkeeping → selection/expansion/backpropagation → budgets and optimizations**. Begin with a tiny pool/subgame that can be exhaustively checked. A discussed budget illustration, 5,000 simulations × four completions ≈20,000 evaluations, was not a measured runtime or chosen requirement.

## 18. Utility, uncertainty, and opponent assumptions

Initially search primarily on `q_sol`; historical outcome may be displayed independently. Mixing it into preference can reintroduce team/style associations. Any future combination must earn its place through independent decision evaluation.

**Required sign correction:** orient advantage to the requester before subtracting uncertainty:

```python
mean_for_requester = sign_for_requester * q_blue
utility = mean_for_requester - beta * disagreement - practical_cost
# Requester maximizes; opponent minimizes this fixed-root quantity.
```

Subtracting uncertainty from Blue score and then letting Red minimize rewards uncertainty for Red. Store raw preference and uncertainty separately; cache root-specific utility only with its perspective/configuration. This is a conservative requester convention, not a claim that both teams’ personal risk costs are zero-sum.

| Quantity | Distinction |
| --- | --- |
| Model uncertainty | Evaluator may be wrong; inspect ensembles and support |
| Outcome uncertainty | Game result is unpredictable; a well-understood matchup can be 50/50 |
| Strategic fragility | Success depends on narrow resources/execution/scenarios; needs suitable supervision |
| Search uncertainty | Limited exploration of the tree; more rollouts may reduce this without fixing evaluator error |

A generic uncertainty head cannot identify all four from winners. Ensemble agreement is not proof; models can share bias. Check support in champion-role combinations, important interactions, patch changes, and preference examples—not merely whole-draft rarity. Align preference scales before averaging; compare ensemble decision deltas `q_m(A)-q_m(B)` as well as absolute scores.

Opponent modes discussed: worst-case, likely-response, robust sets of plausible strong responses, and optional scouting. A behavior prior only orders exploration unless opponent decisions actually follow that distribution.

**Utility scale:** deterministic minimax preserves choices under strictly increasing transforms; averaging, mixed strategies, and additive penalties generally do not. Example: raw outcomes `[4, -1]` average above `[1, 1]`, while their sigmoid averages rank below it. Define and sensitivity-test the preference scale before expected-value search; bounded transforms do not create a factual win utility.

## 19. Search engineering and explanations

- Mix candidates from behavioral priors, preference scores, threat answers, feasible role options, coherent packages, and controlled exploration. Popularity alone must not veto supported off-meta actions.
- Preserve two-pick packages where isolated screening would discard their first member. Treat them as exact macro-actions only when no opposing decision/relevant observation intervenes.
- Batch leaf evaluations; cache static champion/patch features, role matchings, terminal scores, and transpositions. Consider progressive widening, subtree reuse, move ordering, and exact late-draft search.
- Terminal cache keys include both assigned compositions, patch/side context, and model/ontology versions. State keys additionally need actor, ruleset, availability/restrictions, series history, and any policy-relevant history/belief. Champion sets alone are insufficient.
- Exact alpha-beta pruning preserves the specified minimax tree’s answer; learned candidate pruning is approximate and needs recall checks.
- Common random draws across valid conditional rollout generators may reduce comparison noise, but must not force illegal identical continuations and are not universally beneficial.
- Report top alternatives, preference/historical deltas separately, uncertainty/support, changed capabilities and role options, strongest replies, and relevant annotated/historical neighbors. Explain from those facts, not invented causal stories.

**Search exploitation:** optimizing a learned evaluator can find its mistakes. Audit search-selected drafts, not only ordinary held-out games. If deeper search raises internal score while blinded expert preference worsens, the search is exposing evaluator failure. Self-play against a learned evaluator is not independent strategic validation.

## 20. Evaluation and research discipline

| Track | Main evidence |
| --- | --- |
| Historical outcomes | Future-period log loss, Brier score, calibration/reliability, ECE with bin sensitivity, ROC-AUC; accuracy secondary |
| Preferences | Held-out pair loss/agreement, anchor quality, ties, consistency, reason-code slices, context reversals/packages, heuristic failures |
| Representation | Role/context generalization, new patches/champions, invariance, support slices, ontology ablations and controlled interventions |
| Search | Legality, feasible completions, expert judgments, strongest-response robustness, stability, diversity, exploitation rate, utility sensitivity |
| Efficiency/correctness | Latency/evaluator calls at equal quality, exact tiny-subgame agreement, consecutive turns, bans, matching, perspective |

Use paired comparisons on the same examples, multiple seeds, and confidence intervals clustered by series/comparison family—not individual synthetic rows. Publish coverage and failures instead of dropping unannotated difficult champions. Keep separate development, calibration, and final tests where data allows. Do not tune rules, ontology, labels, or search weights on the locked gold test.

Compare draft-only, temporally valid team-strength-only, and full-context pregame models. Nuisance research options included hierarchical team/player/league effects, cross-fitting/residualization, within-series analysis, adversarial team-signal removal, and narrow propensity-aware studies. None automatically identifies causal draft value; deleting a team branch at inference does not establish equal-player probability.

Solo queue is an optional transfer experiment: pro-only versus solo pretraining→pro fine-tuning, naive mixing, and domain-aware mixing. Select on future professional games and report negative transfer. Large action spaces and poor historical overlap also limit off-policy evaluation of unplayed alternatives.

Meaningful engineering checks cover ingestion/chronology, split leakage, train-only statistics, invariance and perspective, missing inputs, LF abstention/dependencies, deterministic evaluation, legal transitions, role completion, Fearless, hashing/cache correctness, budgets, and the uncertainty penalty’s direction. These are requirements for relevant implemented components, not evidence that a suite already passes.

## 21. Experiment backlog and practical sequence

The original registry remains useful as a checklist:

| ID | Experiment |
| --- | --- |
| E00 | Global/patch side-rate baseline |
| E01 | Champion-role one-hot/logistic/additive baseline |
| E02 | Shrunk empirical synergy/counter model |
| E03 | LightGBM/tabular baseline |
| E04 | Clean LDANet reproduction |
| E05 | Deep Sets |
| E06 | Relational encoder |
| E07 | Ontology ablation |
| E08 | Patch ablation |
| E09 | Ban ablation |
| E10 | Team-strength/full-context diagnostics |
| E11 | Gold preference learning |
| E12 | Weak supervision versus gold-only/grouped voting |
| E13 | Shared/frozen/separate representations |
| E14 | Concept supervision |
| E15 | Uncertainty/support methods |
| E16 | Solo-queue transfer |
| E17 | Strict/exploratory roles |
| E18 | Beam/minimax versus MCTS under equal compute |
| E19 | Historical versus preference-led decision objectives |

Additional focused experiments: comparison anchors, context reversals, two-pick packages, continuation-policy sensitivity, search-budget audits, answer overload, scenario fragility, and learned patch adaptation. They are hypotheses, not guaranteed accuracy improvements.

**Consolidated development sequence:**

1. Keep the current additive baseline, canonical input contract, and reproducible temporal evaluation dependable.
2. Write a precise annotation rubric and collect a small gold pilot with anchors and interaction cases.
3. Train full-draft preference; compare simple representations before adding complexity.
4. Build the tiny rules/search exercise, with correct actors and role matching; it can serve learning before production deployment.
5. Define the partial-value continuation target and validate it against legal full drafts/search.
6. Evaluate shallow recommendations independently; increase search only when decisions improve.
7. Add meta behavior, ontology depth, weak labels, uncertainty machinery, or richer encoders one at a time when failures justify them.
8. Defer full series optimization, large networks, spell simulators, broad draft RL, and Sinner/Lua until evidence supports them.

For every experiment: state the hypothesis, change one conceptual factor, preserve data/splits/seeds, report compute and primary metrics, keep negative results, and record the decision caused by the result. No fixed target accuracy or final model size has been established.

## 22. Open decisions

- Exact usable dataset coverage, current OE chronology/first-pick metadata, series reconstruction, and final split boundaries.
- Final five-versus-ten coefficient treatment, first-pick context, and next interaction baseline after additive Sol_1.
- Preference annotation scale, side assumptions, gold budget, independent reviewers, and acceptable consistency.
- Learned versus computed/hybrid capabilities; ontology granularity, role/resource conditioning, and missing-data policy.
- Full/partial head sharing and precise completion/opponent distribution for partial targets.
- Draft-health penalty composition, mitigation, labels, and distinction from other fragility concepts.
- Meta feature windows/smoothing, opponent-policy training, and how strongly behavior affects search.
- Role support thresholds, hidden assignment/reveal model, and exploratory-mode safeguards.
- PUCT settings, candidate mixture, utility scale, uncertainty strength, practical costs, and equal-compute comparisons.
- Whether research release should stop at the evaluator/preference benchmark or include validated search; whether solo transfer, weak labels, or patch adapters help at all.

## 23. Learning, research framing, and references

The project is also a vehicle for learning ML research engineering. The user prefers forming hypotheses and building iterations, with targeted help and code-first explanations rather than following a fully prescribed architecture. Vague initial hypotheses can become useful through small measurable comparisons and failure analysis; reading every paper before building is unnecessary.

A defensible first research contribution could be a reproducible pro-draft benchmark plus an explicitly supervised preference dataset/evaluator, clean temporal splits, baselines, calibration, and ablations. Full search is optional for a first paper. Report historical association, expert preference, and evaluator-relative search quality separately; neither old accuracy nor internal search wins proves causal advantage or more real match wins.

Expected release materials discussed: reproducible construction scripts/data subject to licensing, manifests, ontology/annotation contracts, checkpoints where appropriate, model card, failure analysis, negative results, and eventually a draft interface. A proposed paper structure runs from task/data/representation/supervision through benchmarks, ablations, limitations, and optional search.

**AI-assistance selection:** evaluate on Sol-specific leakage, confounding, paper transfer, experiments, and repository work. Earlier suggested weighting: custom project tasks **40%**, reasoning/data analysis **25%**, repository coding **20%**, instruction/long-context consistency **10%**, ordinary coding benchmarks **5%**. RE-Bench/MLE-bench, SWE/Terminal benchmarks, reasoning/math and long-context tests were possible signals, not a definitive model ranking.

Reading topics already discussed or cited:

| Reference | Relevance |
| --- | --- |
| [RankNet](https://www.microsoft.com/en-us/research/publication/learning-to-rank-using-gradient-descent/) | Pairwise score-difference learning |
| AlphaZero and MCTS/PUCT | Policy priors, search visits, partial-state value; Sol has different supervision and no real self-play simulator |
| [JueWuDraft](https://arxiv.org/abs/2012.10171) | Terminal predictor versus search policy/value; different game/data scale and reported ban limitations |
| [DraftRec](https://arxiv.org/abs/2204.12750) | Related personalized drafting work; different player-history objective |
| [Deep Sets](https://arxiv.org/abs/1703.06114), [Relation Networks](https://arxiv.org/abs/1706.01427), [Set Transformer](https://proceedings.mlr.press/v97/lee19d.html) | Invariance and relational representation |
| [Data Programming](https://arxiv.org/abs/1605.07723), [Snorkel](https://arxiv.org/abs/1711.10160) | Noisy programmatic supervision and assumptions |
| [Calibration](https://proceedings.mlr.press/v70/guo17a.html), [Deep Ensembles](https://arxiv.org/abs/1612.01474), [Uncertainty under Shift](https://arxiv.org/abs/1906.02530) | Probability quality, disagreement, robustness |
| [Conservative Objective Models](https://proceedings.mlr.press/v139/trabucco21a.html), [Reward Model Ensembles](https://arxiv.org/abs/2310.02743) | Optimizers exploiting learned evaluators |
| [Active Reward Modeling](https://proceedings.mlr.press/v267/shen25c.html) | Informative comparison selection; transfer to Sol remains a hypothesis |
| [Concept Bottleneck Models](https://proceedings.mlr.press/v119/koh20a.html) | Concepts on versus outside the actual decision path |
| [Counterfactual Risk Minimization](https://proceedings.mlr.press/v37/swaminathan15.html), [Leakage in ML Science](https://arxiv.org/abs/2207.07048) | Logged-feedback assumptions and evaluation discipline |
| [Gradient Surgery](https://arxiv.org/abs/2001.06782) | Optional response to demonstrated multi-task gradient conflict |
| [Game Avatar Embedding](https://arxiv.org/abs/1803.10402), [Information Set MCTS](https://eprints.whiterose.ac.uk/id/eprint/75048/1/CowlingPowleyWhitehouse2012.pdf) | Related synergy/opposition and hidden-information ideas; the former was noted as a rejected draft, not an accepted benchmark result |

## 24. Source record

This summary consolidates the available project conversations through 4 November 2026, including Sol_1, dataset/inference/environment work, search, specific champion interactions, draft health, meta, and relevant coaching context, plus these documents read in full:

- [Saint_Research_and_Engineering_Plan.md](https://chatgpt.com/library?file_id=libfile_82e4443117ac8191b0914eea66015b82&account_id=personal) — plan dated 1 August 2026.
- [Sol_Architecture_Review.md](https://chatgpt.com/library?file_id=libfile_e687209829e48191897a32a4ab7c28b8&account_id=personal) — 5 September 2026.
- [Sol_Architecture_Deep_Dive.md](https://chatgpt.com/library?file_id=libfile_47c88eec62708191ab642185a8f70733&account_id=personal) — 12 September 2026.

Current choices, historical observations, and recommendations are separated above. Where an exact answer, parameter, or implementation was unavailable, it is preserved as open rather than invented. Research links are carried forward from those discussions/documents; this consolidation did not rerun their experiments or independently reverify current external sources.
