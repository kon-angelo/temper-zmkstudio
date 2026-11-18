#!/usr/bin/env python3
"""Build this repo's CI matrix inside the ZMK Docker image."""

import hashlib
import os
from pathlib import Path
import shlex
import shutil
import subprocess

import yaml


REPO = Path("/config")
WORKSPACE = Path("/workspace")


def run(*args):
    print(f"+ {shlex.join(str(arg) for arg in args)}", flush=True)
    subprocess.run([str(arg) for arg in args], cwd=WORKSPACE, check=True)


def main():
    with (REPO / "build.yaml").open() as source:
        matrix = yaml.safe_load(source)
    # The repo uses explicit include entries, just like the CI build matrix.
    if set(matrix) != {"include"} or not matrix["include"]:
        raise ValueError("build.yaml must contain a nonempty include-only matrix")
    targets = matrix["include"]
    names = set()
    for target in targets:
        name = target["artifact-name"]
        if not name or name in {".", ".."} or Path(name).name != name or name in names:
            raise ValueError(f"Invalid or duplicate artifact-name: {name!r}")
        names.add(name)

    # Keep west's writable workspace separate from the read-only source checkout.
    config = WORKSPACE / "config"
    if config.exists():
        shutil.rmtree(config)
    shutil.copytree(REPO / "config", config)
    initialized = (WORKSPACE / ".west").exists()
    if not initialized:
        run("west", "init", "-l", config)

    manifest_hash = hashlib.sha256((config / "west.yml").read_bytes()).hexdigest()
    stamp = WORKSPACE / ".manifest-sha256"
    if (
        not initialized
        or not stamp.exists()
        or stamp.read_text() != manifest_hash
        or os.environ.get("UPDATE") == "1"
    ):
        # A failed update must be retried before building from a partial workspace.
        stamp.unlink(missing_ok=True)
        run("west", "update", "--fetch-opt=--filter=tree:0")
        stamp.write_text(manifest_hash)
    run("west", "zephyr-export")
    run("git", "-C", WORKSPACE / "zmk", "rev-parse", "HEAD")

    artifacts = []
    for target in targets:
        name = target["artifact-name"]
        build_dir = WORKSPACE / "build" / name
        command = [
            "west", "build", "--pristine=always",
            "-s", WORKSPACE / "zmk/app", "-d", build_dir,
            "-b", target["board"],
        ]
        if target.get("snippet"):
            command.extend(["-S", target["snippet"]])
        command.extend([
            "--", f"-DZMK_CONFIG={config}", f"-DZMK_EXTRA_MODULES={REPO}",
        ])
        if target.get("shield"):
            command.append(f"-DSHIELD={target['shield']}")
        command.extend(shlex.split(target.get("cmake-args", "")))
        run(*command)
        uf2 = build_dir / "zephyr/zmk.uf2"
        if not uf2.is_file() or uf2.stat().st_size == 0:
            raise RuntimeError(f"Build did not produce firmware: {uf2}")
        artifacts.append((uf2, f"{name}.uf2"))

    # Publish only after every target has built successfully.
    for uf2, filename in artifacts:
        shutil.copyfile(uf2, Path("/output") / filename)
        print(f"Exported {filename} ({uf2.stat().st_size:,} bytes)", flush=True)


if __name__ == "__main__":
    main()
