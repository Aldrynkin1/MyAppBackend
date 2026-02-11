from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
import uuid

from app.content import SCENES, INITIAL_STATE
from app.game_logic import process_move
from app.models import PlayerState, GameRequest, GameResponse, Choice  

app = FastAPI(title='Эдик педик', version='1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game_sessions: Dict[str, Dict[str, Any]] = {} 

def get_condition_texts(scene: Dict[str, Any], player_state: Dict[str, Any]) -> List[str]:
    texts = []
    for condition in scene.get('conditions', []):
        try:
            if condition['check'](player_state):
                texts.append(condition['text'])
        except Exception as e:
            print(f"Ошибка в условии: {e}")
    return texts

@app.post('/api/game/start', response_model=GameResponse) 
async def start_game():
    session_id = str(uuid.uuid4())

    game_sessions[session_id] = {
        'player_state': INITIAL_STATE.copy(),
        'session_id': session_id,
    }
    
    player_state = game_sessions[session_id]['player_state']
    current_scene = SCENES[player_state['current_scene']]

    condition_texts = get_condition_texts(current_scene, player_state)

    return GameResponse( 
        session_id=session_id,
        scene_id=player_state['current_scene'],
        text=current_scene['text'],
        choices=[Choice(**choice) for choice in current_scene.get('choices', [])],
        player_state=PlayerState(**player_state),
        condition_texts=condition_texts,
        event_text='Игра началась.'
    )
    
@app.post("/api/game/move", response_model=GameResponse)
async def make_move(request: GameRequest):
    session_id = request.session_id
    
    if not session_id or session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    
    game_data = game_sessions[session_id]
    player_state = game_data['player_state']
    
    current_scene_id = player_state['current_scene']
    current_scene = SCENES.get(current_scene_id)
    
    if not current_scene:
        raise HTTPException(status_code=400, detail="Сцена не найдена")
    
    choices = current_scene.get('choices', [])
    if request.choice_index < 0 or request.choice_index >= len(choices):
        raise HTTPException(status_code=400, detail="Неверный выбор")
    
    choice_data = choices[request.choice_index]
    
    new_state, event_text, death_reason = process_move(player_state, choice_data, current_scene)
    
    if death_reason:
        death_scene_map = {
            'hunger': 'death_hunger',
            'time': 'death_time',
            'depression': 'death_depression',
            'debt': 'death_unemployed'
        }
        
        next_scene_id = death_scene_map.get(death_reason, 'death_hunger')
        event_text = "Критическое состояние!"
        
        death_state = {
            'is_dirty': new_state.get('is_dirty', True),
            'vibe': new_state.get('vibe', 0),
            'time': new_state.get('time', 0),
            'hungry': new_state.get('hungry', 0),
            'money': new_state.get('money', 500),
            'current_scene': next_scene_id
        }
        new_state = death_state
    else:
        next_scene_id = choice_data['next']
    
    new_state['current_scene'] = next_scene_id
    game_sessions[session_id]['player_state'] = new_state
    
    next_scene = SCENES[next_scene_id]
    condition_texts = get_condition_texts(next_scene, new_state)
    
    return GameResponse(
        session_id=session_id,
        scene_id=next_scene_id,
        text=next_scene['text'],
        choices=[Choice(**choice) for choice in next_scene.get('choices', [])],
        player_state=PlayerState(**new_state),
        condition_texts=condition_texts,
        event_text=event_text
    )

@app.get("/api/game/state/{session_id}", response_model=GameResponse)  
async def get_game_state(session_id: str):
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    
    player_state = game_sessions[session_id]['player_state']
    current_scene = SCENES[player_state['current_scene']]
    
    condition_texts = get_condition_texts(current_scene, player_state)
    
    return GameResponse(  
        session_id=session_id,
        scene_id=player_state['current_scene'],
        text=current_scene['text'],
        choices=[Choice(**choice) for choice in current_scene.get('choices', [])],
        player_state=PlayerState(**player_state),
        condition_texts=condition_texts  
    )