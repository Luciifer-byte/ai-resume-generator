# Contributing

## Why I built this

I was applying to 40+ working student and internship roles in German
companies at the same time, and rewriting my CV by hand for every job description
was slowing me down and introducing copy-paste mistakes. I wanted one YAML file as
the single source of truth, a CI pipeline that renders it into a clean ATS-friendly
PDF automatically, and a repeatable AI prompt that could tailor the content per JD
without ever inventing experience I don't have. This repo is that pipeline, cleaned
up so anyone can fork it and use it for their own search.

## How to contribute

Issues and PRs are welcome, especially for:

- Additional RenderCV themes/templates
- Improvements to the `SKILL.md` tailoring prompt (better JD parsing, sharper
  cover letter tone, more accurate changes-table output)
- Bug fixes in the GitHub Actions workflow
- Documentation and example improvements

### Before opening a PR

1. Fork the repo and create a branch off `main`.
2. Keep `cv.yaml`'s `design:`, `locale:`, and `settings:` blocks untouched in any
   example changes — only the `cv:` block should reflect tailoring logic changes.
3. Test that `rendercv render cv.yaml` still produces a valid PDF locally before
   submitting.
4. Describe what changed and why in the PR description.

### Reporting issues

Open a GitHub issue with:
- What you expected to happen
- What actually happened
- Your `cv.yaml` structure (redact personal info) if the render failed
