#!/usr/bin/env python3
"""
AI-assisted CV tailoring for the ai-resume template.

Reads cv.yaml + a target job description, asks an LLM to rewrite the
`highlights` of each experience entry to be more relevant to that role,
and writes cv.tailored.yaml for human review.

Supports OpenAI, Anthropic (Claude), Google Gemini, and any OpenAI-compatible
endpoint (Ollama, Groq, Together, DeepSeek, ...). Choose with AI_PROVIDER.

OPTIONAL + LOCAL. Nothing leaves your machine unless you provide an API key.
Review the output before using it anywhere.
"""
import argparse
import os
import yaml

SYSTEM_PROMPT = (
    "You are an expert resume editor. Rewrite bullet-point achievements so they "
    "are maximally relevant to a given job description, WITHOUT inventing facts. "
    "Keep the candidate's real numbers and scope. Output ONLY a YAML list of "
    "strings, one per highlight, preserving order. Be concise."
)


def load_cv(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


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
                        base_url=os.environ.get("OPENAI_BASE_URL"))  # None -> OpenAI default
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
    ap.add_argument("--provider", default=os.environ.get("AI_PROVIDER", "openai"))
    args = ap.parse_args()

    defaults = {
        "openai": ("OPENAI_API_KEY", "gpt-4o-mini"),
        "anthropic": ("ANTHROPIC_API_KEY", "claude-3-5-sonnet-latest"),
        "gemini": ("GEMINI_API_KEY", "gemini-1.5-flash"),
    }
    if args.provider not in defaults:
        sys.exit(f"AI_PROVIDER must be one of: {', '.join(defaults)}")
    key_var, default_model = defaults[args.provider]
    if not os.environ.get(key_var):
        sys.exit(f"Set the {key_var} environment variable first.")

    model = os.environ.get(f"{args.provider.upper()}_MODEL", default_model)

    cv = load_cv(args.cv)
    jd = open(args.jd, encoding="utf-8").read()
    for section, name, entry in collect(cv):
        print(f"Tailoring: {name} ({section}) [{args.provider}/{model}]")
        entry["highlights"] = tailor(entry["highlights"], jd, args.provider, model)
    with open(args.out, "w", encoding="utf-8") as f:
        yaml.safe_dump(cv, f, sort_keys=False, allow_unicode=True)
    print(f"Wrote {args.out} — review it, then: rendercv render {args.out}")


if __name__ == "__main__":
    main()
