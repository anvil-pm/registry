from pathlib import Path
from datetime import date
import tomllib
import tomlkit
import hashlib


def sha256_file(path):
  hasher = hashlib.sha256()

  with open(path, "rb") as f:
    while chunk := f.read(65536):
      hasher.update(chunk)

  return hasher.hexdigest()


ROOT = Path(__file__).parent.parent.parent

manifest = tomlkit.document()

manifest["registry"] = {
  "version": "1",
  "updated_at": str(date.today()),
}

project_types = tomlkit.aot()

for file in sorted((ROOT / "project-types").glob("*.toml")):
  with open(file, "rb") as f:
    data = tomllib.load(f)

  project_type = data["project_type"]

  entry = tomlkit.table()
  entry["id"] = project_type["id"]
  entry["name"] = project_type["name"]
  entry["version"] = project_type["version"]
  entry["file"] = str(file.relative_to(ROOT)).replace("\\", "/")
  entry["sha256"] = sha256_file(file)

  project_types.append(entry)

manifest["project_types"] = project_types

toolchains = tomlkit.aot()

for toolchain_dir in sorted((ROOT / "toolchains").iterdir()):
  if not toolchain_dir.is_dir():
    continue

  toolchain_file = toolchain_dir / "toolchain.toml"

  if not toolchain_file.exists():
    continue

  with open(toolchain_file, "rb") as f:
    data = tomllib.load(f)

  tc = data["toolchain"]

  files = []

  for path in sorted(toolchain_dir.rglob("*")):
    if not path.is_file():
      continue

    file_entry = tomlkit.table()
    file_entry["path"] = str(path.relative_to(ROOT)).replace("\\", "/")
    file_entry["sha256"] = sha256_file(path)

    files.append(file_entry)

  entry = tomlkit.table()
  entry["id"] = tc["id"]
  entry["name"] = tc["name"]
  entry["version"] = tc["version"]
  entry["project_type"] = tc["project_type"]
  if "description" in tc:
    entry["description"] = tc["description"]
  entry["files"] = files

  toolchains.append(entry)

manifest["toolchains"] = toolchains

output = ROOT / "manifest.toml"

with open(output, "w", encoding="utf-8") as f:
  f.write(tomlkit.dumps(manifest))
