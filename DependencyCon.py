import json
import requests
import os
import sys

def check_npm_package_exists(pkg_name):
    resp = requests.get(f"https://registry.npmjs.org/{pkg_name}")
    return resp.status_code == 200

def analyze_package_json(file_path):
    if not os.path.exists(file_path):
        print(f"[!] Error: '{file_path}' not found.")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"[!] Error: '{file_path}' is not valid JSON.")
            return []

    dependencies = data.get("dependencies", {})
    dev_dependencies = data.get("devDependencies", {})
    all_deps = {**dependencies, **dev_dependencies}

    print(f"[*] Found {len(all_deps)} dependencies in '{file_path}'.")
    suspicious = []

    for pkg in all_deps:
        print(f"[-] Checking '{pkg}' on npm registry...")
        if not check_npm_package_exists(pkg):
            print(f"[!] '{pkg}' NOT found on npm – possible internal package")
            suspicious.append(pkg)

    return suspicious

def main():
    if len(sys.argv) != 2:
        print("Usage: python DependencyCon.py /path/to/package.json")
        sys.exit(1)

    pkg_json_path = sys.argv[1]
    print("📦 NPM/PNPM Dependency Confusion Scanner\n")
    potential_vulns = analyze_package_json(pkg_json_path)

    print("\n=== Potential Dependency Confusion Targets ===")
    if potential_vulns:
        for pkg in potential_vulns:
            print(f" - {pkg}")
    else:
        print("✅ No suspicious internal packages found.")

if __name__ == "__main__":
    main()