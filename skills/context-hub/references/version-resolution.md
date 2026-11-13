# Resolving the pinned version

Prefer resolved dependency information: a lockfile records the intended resolution,
while manifests may only give ranges. Installed environments can drift from the lockfile.

| Ecosystem          | Lockfile (resolved version)                                       | Manifest (declared range)                                         |
| ------------------ | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| npm                | `package-lock.json` → `packages["node_modules/<name>"].version`   | `package.json` dependencies                                       |
| pnpm               | `pnpm-lock.yaml` → `importers.<path>.dependencies.<name>.version` | `package.json`                                                    |
| Yarn               | `yarn.lock` → entry `"<name>@<range>"` → `version`                | `package.json`                                                    |
| Python (pip)       | `requirements*.txt` with `==` pins, or a constraints file         | `requirements*.txt`, `setup.cfg`                                  |
| Python (Poetry/uv) | `poetry.lock` / `uv.lock` → `[[package]] name/version`            | `pyproject.toml`                                                  |
| Go                 | `go list -m -json <module>` from the relevant module/workspace   | `go.mod`, `go.work` and their `replace` directives                 |
| Rust               | `Cargo.lock` → `[[package]] name/version`                         | `Cargo.toml`                                                      |
| .NET               | `packages.lock.json`                                              | `*.csproj` `PackageReference Version`, `Directory.Packages.props` |
| Java               | `gradle.lockfile`                                                 | `pom.xml`, `build.gradle(.kts)`, version catalogs                 |
| Ruby               | `Gemfile.lock`                                                    | `Gemfile`                                                         |

Go's `go.sum` stores checksums, not the selected dependency graph; it can contain
multiple historical versions. Inspect `Version` and `Replace` in `go list -m -json`
output. A local replacement has no guaranteed upstream release version: inspect that
checkout rather than attributing upstream documentation to it. If module resolution
would require unavailable downloads, report that limitation and treat `go.mod` as
declared information rather than verified resolution.

For pip, constraints only constrain packages actually selected for installation. Confirm
which requirements/constraints files the project uses. For pnpm, use the relevant
workspace importer and account for aliases and peer-dependency suffixes.

For HTTP APIs without a client package, use the API version the code sends (URL path such as
`/v2/`, an `api-version` query parameter, or a version header) and check that version's
reference.

Monorepos can pin different versions per package: resolve the version for the package that
contains the changed file.
