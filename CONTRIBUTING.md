# Contributing

Thank you for your interest in contributing to the Anvil Registry.

To keep reviews simple and ensure registry entries remain easy to audit, all pull requests must follow the contribution rules outlined below.

## Contribution Types

Every pull request must be **exactly one** of the following:

1. Add or Update a Project Type

A project type contribution may:

- Add a new file under `project-types/`
- Update an existing project type
- Modify detection markers
- Modify language definitions
- Increment the project type version

A project type contribution must not:

- Add or modify toolchains
- Include unrelated registry changes

2. Add or Update a Toolchain

A toolchain contribution may:

- Add a new directory under `toolchains/`
- Update an existing toolchain
- Add, remove, or modify template files
- Increment the toolchain version

A toolchain contribution must not:

- Add or modify project types
- Include unrelated registry changes

---

## One Contribution Per Pull Request

A pull request should contain a single logical contribution.

### Good Examples

- Add a new Rust project type
- Add a new Unity project type
- Add a new Vite + React + TypeScript toolchain
- Add a new Rust Workspace toolchain

### Bad Examples

- Add a Rust project type and a Rust toolchain
- Add multiple unrelated toolchains
- Add a toolchain while modifying existing registry entries
- Add documentation changes unrelated to the submitted registry entry

---

## Versioning Requirements

Any modifications to an existing registry entry must increase it's version number.

Examples:

```toml
version = "1.0.0" # -> "1.0.1" or "1.1.0"
```

Pull requests that modify an existing entry without increasing it's version may be rejected by automated validation.

---

## Project Type Requirements

Project type identifiers must be unique.

Example structure:

```
project-types/
└── rust.toml
```

Project types should:

- Use a stable identifier
- Include a human-readable name
- Include a version
- Provide accurate markers and/or language detection rules

Project types should be generic and describe a technology stack rather than a specific project layout.

### Good:

- Rust
- Unity
- C#
- Node.js
- Godot

### Bad:

- Rust Workspace
- Vite React App
- Unity FPS Template

Those are toolchains, not project types.

---

## Toolchain Requirements

Toolchain identifiers must be unique.

Example structure:

```
toolchains/
└── rust-workspace/
    ├── toolchain.toml
    └── templates/
```

Toolchains should:

- Target an existing project type
- Include a version
- Include a clear description
- Be reproducable on a clean system
- Avoid unnecessary external dependencies

Toolchains describe project layouts, templates, and scaffolding workflows.

Examples:

- Rust Workspace
- Vite + React + TypeScript
- Unity URP Project
- ASP.NET Web API

---

### Templates

Template files must be stored inside the toolchain's `templates/` directory.

Example:

```
toolchains/
└── rust-workspace/
    ├── toolchain.toml
    └── templates/
        └── workspace-root.toml
```

Template should use variable substitution where appropriate rather than hardcoded project names.

---

## Generated Files

Do not manually edit:

```
manifest.toml
```

The registry manifest is generated automatically by GitHub Actions.

If your contribution is accepted, the manifest will be updated automatically.

---

## Review Criteria

Contributions are reviewed for:

- Correctness
- Consistency
- Maintainability
- Security
- Reproducibility

Pull requests that do not follow these guidelines may be closed without review.

Thank you for helping improve the Anvil Registry.
