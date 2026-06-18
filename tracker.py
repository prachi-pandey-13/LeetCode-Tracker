import json
import os

def push_to_github():
    os.system("git add .")
    os.system('git commit -m "Auto update leetcode tracker"')
    os.system("git push")

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "categories": {},
            "dates_logged": [],
            "streak": 0,
            "last_logged": None
        }
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
from datetime import date

def log_problem(data):
    print("\n--- Log Today's Practice ---")
    category = input("Category (Maths/arrays/strings/trees/dp/graphs): ").strip().lower()
    difficulty = input("Difficulty (easy/medium/hard): ").strip().lower()
    count = int(input("How many problems solved: ").strip())

    # hashing: update category count
    if category not in data["categories"]:
        data["categories"][category] = {"easy": 0, "medium": 0, "hard": 0, "total": 0}

    data["categories"][category][difficulty] += count
    data["categories"][category]["total"] += count

    # streak logic
    today = str(date.today())
    if today not in data["dates_logged"]:
        data["dates_logged"].append(today)

    if data["last_logged"] == str(date.today()):
        print(f"\n✅ Updated! Total {category} solved: {data['categories'][category]['total']}")
    else:
        data["streak"] += 1
        data["last_logged"] = today
        print(f"\n✅ Logged! 🔥 Streak is now {data['streak']} days")

    save_data(data)
def show_stats(data):
    categories = data["categories"]
    
    if not categories:
        print("\nNo data yet. Start logging with: python tracker.py log")
        return

    # sort by total solved — practice sorting a dict
    sorted_cats = sorted(categories.items(), key=lambda x: x[1]["total"], reverse=True)
    
    # find weak areas — total solved less than 5
    total_all = sum(v["total"] for v in categories.values())
    weak_threshold = 5

    print("\n📊 Your LeetCode Stats:")
    print("-" * 40)
    for cat, counts in sorted_cats:
        weak = "  ⚠  weak area" if counts["total"] < weak_threshold else ""
        print(f"  {cat:<12} → {counts['total']} problems  "
              f"(E:{counts['easy']} M:{counts['medium']} H:{counts['hard']}){weak}")
    
    print("-" * 40)
    print(f"  Total solved : {total_all}")
    print(f"  🔥 Streak    : {data['streak']} days")
    print(f"  Days active  : {len(data['dates_logged'])}")
def reset_data():
    confirm = input("Are you sure you want to reset all data? (yes/no): ")
    if confirm.lower() == "yes":
        os.remove(DATA_FILE)
        print("✅ Data reset.")
    else:
        print("Cancelled.")

import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python tracker.py [log | stats | reset]")
        return

    command = sys.argv[1].lower()
    data = load_data()

    if command == "log":
        log_problem(data)
        push_to_github()
    elif command == "stats":
        show_stats(data)
    elif command == "reset":
        reset_data()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()