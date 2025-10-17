
# ==========================================================
#  ULTIMATE PATTERN PROJECT - FULLY FEATURED PATTERN GENERATOR
#  Features : Quick Preview, Interactive Creation, Preview Before Saving,
#            Replay Single/Multiple Patterns, Clear Saved Patterns, Search Saved Pattern
#  Author : Mayank Baranwal
# ==========================================================
# python Ultimate_Pattern_Collector.py
# Description : A comprehensive pattern generator with interactive and quick preview modes.
# ==========================================================


# ---------- BASIC PATTERN FUNCTIONS ----------
def right_triangle(rows, symbol): return [symbol * i for i in range(1, rows + 1)]
def inverted_triangle(rows, symbol): return [symbol * i for i in range(rows, 0, -1)]
def pyramid(rows, symbol): return [" " * (rows - i) + symbol * (2 * i - 1) for i in range(1, rows + 1)]
def diamond(rows, symbol):
    lines = [" " * (rows - i) + symbol * (2 * i - 1) for i in range(1, rows + 1)]
    lines += [" " * (rows - i) + symbol * (2 * i - 1) for i in range(rows - 1, 0, -1)]
    return lines
def hollow_pyramid(rows, symbol):
    lines = []
    for i in range(1, rows + 1):
        if i == rows: lines.append(symbol * (2 * rows - 1))
        else: lines.append(" " * (rows - i) + symbol + " " * (2 * i - 3) + (symbol if i > 1 else ""))
    return lines
def number_pattern(rows): return [" ".join(str(j) for j in range(1, i + 1)) for i in range(1, rows + 1)]
def alphabet_pattern(rows): return [" ".join(chr(65 + j) for j in range(i)) for i in range(1, rows + 1)]
def zigzag(rows, symbol): return ["".join(symbol if (i + j) % 2 == 0 else " " for j in range(rows)) for i in range(1, rows + 1)]
def arrow(rows, symbol):
    lines = [" " * (rows - i) + symbol * (2 * i - 1) for i in range(1, rows + 1)]
    lines += [" " * (rows - i) + symbol * (2 * i - 1) for i in range(rows - 1, 0, -1)]
    return lines
def diagonal(rows, symbol, direction="\\"): return [" " * i + symbol for i in range(rows)] if direction == "\\" else [" " * (rows - i - 1) + symbol for i in range(rows)]


# ---------- FILE FUNCTIONS ----------
def save_pattern(name, lines):
    with open("saved_patterns.txt", "a") as f:
        f.write(f"\n--- {name} ---\n")
        for line in lines: f.write(line + "\n")
    print(f"\n✅ Pattern '{name}' saved successfully!\n")

def clear_saved_patterns():
    open("saved_patterns.txt", "w").close()
    print("\n🗑️ All saved patterns cleared.\n")


# ---------- REPLAY FUNCTIONS ----------
def replay_single_pattern():
    try:
        with open("saved_patterns.txt", "r") as f:
            lines = f.readlines()
            if not lines: print("\nNo saved patterns found.\n"); return
    except FileNotFoundError:
        print("\nNo saved patterns found.\n")
        return

    pattern_names = [line.replace("-", "").strip() for line in lines if line.startswith("---")]
    if not pattern_names:
        print("\nNo saved patterns found.\n"); return

    print("\nSaved Patterns:")
    for i, name in enumerate(pattern_names, 1): print(f"{i}. {name}")

    try:
        choice_index = int(input("\nEnter the number of the pattern to replay: ")) - 1
        if choice_index < 0 or choice_index >= len(pattern_names): print("Invalid choice."); return
    except ValueError:
        print("Invalid input."); return

    selected_name = pattern_names[choice_index]
    replay_pattern_by_name(selected_name)

def replay_pattern_by_name(selected_name):
    new_symbol = input("Enter a symbol to override (leave empty for original): ")
    try: new_rows = int(input("Enter new number of rows (leave empty for original): "))
    except ValueError: new_rows = None

    # Mapping saved pattern names to functions
    pattern_functions = {
        "Right Triangle": right_triangle,
        "Inverted Triangle": inverted_triangle,
        "Pyramid": pyramid,
        "Diamond": diamond,
        "Hollow Pyramid": hollow_pyramid,
        "Number Pattern": number_pattern,
        "Alphabet Pattern": alphabet_pattern,
        "Zigzag": zigzag,
        "Arrow": arrow,
        "Diagonal (\\)": lambda r, s: diagonal(r, s, "\\"),
        "Diagonal (/)": lambda r, s: diagonal(r, s, "/"),
    }

    func = pattern_functions.get(selected_name)
    if not func:
        print("Pattern function not found."); return

    try:
        with open("saved_patterns.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("\nNo saved patterns found.\n"); return

    # Determine rows
    if new_rows: rows = new_rows
    else: rows = sum(1 for line in lines if line.strip() and not line.startswith("---")) // len([l for l in lines if l.startswith("---")])
    if rows == 0: rows = 5
    symbol = new_symbol if new_symbol else "*"
    generated = func(rows, symbol)

    print(f"\n--- {selected_name} ---")
    for line in generated: print(line)
    print("\n===== END OF REPLAY =====\n")

def replay_multiple_patterns():
    try:
        with open("saved_patterns.txt", "r") as f: lines = f.readlines()
        if not lines: print("\nNo saved patterns.\n"); return
    except FileNotFoundError:
        print("\nNo saved patterns found.\n"); return

    pattern_positions = [(line.replace("-", "").strip(), idx) for idx, line in enumerate(lines) if line.startswith("---")]
    if not pattern_positions: print("\nNo saved patterns.\n"); return

    print("\nSaved Patterns:")
    for i, (name, _) in enumerate(pattern_positions, 1): print(f"{i}. {name}")

    choices = input("\nEnter numbers of patterns to replay (comma-separated, e.g., 1,3,5): ")
    selected_indices = []
    for part in choices.split(","):
        try: selected_indices.append(int(part.strip()) - 1)
        except ValueError: continue

    new_symbol = input("Enter a symbol to override (leave empty for original): ")
    try: new_rows = int(input("Enter new number of rows (leave empty for original): "))
    except ValueError: new_rows = None

    pattern_functions = {
        "Right Triangle": right_triangle,
        "Inverted Triangle": inverted_triangle,
        "Pyramid": pyramid,
        "Diamond": diamond,
        "Hollow Pyramid": hollow_pyramid,
        "Number Pattern": number_pattern,
        "Alphabet Pattern": alphabet_pattern,
        "Zigzag": zigzag,
        "Arrow": arrow,
        "Diagonal (\\)": lambda r, s: diagonal(r, s, "\\"),
        "Diagonal (/)": lambda r, s: diagonal(r, s, "/"),
    }

    for idx in selected_indices:
        if idx < 0 or idx >= len(pattern_positions): continue
        name, start_idx = pattern_positions[idx]

        if new_rows: rows = new_rows
        else:
            end_idx = pattern_positions[idx + 1][1] if idx + 1 < len(pattern_positions) else len(lines)
            rows = sum(1 for line in lines[start_idx+1:end_idx] if line.strip())
        symbol = new_symbol if new_symbol else "*"

        func = pattern_functions.get(name)
        print(f"\n--- {name} ---")
        if func:
            generated = func(rows, symbol)
            for l in generated: print(l)
        else:
            end_idx = pattern_positions[idx + 1][1] if idx + 1 < len(pattern_positions) else len(lines)
            for l in lines[start_idx+1:end_idx]:
                print(l.replace("*", symbol) if new_symbol else l.strip())

    print("\n===== END OF REPLAY =====\n")

# ---------- SEARCH FUNCTION ----------
def search_saved_pattern():
    query = input("\nEnter name or part of the pattern to search: ").strip().lower()
    try:
        with open("saved_patterns.txt", "r") as f: lines = f.readlines()
    except FileNotFoundError:
        print("\nNo saved patterns found.\n"); return

    pattern_names = [line.replace("-", "").strip() for line in lines if line.startswith("---")]
    matched = [name for name in pattern_names if query in name.lower()]

    if not matched:
        print("\nNo matching patterns found.\n"); return

    print("\nMatched Patterns:")
    for i, name in enumerate(matched, 1): print(f"{i}. {name}")

    try:
        choice_index = int(input("\nEnter the number of the pattern to replay: ")) - 1
        if choice_index < 0 or choice_index >= len(matched): print("Invalid choice."); return
    except ValueError:
        print("Invalid input."); return

    replay_pattern_by_name(matched[choice_index])

# ---------- QUICK PREVIEW ----------
def quick_preview():
    rows = 5; symbol = "*"
    previews = [
        ("Right Triangle", right_triangle(rows, symbol)),
        ("Inverted Triangle", inverted_triangle(rows, symbol)),
        ("Pyramid", pyramid(rows, symbol)),
        ("Diamond", diamond(rows, symbol)),
        ("Hollow Pyramid", hollow_pyramid(rows, symbol)),
        ("Number Pattern", number_pattern(rows)),
        ("Alphabet Pattern", alphabet_pattern(rows)),
        ("Zigzag", zigzag(rows, symbol)),
        ("Arrow", arrow(rows, symbol)),
        ("Diagonal (\\)", diagonal(rows, symbol, "\\")),
        ("Diagonal (/)", diagonal(rows, symbol, "/")),
    ]
    print("\n===== QUICK PATTERN PREVIEW =====\n")
    for name, lines in previews:
        print(f"\n--- {name} ---")
        for line in lines: print(line)
    print("\n===== END OF PREVIEW =====\n")

# ---------- INTERACTIVE CREATION ----------
def interactive_creation():
    patterns = {
        "1": ("Right Triangle", right_triangle),
        "2": ("Inverted Triangle", inverted_triangle),
        "3": ("Pyramid", pyramid),
        "4": ("Diamond", diamond),
        "5": ("Hollow Pyramid", hollow_pyramid),
        "6": ("Number Pattern", number_pattern),
        "7": ("Alphabet Pattern", alphabet_pattern),
        "8": ("Zigzag", zigzag),
        "9": ("Arrow", arrow),
        "10": ("Diagonal (\\)", lambda r, s: diagonal(r, s, "\\")),
        "11": ("Diagonal (/)", lambda r, s: diagonal(r, s, "/")),
    }

    print("\nChoose a pattern to create:")
    for k, (name, _) in patterns.items(): print(f"{k}. {name}")

    choice = input("\nEnter choice: ")
    if choice not in patterns: print("Invalid choice."); return

    name, func = patterns[choice]
    rows = int(input("Enter number of rows: "))
    symbol = input("Enter symbol (default *): ") or "*"

    generated = func(rows, symbol)
    print(f"\n--- {name} (Preview) ---")
    for line in generated: print(line)

    if input("\nSave this pattern? (y/n): ").lower() == "y": save_pattern(name, generated)

# ---------- MAIN MENU ----------
def main_menu():
    while True:
        print("\n🎨 Ultimate Pattern Project Menu 🎨")
        print("1. Quick Preview of Patterns")
        print("2. Interactive Pattern Creation")
        print("3. Replay Single Saved Pattern")
        print("4. Replay Multiple Saved Patterns")
        print("5. Search Saved Pattern by Name")
        print("6. Clear All Saved Patterns")
        print("7. Exit")
        choice = input("\nEnter your choice: ")

        if choice == "1": quick_preview()
        elif choice == "2": interactive_creation()
        elif choice == "3": replay_single_pattern()
        elif choice == "4": replay_multiple_patterns()
        elif choice == "5": search_saved_pattern()
        elif choice == "6": clear_saved_patterns()
        elif choice == "7": print("\nThanks for using the Ultimate Pattern Project! 🎉"); break
        else: print("Invalid choice. Try again.")

# ---------- MAIN ----------
if __name__ == "__main__":
    main_menu()
