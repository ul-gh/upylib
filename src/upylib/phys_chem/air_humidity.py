# Source: https://www.wufi-forum.com/viewtopic.php?t=1615
# Source: https://de.wikipedia.org/wiki/Sättigungsdampfdruck
import math

def water_p_sat(t):
    """Saturated water vapour pressure in hPa
    Magnus formula coefficients accurate for t = -45°C...60°C
    According to https://de.wikipedia.org/wiki/Sättigungsdampfdruck
        t: Temperture in °C
    """
    assert -45 <= t <=60, "Definition range is -45°C ... 60°C only!"
    C1 = 6.112 # hPa
    C2 = 17.62 # 1
    C3 = 243.12 # °C
    return C1 * math.exp((C2*t)/(C3+t))

def air_p_w(rh, t):
    """Partial pressure of water in humid air based on relative humidity, in hPa
        rh: relative humidity in %
        t: temperature in °C
    """
    return rh/100.0 * water_p_sat(t)


def air_dew_point_pw(p_w):
    """Humid air dew point temperature in °C based on water partial pressure
    (inverse of magnus formula)
        p_w: Partial pressure of water in humid air, in hPa
    """
    C1 = 6.112 # hPa
    C2 = 17.62 # 1
    C3 = 243.12 # °C
    return C3 * math.log(p_w/C1) / (C2 - math.log(p_w/C1))

def air_dew_point(rh, t):
    """Humid air dew point temperature in °C, based on
    relative humidity at given temperature
        rh: relative humidity in %
    """
    return air_dew_point_pw(air_p_w(rh, t))

def air_abs_hum_vol(rh, t):
    """Per-volume absolute humidity in g/m³, based on
    relative humidity at given temperature.
        rh: relative humidity in %
        t: temperature in °C
    """
    # molar mass of water
    M_water = 18.016
    # universal gas constant
    R_gas = 8314.3
    # absolute temperature at 0°C
    T_zero = 273.15
    return 1E5 * M_water / R_gas * air_p_w(rh, t)/(t + T_zero)

def air_x_w(rh, t, p=1013):
    """Water mass fraction based on relative humidity, in g/kg (promille)
        p: air pressure in hPa
        rh: relative humidity in %
        t: temperature in °C
    """
    # water molar fraction acc. to Dalton's law
    # y_water = n_water/(n_water + n_air) = p_water/(p_water + p_air) = p_water/p
    # x_water = n_water*M_water / (n_water*M_water + n_air*M_dry_air)
    # n_air = n_water * (1-y_water)/y_water = n_water * (p/p_water - 1)
    # x_water = M_water / (M_water + (p/p_water - 1)*M_dry_air)
    # molar mass of water
    M_water = 18.016
    # molar mass of dry air (standard atmosphere)
    M_dry_air = 28.9644
    return 1000 * M_water / (M_water + (p/air_p_w(rh, t) - 1) * M_dry_air)