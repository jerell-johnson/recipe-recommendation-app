import tkinter as tk
import json


# ---------------- LOAD RECIPES ----------------
def load_recipes():
    try:
        with open("rec2.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


recipes = load_recipes()


# ---------------- RECOMMEND RECIPES ----------------
def recommend_recipes(ingredients, diet):
    results = []

    for recipe in recipes:
        if diet != "Any" and recipe.get("diet") != diet:
            continue

        recipe_ingredients = [ingredient.lower() for ingredient in recipe["ingredients"]]
        matches = 0

        for item in ingredients:
            if item in recipe_ingredients:
                matches += 1

        if matches > 0:
            percentage = (matches / len(recipe_ingredients)) * 100
            results.append((percentage, recipe))

    results.sort(key=lambda x: x[0], reverse=True)
    return results


# ---------------- SEARCH FUNCTION ----------------
def search():
    listbox_results.delete(0, tk.END)
    details_text.delete("1.0", tk.END)

    user_input = entry_ingredients.get().strip().lower()

    if user_input == "":
        listbox_results.insert(tk.END, "Please enter ingredients")
        return

    ingredients = [item.strip() for item in user_input.split(",")]
    diet = diet_var.get()
    found = recommend_recipes(ingredients, diet)

    if not found:
        listbox_results.insert(tk.END, "No recipes found")
    else:
        for percentage, recipe in found:
            listbox_results.insert(
                tk.END,
                f"{recipe['name']} ({int(percentage)}% match)"
            )


# ---------------- SHOW DETAILS ----------------
def show_details(event):
    selection = listbox_results.curselection()

    if not selection:
        return

    selected_text = listbox_results.get(selection[0])
    recipe_name = selected_text.split(" (")[0]

    for recipe in recipes:
        if recipe["name"] == recipe_name:
            details_text.delete("1.0", tk.END)
            details_text.insert(tk.END, recipe["name"] + "\n\n")
            details_text.insert(tk.END, "Ingredients:\n")

            for ingredient in recipe["ingredients"]:
                details_text.insert(tk.END, "- " + ingredient + "\n")

            details_text.insert(tk.END, "\nMethod:\n")
            details_text.insert(tk.END, recipe["method"])
            break


# ---------------- CLEAR FUNCTION ----------------
def clear_all():
    entry_ingredients.delete(0, tk.END)
    listbox_results.delete(0, tk.END)
    details_text.delete("1.0", tk.END)


# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("Recipe Finder - Prototype 2")
root.geometry("700x500")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Enter ingredients (comma separated):").pack()
entry_ingredients = tk.Entry(frame_top, width=40)
entry_ingredients.pack(pady=5)

tk.Label(frame_top, text="Dietary preference:").pack()
diet_var = tk.StringVar(value="Any")
tk.OptionMenu(frame_top, diet_var, "Any", "Vegetarian", "Vegan").pack(pady=5)

tk.Button(frame_top, text="Search", command=search).pack(pady=3)
tk.Button(frame_top, text="Clear", command=clear_all).pack(pady=3)

frame_middle = tk.Frame(root)
frame_middle.pack(pady=10)

listbox_results = tk.Listbox(frame_middle, width=50, height=10)
listbox_results.pack(side="left", padx=10)
listbox_results.bind("<<ListboxSelect>>", show_details)

details_text = tk.Text(root, width=70, height=12, wrap="word")
details_text.pack(pady=10)

root.mainloop()
