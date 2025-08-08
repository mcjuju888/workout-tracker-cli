import json
from datetime import date
from collections import defaultdict
import matplotlib.pyplot as plt

WORKOUT_FILE = "workouts.json"

def load_workouts():
    try:
        with open(WORKOUT_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_workouts(workouts):
    with open(WORKOUT_FILE, "w") as file:
        json.dump(workouts, file, indent=4)

def add_workout():
    today = date.today().isoformat()
    exercise = input("Enter exercise name: ")
    sets = int(input("Enter number of sets: "))
    reps = int(input("Enter number of reps: "))
    weight = float(input("Enter weight used (lbs): "))
    notes = input("Any notes? (press Enter to skip): ")

    workout = {
        "date": today,
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
        "weight": weight,
        "notes": notes
    }

    workouts = load_workouts()
    workouts.append(workout)
    save_workouts(workouts)
    print(f"Workout for {exercise} saved successfully!")

def view_workouts():
    workouts = load_workouts()
    if not workouts:
        print("No workouts found.")
        return

    for i, w in enumerate(workouts, start=1):
        volume = w['sets'] * w['reps'] * w['weight']
        print(f"{i}. {w['date']} - {w['exercise']} | {w['sets']}x{w['reps']} @ {w['weight']} lbs "
              f"(Volume: {volume} lbs) | Notes: {w['notes']}")

def search_by_date():
    search_date = input("Enter date (YYYY-MM-DD): ")
    workouts = load_workouts()
    results = [w for w in workouts if w["date"] == search_date]
    if results:
        for w in results:
            volume = w['sets'] * w['reps'] * w['weight']
            print(f"{w['date']} - {w['exercise']} | {w['sets']}x{w['reps']} @ {w['weight']} lbs "
                  f"(Volume: {volume} lbs) | Notes: {w['notes']}")
    else:
        print("No workouts found for that date.")

def search_by_exercise():
    search_term = input("Enter exercise name: ").lower()
    workouts = load_workouts()
    results = [w for w in workouts if search_term in w["exercise"].lower()]
    if results:
        for w in results:
            volume = w['sets'] * w['reps'] * w['weight']
            print(f"{w['date']} - {w['exercise']} | {w['sets']}x{w['reps']} @ {w['weight']} lbs "
                  f"(Volume: {volume} lbs) | Notes: {w['notes']}")
    else:
        print("No workouts found for that exercise.")

def delete_workout():
    view_workouts()
    workouts = load_workouts()
    try:
        choice = int(input("Enter the number of the workout to delete: ")) - 1
        if 0 <= choice < len(workouts):
            removed = workouts.pop(choice)
            save_workouts(workouts)
            print(f"Deleted: {removed['date']} - {removed['exercise']}")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")

def edit_workout():
    view_workouts()
    workouts = load_workouts()
    try:
        choice = int(input("Enter the number of the workout to edit: ")) - 1
        if 0 <= choice < len(workouts):
            workout = workouts[choice]
            print("Press Enter to keep the current value.")
            workout["exercise"] = input(f"Exercise ({workout['exercise']}): ") or workout["exercise"]
            workout["sets"] = int(input(f"Sets ({workout['sets']}): ") or workout["sets"])
            workout["reps"] = int(input(f"Reps ({workout['reps']}): ") or workout["reps"])
            workout["weight"] = float(input(f"Weight ({workout['weight']}): ") or workout["weight"])
            workout["notes"] = input(f"Notes ({workout['notes']}): ") or workout["notes"]

            workouts[choice] = workout
            save_workouts(workouts)
            print("Workout updated successfully!")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")

def show_personal_bests():
    workouts = load_workouts()
    if not workouts:
        print("No workouts found.")
        return

    pr_dict = defaultdict(float)
    for w in workouts:
        if w['weight'] > pr_dict[w['exercise']]:
            pr_dict[w['exercise']] = w['weight']

    print("\n🏆 Personal Bests:")
    for exercise, weight in pr_dict.items():
        print(f"{exercise}: {weight} lbs")

def show_total_volume():
    workouts = load_workouts()
    if not workouts:
        print("No workouts found.")
        return

    total_volume = sum(w['sets'] * w['reps'] * w['weight'] for w in workouts)
    print(f"\n📊 Total Training Volume: {total_volume} lbs")

def show_progress_graph():
    search_term = input("Enter exercise name for progress graph: ").lower()
    workouts = load_workouts()

    # Filter only matching exercise logs
    filtered = [w for w in workouts if search_term in w["exercise"].lower()]
    if not filtered:
        print("No workouts found for that exercise.")
        return

    # Sort by date for chronological plotting
    filtered.sort(key=lambda x: x["date"])

    dates = [w["date"] for w in filtered]
    weights = [w["weight"] for w in filtered]

    plt.plot(dates, weights, marker="o")
    plt.title(f"Progress for {filtered[0]['exercise']}")
    plt.xlabel("Date")
    plt.ylabel("Weight (lbs)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    while True:
        print("\n🏋️ Workout Tracker")
        print("1. Add Workout")
        print("2. View Workouts")
        print("3. Search by Date")
        print("4. Search by Exercise")
        print("5. Edit Workout")
        print("6. Delete Workout")
        print("7. Show Personal Bests")
        print("8. Show Total Volume")
        print("9. Show Progress Graph")
        print("10. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_workout()
        elif choice == "2":
            view_workouts()
        elif choice == "3":
            search_by_date()
        elif choice == "4":
            search_by_exercise()
        elif choice == "5":
            edit_workout()
        elif choice == "6":
            delete_workout()
        elif choice == "7":
            show_personal_bests()
        elif choice == "8":
            show_total_volume()
        elif choice == "9":
            show_progress_graph()
        elif choice == "10":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
