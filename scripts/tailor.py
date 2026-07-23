#!/usr/bin/env python3
"""
AI-assisted CV tailoring for the ai-resume template.

Reads cv.yaml + a target job description, asks an LLM to rewrite the
`highlights` of each experience entry to be more relevant to that role,
and writes cv.tailored.yaml for human review.

Supports OpenAI, Anthropic (Claude), Google Gemini, and any OpenAI-compatible
endpoint (Ollama, Groq, Together, DeepSeek, ...). The provider is auto-detected
from whichever API key is set (OPENAI_API_KEY / ANTHROPIC_API_KEY / GEMINI_API_KEY),
or forced with the AI_PROVIDER env var / --provider flag.

OPTIONAL + LOCAL. Nothing leaves your machine unless you provide an API key.
Review the output before using it anywhere.

Note: YAML I/O uses ruamel.yaml, which RenderCV installs automatically, so no
separate PyYAML install is required.
"""
import argparse
import os
import sys

try:
    from ruamel.yaml import YAML
    _ryaml = YAML()
    _ryaml.preserve_quotes = True
    _ryaml.indent(mapping=2, sequence=4, offset=2)
    _HAS_RUAMEL = True
except ImportError:
    import yaml as _pyyaml
    _HAS_RUAMEL = False


SYSTEM_PROMPT = (
    "You are an expert resume editor. Rewrite bullet-point achievements so they "
    "are maximally relevant to a given job description, WITHOUT inventing facts. "
    "Keep the candidate's real numbers and scope. Output ONLY a YAML list of "
    "strings, one per highlight, preserving order. Be concise."
)

# provider -> (env var holding the key, default model)
PROVIDERS = {
    "openai": ("OPENAI_API_KEY", "gpt-4o-mini"),
    "anthropic": ("ANTHROPIC_API_KEY", "claude-3-5-sonnet-latest"),
    "gemini": ("GEMINI_API_KEY", "gemini-1.5-flash"),
}


def detect_provider():
    for name, (key_var, _) in PROVIDERS.items():
        if os.environ.get(key_var):
            return name
    return None


def load_cv(path):
    with open(path, encoding="utf-8") as f:
        if _HAS_RUAMEL:
            return _ryaml.load(f)
        return _pyyaml.safe_load(f)


def save_cv(data, path):
    with open(path, "w", encoding="utf-8") as f:
        if _HAS_RUAMEL:
            _ryaml.dump(data, f)
        else:
            _pyyaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def collect(cv):
    out = []
    for section, entries in cv.get("sections", {}).items():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if isinstance(entry, dict) and "highlights" in entry:
                out.append((section, entry.get("company") or entry.get("institution"), entry))
    return out


def parse_bullets(text, fallback):
    new = [line.lstrip("- ").strip() for line in text.splitlines() if line.strip().startswith("- ")]
    return new or fallback


def tailor(highlights, jd, provider, model):
    user = f"JOB DESCRIPTION:\n{jd}\n\nCURRENT BULLETS:\n" + "\n".join(f"- {h}" for h in highlights)

    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"],
                        base_url=os.environ.get("OPENAI_BASE_URL"))
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT},
                      {"role": "user", "content": user}],
            temperature=0.2,
        )
        return parse_bullets(resp.choices[0].message.content, highlights)

    if provider == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        resp = client.messages.create(
            model=model,
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user}],
        )
        return parse_bullets(resp.content[0].text, highlights)

    if provider == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model_obj = genai.GenerativeModel(model, system_instruction=SYSTEM_PROMPT)
        resp = model_obj.generate_content(user, generation_config={"temperature": 0.2})
        return parse_bullets(resp.text, highlights)

    raise SystemExit(f"Unknown AI_PROVIDER: {provider}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cv", default="cv.yaml")
    ap.add_argument("--jd", required=True, help="Job description .txt/.md")
    ap.add_argument("--out", default="cv.tailored.yaml")
    ap.add_argument("--provider", default=os.environ.get("AI_PROVIDER") or None,
                    help="openai | anthropic | gemini (auto-detected if omitted)")
    args = ap.parse_args()

    # Use the requested provider only if its key is present; else auto-detect.
    requested = args.provider
    provider = None
    if requested and requested in PROVIDERS and os.environ.get(PROVIDERS[requested][0]):
        provider = requested
    else:
        provider = detect_provider()

    if provider is None:
        sys.exit("No LLM API key found. Set one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, "
                 "GEMINI_API_KEY (optionally also set AI_PROVIDER to force a choice).")

    key_var, default_model = PROVIDERS[provider]
    model = os.environ.get(f"{provider.upper()}_MODEL", default_model)

    cv = load_cv(args.cv)
    jd = open(args.jd, encoding="utf-8").read()
    for section, name, entry in collect(cv):
        print(f"Tailoring: {name} ({section}) [{provider}/{model}]")
        entry["highlights"] = tailor(entry["highlights"], jd, provider, model)
    save_cv(cv, args.out)
    print(f"Wrote {args.out} — review it, then: rendercv render {args.out}")


if __name__ == "__main__":
    main()
