# scripts/terraform_summary.py

import re

def extract_resources(plan_text: str, keyword: str) -> list:
    pattern = rf'^# (.+?) {keyword}'
    return re.findall(pattern, plan_text, flags=re.MULTILINE)

def summarize_plan(plan_text: str) -> str:
    sections = []

    actions = [
        ("🟢 (+) Resources to add", "will be created"),
        ("🟡 (~) Resources to change", "will be changed"),
        ("🔴 (-) Resources to destroy", "will be destroyed"),
        ("🔄 (-/+) Resources to replace (delete before create)", "must be replaced"),
        ("♻️ (+/-) Resources to recreate (delete after create)", "will be recreated"),
    ]

    for label, keyword in actions:
        resources = extract_resources(plan_text, keyword)
        if resources:
            sections.append(f"{label}: {len(resources)}\n" +
                            "\n".join([f"   {i+1}. {r}" for i, r in enumerate(resources)]))

    return "## Terraform Plan Summary\n" + "\n\n".join(sections)

def main():
    with open("plan.txt", "r") as f:
        plan_text = f.read()

    summary = summarize_plan(plan_text)
    print(summary)

    body = (
        summary
        + "\n\n<details>\n<summary>Full Terraform Plan</summary>\n\n"
        + "```\n"
        + plan_text
        + "\n```\n</details>\n"
    )

    with open("issue_body.md", "w") as f:
        f.write(body)

if __name__ == "__main__":
    main()
