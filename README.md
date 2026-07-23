# ai-resume-generator

> An open-source resume pipeline: a single YAML source of truth → an ATS-friendly PDF,
> rendered automatically by GitHub Actions (RenderCV + LaTeX). CV content is tailored to a
> job description with any LLM using a reusable prompt (see `SKILL.md`).

![Build](https://github.com/Luciifer-byte/ai-resume-generator/actions/workflows/render-cv.yml/badge.svg)
![License](https://img.shields.io/github/license/Luciifer-byte/ai-resume-generator)

![CV preview](https://raw.githubusercontent.com/Luciifer-byte/ai-resume-generator/main/rendercv_output/preview.png)

## How it works

```mermaid
flowchart LR
  A[Edit cv.yaml] --> B[git push]
  B --> C{GitHub Actions}
  C --> D[RenderCV renders PDF + PNG]
  D --> E[Commit to rendercv_output/]
  F[Any LLM + SKILL.md + JD] -->|tailors cv.yaml| A
```

## Features
- YAML-based, version-controlled resume (single source of truth)
- Automatic PDF generation via CI/CD (no local LaTeX needed)
- ATS-friendly, clean LaTeX output
- **AI-assisted tailoring** with any LLM (ChatGPT / Claude / Gemini) using a reusable prompt — no API key, no cost
- Easy theming (colors, fonts, margins)

## Tech Stack
YAML · RenderCV · GitHub Actions · LaTeX · (optional) any LLM for tailoring

## Project Structure
```
cv.yaml                 # your resume data + design
SKILL.md                # reusable LLM prompt for tailoring + cover letter
rendercv_output/        # generated PDF + preview.png (committed)
.github/workflows/      # CI that renders on every push
```

## Quick start (use it as your own)
1. Fork / clone the repo.
2. Edit `cv.yaml` (replace the example data with yours).
3. `pip install "rendercv[full]==2.8"` then `rendercv render cv.yaml` (or just push — CI does it).
4. Push → GitHub Actions regenerates the PDF + preview automatically.

## AI tailoring (optional, free)
You don't need an API key. Use any chat LLM with the prompt in [`SKILL.md`](SKILL.md):

1. Open your LLM and paste the contents of `SKILL.md` as the instructions.
2. Send your `cv.yaml` + the job description you're applying for (see "HOW TO USE THIS SKILL" in `SKILL.md`).
3. The LLM returns a tailored `cv:` block, a cover letter, and a changes table.
4. Paste the `cv:` block back into `cv.yaml` (keep `design:`, `locale:`, `settings:` untouched).
5. Commit → the pipeline renders your tailored PDF.

The AI only rewords existing experience; it never invents facts. Always review before applying.

## License
MIT — see [LICENSE](LICENSE).```

It is **not** part of the automatic GitHub Actions render — you run it on your own
computer only when you want to tailor a resume for a particular application. The AI
only rewords existing experience; it cannot add skills you don't have, so always
review the output before sending it anywhere.

### Supported providers

Set `AI_PROVIDER` to choose a model. Install the matching SDK and set its API key:

| Provider | `AI_PROVIDER` | Install | API key | Default model |
| --- | --- | --- | --- | --- |
| OpenAI | `openai` | `pip install openai` | `OPENAI_API_KEY` | `gpt-4o-mini` |
| Anthropic (Claude) | `anthropic` | `pip install anthropic` | `ANTHROPIC_API_KEY` | `claude-3-5-sonnet-latest` |
| Google Gemini | `gemini` | `pip install google-generativeai` | `GEMINI_API_KEY` | `gemini-1.5-flash` |
| Any OpenAI-compatible (Ollama, Groq, Together, DeepSeek, …) | `openai` + `OPENAI_BASE_URL` | `pip install openai` | `OPENAI_API_KEY` | `gpt-4o-mini` |

Override the model with `<PROVIDER>_MODEL` (e.g. `OPENAI_MODEL=gpt-4o`,
`ANTHROPIC_MODEL=claude-3-5-haiku-latest`).

### Example — OpenAI
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...        # Windows: set OPENAI_API_KEY=sk-...
python scripts/tailor.py --cv cv.yaml --jd job_description.example.txt --out cv.tailored.yaml
rendercv render cv.tailored.yaml    # review the tailored PDF
```

### Example — Anthropic (Claude)
```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/tailor.py --cv cv.yaml --jd job_description.example.txt --provider anthropic --out cv.tailored.yaml
```

### Example — Google Gemini
```bash
pip install google-generativeai
export GEMINI_API_KEY=...
python scripts/tailor.py --cv cv.yaml --jd job_description.example.txt --provider gemini --out cv.tailored.yaml
```

### Example — local Ollama (no API key, runs on your machine)
```bash
ollama pull llama3.1
export OPENAI_BASE_URL=http://localhost:11434/v1
export OPENAI_API_KEY=ollama        # ignored locally, but the SDK requires a value
python scripts/tailor.py --cv cv.yaml --jd job_description.example.txt --out cv.tailored.yaml
```

## License
MIT — see [LICENSE](LICENSE).
