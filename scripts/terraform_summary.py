# scripts/terraform_summary.py

import re

def extract_resources(plan_text: str, keyword: str) -> list:
    """
    Extract resource identifiers from plan.txt for a given keyword.
    Matches lines like: '# azurerm_resource_group.rg will be created'
    """
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
        if resources:  # only show if non-zero
            sections.append(f"{label}: {len(resources)}\n" +
                            "\n".join([f"   {i+1}. {r}" for i, r in enumerate(resources)]))

    return "## Terraform Plan Summary\n" + "\n\n".join(sections)

def main():
    with open("plan.txt", "r") as f:
        plan_text = f.read()

    summary = summarize_plan(plan_text)
    print(summary)  # pipeline logs

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
