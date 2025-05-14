from pythermalcomfort.models import pmv_ppd_iso
import math

def calculate_thermal_comfort(air_temperature, mean_radiant_temp, air_velocity, 
                            relative_humidity, met, clo):
    """
    Calculate PMV and PPD values using ISO 7730-2005 model
    """
    result = pmv_ppd_iso(
        tdb=air_temperature,
        tr=mean_radiant_temp,
        vr=air_velocity,
        rh=relative_humidity,
        met=met,
        clo=clo,
        model="7730-2005"
    )

    pmv = result.pmv
    ppd = result.ppd

    # Handle nan values
    if math.isnan(pmv) or math.isnan(ppd):
        return "Invalid input", "Invalid input"
    
    return f"{pmv:.2f}", f"{ppd:.1f}"

def get_comfort_recommendations(pmv, ppd, comfort_pmv_min, comfort_pmv_max, comfort_ppd_max):
    """
    Get recommendations based on comfort parameters
    """
    recommendations = []
    if pmv < comfort_pmv_min:
        recommendations.append("• Increase air temperature or clothing insulation")
        recommendations.append("• Reduce air speed")
    elif pmv > comfort_pmv_max:
        recommendations.append("• Decrease air temperature or clothing insulation")
        recommendations.append("• Increase air speed")
    if ppd > comfort_ppd_max:
        recommendations.append("• Adjust humidity levels if possible")
    
    return recommendations 