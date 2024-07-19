import gurobipy as gp
from gurobipy import GRB
import streamlit as st
import pandas as pd

# Define vehicle types and their capacities for in-house and outsourced
vehicle_types_inhouse = {
    "AXD_55863": 210, "AXD_31638": 210, "AXD_55943": 210, "AXD_30561": 210,
    "AXD_55902": 210, "AXD_43076": 210, "AXD_43057": 210, "AXD_98924": 210,
    "AXD_98921": 210, "AXD_54943": 210, "G_32133": 275, "K_13158": 275,
    "T_39489": 275, "T_39488": 275, "U_82779": 330, "G_37103": 165,
    "G_36541": 165, "J_67680": 165, "J_67497": 165, "O_35933": 165,
    "O_35932": 165, "C_94907": 42, "H_77215": 210, "M_50897": 210,
    "G_94181": 210, "H_64207": 210, "F_72031": 210, "H_21715": 210,
    "M_50896": 210, "K_25743": 210, "T_15770": 210, "T_15771": 210,
    "N_48278": 165, "H_40630": 210, "G_99238": 210, "H_57199": 210,
    "C_73668": 210, "M_49819": 210, "F_69415": 210
}

vehicle_types_outsourced = {
    42: 42, 165: 165, 210: 210, 275: 275, 330: 330
}

# Define routes and permitted vehicle types
routes_vehicles = {
    "R7": ["AXD_55863", "AXD_31638", "AXD_55943", "AXD_30561", "AXD_55902", "AXD_43076", "AXD_43057", "AXD_98924", "AXD_98921", "AXD_54943"],
    "R11": list(vehicle_types_inhouse.keys()),
    "R12/R13": list(vehicle_types_inhouse.keys()),
    "R9": ["G_94181", "C_73668", "F_72031", "O_35932", "J_67497"],
    "R10": list(vehicle_types_inhouse.keys()),
    "R59": list(vehicle_types_inhouse.keys()),
    "R30": list(vehicle_types_inhouse.keys()),
    "R41": list(vehicle_types_inhouse.keys()),
    "R19": list(vehicle_types_inhouse.keys()),
    "R35": list(vehicle_types_inhouse.keys()),
    "R21": list(vehicle_types_inhouse.keys()),
    "R18": list(vehicle_types_inhouse.keys()),
    "R20": list(vehicle_types_inhouse.keys()),
    "R17": list(vehicle_types_inhouse.keys()),
    "R32": list(vehicle_types_inhouse.keys()),
    "R33/R34": list(vehicle_types_inhouse.keys()),
    "R36": list(vehicle_types_inhouse.keys()),
    "R23/R55": list(vehicle_types_inhouse.keys()),
    "R26": list(vehicle_types_inhouse.keys()),
    "R24": list(vehicle_types_inhouse.keys()),
    "R31": list(vehicle_types_inhouse.keys()),
    "R28": list(vehicle_types_inhouse.keys()),
    "R22": list(vehicle_types_inhouse.keys()),
    "R58": list(vehicle_types_inhouse.keys()),
    "R60": list(vehicle_types_inhouse.keys()),
    "R29": list(vehicle_types_inhouse.keys()),
    "R15": ["H_40630", "G_99238", "T_15771", "H_57199", "H_64207", "T_15770"],
    "R16": ["H_40630", "G_99238", "T_15771", "H_57199", "H_64207", "T_15770"],
    "R37": ["H_40630", "G_99238", "T_15771", "H_57199", "H_64207", "T_15770"],
    "R8": ["H_40630", "G_99238", "T_15771", "H_57199", "H_64207", "T_15770"],
    "R38": ["H_40630", "G_99238", "T_15771", "H_57199", "H_64207", "T_15770"],
    "R27": ["H_40630", "G_99238", "T_15771", "H_57199", "H_64207", "T_15770"],
    "R14": list(vehicle_types_inhouse.keys()),
    "R6": ["AXD_55863", "AXD_31638", "AXD_55943", "AXD_30561", "AXD_55902", "AXD_43076", "AXD_43057", "AXD_98924", "AXD_98921", "AXD_54943"],
    "R5/R56": ["AXD_55863", "AXD_31638", "AXD_55943", "AXD_30561", "AXD_55902", "AXD_43076", "AXD_43057", "AXD_98924", "AXD_98921", "AXD_54943"],
    "R3": ["AXD_55863", "AXD_31638", "AXD_55943", "AXD_30561", "AXD_55902", "AXD_43076", "AXD_43057", "AXD_98924", "AXD_98921", "AXD_54943"],
    "R1": ["AXD_55863", "AXD_31638", "AXD_55943", "AXD_30561", "AXD_55902", "AXD_43076", "AXD_43057", "AXD_98924", "AXD_98921", "AXD_54943"],
    "R4": ["AXD_55863", "AXD_31638", "AXD_55943", "AXD_30561", "AXD_55902", "AXD_43076", "AXD_43057", "AXD_98924", "AXD_98921", "AXD_54943"],
    "R25": ["AXD_55863", "AXD_31638", "AXD_55943", "AXD_30561", "AXD_55902", "AXD_43076", "AXD_43057", "AXD_98924", "AXD_98921", "AXD_54943"],
    "R48": list(vehicle_types_inhouse.keys()),
    "R2": ["AXD_55863", "AXD_31638", "AXD_55943", "AXD_30561", "AXD_55902", "AXD_43076", "AXD_43057", "AXD_98924", "AXD_98921", "AXD_54943"],
    "R54": ["AXD_55863", "AXD_31638", "AXD_55943", "AXD_30561", "AXD_55902", "AXD_43076", "AXD_43057", "AXD_98924", "AXD_98921", "AXD_54943"]
}

# Initialize demands
initial_demand = {route: 0 for route in routes_vehicles}

# Streamlit input for demands
st.title("Truck Allocation Optimization")
st.header("Input Demands for Routes")
for route in initial_demand.keys():
    initial_demand[route] = st.number_input(f"Demand for {route}", min_value=0, value=0, step=1)

# Function to solve the truck allocation problem
def solve_truck_allocation(demands):
    # Number of in-house vehicles available
    m = {
        "AXD_55863": 1, "AXD_31638": 1, "AXD_55943": 1, "AXD_30561": 1,
        "AXD_55902": 1, "AXD_43076": 1, "AXD_43057": 1, "AXD_98924": 1,
        "AXD_98921": 1, "AXD_54943": 1, "G_32133": 1, "K_13158": 1,
        "T_39489": 1, "T_39488": 1, "U_82779": 1, "G_37103": 1,
        "G_36541": 1, "J_67680": 1, "J_67497": 1, "O_35933": 1,
        "O_35932": 1, "C_94907": 1, "H_77215": 1, "M_50897": 1,
        "G_94181": 1, "H_64207": 1, "F_72031": 1, "H_21715": 1,
        "M_50896": 1, "K_25743": 1, "T_15770": 1, "T_15771": 1,
        "N_48278": 1, "H_40630": 1, "G_99238": 1, "H_57199": 1,
        "C_73668": 1, "M_49819": 1, "F_69415": 1
    }

    # Initialize the model
    model = gp.Model("truck_allocation")

    # Decision variables
    x = model.addVars(vehicle_types_inhouse, routes_vehicles.keys(), vtype=GRB.BINARY, name="x")  # In-house truck assignment
    L = model.addVars(vehicle_types_inhouse, routes_vehicles.keys(), vtype=GRB.CONTINUOUS, name="L")  # Load carried by in-house trucks
    M = model.addVars(vehicle_types_inhouse, routes_vehicles.keys(), vtype=GRB.INTEGER, name="M")  # Number of in-house trucks assigned
    y = model.addVars(vehicle_types_outsourced, routes_vehicles.keys(), vtype=GRB.BINARY, name="y")  # Outsourced truck assignment
    OL = model.addVars(vehicle_types_outsourced, routes_vehicles.keys(), vtype=GRB.CONTINUOUS, name="OL")  # Load carried by outsourced trucks
    O = model.addVars(vehicle_types_outsourced, routes_vehicles.keys(), vtype=GRB.INTEGER, name="O")  # Number of outsourced trucks assigned
    Z = model.addVars(routes_vehicles.keys(), vtype=GRB.BINARY, name="Z")  # Demand check for routes with less than or equal to 42
    zero_load = model.addVars(vehicle_types_inhouse, routes_vehicles.keys(), vtype=GRB.BINARY, name="zero_load")  # Auxiliary variable

    # Objective function: Minimize unused capacity and use of outsourced trucks
    C = 1e5  # A large number to penalize the use of outsourced trucks
    penalty_zero_load = 1e6  # A large penalty to discourage zero loads
    penalty_outsourced = 1e7  # A large penalty to discourage the use of outsourced trucks
    model.setObjective(
        gp.quicksum((M[i, j] * vehicle_types_inhouse[i] - L[i, j]) for i in vehicle_types_inhouse for j in routes_vehicles) +
        C * gp.quicksum((O[i, j] * vehicle_types_outsourced[i] - OL[i, j]) for i in vehicle_types_outsourced for j in routes_vehicles) +
        penalty_zero_load * gp.quicksum(zero_load[i, j] for i in vehicle_types_inhouse for j in routes_vehicles) +  # Penalize zero loads
        penalty_outsourced * gp.quicksum(y[i, j] for i in vehicle_types_outsourced for j in routes_vehicles),  # Penalize use of outsourced trucks
        GRB.MINIMIZE
    )

    # Constraints
    # Truck assignment constraints
    model.addConstrs((M[i, j] <= x[i, j] for i in vehicle_types_inhouse for j in routes_vehicles), "truck_assignment")
    model.addConstrs((gp.quicksum(M[i, j] for j in routes_vehicles) <= m[i] for i in vehicle_types_inhouse), "truck_availability")
    model.addConstrs((L[i, j] <= vehicle_types_inhouse[i] * M[i, j] for i in vehicle_types_inhouse for j in routes_vehicles), "truck_capacity")

    # Demand fulfillment
    model.addConstrs((gp.quicksum(L[i, j] for i in vehicle_types_inhouse) + gp.quicksum(OL[k, j] for k in vehicle_types_outsourced) == demands[j] for j in routes_vehicles), "demand_fulfillment")

    # Outsourced truck constraints
    model.addConstrs((OL[i, j] <= vehicle_types_outsourced[i] * O[i, j] for i in vehicle_types_outsourced for j in routes_vehicles), "outsourced_capacity")
    model.addConstrs((O[i, j] <= y[i, j] for i in vehicle_types_outsourced for j in routes_vehicles), "outsourced_assignment")

    # Special truck constraints
    model.addConstrs((demands[j] - 42 <= C * (1 - Z[j]) for j in routes_vehicles), "special_truck_demand")
    model.addConstrs((x["C_94907", j] <= Z[j] for j in routes_vehicles), "special_truck_usage")

    # Zero load penalty constraints
    for i in vehicle_types_inhouse:
        for j in routes_vehicles:
            model.addConstr(zero_load[i, j] >= x[i, j] - (L[i, j] / vehicle_types_inhouse[i]))

    # Ensure no trucks are assigned to routes with zero demand
    for j in routes_vehicles:
        if demands[j] == 0:
            model.addConstr(gp.quicksum(x[i, j] for i in vehicle_types_inhouse) + gp.quicksum(y[k, j] for k in vehicle_types_outsourced) == 0)

    # Route constraints for 275 trucks
    routes_275_trucks = ["R35", "R21", "R32", "R33/R34", "R36", "R23/R55"]
    for route in routes_vehicles.keys():
        if route not in routes_275_trucks:
            for vehicle in ["G_32133", "K_13158", "T_39489", "T_39488"]:
                model.addConstr(x[vehicle, route] == 0)
                model.addConstr(y[275, route] == 0)

    # Route constraints for 330 trucks
    routes_330_trucks = ["R35", "R21"]
    for route in routes_vehicles.keys():
        if route not in routes_330_trucks:
            for vehicle in ["U_82779"]:
                model.addConstr(x[vehicle, route] == 0)
                model.addConstr(y[330, route] == 0)

    # Optimize the model
    model.optimize()

    # Check for infeasibility
    if model.status == GRB.INFEASIBLE:
        st.error("Model is infeasible. Check the constraints and demands.")
        return None

    # Mapping of capacities to truck types
    capacity_to_type = {42: "42", 165: "165", 210: "210", 275: "275", 330: "330"}

    # Extract results
    results = []
    for route in routes_vehicles:
        total_inhouse_trucks = 0
        total_inhouse_load = 0
        total_unused_capacity_inhouse = 0

        for vehicle in vehicle_types_inhouse:
            if x[vehicle, route].X > 0.5:
                inhouse_trucks = x[vehicle, route].X
                inhouse_load = L[vehicle, route].X
                unused_capacity = vehicle_types_inhouse[vehicle] - inhouse_load
                total_inhouse_trucks += inhouse_trucks
                total_inhouse_load += inhouse_load
                total_unused_capacity_inhouse += unused_capacity
                results.append([route, vehicle_types_inhouse[vehicle], vehicle, inhouse_load, unused_capacity])

        total_outsourced_trucks = 0
        total_outsourced_load = 0
        total_unused_capacity_outsourced = 0

        for vehicle in vehicle_types_outsourced:
            if y[vehicle, route].X > 0.5:
                outsourced_trucks = y[vehicle, route].X
                outsourced_load = OL[vehicle, route].X
                unused_capacity = vehicle_types_outsourced[vehicle] - outsourced_load
                total_outsourced_trucks += outsourced_trucks
                total_outsourced_load += outsourced_load
                total_unused_capacity_outsourced += unused_capacity
                results.append([route, vehicle_types_outsourced[vehicle], "Outsourced", outsourced_load, unused_capacity])

    results_df = pd.DataFrame(results, columns=["Route", "Vehicle Type", "Vehicle Code", "Load Carried", "Unused Capacity"])
    return results_df

# Solve the truck allocation problem with the input demands
results_df = solve_truck_allocation(initial_demand)

if results_df is not None:
    st.header("Results")
    st.dataframe(results_df)
