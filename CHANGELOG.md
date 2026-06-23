# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this
project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Modern Sphinx documentation under `docs/` with a cached build pipeline
  (`pyclawd docs build`): MyST Markdown sources → executed notebooks
  (jupyter-cache) → Sphinx + nbsphinx HTML. The builder is the standalone
  `docs/cli.py`, run with the project Python; its toolchain is the `docs`
  dependency group (`pip install -e . --group docs`).

### Changed
- Adopted the [pyclawd](https://github.com/anyoptimization) dev toolkit and moved
  to a modern `src/` layout with a `pyproject.toml` (hatchling) build.
- Replaced Travis CI with GitHub Actions (`lint`, `typecheck`, `test` matrix).
- Converted the test suite from bespoke `unittest` runners to pytest.
- Replaced the ancient single-`index.ipynb` Sphinx setup with the new docs
  pipeline above.
- Rewrote the README in Markdown.

### Fixed
- `SobolSampling` crashed on NumPy 2.x (`np.int` was removed); now uses
  `np.int64`.
- Fixed an invalid regex escape in the Sobol resource parser (`"\s"` -> `r"\s"`).
- Removed unreachable/dead branches and an undefined return in `util.cdist`; the
  alternative implementations are now selectable via `"matmul"` / `"broadcast"`.

## [0.1.2]

### Added
- Initial public release: random, Latin Hypercube, Halton and Sobol sampling
  plus discrepancy/uniformity measures.
