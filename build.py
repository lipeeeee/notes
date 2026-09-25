"""Build LaTeX notes. latexmk tracks changes; Git does not track the last successful build."""

import argparse
import filecmp
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / ".build"
PDF = ROOT / "pdf"


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("notes", nargs="*", help="specific .tex files; default: all notes")
  args = parser.parse_args()

  git, latexmk = shutil.which("git"), shutil.which("latexmk")
  if not git or not latexmk: raise SystemExit(f"Missing tool: {'git' if not git else 'latexmk'}")
  repo = subprocess.run([git, "rev-parse", "--show-toplevel"], cwd=ROOT, capture_output=True, text=True)
  if repo.returncode or Path(repo.stdout.strip()).resolve() != ROOT: raise SystemExit("build.py must be at the Git root")

  paths = [ROOT / name for name in args.notes]
  if not paths: paths = [p for section in ("math", "ml") for p in (ROOT / section).rglob("*.tex")]
  sources = sorted({path.resolve() for path in paths})
  for source in sources:
    if not source.is_file() or source.suffix.lower() != ".tex" or not source.is_relative_to(ROOT):
      raise SystemExit(f"Invalid note: {source}")
    if source.relative_to(ROOT).parts[0] not in ("math", "ml"): raise SystemExit(f"Note must be under math/ or ml/: {source}")
  if len({source.stem.casefold() for source in sources}) != len(sources):
    raise SystemExit("Two notes have the same filename and would overwrite one PDF")
  if BUILD.is_symlink() or PDF.is_symlink(): raise SystemExit("Build and PDF directories must not be symlinks")

  for source in sources:
    relative = source.relative_to(ROOT)
    work = BUILD / relative.parent
    if not work.resolve().is_relative_to(BUILD.resolve()): raise SystemExit(f"Unsafe build directory: {work}")
    work.mkdir(parents=True, exist_ok=True)
    print(f"Checking {relative}...", flush=True)
    result = subprocess.run([
      latexmk, "-pdf", "-halt-on-error", "-interaction=nonstopmode", f"-outdir={work}", source.name
    ], cwd=source.parent)
    if result.returncode: raise SystemExit(f"latexmk failed for {relative}")

    generated = work / f"{source.stem}.pdf"
    if not generated.is_file(): raise SystemExit(f"latexmk did not produce {generated}")
    target = PDF / generated.name
    if target.is_symlink() or (target.exists() and not target.is_file()): raise SystemExit(f"Unsafe PDF target: {target}")
    if target.exists() and filecmp.cmp(generated, target, shallow=False):
      print(f"Unchanged {target.relative_to(ROOT)}")
      continue

    PDF.mkdir(exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=PDF, delete=False) as temporary: temp = Path(temporary.name)
    try:
      shutil.copyfile(generated, temp)
      temp.replace(target)
    finally:
      temp.unlink(missing_ok=True)
    print(f"Updated {target.relative_to(ROOT)}")


if __name__ == "__main__": main()
