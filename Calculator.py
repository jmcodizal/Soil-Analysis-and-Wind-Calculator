import csv
import os

def log_soil_analysis_to_csv(soil_analysis):
    file_exists = os.path.isfile('soil_analysis_history.csv')
    with open('soil_analysis_history.csv', mode = 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Soil Type', 'Soil Bearing Capacity (kN/m^2)', 'Depth  of Soil layer (m)',
            'Water table Depeth (m)', 'Allowable Bearing Capacity (kN)', 'Settlement (m)', 
            'Lateral Earth Pressure', 'Water Table Effect'])

        writer.writerow([soil_analysis.soil_type, soil_analysis.soil_bearing_capacity, 
                         soil_analysis.depth_of_soil_layer, soil_analysis.water_table_depth, 
                         soil_analysis.calculate_soil_bearing_capacity(), soil_analysis.calculate_settlement(), 
                         soil_analysis.calculate_lateral_earth_pressure(), soil_analysis.water_table_effect()])
        
def log_wind_load_to_csv(wind_load, structure_type, specific_type, acceptable_limits):
    file_exists = os.path('wind_load_history.csv')
    with open('wind_load_history.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Writing header row if file doesn't exist
            writer.writerow(['Wind Load Calculation', 'Structure Type', 'Specific Type', 'Acceptable Limits'])
        # Writing the data row for wind load calculation
        writer.writerow([wind_load, structure_type, specific_type, acceptable_limits])


class SoilAnalysis:

    def __init__(self, soil_type, soil_bearing_capacity, depth_of_soil_layer, water_table_depth):
        self.soil_type = soil_type
        self.soil_bearing_capacity = soil_bearing_capacity
        self.depth_of_soil_layer = depth_of_soil_layer
        self.water_table_depth = water_table_depth

    def soil_type_info(self):
        soil_info = {
            'Clay': 'Clay soils are cohesive, sticky, and often have poor drainage.',
            'Sand': 'Sand soils are loose, non-cohesive, and drain quickly.',
            'Silt': 'Silt soils are smooth, slippery, and drain moderately.',
            'Loam': 'Loam soils are a mixture of sand, silt, and clay and have good drainage.'
        }
        return soil_info.get(self.soil_type, 'Unknown soil type')
    
    def check_soil_bearing_capacity(self):
        if self.soil_bearing_capacity < 100:
            return "Low soil bearing capacity"
        elif 100 <= self.soil_bearing_capacity <= 300:
            return "Medium soil bearing capacity"
        else:
            return "High soil bearing capacity"
        
    def calculate_soil_bearing_capacity(self):
        safety_factor = 3.0
        load_factor = 1.2 if self.soil_type == 'Clay' else 1.0
        total_bearing_capacity = self.soil_bearing_capacity * load_factor * self.depth_of_soil_layer
        allowable_bearing_capacity = total_bearing_capacity / safety_factor
        return allowable_bearing_capacity
    
    def calculate_settlement(self):
        applied_pressure = 150   # Standard Applied pressure (in kN/m^2) 
        foundation_width = 1   # Standard width of the foundation (in meters)
        young_modulus = 10e6  # Standard Young's modulus for the soil (in kN/m^2)
        poisson_ratio = 0.3  # Poisson's ratio for the soil (dimensionless)
        settlement = (applied_pressure * foundation_width) / (young_modulus * (1 - poisson_ratio**2))
        return settlement
    
    def calculate_lateral_earth_pressure(self):
        friction_angle = 30 # Assumed friction angle of the soil (in degrees)
        K = (1 - (3.14159 * friction_angle) / (1 + (3.14159 * friction_angle))) # Simplified calculation
        return K
    
    def water_table_effect(self):
        if self.water_table_depth < 2:
            return "Water table is too high. This may reduce the bearing capacity significantly."
        else:
            return "Water table depth is adequate for construction."
        
    def display_analysis(self):
        allowable_bearing_capacity = self.calculate_soil_bearing_capacity()
        settlement = self.calculate_settlement()
        lateral_pressure = self.calculate_lateral_earth_pressure()
        result = f"\nSoil Type: {self.soil_type}"
        result += f"\nSoil Type Information: {self.soil_type_info()}"
        result += f"\nSoil bearing Capacity: {self.soil_bearing_capacity} kN/m^2"
        result += f"\nSoil bearing Capacity Evaluation: {self.check_soil_bearing_capacity()}"
        result += f"\nDepth of Soil Layer: {self.depth_of_soil_layer} meters"
        result += f"\nLoad Distribution Capacity: {allowable_bearing_capacity} kN"
        result += f"\nSettlement (Estimated): {settlement} meters"
        result += f"\nLateral Earth Pressure Coefficient: {lateral_pressure}"
        result += f"\nWater Table Depth: {self.water_table_depth} meters"
        result += f"\nWater Table Effect: {self.water_table_effect()}\n"       
        if allowable_bearing_capacity < 100:   
            result += "\n[WARNING]: The allowable soil bearing capacity is too low for safe construction!"
        if settlement > 0.01: 
            result += "\n[WARNING]: Settlement exceeds acceptable limits! Consider revising the foundation design."
        if lateral_pressure > 1.5:
            result += "\n[WARNING]: Lateral earth pressure is high. Consider reinforcing structures like retaining walls."
        if self.water_table_depth < 2:
            result += "\n[WARNING]: High water table detected. This may reduce soil stability and bearing capacity!"
        print(result)
        log_soil_analysis_to_csv(self)

def get_soil_type():
    valid_soil_types = ['Clay', 'Sand', 'Silt', 'Loam']
    while True:
        soil_type = input("Soil type (Clay, Sand, Silt, Loam): ").capitalize()
        if soil_type in valid_soil_types:
            return soil_type
        else:
            print("Invalid input. Please enter a valid soil type (Clay, Sand, Silt, Loam).")

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            else:
                print("Invalid input. Please input a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_soil_analysis_inputs():
    print("\nPlease enter the soil analysis parameters:")
    soil_type = get_soil_type()
    soil_bearing_capacity = get_positive_float("Soil bearing capacity (kN/m^2): ")
    depth_of_soil_layer = get_positive_float("Depth of soil layer (meters): ")
    water_table_depth = get_positive_float("Water table depth (meters): ")
    return SoilAnalysis(soil_type, soil_bearing_capacity, depth_of_soil_layer, water_table_depth) 


def calculate_wind_load(q, G, Cd, area):
    calculate_wind_load = q * G * Cd * area
    return calculate_wind_load

def wind_load_calculation():
    while True:
        try: 
            wind_speed = int(input("Enter the wind speed (m/s): "))
            if wind_speed <= 0:
                print("Wind speed must be a positive number.")
                continue
            break   
        except ValueError:
            print("Invalid input. Please enter a valid numerical value for wind speed.")         
    q = 0.613 * wind_speed**2

    print("Choices:\nA: Open water or flat terrain\nB: Suburban terrain\nC: Urban areas with buildings and trees\nD: Open terrain with no obstructions\nE: Intermediate category for areas with moderate density\nF: Areas with very high density and tall structures")
    while True:
        exposure_category = input("Enter Gust factor (G) based on building height and exposure category (A, B, C, D, E, F): ").upper()
        if exposure_category not in ["A", "B", "C", "D", "E", "F"]:
            print("Invalid input. Please enter a valid exposure category (A, B, C, D, E, F).")
            continue
        if exposure_category == "A":
            G = 0.8
        elif exposure_category == "B":
            G = 1.0
        elif exposure_category == "C":
            G = 1.2
        elif exposure_category == "D":
            G = 1.4
        elif exposure_category == "E":
            G = 1.4
        elif exposure_category == "F":
            G = 1.8
        break    

    print("Choices: rectangular, cylindrical, triangular, hexagonal, octagonal, dome, parabolic, irregular, sphere, cone, airfoil")
    while True:
        structural_shape = input("Enter the shape of the structure or type 'exit' to quit: ").lower()
        if structural_shape == 'exit':
            print("Exiting the program.")
            return
        if structural_shape == "rectangular":
            Cd = 1.3
        elif structural_shape == "cylindrical":
            Cd = 0.6
        elif structural_shape == "triangular":
            Cd = 1.2
        elif structural_shape == "hexagonal":
            Cd = 1.1
        elif structural_shape == "octagonal":
            Cd = 1.05
        elif structural_shape == "dome":
            Cd = 0.4
        elif structural_shape == "parabolic":
            Cd = 0.9
        elif structural_shape == "irregular":
            Cd = 1.5
        elif structural_shape == "sphere":
            Cd = 0.47
        elif structural_shape == "cone":
            Cd = 0.5
        elif structural_shape == "airfoil":
            Cd = 0.04
        else:
            print("Invalid structural shape. Please choose from the available options.")
            continue
        break   
    
    while True:
        try:
            area = int(input("Enter the area exposed to wind (m^2): "))
            if area <= 0:
                print("Area must be a positive number.")
                continue
            break  
        except ValueError:
            print("Invalid input. Please enter a valid numerical value for area.")
    wind_load = calculate_wind_load(q, G, Cd, area)
    print(f"The calculated wind load is: {wind_load} N")
    structure_type = input("Enter the building structure type (residential, commercial, industrial, infrastructural, institutional, agricultural, recreational, mixed use, civic, transportation, hospitality): ").lower()
    if structure_type not in ["residential", "commercial", "industrial", "infrastructural", "institutional", "agricultural", "recreational", "mixed use", "civic", "transportation", "hospitality"]:
        print("Invalid structure type. Please enter a valid building structure type.")
        return
    acceptable_limits = None
    if structure_type == "residential": 
        specific_type = input("Enter the specific residential type (single-family, duplex, apartment): ").lower()
        if specific_type == "single-family":
            acceptable_limits = 1200
        elif specific_type == "duplex":
            acceptable_limits = 1300
        elif specific_type == "apartment":
            acceptable_limits = 1400
    elif structure_type == "commercial": 
        specific_type = input("Enter the specific commercial type (retail, office, shopping mall): ").lower()
        if specific_type == "retail":
            acceptable_limits = 2800
        elif specific_type == "office":
            acceptable_limits = 2900
        elif specific_type == "shopping mall":
            acceptable_limits = 3000
    elif structure_type == "industrial": 
        specific_type = input("Enter the specific industrial type (factory, warehouse, power plant): ").lower()
        if specific_type == "factory":
            acceptable_limits = 5000
        elif specific_type == "warehouse":
            acceptable_limits = 4000
        elif specific_type == "power plant":
            acceptable_limits = 6000
    elif structure_type == "infrastructural": 
        specific_type = input("Enter the specific infrastructural type (bridge, tower, dam): ").lower()
        if specific_type == "bridge":
            acceptable_limits = 5000
        elif specific_type == "tower":
            acceptable_limits = 6000
        elif specific_type == "dam":
            acceptable_limits = 5000
    elif structure_type == "institutional": 
        specific_type = input("Enter the specific institutional type (school, university, hospital): ").lower()
        if specific_type == "school":
            acceptable_limits = 2300
        elif specific_type == "university":
            acceptable_limits = 2400
        elif specific_type == "hospital":
            acceptable_limits = 2500
    elif structure_type == "agricultural": 
        specific_type = input("Enter the specific agricultural type (barn, silo, greenhouse): ").lower()
        if specific_type == "barn":
            acceptable_limits = 1800
        elif specific_type == "silo":
            acceptable_limits = 1900
        elif specific_type == "greenhouse":
            acceptable_limits = 2000
    elif structure_type == "recreational": 
        specific_type = input("Enter the specific recreational type (sports complex, fitness center, recreation center): ").lower()
        if specific_type == "sports complex":
            acceptable_limits = 2800
        elif specific_type == "fitness center":
            acceptable_limits = 2900
        elif specific_type == "recreation center":
            acceptable_limits = 3000
    elif structure_type == "mixed use": 
        specific_type = input("Enter the specific mixed-use type (live-work, mixed development): ").lower()
        if specific_type == "live-work":
            acceptable_limits = 3300
        elif specific_type == "mixed development":
            acceptable_limits = 3500
    elif structure_type == "civic": 
        specific_type = input("Enter the specific civic type (community center, library, cultural facility): ").lower()
        if specific_type == "community center":
            acceptable_limits = 2200
        elif specific_type == "library":
            acceptable_limits = 2300
        elif specific_type == "cultural facility":
            acceptable_limits = 2400
    elif structure_type == "transportation": 
        specific_type = input("Enter the specific transportation type (airport, train station, bus terminal): ").lower()
        if specific_type == "airport":
            acceptable_limits = 3900
        elif specific_type == "train station":
            acceptable_limits = 4000
        elif specific_type == "bus terminal":
            acceptable_limits = 4100
    elif structure_type == "hospitality": 
        specific_type = input("Enter the specific hospitality type (hotel, motel, resort): ").lower()
        if specific_type == "hotel":
            acceptable_limits = 2800
        elif specific_type == "motel":
            acceptable_limits = 2900
        elif specific_type == "resort":
            acceptable_limits = 3000
    print(f"Specific {structure_type.capitalize()} Building Type: {specific_type.capitalize()}")
    if wind_load > acceptable_limits:
        print(f"[WARNING!] Wind load exceeds the acceptable limit for {structure_type} structures!")
        print("[RECOMMENDATION] Consider reinforcing the structure to withstand higher loads.")
    elif wind_load > 0.75 * acceptable_limits:
        print(f"[WARNING!] Wind load is approaching the limit for {structure_type} structures.")
        print("[RECOMMENDATION] Monitor the structure for any signs of damage or strain.")
    else:
        print(f"[RECOMMENDATION] Wind load is within safe limits for {structure_type} structures.") 
    log_wind_load_to_csv(wind_load, structure_type, specific_type, acceptable_limits)


    continue_option = input("Do you want to calculate again? (yes/no): ").lower()
    if continue_option in ['no']:
        print("Thank you for using the Wind Load Calculator. Goodbye!")

def main():
    while True:
        print("-----------------------------------WELCOME TO SOIL ANALYSIS AND WIND LOAD CALCULATOR!----------------------------------")
        print("\nWhich calculation would you like to perform? Enter (1, 2, or 3)")
        print("1: Soil Analysis")
        print("2: Wind Load Calculation")
        print("3: Exit")
        choice = input("Enter the number of your choice: ").strip()
        if choice == '1':
            soil_analysis = get_soil_analysis_inputs()
            soil_analysis.display_analysis()
        elif choice == '2':
            wind_load_calculation()
        elif choice == '3':
            print("THANKYOU FOR USING SOIL ANALYSIS & WIND LOAD CALCULATOR. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
