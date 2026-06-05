## Toolchain Contribution

### ID

<!-- Example: vite-react-ts -->

```text
<id>
```

### Version

<!-- Example: 0.0.1 -->

```text
<version>
```

### Project Type

<!-- Example: node -->

```text
<project_type>
```

### Change Type

- [ ] New Toolchain
- [ ] Update Existing Toolchain

### Summary

<!-- Describe the toolchain and what changed. -->

```text
<summary>
```

### Parameters

<!-- List any parameters exposed by the toolchain. -->

```text
<parameters>
```

### Steps

<!-- Brief summary of the toolchain workflow. -->

```text
<steps>
```

### Validation

- [ ] Directory name matches toolchain ID
- [ ] Referenced project type exists
- [ ] Version follows semantic versioning
- [ ] Version was incremented (if updating an existing toolchain)
- [ ] Templates referenced by create_file exist
- [ ] Toolchain was tested locally

### Contribution Policy

- [ ] This PR modifies exactly one toolchain
- [ ] This PR does not modify any project types
- [ ] No unrelated files were modified
