def calculate_worker_health_index(co_ppm, voc_index, temp_c):
    # CO Thresholds (Based on OSHA: 50ppm is PEL)
    co_score = min(100, (co_ppm / 50) * 100)
    
    # VOC Thresholds (General air quality)
    voc_score = min(100, (voc_index / 300) * 100)
    
    # Thermal Stress (Working in heat)
    temp_score = min(100, max(0, (temp_c - 25) * 4)) 
    
    # Weighted average
    total_index = (0.5 * co_score) + (0.3 * voc_score) + (0.2 * temp_score)
    
    return round(total_index, 2)