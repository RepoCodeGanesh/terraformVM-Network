#!/usr/bin/env python3
import json

with open("plan.json") as f:
    plan = json.load(f)

# Emoji markers for each action
markers = {
    "+": "✅ + → Create",
    "-": "❌ - → Destroy",
    "~": "🔄 ~ → Update/Modify",
    "-/+": "♻️ -/+ → Replace (delete then create)",
    "+/-": "⚠️ +/- → Create then Destroy",
    "<=": "📘 <= → Read (data source)"
}

actions = {s: [] for s in markers.keys()}

for res in plan.get("resource_changes", []):
    addr = res["address"]
    acts = res["change"]["actions"]

    if set(acts) == {"create","delete"}:
        actions["-/+"].append(addr)
    elif acts == ["create","delete"]:
        actions["+/-"].append(addr)
    elif acts == ["create"]:
        actions["+"].append(addr)
    elif acts == ["delete"]:
        actions["-"].append(addr)
    elif acts == ["update"]:
        actions["~"].append(addr)
    elif acts == ["read"]:
        actions["<="].append(addr)

# Print summary header
print("Terraform Plan Summary\n")

# Print only relevant groups, with numbering
for symbol, resources in actions.items():
    if resources:
        print(markers[symbol])
        for idx, r in enumerate(resources, start=1):
            print(f"  {idx}. {r}")
        print()
