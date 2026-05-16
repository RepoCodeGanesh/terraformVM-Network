# scripts/terraform_summary.py

def summarize_plan(plan_text: str) -> str:
    """
    Very basic summary: counts resources to add/change/destroy
    by scanning the human-readable plan.txt.
    """
    add_count = plan_text.count("will be created")
    change_count = plan_text.count("will be changed")
    destroy_count = plan_text.count("will be destroyed")

    summary = (
        f"Terraform Plan Summary:\n"
        f"- Resources to add: {add_count}\n"
        f"- Resources to change: {change_count}\n"
        f"- Resources to destroy: {destroy_count}\n"
    )
    return summary


def main():
    with open("plan.txt", "r") as f:
        plan_text = f.read()

    summary = summarize_plan(plan_text)
    print(summary)


if __name__ == "__main__":
    main()
