medicine_database = {
    "Aspirin": {"stack_number": 1, "strips_per_stack": 10},
    "Paracetamol": {"stack_number": 2, "strips_per_stack": 8},
    "Ibuprofen": {"stack_number": 3, "strips_per_stack": 12},
    "Loratadine": {"stack_number": 4, "strips_per_stack": 6},
    "Amoxicillin": {"stack_number": 5, "strips_per_stack": 16},
    "Omeprazole": {"stack_number": 6, "strips_per_stack": 14},
    "Atorvastatin": {"stack_number": 7, "strips_per_stack": 10},
    "Simvastatin": {"stack_number": 8, "strips_per_stack": 10},
    "Metformin": {"stack_number": 9, "strips_per_stack": 12},
    "Losartan": {"stack_number": 10, "strips_per_stack": 8},
    "Amlodipine": {"stack_number": 11, "strips_per_stack": 10},
    "Albuterol": {"stack_number": 12, "strips_per_stack": 18},
    "Atenolol": {"stack_number": 13, "strips_per_stack": 10},
    "Tramadol": {"stack_number": 14, "strips_per_stack": 14},
    "Citalopram": {"stack_number": 15, "strips_per_stack": 12},
    "Gabapentin": {"stack_number": 16, "strips_per_stack": 8},
    "Duloxetine": {"stack_number": 17, "strips_per_stack": 10},
    "Warfarin": {"stack_number": 18, "strips_per_stack": 8},
    "Pregabalin": {"stack_number": 19, "strips_per_stack": 10},
    "Aripiprazole": {"stack_number": 20, "strips_per_stack": 6},
    "Risperidone": {"stack_number": 21, "strips_per_stack": 10},
    "Levothyroxine": {"stack_number": 22, "strips_per_stack": 8},
    "Phentermine": {"stack_number": 23, "strips_per_stack": 10},
    "Metoprolol": {"stack_number": 24, "strips_per_stack": 12}
}

def check_medicine_availability(patient_details):
    available_stacks = []
    medicines = patient_details.get("medicines", {})
    for medicine, quantity in medicines.items():
        if medicine in medicine_database:
            stack_number = medicine_database[medicine]["stack_number"]
            available_stacks.extend([str(stack_number)] * quantity)
    return ", ".join(available_stacks)

def get_patient_details(input_str):
    patient_details = {}
    patient_details["name"], patient_details["age"], patient_details["gender"], patient_details["id"], medicines_str = input_str.split(',')
    medicines = {}
    for item in medicines_str.split(';'):
        medicine, quantity = item.strip().split(':')
        medicines[medicine.strip()] = int(quantity.strip())
    patient_details["medicines"] = medicines
    return patient_details

# Main code
input_str = input("Enter patient details in the format 'name,age,gender,id,medicine1:quantity1;medicine2:quantity2;...': ")
patient_details = get_patient_details(input_str)
available_stacks = check_medicine_availability(patient_details)
print("Available stack numbers:", available_stacks)
