elec_cost_stack={ "wholesale":12.0, "network": 6.5, "policy":2, "operating": 3.0, "margin":1.5}
total =0.0 
for component in elec_cost_stack.values():
    total = total + component
print(f"Total electricity cost: {total:.2f}p per/kWh")

gas_cost_stack={"wholesale": 4.2, "network": 1.4, "policy": 0.4, "operating": 0.7, "margin": 0.3}
gas_total=0.0
for component in gas_cost_stack.values():
    gas_total = gas_total + component
print(f"Total gas cost: {gas_total:.2f}p per/kWh")

# Typical Consumptions + Standing charges per Ofgem's figures for average homes (from 01 Jul'26)

ELEC_CONSUMPTION_KWH = 2500
GAS_CONSUMPTION_KWH = 9500
DAYS_IN_YEAR = 365

ELEC_STANDING_CHARGES = 57.19
GAS_STANDING_CHARGES = 29.04

def annual_bill(unit_rate, standing_charges, consumption_kwh):
    energy_cost= unit_rate * consumption_kwh
    standing_cost=standing_charges * DAYS_IN_YEAR
    total_cost = energy_cost + standing_cost
    return round(total_cost/100, 2)

elec_bill = annual_bill(total, ELEC_STANDING_CHARGES, ELEC_CONSUMPTION_KWH)
gas_bill = annual_bill(gas_total, GAS_STANDING_CHARGES, GAS_CONSUMPTION_KWH)
dual_bill = round (elec_bill + gas_bill, 2)

print(f"\n Electricity annual bill: £{elec_bill:,.2f}")
print(f" Gas annual bill: £{gas_bill:,.2f}")
print(f" Dual fuel annual bill: £{dual_bill:,.2f}")


#Real Ofgem cap rates for 01 Jul'26
CAP_ELEC_RATE = 26.11
CAP_GAS_RATE = 7.33
CAP_ELEC_STANDING_CHARGE = 57.19
CAP_GAS_STANDING_CHARGE = 29.04

cap_elec_bill=annual_bill(CAP_ELEC_RATE, CAP_ELEC_STANDING_CHARGE, ELEC_CONSUMPTION_KWH)
cap_gas_bill=annual_bill(CAP_GAS_RATE, CAP_GAS_STANDING_CHARGE, GAS_CONSUMPTION_KWH)
cap_total=round(cap_elec_bill + cap_gas_bill, 2)

headroom = round(cap_total - dual_bill, 2)
if dual_bill <= cap_total:
    status = "Under Cap - Compliant"
else:
    status = "Over Cap - Non-Compliant"
print(f"\n Ofgem cap annual bill: £{cap_total:,.2f}")
print(f" Our tariff: £{dual_bill:,.2f}")
print(f" Headroom: £{headroom:,.2f}")
print(f" Status: {status}")


# Calculating ehere does tariff crosses the cap

print(f"\n {'Wholesale move': <16} {'Our bill': >10} {'Headroom': >10}")
crossover=None
for pct in range(0,21):
    move=pct/100

    shocked_elec_prices = total+(elec_cost_stack["wholesale"]*move)
    shocked_gas_prices = gas_total+(gas_cost_stack["wholesale"]*move)

    new_elec_bill = annual_bill(shocked_elec_prices, ELEC_STANDING_CHARGES, ELEC_CONSUMPTION_KWH)
    new_gas_bill = annual_bill(shocked_gas_prices, GAS_STANDING_CHARGES, GAS_CONSUMPTION_KWH)
    new_total= round(new_elec_bill + new_gas_bill, 2)
    new_headroom = round(cap_total - new_total, 2)
    if pct % 2==0:
        print(f" +{pct:<15}% £{new_total:>8,.2f} £{new_headroom:>8,.2f}")
        if new_headroom <0 and crossover is None:
            crossover=pct
if crossover:
    print(f"\n Our tariff breaches the cap at +{crossover}% wholesale price increase")