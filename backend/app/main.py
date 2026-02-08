from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
import uuid

from app.content import SCENES, INITIAL_STATE
from app.game_logic import process_move
from app.models import PlayerState, GameRequest, GameResponce, Choice

app = FastAPI(title='Сюжетка моя' , version='1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game_session: Dict[str, Dict[str, Any]] = {}

def get_condition_texts(scene: Dict[str, Any], player_state: Dict[str, Any]) -> List[str]:
    texts = []
    for condition in scene.get('conditions', []):
        try:
            if condition['check'](player_state):
                texts.append(condition['text'])
        except:
            pass
    return texts

@app.post('/api/game/start', response_model=GameResponce)
async def start_game():
    session_id = str(uuid.uuid4())

    game_session[session_id] = {
        'player_state': INITIAL_STATE.copy(),
        'session_id': session_id,
    }
    
    player_state = game_session[session_id]['player_state']
    current_scene = SCENES[player_state['current_scene']]

    condition_texts = get_condition_texts(current_scene, player_state)

    return GameResponce(
        session_id=session_id,
        scene_id = player_state['current_scene'],
        text = current_scene['text'],
        choices = [Choice(**choice) for choice in current_scene.get('choices', [])],
        player_state = PlayerState(**player_state),
        conditions_texts = condition_texts,
        event_text = 'Игра началась.'
    )
    
@app.post("/api/game/move", response_model=GameResponce)
async def make_move(request: GameRequest):
    """Сделать ход в игре"""
    session_id = request.session_id
    
    if not session_id or session_id not in game_session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    
    game_data = game_session[session_id]
    player_state = game_data['player_state']
    
    current_scene_id = player_state['current_scene']
    current_scene = SCENES.get(current_scene_id)
    
    if not current_scene:
        raise HTTPException(status_code=400, detail="Сцена не найдена")
    
    choices = current_scene.get('choices', [])
    if request.choice_index < 0 or request.choice_index >= len(choices):
        raise HTTPException(status_code=400, detail="Неверный выбор")
    
    choice_data = choices[request.choice_index]
    
    new_state, event_text = process_move(player_state, choice_data, current_scene)
    
    new_state['current_scene'] = choice_data['next']
    game_session[session_id]['player_state'] = new_state
    
    next_scene = SCENES[choice_data['next']]
    
    condition_texts = get_condition_texts(next_scene, new_state)
    
    return GameResponce(
        session_id=session_id,
        scene_id=choice_data['next'],
        text=next_scene['text'],
        choices = [Choice(**choice) for choice in next_scene.get('choices', [])], 
        player_state=PlayerState(**new_state),
        condition_texts=condition_texts,
        event_text=event_text
    )

@app.get("/api/game/state/{session_id}", response_model=GameResponce)
async def get_game_state(session_id: str):
    """Получить текущее состояние игры"""
    if session_id not in game_session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    
    player_state = game_session[session_id]['player_state']
    current_scene = SCENES[player_state['current_scene']]
    
    condition_texts = get_condition_texts(current_scene, player_state)
    
    return GameResponce(
        scene_id=player_state['current_scene'],
        text=current_scene['text'],
        choices=[Choice(**choice) for choice in current_scene.get('choices', [])],
        player_state=PlayerState(**player_state),
        condition_texts=condition_texts
    )

@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в текстовую игру API!",
        "endpoints": {
            "start_game": "POST /api/game/start",
            "make_move": "POST /api/game/move",
            "get_state": "GET /api/game/state/{session_id}"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}