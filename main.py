from database_operations import store_in_database, update_client_info, load_from_database
from client import Client
from other_operations import calculate_nutrition


#--Collect data for a single client
def get_client_data():
    name = input("Enter client's name: ")
    age = int(input("Enter client's age: "))
    sex = input("Enter client's sex (F/M): ").upper()
    while sex not in ['F', 'M']:
        print("Invalid input. Please enter 'F' or 'M'.")
    weight = float(input("Enter client's weight (kg): "))
    height = float(input("Enter client's height (cm): "))
    waist = float(input("Enter client's waist measurement (cm): "))
    hip = float(input("Enter client's hip measurement (cm): "))
    activity_index = float(input("Enter client's activity index: "))
    goal = input("Would you like to lose or gain weight? (lose/gain/none): ").lower()
    return Client(name, age, sex, weight, height, waist, hip, activity_index, goal)

#--Function to collect client data
def collect_client_data():
    clients = []
    while True:
        action = input("Would you like to add a new client, update an existing client, or calculate nutrition? (add/update/nutrition/finish): ").lower()
        if action == 'add':
            clients.append(get_client_data())
        elif action == 'update':
            update_client()
        elif action == 'nutrition':
            name = input("Enter the name of the client: ")
            calculate_nutrition_plan(name)
        elif action == 'finish':
            break
        else:
            print("Invalid input. Please enter 'add', 'update', 'nutrition', or 'finish'.")
    return clients


#--Update existing client
def update_client():
    name = input("Enter the name of the client you want to update: ")
    #Check if the client exists
    if check_client_exists(name):
        column = input("Enter the name of the column you want to update (name/age/sex/weight/height/waist/hip): ")
        new_value = input(f"Enter the new value for {column}: ")
        #Update client information
        update_client_info(name, column, new_value)
        print(f"Client {name}'s {column} has been updated to {new_value}.")
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
        protein_percentage = float(input("Enter the protein percentage: "))
        carbohydrates_percentage = float(input("Enter the carbohydrates percentage: "))
        calorie_deficiency = float(input("Enter the calorie deficiency amount: "))
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