---
name: codex-claude-skill-bootstrap
description: Build safe one-command installers or migration packages for user-owned Codex and Claude agent skills. Use when the user asks to package, bootstrap, install, sync, migrate, or publish Codex/Claude skills, create install.sh scripts, create skills manifests, or make GitHub-based one-line installers while respecting proprietary official skill licenses.
---

# Codex Claude Skill Bootstrap

## Goal

Create a safe, repeatable installation package for user-owned Codex and Claude skills. The package should let the user install or update selected skills into `~/.codex/skills` and/or `~/.claude/skills` with one command, while avoiding accidental publication of official, proprietary, credentialed, or third-party restricted skill content.

This skill is for building the packaging workflow, installer scripts, manifests, and documentation. It does not automatically install Codex or Claude clients unless the user explicitly requests that and the official installation method is verified.

## Default Policy

When the destination repository is public:

- Include only user-owned skills.
- Do not copy Claude/Codex official skills or any skill whose frontmatter or files indicate `license: Proprietary`, `Complete terms in LICENSE.txt`, marketplace origin, bundled plugin origin, or unclear redistribution rights.
- For official/proprietary skills, only detect and report whether they exist locally.
- Do not store credentials, API keys, backend session URLs, tokens, browser cookies, or machine-specific secrets.

When the destination repository is private:

- Still separate user-owned skills from official/proprietary skills.
- Ask the user before copying restricted third-party content.
- Prefer a local ignored backup for proprietary skills rather than committing them.

## Skill Audit Workflow

1. Inspect local skill roots:
   - Codex: `~/.codex/skills`
   - Claude: `~/.claude/skills`
2. For each skill, read only its `SKILL.md` frontmatter and nearby license files first.
3. Classify each skill:
   - `owned`: user-authored or repo-authored skill, safe to package.
   - `official_or_proprietary`: official bundled skill, marketplace skill, or license-restricted skill.
   - `unclear`: no obvious ownership or license signal; do not publish until clarified.
4. Build a table with:
   - skill name
   - source path
   - target directory name
   - classification
   - reason
   - include in repo: yes/no
5. If a public repo is involved, fail closed: exclude anything not clearly `owned`.

## Installer Requirements

When creating an installer script, use Bash unless the user requests another language.

The installer should support:

- `--target codex|claude|both`, default `both`
- `--dry-run`
- `--force`
- `--backup`
- `--branch <branch>`, default `main`
- `--repo <owner/repo>` when useful
- `--help`

Required behavior:

- Detect whether it is running from a cloned repo or from a GitHub raw one-line command.
- For raw execution, download the repository tarball into a temporary directory and clean it up after installation.
- Copy only skills listed in a manifest such as `installer/skills-manifest.json`.
- Install to:
  - `~/.codex/skills/<skill-name>`
  - `~/.claude/skills/<skill-name>`
- If a target skill already exists:
  - With `--backup`, move it to a timestamped backup directory first.
  - Without `--force`, do not overwrite a non-empty directory.
  - With `--force`, replace the target after backup or explicit removal.
- Check for `codex` and `claude` commands; warn if missing, but do not fail skill installation.
- Check selected official skills locally and report present/missing; never copy them from local official directories into a public repo.

## Manifest Requirements

Create `installer/skills-manifest.json` with deterministic fields:

```json
{
  "version": 1,
  "skills": [
    {
      "name": "read-literature-pdf",
      "source": ".",
      "target": "read-literature-pdf",
      "owner": "user",
      "description": "Deep Chinese biomedical PDF reading report skill"
    }
  ],
  "official_skill_checks": [
    {
      "name": "pdf",
      "codex_path": "~/.codex/skills/pdf",
      "claude_path": "~/.claude/skills/pdf",
      "action": "detect_only"
    }
  ]
}
```

Rules:

- `source` must be relative to the repository root.
- Root skill compatibility is allowed: `source: "."` can represent the repository root skill if it contains `SKILL.md`.
- Do not include absolute local paths in a committed manifest.
- Do not list proprietary skills under `skills`; list them only under `official_skill_checks`.

## Documentation Requirements

Update the repository README with:

- One-line install command:

  ```bash
  bash -c "$(curl -fsSL https://raw.githubusercontent.com/<owner>/<repo>/main/install.sh)"
  ```

- Local install command:

  ```bash
  git clone git@github.com:<owner>/<repo>.git
  cd <repo>
  ./install.sh --target both
  ```

- Clear statement that public repositories include only user-owned skills.
- Clear statement that official/proprietary skills are detected only and should be installed through official channels.
- Update command:

  ```bash
  ./install.sh --target both --force --backup
  ```

- Dry-run command:

  ```bash
  ./install.sh --dry-run --target both
  ```

## Validation Checklist

Before finishing:

- Run `git status --short` and confirm only intended files changed.
- Run the installer in dry-run mode for `both`.
- Run install tests for `codex` and `claude` targets when safe.
- Verify every installed target skill contains `SKILL.md`.
- Verify required bundled folders such as `scripts/`, `references/`, `agents/`, and `assets/` are copied when present.
- Search the repository for restricted content indicators:
  - `license: Proprietary`
  - `Complete terms in LICENSE.txt`
  - `AppSecret`
  - `token=`
  - browser cookies or session URLs
- Confirm proprietary or official skill bodies were not committed to a public repository.
- If pushing to GitHub, confirm the repository visibility before deciding whether restricted content can be committed.

## Do Not

- Do not publish Claude/Codex official or proprietary skill content to a public repository.
- Do not copy `.git/`, `__pycache__/`, `.DS_Store`, temporary outputs, generated reports, or local backups into packaged skills.
- Do not overwrite the user's existing local skills without backup or explicit `--force`.
- Do not install or update Codex/Claude clients unless explicitly requested and the official installation method has been verified.
- Do not store secrets, tokens, backend URLs, or credentials in manifests, README files, logs, or installer scripts.
