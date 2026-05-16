import re

def extract_resources(plan_text: str, keyword: str) -> list:
    pattern = rf'^\s*# (.+?) {re.escape(keyword)}'
    return re.findall(pattern, plan_text, flags=re.MULTILINE)

def summarize_plan(plan_text: str) -> str:
    sections = []

    actions = [
        ("🟢 Resources to add", "will be created"),
        ("🟡 Resources to change", "will be updated in-place"),
        ("🔴 Resources to destroy", "will be destroyed"),
        ("🔄 Resources to replace", "must be replaced"),
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
        return "## Terraform Plan Summary\n\nNo infrastructure changes detected."

    return "## Terraform Plan Summary\n\n" + "\n\n".join(sections)
