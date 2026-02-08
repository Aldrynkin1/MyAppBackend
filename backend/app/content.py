SCENES = {
    'start': {
        'text': 'Ты проснулся.',
        'conditions': [{
            'check': lambda state: state['time'] > 540,
            'text': 'Опаздываешь на работу. Пора вставать',
        }],
        'random_events': [{
            'chance': 0,
            'text': '',
            'effects': {}
        }],
        'choices': [
            {'text': 'Открыть глаза', 'next': 'your_room', 'effects': {'is_dirty': True, 'vibe': 0, 'time': 0, 'hungry': 0, 'money': 500}},
            {'text': 'Спать дальше', 'next': 'start', 'effects': {'vibe': 5, 'time': 90, 'hungry': 5}},
        ],
    },
    
    'your_room': {
        'text': 'Ты в своей комнате. Тебе тут все так приелось.',
        'choices': [
            {'text': 'Пойти умыться', 'next': 'bathroom', 'effects': {'vibe': 1, 'time': 5, 'hungry': 1}},
            {'text': 'Пойти позавтракать', 'next': 'kitchen', 'effects': {'vibe': 0, 'time': 1, 'hungry': 0}}
        ],
    },
    
    'bathroom': {
        'text': 'Ты в ванной. После умывания твое зеркало запотело, но тебя это не волнует',
        'choices': [
            {'text': 'Умыться', 'next': 'mirror', 'effects': {'is_dirty': False, 'vibe': 10, 'time': 5, 'hungry': 1}},
        ],
    },
    
    'mirror': {
        'text': 'Вроде бы сегодня выгляжу неплохо...',
        'choices': [
            {'text': 'Пора бы позавтракать', 'next': 'kitchen', 'effects': {'vibe': 5, 'time': 1, 'hungry': 1}},
        ],
    },
    
    'kitchen': {
        'text': 'Ты на кухне. Пахнет старым кофе... что съешь на завтрак?',
        'choices': [
            {'text': 'Я не голоден', 'next': 'now_room', 'effects': {'hungry': 10, 'vibe': -5}},
            {'text': 'Доширак', 'next': 'now_room', 'effects': {'hungry': -10, 'time': 15}},
            {'text': 'Творог с молоком', 'next': 'now_room', 'effects': {'hungry': -20, 'time': 10}},
        ],
    },
    
    'now_room': {
        'text': 'Пора на работу...',
        'conditions': [
            {'check': lambda state: state['is_dirty'] == True, 'text': 'Ты понимаешь, что от тебя пахнет... Соседи в лифте будут недовольны.'},
            {'check': lambda state: state['hungry'] > 70, 'text': 'Твой живот урчит так, что ты не можешь это игнорировать'},
            {'check': lambda state: state['time'] > 540, 'text': 'Ты опаздываешь... Пора придумать отмазку.'},
        ],
        'choices': [
            {'text': 'Одеться', 'next': 'hall', 'effects': {'vibe': -5, 'time': 5}},
            {'text': 'Сказать боссу, что заболел', 'next': 'start', 'effects': {'vibe': 5, 'time': 1200, 'hungry': 30, 'is_dirty': True}},
        ],
    },
    
    'hall': {
        'text': 'Ты в коридоре.',
        'conditions': [
            {'check': lambda state: state['vibe'] < 10, 'text': 'Да уж... Утро как-то не задалось.'},
            {'check': lambda state: state['hungry'] > 70, 'text': 'Еще и голодный как не знаю кто... Ладно, по пути в магазине что-нибудь прихвачу.'},
        ],
        'random_events': [{
            'chance': 0.2,
            'text': 'У вас заболела голова',
            'effects': {'vibe': -5},
        }],
        'choices': [
            {'text': 'Выйти из дома', 'next': 'lift', 'effects': {'vibe': -1, 'time': 5}},
        ],
    },
    
    'lift': {
        'text': 'Ты в лифте.',
        'conditions': [
            {'check': lambda state: state['vibe'] < 10, 'text': 'Соседи видят, что у тебя плохое настроение.'},
            {'check': lambda state: state['is_dirty'] == True, 'text': 'Соседи прикрыли носы от твоего запаха. Тебе стало стыдно.'},
            {'check': lambda state: state['time'] >= 540, 'text': 'Ты в ужасном настроении, ведь, несмотря на все остальное, ты еще и опаздываешь.'},
        ],
        'choices': [
            {'text': 'Ты выходишь на улицу', 'next': 'street', 'effects': {'vibe': -1, 'time': 2}},
        ],
    },
    
    'street': {
        'text': 'Вы идете на работу, которую ненавидите.',
        'conditions': [
            {'check': lambda state: state['hungry'] > 70, 'text': 'Надо бы зайти купить себе перекусить.'},
        ],
        'random_events': [{
            'chance': 0.1,
            'text': 'Вы подвернули ногу. Впредь будьте аккуратнее.',
            'effects': {'vibe': -5, 'time': 5}
        }],
        'choices': [
            {'text': 'Зайти в магазин.', 'next': 'shop', 'effects': {'time': 5}},
            {'text': 'Идти на работу голодным', 'next': 'job', 'effects': {'hungry': 5, 'vibe': -5}}
        ],
    },
}

INITIAL_STATE = {
    'is_dirty': True,
    'vibe': 0,
    'time': 0,
    'hungry': 0,
    'money': 500,
    'current_scene': 'start'
}