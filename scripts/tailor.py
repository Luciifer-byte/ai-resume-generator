#!/usr/bin/env python3
"""
AI-assisted CV tailoring for the ai-resume template.

Reads cv.yaml + a target job description, asks an LLM to rewrite the
`highlights` of each experience entry to be more relevant to that role,
and writes cv.tailored.yaml for human review.

OPTIONAL + LOCAL. Nothing leaves your machine unless you provide an API key.
Review the output before using it anywhere.
"""
import argparse, os, sys, yaml

try:
    from openai import OpenAI
except ImportError:
    sys.exit("Install the SDK first: pip install openai")

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

def tailor(highlights, jd, model):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    user = f"JOB DESCRIPTION:\n{jd}\n\nCURRENT BULLETS:\n" + "\n".join(f"- {h}" for h in highlights)
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": user}],
        temperature=0.2,
    )
    text = resp.choices[0].message.content
    new = [l.lstrip("- ").strip() for l in text.splitlines() if l.strip().startswith("- ")]
    return new or highlights

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cv", default="cv.yaml")
    ap.add_argument("--jd", required=True, help="Job description .txt/.md")
    ap.add_argument("--out", default="cv.tailored.yaml")
    ap.add_argument("--model", default=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"))
    args = ap.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("Set OPENAI_API_KEY first.")

    cv = load_cv(args.cv)
    jd = open(args.jd, encoding="utf-8").read()
    for section, name, entry in collect(cv):
        print(f"Tailoring: {name} ({section})")
        entry["highlights"] = tailor(entry["highlights"], jd, args.model)
    with open(args.out, "w", encoding="utf-8") as f:
        yaml.safe_dump(cv, f, sort_keys=False, allow_unicode=True)
    print(f"Wrote {args.out} — review it, then: rendercv render {args.out}")

if __name__ == "__main__":
    main()
