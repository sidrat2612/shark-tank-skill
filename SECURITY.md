# Security

This project is Markdown, JSON, and a small Python validator. It runs no server and stores no secrets. The Shark sub-agents only have the Read, Grep, and Glob tools.

The realistic risks are:

- **Prompt injection through a pitch.** A pitch or a file in your project could contain instructions aimed at the Sharks. The Sharks cannot run commands or edit files, so the worst case is a misleading verdict.
- **A malicious contribution.** For example, an agent file that asks for more tools, or a brain file that carries hidden instructions. Every PR is reviewed for this, and CI checks agent frontmatter.

## Reporting

Please report a vulnerability privately through [GitHub security advisories](https://github.com/sidrat2612/shark-tank-skill/security/advisories/new), not in a public issue. You should hear back within a week.
