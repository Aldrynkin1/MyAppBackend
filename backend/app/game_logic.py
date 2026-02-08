import random
from typing import Dict, Tuple, Any

def process_move(player_state: Dict[str, Any], choice_data: Dict[str, Any], scene_config: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
    event_text = ""
    event_effects = {}
    
    for event in scene_config.get('random_events', []):
        if random.random() < event['chance']:
            event_text = event.get('text', '' )
            event_effects = event.get('effects', {})

    all_effects = {**choice_data.get('effects', {}), **event_effects}
    
    new_state = player_state.copy()
    
    for key, value in all_effects.items():
        if key in new_state:
            is_numeric = isinstance(value, (int, float)) and isinstance(new_state.get(key), (int, float))
            is_boolean = isinstance(new_state.get(key), bool)

            if is_numeric and not is_boolean:
                new_state[key] += value
            else:
                new_state[key] = value
        else:
            new_state[key] = value
        
    return new_state, event_text