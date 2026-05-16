# scripts/terraform_summary.py

import re

def extract_resources(plan_text: str, keyword: str) -> list:
    """
    Extract resource identifiers from plan.txt for a given keyword.
    Matches lines like: '# azurerm_resource_group.rg will be created'
    """
    pattern = rf'^# (.+?) {keyword}'
    matches = re.findall(pattern, plan_text, flags=re.MULTILINE)
    return matches

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
    replace_resources = extract_resources(plan_text, "must be replaced")
    if replace_resources:
        sections.append("🔄 (-/+) Resources to replace (delete before create): {}\n{}".format(
            len(replace_resources),
            "\n".join([f"   {i+1}. {r}" for i, r in enumerate(replace_resources)])
        ))

    # Recreate (+/-)
    recreate_resources = extract_resources(plan_text, "will be recreated")
    if recreate_resources:
        sections.append("♻️ (+/-) Resources to recreate (delete after create): {}\n{}".format(
            len(recreate_resources),
            "\n".join([f"   {i+1}. {r}" for i, r in enumerate(recreate_resources)])
        ))

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

    with open("issue_body.md", "w") as f:
        f.write(body)


if __name__ == "__main__":
    main()
