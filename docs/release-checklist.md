# Release Checklist

1. Update `CHANGELOG.md`.
2. Create `docs/release-vX.Y.Z.md`.
3. Run validation and tests.
4. Run `python scripts/agent_radar.py release-draft`.
5. Create and push tag `vX.Y.Z`.
6. Confirm the GitHub Release workflow succeeds.
7. Confirm the release URL resolves.

## Release Discipline

- Keep `## Unreleased` at the top of `CHANGELOG.md`.
- Move shipped items from `Unreleased` into the version section before tagging.
- Use `docs/release-vX.Y.Z.md` as the GitHub Release notes source.
- Do not tag if validation, tests, or secret scan fail.
