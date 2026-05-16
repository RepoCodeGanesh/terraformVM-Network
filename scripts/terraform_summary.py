# scripts/terraform_summary.py

def summarize_plan(plan_text: str) -> str:
    """
    Counts resources to add/change/destroy by scanning plan.txt.
    """
    add_count = plan_text.count("will be created")
    change_count = plan_text.count("will be changed")
    destroy_count = plan_text.count("will be destroyed")

    summary = (
        f"## Terraform Plan Summary\n"
        f"🟢 Resources to add: {add_count}\n"
        f"🟡 Resources to change: {change_count}\n"
        f"🔴 Resources to destroy: {destroy_count}\n"
    )
    return summary


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
