import math
import fluids

viscosity_water_20 = 1001.61e-6
rho_water_20 = 998.206


def v_flow(Q_l_min, Di_mm):
    """Returns flow in m/s
    
    Parameters:
        Q_l_min: Flow in liters per minute
        Di_mm: Inner diameter in mm
    """
    A_mm2 = 1/4 * math.pi * Di_mm ** 2
    return Q_l_min / (60e-3 * A_mm2)

def reynolds(v_f, rho, Di_mm, viscosity_dyn):
    """Returns reynolds number
    
    Parameters:
        v_f: flow in m/s
        rho: fluid density in kg/m³ (!) (1000 for water)
        viscosity_dyn: fluid dynamic viscosity in Pa*s = kg*m/s
    """
    return rho * v_f * Di_mm/1000.0 / viscosity_dyn

def pipe_friction_lambda(Re, eD, rel_tol=1e-12):
    """Darcy friction factor for flow in smooth and rough conduits
    
    Parameters:
        Re: reynolds number
        eD: Pipe relative roughness eD = k/Di with absolute roughness k
    
    Uses the Colebrook and White formula according to:
    https://de.wikipedia.org/wiki/Rohrreibungszahl
    
    This iterates a thousand times maximum; convergence should happen much sooner than that
    """
    def inv_lambda_sqrt_next(inv_lambda_sqrt_prev, Re, eD):
        return -2 * math.log10(inv_lambda_sqrt_prev * 2.51 / Re + eD/3.71)
    if math.isclose(Re, rel_tol):
        print("Reynolds number is close to zero, this is not plausible")
        return math.nan
    # For laminar flow:
    if Re < 2300:
        return 64 / Re
    # Turbulent flow - this is the Colebrook and White formula which is valid for flow in smooth
    # and rough conduits but has limited accuracy between 2300 < Re < 4000
    inv_lambda_sqrt = inv_lambda_sqrt_next(1e-15, Re, eD)
    for i in range(1, 1001):
        previous_value = inv_lambda_sqrt
        inv_lambda_sqrt = inv_lambda_sqrt_next(inv_lambda_sqrt, Re, eD)
        if math.isclose(inv_lambda_sqrt, previous_value, rel_tol=rel_tol):
            rel_error = inv_lambda_sqrt / previous_value - 1.0
            print(f"Succeeded iteration after {i} cycles! Relative error: {rel_error}")
            break
    if i == 1000:
        rel_error = inv_lambda_sqrt / previous_value - 1.0
        print(f"Warning: Iteration error limit not reached after {i} cycles! Abs. relative error: {rel_error}")
    return 1 / inv_lambda_sqrt ** 2

def pipe_zeta(l_m, Di_mm, friction_lambda):
    """Calculates zeta number from Darcy friction number and pipe dimensions
    
    Parameters:
        l_m: length in meters
        Di_mm: Inner diameter in mm
    """
    return friction_lambda * l_m * 1000.0/Di_mm

def pipe_delta_p_mbar(l_m, Di_mm, Q_l_min, k_mm, rho, viscosity_dyn):
    """Returns pipe pressure loss in mBar, using the Darcy friction factor
    
    Parameters:
        l_m: length in meters
        Di_mm: Inner diameter in mm
        Q_l_min: Flow in liters per minute
        k_mm: Absolute roughness in mm
        rho: fluid density in kg/m³ (!) (1000 for water)
        viscosity_dyn: fluid dynamic viscosity in Pa*s = kg*m/s
    """
    v_f = v_flow(Q_l_min, Di_mm)
    Re = reynolds(v_f, rho, Di_mm, viscosity_dyn)
    eD = k_mm / Di_mm
    pipe_friction = pipe_friction_lambda(Re, eD)
    zeta = pipe_zeta(l_m, D_i_mm, pipe_friction)
    return 1/100 * zeta * rho/2.0 * v_f**2

def test_pressure_loss():
    """Expected output:
    
    v_f: 1.0185916357881302
    Re: 25378.248080428664
    friction_lambda: 0.02511292846918426
    zeta: 14.063239942743188
    delta_p_mbar: 72.82420934959733
    """
    Q_l_min = 6
    Di_mm = 25
    l_m = 14
    viscosity_dyn = 1001.61E-6
    rho = 998.206
    k_mm = 0.007

    v_f = v_flow(Q_l_min, Di_mm)
    Re = reynolds(v_f, rho, Di_mm, viscosity_dyn)
    eD = k_mm / Di_mm

    print("Preconditions:\n"
          f"Flow: {Q_l_min} liter/minute"
          f"v_f: {v_f}\n"
          f"Re: {Re}\n"
          )

    # Using the functions implemented here:
    pipe_friction = pipe_friction_lambda(Re, eD)
    zeta = pipe_zeta(l_m, Di_mm, pipe_friction)
    delta_p_mbar = pipe_delta_p_mbar(l_m, Di_mm, Q_l_min, k_mm, rho, viscosity_dyn)
    print("\n\nCalculation implemented here results:\n\n"
          f"friction_lambda: {pipe_friction}\n"
          f"zeta: {zeta}\n"
          f"delta_p_mbar: {delta_p_mbar}\n"
          )

    # Using the Python "fluids" package
    pipe_friction = fluids.friction.friction_factor(Re, eD)
    zeta = pipe_zeta(l_m, Di_mm, pipe_friction)
    delta_p_mbar = pipe_delta_p_mbar(l_m, Di_mm, Q_l_min, k_mm, rho, viscosity_dyn)
    print('\n\nCalculation using "fluids" Python package:\n\n'
          f"friction_lambda: {pipe_friction}\n"
          f"zeta: {zeta}\n"
          f"delta_p_mbar: {delta_p_mbar}"
          )
