from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class PlayerState(BaseModel):
    is_dirty: bool = True
    vibe: int = 0
    time: int = 0
    hungry: int = 0
    money: int = 500
    current_scene: str = "start"
    inventory: List[InventoryItems] = []
    max_inventory_size: int = 10
    
class Choice(BaseModel): 
    text: str
    next: str
    effects: Optional[Dict[str, Any]] = {}

class GameRequest(BaseModel):
    session_id: Optional[str] = None
    choice_index: int
    
class GameResponse(BaseModel):
    scene_id: str
    text: str
    choices: List[Choice]
    player_state: PlayerState
    event_text: Optional[str] = ''
    conditions_text: Optional[List[str]] = []
    session_id: str
    inventory: List[InventoryItems] = []
    
class InventoryItems(BaseModel):
    id: str
    name: str
    description: str
    usable: bool = True
    value: int = 0