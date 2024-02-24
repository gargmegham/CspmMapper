import json
import os

def process_framework(cloud, framework_name):
    source_file = os.path.join(f"{cloud}_CSPM", f"{framework_name}.json")
    target_file = os.path.join("CONTROL_MAPPINGS", f"{cloud}_{framework_name}.json")
    
    with open(source_file, "r") as source:
        data = json.load(source)
        res = {}
        for row in data["data"]:
            for subrow in row["tests"]:
                res.setdefault(row["name"], []).append(subrow["title"])

    with open(target_file, "w") as target:
        json.dump(res, target, indent=4)

def main(framework_name):
    clouds = ["AZURE", "AWS", "GCP"]
    for cloud in clouds:
        process_framework(cloud, framework_name)

if __name__ == "__main__":
    main("SOC 2 Type II")
    main("PCI")
