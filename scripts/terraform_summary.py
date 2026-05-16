import json

with open("plan.json") as f:
    plan = json.load(f)

colors = {
    "+": "\033[92m",     # green → create
    "-": "\033[91m",     # red → destroy
    "~": "\033[93m",     # yellow → update/modify
    "-/+": "\033[91m",   # red → replace (delete then create)
    "+/-": "\033[91m",   # red → create then destroy
    "<=": "\033[94m",    # blue → read (data source)
    "end": "\033[0m"
}

actions = {s: [] for s in ["+","-","~","-/+","+/-","<="]}

for res in plan["resource_changes"]:
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

for symbol, resources in actions.items():
    if resources:
        print(f"{colors[symbol]}{symbol}{colors['end']}")
        for r in resources:
            print(f"  {r}")
        print()
