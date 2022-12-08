import json

def main(framework_name):
    clouds = ["AZURE", "AWS", "GCP"]
    for cloud in clouds:
        data = json.load(open(f"{cloud}_CSPM/{framework_name}.json", "r"))
        res = {}
        for row in data["data"]:
            for subrow in row["tests"]:
                if row["name"] not in res:
                    res[row["name"]] = [subrow["title"]]
                else:
                    res[row["name"]].append(subrow["title"])
        json.dump(res, open(f"CONTROL_MAPPINGS/{cloud}_{framework_name}.json", "w"), indent=4)

if __name__ == "__main__":
    main("SOC 2 Type II")
    main("PCI")
