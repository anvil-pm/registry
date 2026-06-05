from pathlib import Path
import subprocess
import sys
import tomllib
import os
import re


def fail(msg: str):
  print(f"ERROR: {msg}")
  sys.exit(1)


SEMVER = re.compile(
  r"^(0|[1-9]\d*)\."
  r"(0|[1-9]\d*)\."
  r"(0|[1-9]\d*)$"
)


def validate_semver(version: str):
  if not SEMVER.match(version):
    fail(f"Invalid semantic version: {version}")


def validate_project_type(path: Path):
  with open(path, "rb") as f:
    data = tomllib.load(f)

  if "project_type" not in data:
    fail(f"{path}: missing [project_type]")

  pt = data["project_type"]

  for field in ("id", "name", "version", "color"):
    if field not in pt:
      fail(f"{path}: missing field '{field}'")

  if "markers" not in pt and "languages" not in pt:
    fail(f"{path}: missing field 'markers' or 'languages'")

  expected = path.stem

  if pt["id"] != expected:
    fail(f"{path}: id '{pt['id']}' must match filename '{expected}'")

  validate_semver(pt["version"])


def validate_toolchain(path: Path):
  with open(path, "rb") as f:
    data = tomllib.load(f)

  if "toolchain" not in data:
    fail(f"{path}: missing [toolchain]")

  tc = data["toolchain"]

  for field in ("id", "name", "project_type", "version"):
    if field not in tc:
      fail(f"{path}: missing field '{field}'")

  expected = path.parent.name

  if tc["id"] != expected:
    fail(f"{path}: id '{tc['id']}' must match directory '{expected}'")

  validate_semver(tc["version"])

  project_type_file = Path("project-types") / f"{tc['project_type']}.toml"

  if not project_type_file.exists():
    fail(f"{path}: project type '{tc['project_type']}' does not exist")

  steps = data["toolchain"].get("steps", [])

  for step in steps:
    if step.get("type") == "create_file" and "template" in step:
      template = path.parent / "templates" / step["template"]

      if not template.exist():
        fail(f"{path}: template '{step['template']}' does not exist")


def get_changed_files():
  base = subprocess.check_output(
    [
      "git",
      "merge-base",
      "HEAD",
      "origin/" + os.environ["GITHUB_BASE_REF"],
    ],
    text=True,
  ).strip()

  files = subprocess.check_output(
    ["git", "diff", "--name-only", base, "HEAD"],
    text=True,
  ).splitlines()

  return [f for f in files if f]


def parse_version(path: Path):
  with open(path, "rb") as f:
    data = tomllib.load(f)

  if path.parts[0] == "project-types":
    return data["project_type"]["version"]

  return data["toolchain"]["version"]


def semver_tuple(version: str):
  return tuple(int(x) for x in version.split("."))


changed = get_changed_files()

# Ignore generated files
changed = [f for f in changed if f != "manifest.toml"]

# ===========================
# Determine Contribution Type
# ===========================

project_type_files = [f for f in changed if f.startswith("project-types/")]

toolchain_files = [f for f in changed if f.startswith("toolchains/")]

other_files = [
  f
  for f in changed
  if not f.startswith("project-types/")
  and not f.startswith("toolchains/")
  and f != "manifest.toml"
]

if other_files:
  fail(f"Pull request modifies unsupported files: {other_files}")

if project_type_files and toolchain_files:
  fail("Pull request may modify project types OR toolchains, not both.")

if not project_type_files and not toolchain_files:
  fail("No project type or toolchain changes detected.")

# ===========================
# Validate Project Type PRs
# ===========================

if project_type_files:
  entries = {Path(f).name for f in project_type_files}

  if len(entries) != 1:
    fail("Only one project type may be modified per PR.")

  file = next(iter(entries))
  path = Path("project-types") / file

  try:
    old = subprocess.check_output(
      [
        "git",
        "show",
        f"origin/{os.environ['GITHUB_BASE_REF']}:project-types/{file}",
      ]
    )

    old_data = tomllib.loads(old.decode("utf-8"))

    with open(path, "rb") as f:
      new_data = tomllib.load(f)

    old_version = old_data["project_type"]["version"]
    new_version = new_data["project_type"]["version"]

    if semver_tuple(new_version) <= semver_tuple(old_version):
      fail(f"Version must increase ({old_version} -> {new_version})")

  except subprocess.CalledProcessError:
    print("New project type detected.")

# ===========================
# Validate Toolchain PRs
# ===========================

if toolchain_files:
  toolchains = {Path(f).parts[1] for f in toolchain_files}

  if len(toolchains) != 1:
    fail("Only one toolchain may be modified per PR.")

  toolchain = next(iter(toolchains))

  toolchain_toml = Path("toolchains") / toolchain / "toolchain.toml"

  try:
    old = subprocess.check_output(
      [
        "git",
        "show",
        f"origin/{os.environ['GITHUB_BASE_REF']}:toolchains/{toolchain}/toolchain.toml",
      ]
    )

    old_data = tomllib.loads(old.decode("utf-8"))

    with open(toolchain_toml, "rb") as f:
      new_data = tomllib.load(f)

    old_version = old_data["project_type"]["version"]
    new_version = new_data["project_type"]["version"]

    if semver_tuple(new_version) <= semver_tuple(old_version):
      fail(f"Version must increase ({old_version} -> {new_version})")

  except subprocess.CalledProcessError:
    print("New toolchain detected")

# ===========================
# Validate entire registry
# ===========================

for file in Path("project-types").glob("*.toml"):
  validate_project_type(file)

for file in Path("toolchains").glob("*/toolchain.toml"):
  validate_toolchain(file)

print("Validation passed.")
