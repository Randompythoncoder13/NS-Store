import json
import os

DATA_FILE = 'data.json'


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print("\n--- Data saved successfully! ---")


def prompt_dict(title, keys):
    print(f"\n--- {title} ---")
    print("(Press Enter to skip a field)")
    result = {}
    for key in keys:
        val = input(f"{key}: ").strip()
        if val:
            result[key] = val
    return result


def prompt_list(title):
    print(f"\n--- {title} ---")
    print("(Enter items one by one. Press Enter on an empty line to finish)")
    result = []
    while True:
        val = input("- ").strip()
        if not val:
            break
        result.append(val)
    return result


def add_vehicle(data):
    if not data:
        print("Add a company first!")
        return

    print("\nSelect a Company:")
    companies = list(data.keys())
    for i, c in enumerate(companies):
        print(f"{i + 1}. {c}")

    comp_idx = int(input("Choice: ")) - 1
    company = companies[comp_idx]

    domain = input("\nSelect Domain (1: Naval, 2: Land, 3: Air): ").strip()
    domain_map = {"1": "Naval", "2": "Land", "3": "Air"}
    domain_name = domain_map.get(domain)

    if not domain_name:
        print("Invalid choice.")
        return

    name = input("\nVehicle Name: ").strip()
    vehicle = {"Name": name}

    # Common Section
    cost_build = prompt_dict("Cost and Build Time", ["Cost", "Build Time"])
    if cost_build: vehicle["Cost and Build Time"] = cost_build

    # Domain Specific Sections
    if domain_name == "Naval":
        specs = prompt_dict("Vessel Specs", ["Displacement", "Speed", "Range", "Crew Size"])
        if specs: vehicle["Vessel Specs"] = specs

        aircraft = prompt_list("Aircraft Carried")
        if aircraft: vehicle["Aircraft Carried"] = aircraft

    elif domain_name == "Land":
        specs = prompt_dict("Vehicle Specs", ["Weight", "Speed", "Range", "Crew", "Passengers"])
        if specs: vehicle["Vehicle Specs"] = specs

        drones = prompt_list("Drones Carried")
        if drones: vehicle["Drones Carried"] = drones

    elif domain_name == "Air":
        dims = prompt_dict("Dimensions & Capacity",
                           ["Empty Weight", "Max Weight", "Length", "Wingspan/Blade span", "Airframe",
                            "Internal fuel capacity"])
        if dims: vehicle["Dimensions & Capacity"] = dims

        perf = prompt_dict("Performance",
                           ["Max Speed", "Cruise Speed", "Combat Radius", "Ferry Range", "Altitude Ceiling"])
        if perf: vehicle["Performance"] = perf

        drones = prompt_list("Drones Carried")
        if drones: vehicle["Drones Carried"] = drones

    # Common Sections continued
    weapons = prompt_list("Weapons")
    if weapons: vehicle["Weapons"] = weapons

    systems = prompt_list("Systems")
    if systems: vehicle["Systems"] = systems

    data[company][domain_name].append(vehicle)
    save_data(data)


def main():
    data = load_data()

    while True:
        print("\n=== RP Game Data Manager ===")
        print("1. Add a new Company")
        print("2. Add a new Vehicle")
        print("3. Quit")
        choice = input("Select an option: ").strip()

        if choice == '1':
            comp_name = input("Company Name: ").strip()
            if comp_name and comp_name not in data:
                data[comp_name] = {"Naval": [], "Land": [], "Air": []}
                save_data(data)
            else:
                print("Company already exists or invalid name.")
        elif choice == '2':
            add_vehicle(data)
        elif choice == '3':
            break


if __name__ == "__main__":
    main()