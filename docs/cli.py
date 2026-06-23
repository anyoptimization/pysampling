#!/usr/bin/env python3
"""pysampling documentation builder CLI.

A standalone, isolated documentation pipeline driven by ``uvx --from ./docs
pysampling-docs``. pyclawd's ``pyclawd docs`` group delegates to this CLI, so all
the heavy docs dependencies (sphinx/nbsphinx/jupyter-cache/...) live in this
isolated env and never pollute the project itself.

Pipeline: MyST ``.md`` sources are compiled to ``.ipynb`` (jupytext), executed
with a content-addressed cache (jupyter-cache, unchanged notebooks are skipped),
then rendered to HTML by Sphinx + nbsphinx.

Adapted from the pymoo docs builder.
"""

import argparse
import glob
import json
import logging
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

log = logging.getLogger("pysampling-docs")


def _setup_logging():
    """Structured logs: `HH:MM:SS  LEVEL  message` (with [notebook] context)."""
    if log.handlers:
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-5s  %(message)s", "%H:%M:%S"))
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    log.propagate = False


# Per-cell execution timeout (s). 30s (nbclient default) can be too low; raise it
# so long-but-legitimate cells don't time out. Override via PYSAMPLING_DOCS_TIMEOUT.
EXEC_TIMEOUT = os.environ.get("PYSAMPLING_DOCS_TIMEOUT", "120")

# Number of notebooks executed in parallel. Default = cores - 2 (min 1); override
# via PYSAMPLING_DOCS_JOBS to keep small machines responsive.
EXEC_JOBS = os.environ.get("PYSAMPLING_DOCS_JOBS") or str(max(1, (os.cpu_count() or 3) - 2))


def read_timings(cache_dir="."):
    """Map notebook abspath -> last execution time (seconds) from the
    jupyter-cache DB. Empty dict if the cache doesn't exist yet."""
    db = Path(cache_dir) / ".jupyter_cache" / "global.db"
    if not db.exists():
        return {}
    timings = {}
    con = sqlite3.connect(str(db))
    try:
        for uri, data in con.execute("SELECT uri, data FROM nbcache"):
            try:
                secs = json.loads(data or "{}").get("execution_seconds")
            except (ValueError, TypeError):
                secs = None
            if secs is not None:
                timings[uri] = secs
    finally:
        con.close()
    return timings


def read_failures(cache_dir="."):
    """Map notebook abspath -> traceback (ANSI-stripped) for notebooks whose last
    execution failed. jupyter-cache stores these in nbproject.traceback."""
    db = Path(cache_dir) / ".jupyter_cache" / "global.db"
    if not db.exists():
        return {}
    failures = {}
    con = sqlite3.connect(str(db))
    try:
        q = "SELECT uri, traceback FROM nbproject WHERE traceback IS NOT NULL AND traceback != ''"
        for uri, tb in con.execute(q):
            failures[uri] = re.sub(r"\x1b\[[0-9;]*m", "", tb)
    finally:
        con.close()
    return failures


def _error_line(tb):
    """The most informative line of a traceback (the exception)."""
    errs = [ln.strip() for ln in tb.splitlines() if re.search(r"(Error|Exception|Timeout\w*):", ln)]
    if errs:
        return errs[-1]
    lines = [ln for ln in tb.splitlines() if ln.strip()]
    return lines[-1].strip() if lines else "(unknown)"


def show_failures(full=False):
    """Print failed notebooks and their errors (full tracebacks with --full)."""
    failures = read_failures(".")
    if not failures:
        print("✅ No failed notebooks recorded in the cache.")
        return
    print(f"❌ {len(failures)} failed notebook(s):")
    for uri in sorted(failures):
        name = uri.split("/docs/source/")[-1]
        if full:
            print(f"\n=== {name} ===\n{failures[uri].strip()}")
        else:
            print(f"   {name}: {_error_line(failures[uri])[:140]}")


def show_timings():
    """Print all cached notebook execution times (slowest first)."""
    timings = read_timings(".")
    if not timings:
        print("No cache timings yet — run a build first.")
        return
    rows = sorted(((s, u) for u, s in timings.items()), reverse=True)
    total = sum(s for s, _ in rows)
    print(f"⏱  Notebook execution time (cached) — total {total:.1f}s across {len(rows)} notebooks:")
    src = Path("source").resolve()
    for secs, uri in rows:
        try:
            uri = str(Path(uri).relative_to(src))
        except ValueError:
            pass
        print(f"   {secs:7.1f}s  {uri}")


def run_command(cmd, cwd=None, check=True):
    """Run a command and stream output to the console."""
    if isinstance(cmd, str):
        cmd = cmd.split()
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, check=False)
    if check and result.returncode != 0:
        sys.exit(result.returncode)
    return result


def clean_docs():
    """Remove generated documentation files (keeps the execution cache)."""
    print("🧹 Cleaning documentation files...")
    build_dir = Path("build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
        print(f"Removed {build_dir}")
    for nb_file in glob.glob("source/**/*.ipynb", recursive=True):
        nb_path = Path(nb_file)
        if nb_path.with_suffix(".md").exists():  # generated from a .md → safe to drop
            nb_path.unlink()
            print(f"Removed generated notebook: {nb_file}")
    print("✅ Clean completed")


def install_project():
    """Install the parent package (editable) so autodoc can import it."""
    try:
        import pysampling  # noqa: F401

        print("✅ pysampling is available")
        return True
    except ImportError:
        print("📦 Installing pysampling in development mode...")
        parent_dir = Path("..").resolve()
        if (parent_dir / "pyproject.toml").exists():
            run_command(["python", "-m", "pip", "install", "-e", str(parent_dir)], check=False)
            return True
        print("⚠️  pysampling source not found in parent directory — API docs may fail")
        return False


def compile_notebooks(force=False, files=None):
    """Convert MyST ``.md`` sources to ``.ipynb`` notebooks (jupytext)."""
    print("📝 Starting notebook compilation...")
    if files:
        md_to_process = files
        print(f"📋 Processing {len(md_to_process)} specified files")
    else:
        all_md_files = glob.glob("source/**/*.md", recursive=True)
        if force:
            md_to_process = all_md_files
            print(f"🔄 Force mode: processing all {len(md_to_process)} markdown files")
        else:
            # Only (re)compile sources that are new or changed since their .ipynb.
            md_to_process = []
            for md_file in all_md_files:
                nb_file = Path(md_file).with_suffix(".ipynb")
                if not nb_file.exists() or Path(md_file).stat().st_mtime > nb_file.stat().st_mtime:
                    md_to_process.append(md_file)
            print(f"📋 {len(md_to_process)} changed/new of {len(all_md_files)} markdown files")

    if not md_to_process:
        print("✅ All notebooks already exist. Use --force to regenerate all.")
        return

    run_command(["python", "-m", "jupytext", "--to", "notebook", *md_to_process])

    # Normalize the kernel to one that exists in the build env.
    import nbformat

    fixed = 0
    for md in md_to_process:
        nb_path = Path(md).with_suffix(".ipynb")
        if not nb_path.exists():
            continue
        nb = nbformat.read(nb_path, 4)
        if nb.metadata.get("kernelspec", {}).get("name") != "python3":
            nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3"}
            nbformat.write(nb, nb_path)
            fixed += 1
    if fixed:
        print(f"🔧 Normalized kernel → python3 in {fixed} notebook(s)")
    print("✅ Notebook compilation completed")


def _execute_one(nb_path, timeout):
    """Execute ONE notebook (kernel forced to python3) and write outputs back.
    Returns (ok, seconds, error_or_None). Runs in its own worker process."""
    import nbformat
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError

    nb = nbformat.read(nb_path, 4)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3"}
    t0 = time.monotonic()
    try:
        NotebookClient(
            nb,
            timeout=int(timeout),
            kernel_name="python3",
            resources={"metadata": {"path": str(Path(nb_path).parent)}},
        ).execute()
        nbformat.write(nb, nb_path)
        return True, time.monotonic() - t0, None
    except CellExecutionError as exc:
        nbformat.write(nb, nb_path)  # keep error output for backtrack
        lines = [ln for ln in str(exc).strip().splitlines() if ln.strip()]
        return False, time.monotonic() - t0, (lines[-1] if lines else "CellExecutionError")[:140]
    except Exception as exc:  # kernel death, timeout, …
        return False, time.monotonic() - t0, f"{type(exc).__name__}: {exc}"[:140]


def run_notebooks(force=False, files=None):
    """Execute notebooks in parallel, caching successes (jupyter-cache STORE).

    Only stale notebooks run; successes are cached and every notebook is hydrated
    with outputs for nbsphinx. Executed outputs never reach git.
    """
    from concurrent.futures import ProcessPoolExecutor, as_completed

    from jupyter_cache import get_cache

    if files:
        nb_files = [str(Path(f).with_suffix(".ipynb")) for f in files]
    else:
        all_md = glob.glob("source/**/*.md", recursive=True)
        nb_files = [str(Path(md).with_suffix(".ipynb")) for md in all_md]
    nb_files = [str(Path(nb).resolve()) for nb in nb_files if Path(nb).exists()]
    if not nb_files:
        log.info("no notebooks to execute (run 'compile' first)")
        return 0

    cache = get_cache(".jupyter_cache")
    jobs = int(EXEC_JOBS)
    src_root = str(Path("source").resolve()) + os.sep

    stale, n_cached = [], 0
    for nb in nb_files:
        if force:
            stale.append(nb)
            continue
        try:
            cache.match_cache_file(nb)
            n_cached += 1
        except KeyError:
            stale.append(nb)

    log.info(
        "execute · %d stale · %d cached · %d workers · %ss/cell timeout",
        len(stale), n_cached, jobs, EXEC_TIMEOUT,
    )

    n_ok = n_fail = 0
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        futures = {pool.submit(_execute_one, nb, EXEC_TIMEOUT): nb for nb in stale}
        for fut in as_completed(futures):
            nb = futures[fut]
            name = nb.replace(src_root, "")
            ok, secs, err = fut.result()
            if ok:
                cache.cache_notebook_file(nb, data={"execution_seconds": secs}, overwrite=True)
                log.info("[%s] ok · %.1fs", name, secs)
                n_ok += 1
            else:
                log.error("[%s] failed · %s", name, err)
                n_fail += 1

    for nb in nb_files:
        try:
            cache.merge_match_into_file(nb)
        except Exception:
            pass  # not cached (a failure) — leave it output-less

    (log.warning if n_fail else log.info)(
        "done · %d ok · %d failed · %d reused", n_ok, n_fail, n_cached
    )
    return n_fail


def exec_single(page):
    """Execute ONE notebook directly (no cache, no pool) and show its error.

    The debug loop: run one → read the traceback → fix the .md → run again.
    """
    name = page.removesuffix(".ipynb").removesuffix(".md")
    md = f"{name}.md" if name.startswith("source/") else f"source/{name}.md"
    if not Path(md).exists():
        print(f"❌ source not found: {md}")
        sys.exit(2)
    nb = Path(md).with_suffix(".ipynb")

    run_command(["python", "-m", "jupytext", "--to", "notebook", md])
    import nbformat

    n = nbformat.read(nb, 4)
    n.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3"}
    nbformat.write(n, nb)

    print(f"\n⚡ Executing {nb} (timeout {EXEC_TIMEOUT}s/cell)...\n")
    result = run_command(
        [
            "python", "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute",
            "--inplace", f"--ExecutePreprocessor.timeout={EXEC_TIMEOUT}", str(nb),
        ],
        check=False,
    )
    if result.returncode == 0:
        print(f"\n✅ {nb} executed cleanly")
    else:
        print(f"\n❌ {nb} failed — full traceback above. Fix {md} and re-run.")
    sys.exit(result.returncode)


def _summarize_render(warnfile: Path, renderlog: Path, returncode: int) -> int:
    """Turn Sphinx's raw warning stream into a structured render verdict."""
    lines = []
    if warnfile.exists():
        lines = [ln.strip() for ln in warnfile.read_text(errors="replace").splitlines() if ln.strip()]

    seen, errors, warnings = set(), [], []
    for ln in lines:
        if ln in seen:
            continue
        seen.add(ln)
        (errors if "ERROR" in ln or "CRITICAL" in ln else warnings).append(ln)

    n = len(errors) + len(warnings)
    if returncode != 0:
        log.error("render · sphinx exited %d — HTML may be incomplete", returncode)
    if n == 0:
        log.info("render · clean · 0 warnings · log %s", renderlog)
        return 0

    emit = log.error if errors else log.warning
    emit(
        "render · %d unique issue(s) · %d error(s) · %d warning(s) · warnlog %s · log %s",
        n, len(errors), len(warnings), warnfile, renderlog,
    )
    for ln in (errors + warnings)[:30]:
        emit("  %s", ln)
    if n > 30:
        emit("  … %d more — see %s", n - 30, warnfile)
    return n


def build_html():
    """Render HTML documentation with Sphinx + nbsphinx."""
    print("🏗️  Building HTML documentation...")
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)

    warnfile = build_dir / "sphinx-warnings.log"
    renderlog = build_dir / "sphinx-render.log"
    cmd = [
        "python", "-m", "sphinx",
        "-b", "html",
        "-d", "build/doctrees",
        "--keep-going",
        "-w", str(warnfile),
        "source",
        "build/html",
    ]
    print(f"$ {' '.join(cmd)}")
    log.info("render · sphinx starting · full log %s", renderlog)
    with open(renderlog, "w") as rf:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
        )
        for line in proc.stdout:
            sys.stdout.write(line)
            rf.write(line)
        proc.wait()

    n_warn = _summarize_render(warnfile, renderlog, proc.returncode)
    if proc.returncode != 0:
        sys.exit(proc.returncode)

    verdict = (
        "✅ HTML build completed"
        if n_warn == 0
        else f"⚠️  HTML build completed with {n_warn} render warning(s) — see {warnfile}"
    )
    print(verdict)
    print(f"📖 Documentation available at: {(build_dir / 'html' / 'index.html').resolve()}")


def serve_docs(port=8000):
    """Serve the built documentation locally."""
    html_dir = Path("build/html")
    if not html_dir.exists():
        print("❌ No built documentation found. Run 'build' first.")
        sys.exit(1)
    print(f"🌐 Serving documentation at http://localhost:{port} (Ctrl+C to stop)")
    try:
        run_command(["python", "-m", "http.server", str(port)], cwd=html_dir)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")


def _maybe_chdir_to_docs():
    """Run from the docs directory regardless of where the command was invoked."""
    if Path("source").is_dir():
        return
    for candidate in [Path("docs"), Path("../docs"), Path("../../docs")]:
        if (candidate / "source").exists():
            target = candidate.resolve()
            os.chdir(target)
            print(f"📁 Changed to docs directory: {target}")
            return
    print("❌ Could not find a docs directory containing 'source/'")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="pysampling documentation builder")
    sub = parser.add_subparsers(dest="command", help="Available commands")

    sub.add_parser("clean", help="Remove generated files (keeps the cache)")

    p_compile = sub.add_parser("compile", help="Convert .md to .ipynb")
    p_compile.add_argument("--force", action="store_true", help="Recompile all files")
    p_compile.add_argument("files", nargs="*", help="Specific files (optional)")

    p_run = sub.add_parser("run", help="Execute notebooks (cached, parallel, skip-unchanged)")
    p_run.add_argument("--force", action="store_true", help="Re-execute all notebooks")
    p_run.add_argument("files", nargs="*", help="Specific files (optional)")
    p_run.add_argument("--continue", dest="cont", action="store_true", help="Don't exit non-zero on failure")

    # `build` renders HTML ONLY (from already-executed notebooks). The full
    # compile→run→render pipeline is `all`. This mirrors what pyclawd expects:
    # `pyclawd docs render` → `build [--fast]`, `pyclawd docs build` → `all`.
    p_build = sub.add_parser("build", help="Render HTML from executed notebooks (no execution)")
    p_build.add_argument("--fast", action="store_true", help="Skip notebooks (smoke render)")

    p_all = sub.add_parser("all", help="Compile → run → render HTML")
    p_all.add_argument("--force", action="store_true", help="Recompile and re-execute everything")
    p_all.add_argument("--continue", dest="cont", action="store_true", help="Render even if notebooks failed")

    p_serve = sub.add_parser("serve", help="Serve built HTML locally")
    p_serve.add_argument("--port", type=int, default=8000)

    sub.add_parser("timings", help="Cached per-notebook execution times (slowest first)")
    p_fail = sub.add_parser("failures", help="Notebooks whose last execution failed")
    p_fail.add_argument("--full", action="store_true", help="Show full tracebacks")
    p_exec = sub.add_parser("exec", help="Execute ONE notebook directly and show its error")
    p_exec.add_argument("page", help="Notebook page, e.g. getting_started")

    args = parser.parse_args()
    _setup_logging()
    _maybe_chdir_to_docs()

    if args.command in {"compile", "run", "build", "exec", "all"}:
        install_project()

    if args.command == "clean":
        clean_docs()
    elif args.command == "compile":
        compile_notebooks(force=args.force, files=args.files)
    elif args.command == "run":
        n_fail = run_notebooks(force=args.force, files=args.files)
        if n_fail and not args.cont:
            sys.exit(1)
    elif args.command == "build":
        if args.fast:
            os.environ["PYSAMPLING_DOCS_FAST_MODE"] = "1"
            print("⚡ Fast render mode: excluding notebooks")
        build_html()
    elif args.command == "all":
        compile_notebooks(force=args.force)
        n_fail = run_notebooks(force=args.force)
        if n_fail and not args.cont:
            log.error(
                "%d notebook(s) failed — NOT building HTML. "
                "Fix them (`failures` / `exec <page>`) or pass --continue.",
                n_fail,
            )
            sys.exit(1)
        build_html()
        log.info("documentation build complete")
    elif args.command == "serve":
        serve_docs(args.port)
    elif args.command == "timings":
        show_timings()
    elif args.command == "failures":
        show_failures(full=args.full)
    elif args.command == "exec":
        exec_single(args.page)
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
