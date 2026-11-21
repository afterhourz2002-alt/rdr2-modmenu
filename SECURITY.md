# Security Policy

## Scope

`rdr2-modmenu` is a hobbyist, offline, single-player tool. It attaches to a
local `RDR2.exe` process via `pymem` and renders an overlay. It ships **no
network code**, **no telemetry**, and **no auto-updater**.

## Supported versions

Only the latest tagged release on `main` receives fixes.

| Version | Supported |
| ------- | --------- |
| 0.9.x   | ✅        |
| < 0.9   | ❌        |

## Reporting a vulnerability

If you find something in scope — e.g. a path-traversal in the config loader,
a pipe-handling issue in `script_hook`, or an unsafe memory write that could
corrupt a save — email **security@rdr2-modmenu.dev** with:

- Affected file / function
- Reproduction steps
- Impact assessment

Do **not** open a public issue for exploitable bugs. We aim to respond within
72 hours and will credit reporters in the release notes unless asked otherwise.

## Out of scope

- Rockstar anti-cheat / RDO bans (this tool is single-player only).
- Issues arising from using mods in Red Dead Online.
- "It doesn't work after the latest patch" — that's an offset issue, use the
  regular issue tracker.

## Disclaimer

Use at your own risk. Modding RDR2 single-player can corrupt save files.
Always back up your `Documents\Rockstar Games\Red Dead Redemption 2\Profiles`
folder before running.