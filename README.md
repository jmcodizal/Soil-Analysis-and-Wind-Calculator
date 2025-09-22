# Soil-Analysis-and-Wind-Calculator
WELCOME TO THE SOIL ANALYSIS & WIND LOAD CALCULATOR!

This program allows you to input various parameters of soil and wind load and performs an analysis to evaluate its suitability for construction. It also provide warnings if the calculated values exceed certain safety thresholds, indicating potential risks for the construction project. Our groupmates decided to choose this system because we often see accidents in terms of building any kind infrastractures most especially when natural disaster like storms and typhoons occured.

SOIL ANALYSIS: Soil Type:

1. Select the type of soil from the following options: Clay: Cohesive, sticky, and typically exhibits poor drainage. Sand: Loose, non-cohesive soil that drains water quickly. Silt: Smooth, slippery, and moderately permeable to water. Loam: A balanced mixture of sand, silt, and clay, offering good drainage properties. The chosen soil type influences the soil's behavior under load and the program's calculations.
2. Soil Bearing Capacity (kN/m²): Enter the soil's load-bearing capacity in kilonewtons per square meter (kN/m²). This value indicates how much weight the soil can safely support without failing.
3. Depth of Soil Layer (meters): Specify the thickness of the soil layer (in meters). This depth is used to compute the total load-bearing potential of the soil.
4. Water Table Depth (meters): Indicate the depth of the water table beneath the ground. A high water table can reduce soil stability and its ability to support structures.

Once the above inputs are provided, the program performs the following calculations and analyses:

1. Soil Bearing Capacity Evaluation: Determines whether the soil has a low, medium, or high bearing capacity based on its characteristics and depth.
2. Settlement Estimation: Estimates the potential settlement (movement or sinking) of the foundation due to the applied load, ensuring it remains within acceptable limits.
3. Lateral Earth Pressure Coefficient: Calculates the lateral pressure exerted by the soil on structures like retaining walls using advanced geotechnical principles.
4. Water Table Effect: Evaluates the influence of the water table depth on soil stability and highlights whether it poses a risk to the foundation's integrity.

WIND LOAD ANALYSIS:

1. Wind Speed (m/s): Input the wind speed in meters per second (m/s). This value is used to calculate the dynamic pressure (q) exerted by the wind on the structure.
2. Exposure Category (A, B, C, D, E, F): Select the exposure category that best describes the surrounding environment to determine the gust factor (G): A: Open water or flat terrain with few obstructions. B: Suburban terrain with scattered buildings and trees. C: Urban areas with dense buildings and obstacles. D: Open terrain with no obstructions. E: Intermediate areas with moderate density. F: Areas with very high density or tall structures.
3. Structural Shape: Choose the structure's shape to determine the drag coefficient (Cd). Available options include: Rectangular: Cd=1.3 Cylindrical: Cd=0.6 Spherical: Cd=0.47 Additional shapes like triangular, dome, parabolic, and others are also available, each with a specific Cd value.
4. Area Exposed to Wind (m²): Enter the area (in square meters) of the structure that is directly exposed to the wind.
5. Building Structure Type: Specify the type of structure (e.g., residential, commercial, industrial, etc.). The program uses this information to set acceptable wind load limits for the structure.

Once the above inputs are provided, the program performs the following calculations and analyses:

1. Wind Load Calculation: The program calculates the total wind load using the formula: Wind Load=q×G×Cd×Area where: q: Dynamic pressure based on wind speed. G: Gust factor from the exposure category. Cd: Drag coefficient from the structural shape. Area: Exposed area of the structure.
2. Load Evaluation: The calculated wind load is compared to the acceptable limits for the specified building type. Alerts and recommendations are provided if: The wind load exceeds safety thresholds, indicating reinforcement may be necessary. The wind load is approaching the safety limit, suggesting closer monitoring of the structure.
