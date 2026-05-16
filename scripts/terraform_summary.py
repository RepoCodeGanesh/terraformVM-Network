import re

def extract_resources(plan_text: str, keyword: str) -> list:
    """
    Extract Terraform resources based on action keywords.
    """
    pattern = rf'^\s*# (.+?) {re.escape(keyword)}'
    return re.findall(pattern, plan_text, flags=re.MULTILINE)

def summarize_plan(plan_text: str) -> str:
    sections = []

    actions = [
        ("🟢 Resources to Add", "will be created"),
        ("🟡 Resources to Change", "will be updated in-place"),
        ("🔴 Resources to Destroy", "will be destroyed"),
        ("🔄 Resources to Replace", "must be replaced"),
    ]

    for label, keyword in actions:
        resources = extract_resources(plan_text, keyword)

        if resources:
            section = (
                f"### {label}\n\n"
                "| # | Resource |\n"
                "|---|----------|\n" +
                "\n".join(
                    [f"| {i+1} | `{r}` |" for i, r in enumerate(resources)]
                )
            )

            sections.append(section)

    if not sections:
        sections.append("✅ No infrastructure changes detected.")

    return "## Terraform Plan Summary\n\n" + "\n\n".join(sections)

def main():
    with open("plan.txt", "r") as f:
        plan_text = f.read()

    summary = summarize_plan(plan_text)

    print(summary)

    body = (
        summary
        + "\n\n<details>\n"
        + "<summary>📄 Full Terraform Plan</summary>\n\n"
        + "```terraform\n"
        + plan_text
        + "\n```\n"
        + "</details>\n"
    )

    with open("issue_body.md", "w") as f:
        f.write(body)

if __name__ == "__main__":
    main()
