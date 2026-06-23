"""pysampling's pyclawd config — drives `pyclawd test/lint/typecheck/docs/...` for this repo."""

from pyclawd import DocsConfig, DoctorConfig, Project, QualityConfig, TestConfig

project = Project(
    name="pysampling",
    conda_env="default",
    root_markers=["pyproject.toml"],
    # Where pyclawd writes this project's transient files (run logs, junit, scratch).
    work_dir="/tmp/pysampling",
    # Default directory `pyclawd ls` lists (the code/source root).
    src_dir="src",
    quality=QualityConfig(
        lint_cmd=["ruff", "check"],
        lint_fix_cmd=["ruff", "check", "--fix"],
        format_cmd=["ruff", "format"],
        format_check_cmd=["ruff", "format", "--check"],
        typecheck_cmd=["mypy", "src"],
        check_sequence=["format-check", "lint", "typecheck", "test"],
    ),
    # Docs build runs in the project env: `pip install -e . --group docs`, then
    # `pyclawd docs build` → `python docs/cli.py all`. (Swap `runner` for an
    # isolated env, e.g. uvx, if you'd rather not install the docs deps here.)
    docs=DocsConfig(
        runner=["python", "docs/cli.py"],
        source_dir="docs/source",
        cache_dir="docs/.jupyter_cache",
        cache_db="docs/.jupyter_cache/global.db",
        build_html="docs/build/html",
        branch="master",
    ),
    test=TestConfig(
        tests_dir="tests/",
        classname_prefix="tests.",
        integration_files=[],
        markers={"default": "not slow", "fast": "not slow", "all": ""},
    ),
    doctor=DoctorConfig(
        core_deps=["numpy"],
        dev_deps=["pytest"],
        tool_files=[],
        binaries=[
            ("ruff", "pip install ruff"),
            ("mypy", "pip install mypy"),
            ("pandoc", "conda install -c conda-forge pandoc"),  # nbsphinx HTML render
        ],
    ),
)
