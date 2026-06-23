# pysampling documentation builder

The documentation pipeline for pysampling. `pyclawd docs` delegates to this
builder (see `DocsConfig.runner` in `../.pyclawd/config.py`), which is just the
standalone script `cli.py` run with the project's Python:

    runner = ["python", "docs/cli.py"]

The docs toolchain (sphinx, nbsphinx, jupytext, jupyter-cache, …) is the `docs`
dependency group in the project's `pyproject.toml`. Install it once into your
environment:

```bash
pip install -e . --group docs
```

> The runner is just a command list — if you'd rather keep the docs deps out of
> your project env, point `runner` at an isolated env instead, e.g.
> `["uvx", "--from", "./docs", "..."]`, `["conda", "run", "-n", "docs", "python", "cli.py"]`,
> or a dedicated venv. pyclawd does not care which.

## Quick start

From the project root:

```bash
pyclawd docs build          # compile → execute (cached) → render HTML
pyclawd docs serve          # serve docs/build/html locally
```

The built site lands at `docs/build/html/index.html`.

## How it works

Sources are MyST Markdown (`source/**/*.md`). The pipeline:

1. **compile** — `jupytext` converts changed `.md` → `.ipynb`.
2. **run** — notebooks execute in parallel; successes are cached by
   `jupyter-cache`, so unchanged notebooks are skipped on the next build.
3. **render** — Sphinx + nbsphinx render the executed notebooks to HTML.
   Sphinx itself never executes (`nbsphinx_execute = 'never'`).

Execution and rendering are separate, so a render-only fix re-renders in seconds
without re-executing.

## Commands

Run directly (or via the matching `pyclawd docs <cmd>`):

```bash
python docs/cli.py all       [--force] [--continue]   # full pipeline
python docs/cli.py compile   [--force] [files...]
python docs/cli.py run       [--force] [files...]
python docs/cli.py build     [--fast]                 # render HTML only
python docs/cli.py failures  [--full]
python docs/cli.py exec <page>                        # debug ONE notebook
python docs/cli.py timings
python docs/cli.py clean
```

## Authoring

- Edit the **`.md`** sources, never the generated `.ipynb` (they are gitignored).
- Prose-only pages render instantly; add executable code with MyST
  ` ```{code-cell} ipython3 ` blocks.
- Structural pages (`index.rst`, `api.rst`) are reStructuredText.

Environment overrides: `PYSAMPLING_DOCS_TIMEOUT` (per-cell seconds),
`PYSAMPLING_DOCS_JOBS` (parallel workers).
