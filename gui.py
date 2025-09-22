import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial


# Soil Analysis class
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
        applied_pressure = 150
        foundation_width = 1
        young_modulus = 10e4
        poisson_ratio = 0.3
        settlement = (applied_pressure * foundation_width) / (young_modulus * (1 - poisson_ratio**2))
        return settlement

    def calculate_lateral_earth_pressure(self):
        friction_angle = 30
        K = (1 - (3.14159 * friction_angle) / (1 + (3.14159 * friction_angle)))
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
        result += f"\nSoil Bearing Capacity: {self.soil_bearing_capacity} kN/m^2"
        result += f"\nSoil Bearing Capacity Evaluation: {self.check_soil_bearing_capacity()}"
        result += f"\nDepth of Soil Layer: {self.depth_of_soil_layer} meters"
        result += f"\nLoad Distribution Capacity: {allowable_bearing_capacity:.2f} kN"
        result += f"\nSettlement (Estimated): {settlement:.4f} meters"
        result += f"\nLateral Earth Pressure Coefficient: {lateral_pressure:.4f}"
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

        return result


# Wind Load Calculation classes
def calculate_wind_load_result(wind_speed_entry, area_entry, gust_factor_combobox, shape_combobox, structure_combobox, specific_type_combobox, wind_load_result_label):
    try:
        wind_speed_input = wind_speed_entry.get()
        if not wind_speed_input:
            raise ValueError("Wind speed is required.")
        wind_speed = float(wind_speed_input)
        print(f"Wind Speed: {wind_speed}")  
        
        if wind_speed <= 0:
            raise ValueError("Wind speed must be a positive number.")
        q = 0.613 * wind_speed**2
        
        # Check if the gust factor and shape factor are valid selections
        gust_factor_selection = gust_factor_combobox.get().strip()
        shape_factor_selection = shape_combobox.get().strip()

        print(f"Gust Factor Selection: {gust_factor_selection}")  
        print(f"Shape Factor Selection: {shape_factor_selection}") 

        if not gust_factor_selection or gust_factor_selection not in gust_factor_map:
            raise ValueError(f"Invalid gust factor selected: {gust_factor_selection}")
        if not shape_factor_selection or shape_factor_selection not in shape_factor_map:
            raise ValueError(f"Invalid shape factor selected: {shape_factor_selection}")
        
       
        G = gust_factor_map[gust_factor_selection]
        Cd = shape_factor_map[shape_factor_selection]

       
        area_input = area_entry.get()
        if not area_input:
            raise ValueError("Area is required.")
        area = float(area_input)
        print(f"Area: {area}") 
        
        if area <= 0:
            raise ValueError("Area must be a positive number.")
        
     
        wind_load = calculate_wind_load(q, G, Cd, area)

        
        structure_type = structure_combobox.get().strip().lower()
        specific_type = specific_type_combobox.get().strip().lower()

        print(f"Structure Type: {structure_type}")  
        print(f"Specific Type: {specific_type}")  

        if not structure_type or structure_type not in acceptable_limits_map:
            raise ValueError(f"Invalid structure type selected: {structure_type}")
        if not specific_type or specific_type not in acceptable_limits_map[structure_type]:
            raise ValueError(f"Invalid specific structure type selected: {specific_type}")
        
        acceptable_limits = acceptable_limits_map[structure_type][specific_type]
        
        # Display wind load result and warnings
        result = f"Calculated Wind Load: {wind_load:.2f} N\n"
        if wind_load > acceptable_limits:
            result += "[WARNING!] Wind load exceeds the acceptable limit!\n[RECOMMENDATION] Reinforce the structure."
        elif wind_load > 0.75 * acceptable_limits:
            result += "[CAUTION!] Wind load is approaching the limit.\n[RECOMMENDATION] Monitor for damage."
        else:
            result += "[SAFE] Wind load is within acceptable limits."
        
        wind_load_result_label.config(text=result)

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input or selection: {str(e)}")


# Mappings for Wind Load
gust_factor_map = {"Open water or flat terrain (A)": 0.8, "Suburban terrain (B)": 1.0,
                   "Urban areas (C)": 1.2, "Open terrain (D)": 1.4,
                   "Moderate density (E)": 1.4, "High density (F)": 1.8}

shape_factor_map = {"Rectangular": 1.3, "Cylindrical": 0.6, "Triangular": 1.2,
                    "Hexagonal": 1.1, "Octagonal": 1.05, "Dome": 0.4,
                    "Parabolic": 0.9, "Irregular": 1.5, "Sphere": 0.47,
                    "Cone": 0.5, "Airfoil": 0.04}

acceptable_limits_map = {
    "residential": {"single-family": 1200, "duplex": 1300, "apartment": 1400},
    "commercial": {"retail": 2800, "office": 2900, "shopping mall": 3000},
    "industrial": {"factory": 5000, "warehouse": 4000},
    "infrastructural": {"bridge": 3500, "dam": 10000},
    "institutional": {"hospital": 6000, "school": 5000},
    "agricultural": {"barn": 2000, "greenhouse": 2500},
    "recreational": {"stadium": 7000, "theater": 3000, "arena": 4000}
}

# Wind Load Calculation function
def calculate_wind_load(q, G, Cd, area):
    return q * G * Cd * area

class WindLoadCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Wind Load Calculator")

        self.wind_speed_label = tk.Label(root, text="Wind Speed (m/s):")
        self.wind_speed_label.grid(row=0, column=0)
        self.wind_speed_entry = tk.Entry(root)
        self.wind_speed_entry.grid(row=0, column=1)

        self.area_label = tk.Label(root, text="Area (m²):")
        self.area_label.grid(row=1, column=0)
        self.area_entry = tk.Entry(root)
        self.area_entry.grid(row=1, column=1)

        self.gust_factor_label = tk.Label(root, text="Gust Factor:")
        self.gust_factor_label.grid(row=2, column=0)
        self.gust_factor_combobox = ttk.Combobox(root, values=["Open water or flat terrain (A)", "Suburban terrain (B)", 
                                                              "Urban areas (C)", "Open terrain (D)", 
                                                              "Moderate density (E)", "High density (F)"])
        self.gust_factor_combobox.grid(row=2, column=1)

        self.shape_label = tk.Label(root, text="Shape Factor:")
        self.shape_label.grid(row=3, column=0)
        self.shape_combobox = ttk.Combobox(root, values=["Rectangular", "Cylindrical", "Triangular", 
                                                        "Hexagonal", "Octagonal", "Dome", 
                                                        "Parabolic", "Irregular", "Sphere", "Cone", 
                                                        "Airfoil"])
        self.shape_combobox.grid(row=3, column=1)

        self.structure_label = tk.Label(root, text="Structure Type:")
        self.structure_label.grid(row=4, column=0)
        self.structure_combobox = ttk.Combobox(root, values=["Residential", "Commercial", "Industrial", 
                                                            "Infrastructural", "Institutional", 
                                                            "Agricultural", "Recreational"])
        self.structure_combobox.grid(row=4, column=1)
        self.structure_combobox.bind("<<ComboboxSelected>>", self.update_specific_types)

        self.specific_type_label = tk.Label(root, text="Specific Structure Type:")
        self.specific_type_label.grid(row=5, column=0)
        self.specific_type_combobox = ttk.Combobox(root)
        self.specific_type_combobox.grid(row=5, column=1)

        self.wind_load_result_label = tk.Label(root, text="Wind Load Result: ")
        self.wind_load_result_label.grid(row=6, column=0, columnspan=2)

        self.calculate_button = tk.Button(root, text="Calculate", 
                                          command=partial(calculate_wind_load_result, 
                                                          self.wind_speed_entry, 
                                                          self.area_entry, 
                                                          self.gust_factor_combobox,
                                                          self.shape_combobox,
                                                          self.structure_combobox,
                                                          self.specific_type_combobox,
                                                          self.wind_load_result_label))
        self.calculate_button.grid(row=7, column=0, columnspan=2)

    def update_specific_types(self, event):
        
        structure_type = self.structure_combobox.get().strip()

        # Map structure types to their specific types
        specific_types_map = {
            "Residential": ["Single-Family", "Duplex", "Apartment"],
            "Commercial": ["Retail", "Office", "Shopping Mall"],
            "Industrial": ["Factory", "Warehouse"],
            "Infrastructural": ["Bridge", "Dam"],
            "Institutional": ["Hospital", "School"],
            "Agricultural": ["Barn", "Greenhouse"],
            "Recreational": ["Stadium", "Theater", "Arena"]
        }

        
        if structure_type in specific_types_map:
            self.specific_type_combobox['values'] = specific_types_map[structure_type]
        else:
            self.specific_type_combobox['values'] = []

       
        self.specific_type_combobox.set("")

class SoilAnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Soil Analysis")

        # Soil Parameters Entry
        self.soil_type_label = tk.Label(root, text="Soil Type (Clay, Sand, Silt, Loam):")
        self.soil_type_label.grid(row=0, column=0)
        self.soil_type_entry = tk.Entry(root)
        self.soil_type_entry.grid(row=0, column=1)

        self.soil_bearing_capacity_label = tk.Label(root, text="Soil Bearing Capacity (kN/m²):")
        self.soil_bearing_capacity_label.grid(row=1, column=0)
        self.soil_bearing_capacity_entry = tk.Entry(root)
        self.soil_bearing_capacity_entry.grid(row=1, column=1)

        self.depth_of_soil_layer_label = tk.Label(root, text="Depth of Soil Layer (m):")
        self.depth_of_soil_layer_label.grid(row=2, column=0)
        self.depth_of_soil_layer_entry = tk.Entry(root)
        self.depth_of_soil_layer_entry.grid(row=2, column=1)

        self.water_table_depth_label = tk.Label(root, text="Water Table Depth (m):")
        self.water_table_depth_label.grid(row=3, column=0)
        self.water_table_depth_entry = tk.Entry(root)
        self.water_table_depth_entry.grid(row=3, column=1)

       
        self.result_label = tk.Label(root, text="Soil Analysis Results:")
        self.result_label.grid(row=4, column=0, columnspan=2)

      
        self.calculate_button = tk.Button(root, text="Calculate", command=self.perform_soil_analysis)
        self.calculate_button.grid(row=5, column=0, columnspan=2)

    def perform_soil_analysis(self):
        try:
            # Get the input values
            soil_type = self.soil_type_entry.get().strip()
            soil_bearing_capacity = float(self.soil_bearing_capacity_entry.get())
            depth_of_soil_layer = float(self.depth_of_soil_layer_entry.get())
            water_table_depth = float(self.water_table_depth_entry.get())

            # Create a SoilAnalysis object
            soil_analysis = SoilAnalysis(soil_type, soil_bearing_capacity, depth_of_soil_layer, water_table_depth)

            # Perform analysis and get results
            result = soil_analysis.display_analysis()

            # Display the results in the label
            self.result_label.config(text=result)

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")

# Main Menu window to select between Soil Analysis or Wind Load Calculation
class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")
        
        self.soil_analysis_button = tk.Button(root, text="Soil Analysis", command=self.start_soil_analysis)
        self.soil_analysis_button.grid(row=0, column=0, pady=10)
        
        self.wind_load_button = tk.Button(root, text="Wind Load Calculation", command=self.start_wind_load_calculator)
        self.wind_load_button.grid(row=1, column=0, pady=10)
    
    def start_soil_analysis(self):
        self.root.destroy()  
        new_root = tk.Tk()
        app = SoilAnalysisGUI(new_root)  
        new_root.mainloop()
    
    def start_wind_load_calculator(self):
        self.root.destroy()
        new_root = tk.Tk()
        app = WindLoadCalculator(new_root)
        new_root.mainloop()

def main():
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
