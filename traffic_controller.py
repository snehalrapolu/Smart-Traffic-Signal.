"""
Traffic Signal Controller Module
Calculates green time allocation based on traffic density.
"""
from typing import Dict, Tuple


def calculate_green_times(densities: Dict[str, float], 
                         min_green_time: int = 5,
                         max_green_time: int = 30,
                         total_cycle_time: int = 60) -> Dict[str, int]:
    """
    Calculates green time for each road based on traffic density.
    
    Algorithm:
    1. Sum all densities
    2. Allocate green time proportional to each road's density
    3. Enforce minimum green time to prevent starvation
    4. Normalize to fit within total cycle time
    
    Args:
        densities: Dictionary mapping road names to density scores (0.0-1.0)
        min_green_time: Minimum green time in seconds (default: 5)
        max_green_time: Maximum green time in seconds (default: 30)
        total_cycle_time: Total cycle time in seconds (default: 60)
        
    Returns:
        Dictionary mapping road names to green time in seconds
    """
    if not densities:
        return {}
    
    # Calculate total density
    total_density = sum(densities.values())
    
    if total_density == 0:
        # If no traffic detected, allocate equal time to all roads
        equal_time = total_cycle_time // len(densities)
        return {road: max(min_green_time, equal_time) for road in densities.keys()}
    
    # Calculate proportional green times
    green_times = {}
    for road, density in densities.items():
        # Proportional allocation
        proportional_time = (density / total_density) * total_cycle_time
        
        # Enforce minimum and maximum bounds
        green_time = max(min_green_time, min(max_green_time, proportional_time))
        green_times[road] = int(green_time)
    
    # Normalize to ensure total doesn't exceed cycle time
    total_allocated = sum(green_times.values())
    if total_allocated > total_cycle_time:
        # Scale down proportionally
        scale_factor = total_cycle_time / total_allocated
        green_times = {road: int(time * scale_factor) for road, time in green_times.items()}
        
        # Ensure minimum times are still met
        for road in green_times:
            if green_times[road] < min_green_time:
                green_times[road] = min_green_time
    
    return green_times


def select_active_road(densities: Dict[str, float]) -> str:
    """
    Selects the road with highest traffic density to receive green signal.
    
    Args:
        densities: Dictionary mapping road names to density scores
        
    Returns:
        Name of the road with highest density
    """
    if not densities:
        return "North"  # Default
    
    return max(densities.items(), key=lambda x: x[1])[0]


def get_signal_states(active_road: str, roads: list) -> Dict[str, str]:
    """
    Returns the signal state (RED/GREEN) for each road.
    
    Args:
        active_road: The road currently receiving green signal
        roads: List of all road names
        
    Returns:
        Dictionary mapping road names to signal states ("RED" or "GREEN")
    """
    states = {}
    for road in roads:
        states[road] = "GREEN" if road == active_road else "RED"
    return states

