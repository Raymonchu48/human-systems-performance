from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
target = root / "assets" / "cluster-approved.webp"
with target.open("wb") as fh:
    subprocess.run(
        ["git","show","8612f9f673b6b653822cd41901404b292b7bc56d:assets/cluster-approved.webp"],
        stdout=fh, check=True
    )
try:
    Path(__file__).unlink()
except Exception:
    pass
