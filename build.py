"""Build LaTeX notes. latexmk tracks changes; Git does not track the last successful build."""

import argparse
import filecmp
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / ".build"
PDF = ROOT / "pdf"
SECTIONS = ("math", "ml", "proj")
INDEX_START = "<!-- notes:index:start -->"
INDEX_END = "<!-- notes:index:end -->"


def update_index() -> None:
  notes = (p for section in SECTIONS for p in (ROOT / section).rglob("*")
           if p.is_file() and p.suffix.lower() in (".tex", ".md"))
  rows = []
  for source in sorted(notes, key=lambda p: p.relative_to(ROOT).as_posix().casefold()):
    relative = source.relative_to(ROOT).as_posix()
    label = relative.replace("|", r"\|").replace("[", r"\[").replace("]", r"\]")
    pdf = PDF / f"{source.stem}.pdf"
    pdf_link = f"[PDF](pdf/{quote(pdf.name, safe='')})" if source.suffix.lower() == ".tex" and pdf.is_file() else ""
    rows.append(f"| [{label}]({quote(relative, safe='/')}) | {pdf_link} |")
  table = "\n".join(("| Source | PDF |", "| --- | --- |", *rows))
  readme = ROOT / "README.md"
  content = readme.read_text(encoding="utf-8")
  if INDEX_START not in content or INDEX_END not in content: raise SystemExit("README.md is missing index markers")
  start = content.index(INDEX_START) + len(INDEX_START)
  end = content.index(INDEX_END, start)
  updated = f"{content[:start]}\n{table}\n{content[end:]}"
  if updated == content: return
  readme.write_text(updated, encoding="utf-8", newline="\n")
  print("Updated README.md")


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("notes", nargs="*", help="specific .tex files; default: all notes")
  args = parser.parse_args()

  git, latexmk = shutil.which("git"), shutil.which("latexmk")
  if not git or not latexmk: raise SystemExit(f"Missing tool: {'git' if not git else 'latexmk'}")
  repo = subprocess.run([git, "rev-parse", "--show-toplevel"], cwd=ROOT, capture_output=True, text=True)
  if repo.returncode or Path(repo.stdout.strip()).resolve() != ROOT: raise SystemExit("build.py must be at the Git root")

  paths = [ROOT / name for name in args.notes]
  if not paths: paths = [p for section in SECTIONS for p in (ROOT / section).rglob("*.tex")]
  sources = sorted({path.resolve() for path in paths})
  for source in sources:
    if not source.is_file() or source.suffix.lower() != ".tex" or not source.is_relative_to(ROOT):
      raise SystemExit(f"Invalid note: {source}")
    if source.relative_to(ROOT).parts[0] not in SECTIONS: raise SystemExit(f"Note must be under {', '.join(SECTIONS)}: {source}")
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

  update_index()


if __name__ == "__main__": main()
