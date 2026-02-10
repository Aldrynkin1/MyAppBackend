import random
from typing import Dict, Tuple, Any, Optional

def process_move(player_state: Dict[str, Any], choice_data: Dict[str, Any], scene_config: Dict[str, Any]) -> Tuple[Dict[str, Any], str, Optional[str]]:
    event_text = ""
    event_effects = {}
    
    for event in scene_config.get('random_events', []):
        if random.random() < event['chance']:
            event_text = event.get('text', '')
            event_effects = event.get('effects', {})

    all_effects = {**choice_data.get('effects', {}), **event_effects}
    
    new_state = player_state.copy()
    
    for key, value in all_effects.items():
        if key in new_state:
            current_value = new_state[key]
            
            if isinstance(current_value, bool):
                new_state[key] = value
            elif isinstance(current_value, (int, float)) and isinstance(value, (int, float)):
                new_state[key] = current_value + value
            else:
                new_state[key] = value
        else:
            new_state[key] = value
    
    death_reason = None
    
    if new_state.get('hungry', 0) > 100:
        death_reason = 'hunger'
    elif new_state.get('time', 0) > 1200:  
        death_reason = 'time'
    elif new_state.get('vibe', 0) < -100:
        death_reason = 'depression'
    elif new_state.get('money', 0) < -500:  
        death_reason = 'debt'
    
    return new_state, event_text, death_reason