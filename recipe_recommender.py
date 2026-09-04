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
favourites = []

# ---------------- RECOMMEND RECIPES ----------------
def recommend_recipes(ingredients, diet):
    results = []
    for recipe in recipes:
        if diet != "Any" and recipe.get("diet") != diet:
            continue

        recipe_ingredients = [i.lower() for i in recipe["ingredients"]]
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

    ingredients = [i.strip() for i in user_input.split(",")]
    diet = diet_var.get()
    found = recommend_recipes(ingredients, diet)

    if not found:
        listbox_results.insert(tk.END, "No recipes found")
    else:
        for percentage, recipe in found:
            listbox_results.insert(
                tk.END, f"{recipe['name']} ({int(percentage)}% match)"
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

            for ing in recipe["ingredients"]:
                details_text.insert(tk.END, "- " + ing + "\n")

            details_text.insert(tk.END, "\nMethod:\n")
            details_text.insert(tk.END, recipe["method"])

# ---------------- ADD TO FAVOURITES ----------------
def add_to_favourites():
    selection = listbox_results.curselection()
    if not selection:
        return

    selected_text = listbox_results.get(selection[0])
    recipe_name = selected_text.split(" (")[0]

    if recipe_name not in favourites:
        favourites.append(recipe_name)
        listbox_favourites.insert(tk.END, recipe_name)

# ---------------- GENERATE SHOPPING LIST ----------------
def generate_shopping_list():
    details_text.delete("1.0", tk.END)

    if not favourites:
        details_text.insert(tk.END, "No favourite recipes selected.")
        return

    user_input = entry_ingredients.get().strip().lower()
    user_ingredients = [i.strip() for i in user_input.split(",")]
    missing_items = []

    for recipe in recipes:
        if recipe["name"] in favourites:
            for ing in recipe["ingredients"]:
                if ing.lower() not in user_ingredients:
                    if ing not in missing_items:
                        missing_items.append(ing)

    if missing_items:
        details_text.insert(tk.END, "Shopping List:\n\n")
        for item in missing_items:
            details_text.insert(tk.END, "- " + item + "\n")
    else:
        details_text.insert(tk.END, "You have all required ingredients!")

# ---------------- CLEAR FUNCTION ----------------
def clear_all():
    entry_ingredients.delete(0, tk.END)
    listbox_results.delete(0, tk.END)
    details_text.delete("1.0", tk.END)

# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("Recipe Finder - Prototype 3")

frame_top = tk.Frame(root)
frame_top.pack(pady=5)

tk.Label(frame_top, text="Enter ingredients (comma separated):").pack()
entry_ingredients = tk.Entry(frame_top, width=40)
entry_ingredients.pack(pady=5)

tk.Label(frame_top, text="Dietary preference:").pack()
diet_var = tk.StringVar(value="Any")
tk.OptionMenu(frame_top, diet_var, "Any", "Vegetarian", "Vegan").pack()

tk.Button(frame_top, text="Search", command=search).pack(pady=3)
tk.Button(frame_top, text="Clear", command=clear_all).pack(pady=3)

frame_middle = tk.Frame(root)
frame_middle.pack()

listbox_results = tk.Listbox(frame_middle, width=50, height=8)
listbox_results.pack(side="left", padx=5)
listbox_results.bind("<<ListboxSelect>>", show_details)

listbox_favourites = tk.Listbox(frame_middle, width=25, height=8)
listbox_favourites.pack(side="right", padx=5)

frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=5)

tk.Button(frame_bottom, text="Add to Favourites", command=add_to_favourites).pack(pady=3)
tk.Button(frame_bottom, text="Generate Shopping List", command=generate_shopping_list).pack(pady=3)

details_text = tk.Text(root, width=60, height=10, wrap="word")
details_text.pack(pady=5)

root.mainloop()
