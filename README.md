# Anvil Project Manager Registry

This repository contains project type and toolchain definitions used by Anvil.

The registry is composed of two primary concepts:

- Project Types: Describes how a project is identified.
- Toolchains: Describe how a project is created

---

## Registry Layout

```
(root)
├── project-types/              # Directory containing all project type definitions
│   └── <project-type-id>.toml  # TOML configuration file describing a project type
├── toolchains/                 # Directory containing all toolchain definitions
│   └── <toolchain-id>/
│       ├── toolchain.toml      # TOML configuration file describing a toolchain
│       └── templates/          # An optional templates directory containing files used by the toolchain
│           └── **/*.*
└── manifest.toml               # Registry manifest file containing registry metadata
```

---

## Project Types

A project type represents a technology stack or project category such as Rust, Unity, C#, Node.js, or Godot.

Project types are used to classify existing directories by inspecting files, folders, and detected programming languages.

Example:

```toml
[project_type]
id = "unity"
name = "Unity"
color = "#222222"
version = "0.0.1"

markers = [
  { path = "ProjectSettings", kind = "directory" },
]

languages = ["C#"]
```

### Matching Rules

#### Markers

Markers are file system checks.

```toml
markers = [
  { path = "Cargo.toml", kind = "file" },
]
```

Supported kinds:

- `file`
- `directory`

A project type matches it's marker requirements when **at least one marker matches**.

#### Languages

Languages are determined using source code analysis.

```toml
languages = ["C#", "rust"]
```

Languages are case-insensitive.

A project type matches it's language requirements when **at least one language matches**.

#### Combining Markers and Languages

A project type matches when at least one marker **and** at least one language matches.

---

## Toolchains

A toolchain describes how a project should be created.

Toolchains are associated with a project type and consist of a sequence of creation steps.

Example:

```toml
[toolchain]
id = "vite-react-ts"
name = "Vite + React + TypeScript"
project_type = "node"
version = "0.0.1"

[[toolchain.params]]
name = "package_manager"
label = "Package Manager"
options = ["npm", "pnpm", "yarn"]
default = "npm"
required = true

[[toolchain.steps]]
type = "run_command"
description = "Scaffold Vite project"
command = "{package_manager} create vite@latest --yes . -- --name {project_name} --template react-ts --no-interactive"
working_dir = "{parent_dir}"

[[toolchain.steps]]
type = "run_command"
description = "Install dependencies"
command = "{package_manager} install"
```

---

### Parameters

Toolchains may define parameters that are requested from the user during project creation.

Example:

```toml
[[toolchain.params]]
name = "package_manager"
label = "Package Manager"
options = ["npm", "pnpm", "yarn"]
default = "npm"
required = true
```

Parameter values can be referenced using variable substitution.

```toml
command = "{package_manager} install"
```

---

### Variable Substitution

All string fields support variable substitution.

#### Built-In Variables

| Variable         | Description                 |
| ---------------- | --------------------------- |
| `{project_name}` | Name entered by the user    |
| `{project_dir}`  | Final destination path      |
| `{parent_dir}`   | Selected parent directory   |
| `{temp_dir}`     | Temporary working directory |
| `{<param>}`      | User-defined parameter      |

Example:

```toml
command = "cargo new {project_name}"
```

---

### Toolchain Steps

Toolchains execute steps sequentially.

#### `run_command`

Executes a shell command.

```toml
[[toolchain.steps]]
type = "run_command"
command = "cargo build"
```

| Field         | Required | Description                                  |
| ------------- | -------- | -------------------------------------------- |
| `type`        | Yes      | `"run_command"`                              |
| `command`     | Yes      | Shell command                                |
| `description` | No       | User-facing description                      |
| `working_dir` | No       | Working directory (defaults to `{temp_dir}`) |

---

#### `create_file`

Creates a file.

Exactly one of `content` or `template` must be provided.

```toml
[[toolchain.steps]]
type = "create_file"
path = "README.md"
content = "# {project_name}"
```

| Field      | Required | Description                     |
| ---------- | -------- | ------------------------------- |
| `type`     | Yes      | `"create_file"`                 |
| `path`     | Yes      | Destination path                |
| `content`  | No       | Inline content                  |
| `template` | No       | Template file from `templates/` |

---

#### `create_directory`

Creates a directory.

```toml
[[toolchain.steps]]
type = "create_directory"
path = "src"
```

| Field  | Required | Description          |
| ------ | -------- | -------------------- |
| `type` | Yes      | `"create_directory"` |
| `path` | Yes      | Directory path       |

---

#### `clone_template`

Clones a GIT repository.

```toml
[[toolchain.steps]]
type = "clone_template"
url = "https://github.com/example/template"
detach_remote = true
```

| Field           | Required | Description                                  |
| --------------- | -------- | -------------------------------------------- |
| `type`          | Yes      | `"clone_template"`                           |
| `url`           | Yes      | Git repository URL                           |
| `destination`   | No       | Clone destination                            |
| `detach_remote` | No       | Remove history and create a clean repository |

When `detach_remote = true`:

1. The repository is cloned.
2. The `.git` directory is removed.
3. A new repository is initialized.

This produces a clean project with no connection to the original template repository.

---

#### `git_init`

Initialize a Git repository and optionally generates a `.gitignore`.

```toml
[[toolchain.steps]]
type = "git_init"
gitignore_template = "Rust"
```

| Field                | Required | Description                                                           |
| -------------------- | -------- | --------------------------------------------------------------------- |
| `type`               | Yes      | `"git_init"`                                                          |
| `gitignore_template` | No       | Template from [github/gitignore](https://github.com/github/gitignore) |

If a Git repository already exists, initialization is skipped.

The `.gitignore` generation still occurs.

---

### Templates

Toolchains may contain a `templates/` directory.

Example:

```
toolchains/
└── rust-workspace/
    ├── toolchain.toml
    └── templates/
        ├── Cargo.toml
        └── README.md
```

Template files can be referenced by `create_file` steps.

```toml
[[toolchain.steps]]
type = "create_file"
path = "Cargo.toml"
template = "workspace-root.toml"
```

Template contents are rendered using variable substitution before being written.

---

## Registry Manifest

The registry publishes a generated `manifest.toml` file containing metadata for all project types and toolchains.

The manifest includes:

- Registry version
- Last update timestamp
- Project type metadata
- Toolchain metadata
- File listings
- SHA-256 hashes

Clients can use the manifest to:

- Discover available project types
- Discover available toolchains
- Detect updates
- Verify file integrity
- Cache registry content efficiently

The manifest is generated automatically and should not be edited manually.
