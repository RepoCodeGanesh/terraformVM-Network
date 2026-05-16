# scripts/terraform_summary.py

import re

def extract_resources(plan_text: str, keyword: str) -> list:
    """
    Find resource names associated with a given keyword in plan.txt.
    Example keywords: 'will be created', 'will be changed', 'will be destroyed'
    """
    pattern = rf'resource\s+"([^"]+)"\s+"([^"]+)"\s+{{.*{keyword}'
    matches = re.findall(pattern, plan_text)
    return [f"{m[0]}.{m[1]}" for m in matches]

def summarize_plan(plan_text: str) -> str:
    """
    Build summary with emojis and resource lists.
    Only include categories with non-zero counts.
    """
    sections = []

    # Add
    add_resources = extract_resources(plan_text, "will be created")
    if add_resources:
        sections.append("🟢 (+) Resources to add: {}\n{}".format(
            len(add_resources),
            "\n".join([f"   {i+1}. {r}" for i, r in enumerate(add_resources)])
        ))

    # Change
    change_resources = extract_resources(plan_text, "will be changed")
    if change_resources:
        sections.append("🟡 (~) Resources to change: {}\n{}".format(
            len(change_resources),
            "\n".join([f"   {i+1}. {r}" for i, r in enumerate(change_resources)])
        ))

    # Destroy
    destroy_resources = extract_resources(plan_text, "will be destroyed")
    if destroy_resources:
        sections.append("🔴 (-) Resources to destroy: {}\n{}".format(
            len(destroy_resources),
            "\n".join([f"   {i+1}. {r}" for i, r in enumerate(destroy_resources)])
        ))

    # Replace (-/+)
    replace_count = plan_text.count("-/+")
    if replace_count > 0:
        sections.append(f"🔄 (-/+) Resources to replace (delete before create): {replace_count}")

    # Recreate (+/-)
    recreate_count = plan_text.count("+/-")
    if recreate_count > 0:
        sections.append(f"♻️ (+/-) Resources to recreate (delete after create): {recreate_count}")

    return "## Terraform Plan Summary\n" + "\n\n".join(sections)


def main():
    with open("plan.txt", "r") as f:
        plan_text = f.read()

    summary = summarize_plan(plan_text)

    # Print summary to pipeline logs
    print(summary)

    # Build Markdown body for GitHub issue
    body = (
        summary
        + "\n\n<details>\n<summary>Full Terraform Plan</summary>\n\n"
        + "```\n"
        + plan_text
        + "\n```\n</details>\n"
    )

    # Save to file for gh issue create
    with open("issue_body.md", "w") as f:
        f.write(body)


if __name__ == "__main__":
    main()
