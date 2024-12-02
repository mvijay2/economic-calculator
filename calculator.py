import streamlit as st
import pandas as pd

def calculate_costs(initial_cost, annual_usage, operator_wages, field_capacity, usefull_life,b): #initial cost=rs, annual usage=hours, operator_wages=rs/d, field capaccity=ha/hr

    # Constants
    salvage_cost = 0.1 * initial_cost  # Assume 10% of initial cost done
    life =  usefull_life # years done
    interest_rate = 0.1  # 10% done
    hours_per_year = annual_usage #done
    
    # Fixed Costs
    depreciation = (initial_cost - salvage_cost) / (life * hours_per_year) 
    interest_on_capital = ((initial_cost + salvage_cost) /(hours_per_year * 2)) * interest_rate
    insurance_and_taxes = (initial_cost * 0.015) / hours_per_year
    housing = (initial_cost * 0.005) / hours_per_year
    total_fixed_cost = depreciation + interest_on_capital + insurance_and_taxes + housing #done
    
    ## Variable Cost
    #p=st.selection['battery, petrol, diesel']
    #if p == 'bettery':
    #    return 
    
    if b == "diesel":
        battery_charging = 100
    elif b == "petrol":
        battery_charging = 110
    else:
        battery_charging = 15 # Assume constant Rs/h                to do
    lubrication = battery_charging * 0.1  # Assume constant Rs/h     10% of fuel cost                  to do
    repair_and_maintenance = (initial_cost * 0.05) / hours_per_year   # again done
    total_variable_cost = battery_charging + lubrication + repair_and_maintenance + operator_wages #done
    
    # Operating Costs
    total_operating_cost = total_fixed_cost + total_variable_cost #done rs/hr
    
    total_operating_cost_rs_ha = total_operating_cost / field_capacity #done rs/ha

    # Custom Hiring Cost
    custom_hiring = (total_operating_cost + (total_operating_cost * 0.25))
    custom_hiring_cost = custom_hiring + (custom_hiring * 0.25) # Adding 25% profit margin
 # Adding 50% profit margin
    
    # Breakeven Cost
    breakeven_Point = (total_fixed_cost * hours_per_year)/(custom_hiring_cost-total_operating_cost) #hr/yr
    
    # Payback Period
    payback_period = initial_cost / ((custom_hiring_cost - total_operating_cost) *hours_per_year)
    
    return custom_hiring_cost, breakeven_Point, payback_period, total_operating_cost, total_operating_cost_rs_ha

# Streamlit app
try:
    st.title("Cost Economics Calculator")
    col1, col2 = st.columns(2)
    with col1:
        
        # User inputs
        initial_cost = st.number_input("Initial Cost (Rs)", min_value=100, max_value=10000000, step=1000)
        annual_usage = st.number_input("Annual Usage (Hours)", min_value=1, max_value=1000, step=1)
        operator_wages = st.number_input("Operator Wages (Rs/day)", min_value=1,max_value=100000, step=1)
        operator_wages_per_hr=operator_wages/8
        
    with col2:
        field_capacity = st.number_input("Field Capacity (Acre/h)", min_value=0.1, max_value=1000.0, step=0.1)
        #usefull_life = st.sidebar.number_input("usefull_life (yr)", min_value=1, max_value=1000, step=1)
        usefull_life=st.number_input("usefull_life (yr)")
        b=st.selectbox("Charging Type", ["Battery", "petrol", "diesel"])
        submitted = st.button("Calculate")
        
    if submitted: 
    
    
    
        # Calculate costs
        custom_hiring_cost, breakeven_Point, payback_period, total_operating_cost, total_operating_cost_rs_ha = calculate_costs(
            initial_cost, annual_usage, operator_wages_per_hr, field_capacity, usefull_life,b
        )
        
        # Display results  add total 
            # Prepare results in a DataFrame for tabular display
        results = {
            "Metric": ["Total Operating Cost (Rs/hr)", "Custom Hiring Cost (Rs/hr)", "Breakeven Point (hours/year)", "Payback Period (years)"],
            "Value": [total_operating_cost, custom_hiring_cost, breakeven_Point, payback_period]
        }    
        results_df = pd.DataFrame(results)    
        # Display results in a table
        st.table(results_df)
except ZeroDivisionError:
    st.error("give a valid value")