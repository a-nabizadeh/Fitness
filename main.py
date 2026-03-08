from database_operations import store_in_database, update_client_info, load_from_database
from client import Client
from other_operations import calculate_nutrition


ALLOWED_UPDATE_COLUMNS = {
    "name",
    "age",
    "sex",
    "weight",
    "height",
    "waist",
    "hip",
    "activity_index",
    "goal",
}


def prompt_int(message):
    while True:
        value = input(message).strip()
        try:
            return int(value)
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def prompt_float(message):
    while True:
        value = input(message).strip()
        try:
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def prompt_choice(message, valid_values):
    valid = {v.lower(): v for v in valid_values}
    while True:
        value = input(message).strip().lower()
        if value in valid:
            return value
        print(f"Invalid input. Please enter one of: {', '.join(valid_values)}.")


#--Collect data for a single client
def get_client_data():
    name = input("Enter client's name: ")
    age = prompt_int("Enter client's age: ")
    sex = prompt_choice("Enter client's sex (F/M): ", ["f", "m"]).upper()
    weight = prompt_float("Enter client's weight (kg): ")
    height = prompt_float("Enter client's height (cm): ")
    waist = prompt_float("Enter client's waist measurement (cm): ")
    hip = prompt_float("Enter client's hip measurement (cm): ")
    activity_index = prompt_float("Enter client's activity index: ")
    goal = prompt_choice("Would you like to lose or gain weight? (lose/gain/none): ", ["lose", "gain", "none"])
    return Client(name, age, sex, weight, height, waist, hip, activity_index, goal)

#--Function to collect client data
def collect_client_data():
    clients = []
    while True:
        action = prompt_choice(
            "Would you like to add a new client, update an existing client, or calculate nutrition? (add/update/nutrition/finish): ",
            ["add", "update", "nutrition", "finish"],
        )
        if action == 'add':
            clients.append(get_client_data())
        elif action == 'update':
            update_client()
        elif action == 'nutrition':
            name = input("Enter the name of the client: ")
            calculate_nutrition_plan(name)
        elif action == 'finish':
            break
    return clients


#--Update existing client
def update_client():
    name = input("Enter the name of the client you want to update: ")
    #Check if the client exists
    if check_client_exists(name):
        column = prompt_choice(
            "Enter the name of the column you want to update (name/age/sex/weight/height/waist/hip/activity_index/goal): ",
            sorted(ALLOWED_UPDATE_COLUMNS),
        )
        new_value = input(f"Enter the new value for {column}: ")

        if column in {"age"}:
            try:
                new_value = int(new_value)
            except ValueError:
                print("Invalid value. Age must be a whole number.")
                return
        elif column in {"weight", "height", "waist", "hip", "activity_index"}:
            try:
                new_value = float(new_value)
            except ValueError:
                print(f"Invalid value. {column} must be numeric.")
                return
        elif column == "sex":
            new_value = new_value.upper()
            if new_value not in {"F", "M"}:
                print("Invalid value. Sex must be 'F' or 'M'.")
                return
        elif column == "goal":
            new_value = new_value.lower()
            if new_value not in {"lose", "gain", "none"}:
                print("Invalid value. Goal must be lose, gain, or none.")
                return

        #Update client information
        try:
            update_client_info(name, column, new_value)
            print(f"Client {name}'s {column} has been updated to {new_value}.")
        except ValueError as exc:
            print(exc)
    else:
        print("Client not found.")


#--Check if a client exists in the database
def check_client_exists(name):
    clients = load_from_database()
    for client in clients:
        if client.name == name:
            return True
    return False


#--Calculate the nutritions for the client
def calculate_nutrition_plan(name):
    # Load client data from the database
    clients = load_from_database()
    # Find the client with the given name
    client = next((c for c in clients if c.name == name), None)
    if client is not None:
        # Calculate nutrition plan for the client
        # Ask for additional parameters
        protein_percentage = prompt_float("Enter the protein percentage: ")
        carbohydrates_percentage = prompt_float("Enter the carbohydrates percentage: ")
        calorie_deficiency = prompt_float("Enter the calorie deficiency amount: ")
        if protein_percentage < 0 or carbohydrates_percentage < 0:
            print("Protein and carbohydrate percentages must be non-negative.")
            return
        if protein_percentage + carbohydrates_percentage > 100:
            print("Protein and carbohydrate percentages cannot exceed 100% in total.")
            return
        if calorie_deficiency < 0:
            print("Calorie deficiency amount must be non-negative.")
            return
        calculate_nutrition(client, protein_percentage, carbohydrates_percentage, calorie_deficiency)
    else:
        print(f"Client '{name}' not found in the database.")


#--Main program
def main():
    client = collect_client_data()
    if client:
        store_in_database(client)
        print("Client data has been saved to the database.")
    else:
        print("No client data collected!")


if __name__ == "__main__":
    main()
