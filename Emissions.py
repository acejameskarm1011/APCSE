from scipy import constants




CO2 = 3053.40482195453

Climb = {
    # g/kg
    "Take-Off" : 925,
    "Climb" : 925,
    "Cruise" : 146,
    "Descent" : 1003,
    "Final" : 1003,
    "Taxi" : 657,
	"Idle" : 649
}

HC = {
    "Take-Off" : 44.3,
    "Climb" : 44.3,
    "Cruise" : 51.5,
    "Descent" : 48.4,
    "Final" : 48.4,
    "Taxi" : 53.8,
	"Idle" : 121.5
}

NOx = {
    "Take-Off" : 3.2,	
    "Climb" : 3.2,
    "Cruise" : 52.2,
    "Descent" : 0.7,
    "Final" : 0.2,
    "Taxi" : 2.5,
	"Idle" : 0.2
}

PM = {
    "Take-Off" : 0.093,	
    "Climb" : 0.093,
    "Cruise" : 0.144,
    "Descent" : 0.493,
    "Final" : 0.493,
    "Taxi" : 0.051,
	"Idle" : 0.046
}

eGrid = {
    # g/MJ
    "CO2" : 0.134527827333333,

    "CH4" : 0.00001247378,

    "N2O" : 1.76396888888889E-06

}

def Pb_Emissions(Fuel_mass):
    """
    Get the amount of lead emissions in units of grams [g]

    Paramters
    ---------
    Fuel_mass : int/float
        In units of kg, input the mass of burned fuel

    Returns 
    ------
    Pb_mass : int/float
        In units of g, returns the total mass of burned lead
    """
    Pb_retention = 5/100 # %
    Pb_content = 2.12 # g/gal
    Gas_density = 6 # lb/gal

    Pb_mass = (1-Pb_retention) * (Fuel_mass) * (Pb_content/(Gas_density*constants.lb))
    return Pb_mass


def Emissions(Mass, Energy, Mission, Particle = "ALL"):
    """
    Get the amount of all emissions [CO2, CH4, NOx, Pb] in units of grams [g]

    Paramters
    ---------
    Mass : int/float
        In units of kg, input the mass of burned fuel

    Energy : int/float
        In units of J, input the energy used

    Mission : str
        Phase of the mission that the aircraft is currently in, since the particle factor is based on the aircraft's current phase in its mission

    Returns 
    ------
    Emission_masses : list
        In units of g, returns the total mass of burned carbon dioxide, methane, nitrous oxide, and lead
    """
    Energy /= 1e6
    if Mission == "Landing":
        Mission = "Idle"

    CO2_mass = Mass*CO2 + Energy*eGrid["CO2"]
    CH4_mass = Mass*HC[Mission] + Energy*eGrid["CH4"]
    NOx_mass = Mass*NOx[Mission] + Energy*eGrid["N2O"]
    Pb_mass = Pb_Emissions(Mass)

    Emission_masses = []

    if Particle == "ALL":
        Emission_masses = [CO2_mass, CH4_mass, NOx_mass, Pb_mass]
    
    return Emission_masses

