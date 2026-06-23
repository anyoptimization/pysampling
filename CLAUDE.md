# CLAUDE.md — pysampling

`pysampling` generates well-spread point sets in the unit hypercube `[0, 1]^d`
(random, Latin Hypercube, Halton, Sobol) and provides discrepancy/uniformity
measures to assess them. `README.md` is the human-facing overview; this file is
the working contract for AI agents.

## This project follows pyclawd

Development is driven by [pyclawd](https://github.com/anyoptimization) — a
project-generic Python dev-task CLI. The whole project is described by one file,
[`.pyclawd/config.py`](.pyclawd/config.py), and humans and agents drive it the
same way. **pyclawd is expected to already be installed in your environment**
(it is not vendored into this repo, and neither are its agent skills — install
those once per machine with `pyclawd skills install` if you want them).

Read `.pyclawd/config.py` before assuming how anything is wired — it is the
single source of truth for the env, paths, and checks.

## Critical rule — how to run Python

**ALWAYS run Python through `pyclawd python`. NEVER call bare `python` / `python -c`.**

```bash
pyclawd python script.py               # run a script
pyclawd python -m pytest ...           # run a module
pyclawd python -c "import pysampling"  # quick check
```

`pyclawd python` runs in the project's configured env (`conda_env` in
`.pyclawd/config.py`) with the repo on `PYTHONPATH`. Bare `python` misses the
env and the in-tree source.

## Commands

| Task | Command |
|---|---|
| Health-check the dev env | `pyclawd doctor` |
| Run Python in the env | `pyclawd python <file>` · `-m <mod>` · `-c <code>` |
| Fast smoke tests | `pyclawd test fast` |
| Default test gate | `pyclawd test run` |
| Select tests | `pyclawd test -k <kw>` · `pyclawd test tests/path::node` |
| Lint / autofix | `pyclawd lint` · `pyclawd lint --fix` |
| Format / check | `pyclawd format` · `pyclawd format --check` |
| Type-check | `pyclawd typecheck` |
| **Aggregate quality gate** | `pyclawd check` |
| Build a source/wheel dist | `pyclawd dist` |
| Build / serve the docs | `pyclawd docs build` · `pyclawd docs serve` |

`pyclawd check` runs **format-check → lint → typecheck → test**, fail-fast — the
canonical "am I done?" gate. CI (`.github/workflows/ci.yml`) mirrors it with the
same tools, so a green `pyclawd check` predicts green CI.

## Project layout

```
src/pysampling/            # the package (src layout)
  sample.py                # sample(algorithm, n_points, n_dim, ...) entry point
  sampling.py              # abstract Sampling base class
  algorithms/              # random, lhs, halton, sobol implementations
  measures.py              # discrepancy / uniformity measures
  util.py                  # cdist, prime sieve, resource paths
  resources/*.dat          # Sobol direction-number tables (bundled package data)
tests/                     # pytest suite (+ resources/ for fixtures)
examples/                  # runnable demos (plot_sampling.py)
```

The single source of truth for the version is
`src/pysampling/__init__.py::__version__` (hatchling reads it). Bump it there; do
not reintroduce a separate `version.py`.

## Conventions & boundaries

### Always
- Run code via `pyclawd python` — never bare `python`.
- Run `pyclawd doctor` first when the env looks off or tests fail to import.
- **Run `pyclawd check` before declaring work done.**
- Fix the *cause* of a failing test, not the assertion — use tolerances for
  floats and pinned seeds for stochastic tests (`sample(..., seed=...)`).
- Each discrepancy measure in `measures.py` has a slow loop reference in
  `tests/test_discrepancy.py`; keep them in agreement when you touch either.

### Ask first
- Committing, pushing, opening PRs.
- Changing `.pyclawd/config.py`, dependencies, or the public API (`sample`).

### Never
- Never call bare `python`/`pip` outside the project env.
- Never weaken or delete a test to make a suite pass.
- Never leave the tree with a failing `pyclawd check`.

## How you know you're done

- `pyclawd check` is green (format-check, lint, typecheck, tests all ✓).
- `pyclawd doctor` exits 0.
- Behavior is verified by tests, not just by inspection.
