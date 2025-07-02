# Pipe lengths and quantities
required_pipes = {
    3.502: 2, 7.5: 3, 8.2: 4, 8.3: 5, 9.0: 6, 10.0: 7, 11.0: 8,
    11.5: 9, 11.7: 1, 0.3: 2, 0.2: 3, 0.1: 4, 0.25: 5,
    2.0: 6, 2.5: 7, 1.0: 8
}

# Output list to store results
output_lines = []

# Define logging function
def log(msg):
    print(msg)
    output_lines.append(msg)

# --- User Input ---
try:
    main_rod_length = float(input("Enter length of first rod (in meters): "))
    secondary_rod_length = float(input("Enter length of second rod (to use scraps): "))
    if main_rod_length <= 0 or secondary_rod_length <= 0:
        log("Lengths must be greater than 0.")
        raise SystemExit
except ValueError:
    log("Invalid input. Please enter numeric values.")
    raise SystemExit

# --- Prepare all pipe cuts ---
length_list = []
for length, qty in required_pipes.items():
    length_list.extend([length] * qty)
length_list.sort(reverse=True)

# --- Fit primary rods ---
main_rods = []
for length in length_list:
    placed = False
    for rod in main_rods:
        if sum(rod) + length <= main_rod_length:
            rod.append(length)
            placed = True
            break
    if not placed:
        main_rods.append([length])

# --- Scrap Calculation ---
total_scrap = 0
scrap_pieces = []
for rod in main_rods:
    scrap = round(main_rod_length - sum(rod), 3)
    if scrap > 0.001:
        total_scrap += scrap
        scrap_pieces.append(scrap)

# --- Output Primary Rods ---
log(f"\nCombinations for {main_rod_length} m rod:\n")
for i, rod in enumerate(main_rods, 1):
    total = round(sum(rod), 3)
    scrap = round(main_rod_length - total, 3)
    log(f"Rod {i:<2}:  Cuts = {rod}   |   Used = {total:>6.3f} m   |   Scrap = {scrap:>6.3f} m")

log(f"\nTotal primary rods used: {len(main_rods)}")
log(f"🔧 Total scrap produced from all rods: {round(total_scrap, 3)} m")

# --- Secondary Rods from Scrap ---
secondary_rod_count = int(total_scrap // secondary_rod_length)
final_leftover_scrap = round(total_scrap % secondary_rod_length, 3)

log(f"\n♻️ Secondary Rods:")
log(f"Second rod length: {secondary_rod_length} m")
log(f"✅ Number of secondary rods made from scrap: {secondary_rod_count}")
log(f"❗Leftover scrap after making secondary rods: {final_leftover_scrap} m")

# --- Save to Text File (Pydroid3-safe path) ---
try:
    with open("rod_cutting_output.txt", "w") as f:
        f.write("\n".join(output_lines))
    log("\n✅ Output saved to file: rod_cutting_output.txt (in Pydroid3/files)")
except Exception as e:
    log(f"\n❌ Failed to save output file: {e}")

# --- Hold screen ---
input("\n✔ Done! Press Enter to exit...")
