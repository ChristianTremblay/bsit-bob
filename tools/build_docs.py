from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> None:
    print(f"[build-docs] {' '.join(cmd)}")
    subprocess.run(cmd, check=True, cwd=str(cwd))


def main():
    repo = Path(__file__).resolve().parents[1]
    doc = repo / "doc"

    # Load .env (for S223_FOLDER, etc.)
    try:
        from dotenv import load_dotenv  # type: ignore

        load_dotenv()
    except Exception:
        pass

    # 1) Generate glossary from RDF
    run([sys.executable, str(repo / "tools" / "gen_glossary_from_rdf.py")], cwd=repo)

    # 2) Sync publication figures into Sphinx static path (not committed)
    run(
        [
            sys.executable,
            str(repo / "tools" / "sync_s223_figures.py"),
            "--load-dotenv",
            "--dest",
            str(doc / "_static" / "s223_figures"),
        ],
        cwd=repo,
    )

    # 3) Build Sphinx HTML
    out = doc / "_build" / "html"
    out.mkdir(parents=True, exist_ok=True)
    run(["sphinx-build", "-b", "html", str(doc), str(out)], cwd=repo)

    print(f"[build-docs] Done. Open: {out / 'index.html'}")


if __name__ == "__main__":
    main()
