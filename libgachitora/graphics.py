import subprocess, sys
from pathlib import Path

def extract_gim(gimPath: Path, type: str):
    gimconv = Path("bin/gimconv/GimConv.exe")
    output = gimPath.stem + ".png"

    result = subprocess.run(
        [gimconv, gimPath, type, "-o", output],
        capture_output=True,
        text=True,
        shell=False,
    )
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.returncode != 0:
        sys.stderr.write(f"GimConv failed with return code {result.returncode}\n")
        if result.stderr:
            sys.stderr.write(f"stderr:\n{result.stderr}\n")
        sys.exit(result.returncode)