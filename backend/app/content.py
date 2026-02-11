INITIAL_STATE = {
    'is_dirty': True,
    'vibe': 0,
    'time': 480,
    'hungry': 50,
    'money': 500,
    'current_scene': 'start'
}

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
            {'text': 'Открыть глаза', 'next': 'your_room', 'effects': {'is_dirty': True, 'vibe': 0, 'time': 0, 'hungry': 0, 'money': 0}},
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
    'shop': {
        'text': 'Вы в магазине "24/7". Полки полупустые.',
        'choices': [
            {'text': 'Купить булку (30₽)', 'next': 'street', 'effects': {'money': -30, 'hungry': -20, 'time': 10}},
            {'text': 'Купить воду (20₽)', 'next': 'street', 'effects': {'money': -20, 'vibe': 5, 'time': 5}},
            {'text': 'Уйти без покупок', 'next': 'street', 'effects': {'time': 2}},
        ],
    },
    
    'death_hunger': {
        'text': 'Вы умерли от голода',
        'choices': [
            {'text': 'Начать заново', 'next': 'start', 'effects': INITIAL_STATE},
        ],
    },
    
    'death_time': {
        'text': 'Сердце не выдержало переутомления. Вы умерли от сердечного приступа.',
        'choices': [
            {'text': 'Начать заново', 'next': 'start', 'effects': INITIAL_STATE},
        ],
    },
    
    'death_unemployed': {
        'text': 'Вы умерли от холода на улице, так как у вас закончились деньги',
        'choices': [
            {'text': 'НАЧАТЬ ЗАНОВО', 'next': 'start', 'effects': INITIAL_STATE},
        ],
    },
    
    'existential_crisis': {
        'text': 'Зачем все это??',
        'choices': [
            {'text': 'Продолжить жить', 'next': 'your_room_evening', 'effects': {'vibe': 50}},
            {'text': 'Сдаться', 'next': 'death_depression', 'effects': {}},
        ],
    },
    
    'death_depression': {
        'text': 'Депрессия съела вас заживо.',
        'choices': [
            {'text': 'Начать заново', 'next': 'start', 'effects': INITIAL_STATE},
        ],
    },
    
    'park': {
        'text': 'Вы в парке. Тишина, только шелест листьев.',
        'conditions': [
            {'check': lambda state: state['vibe'] < 10, 'text': 'Природа не приносит успокоения.'},
        ],
        'random_events': [{
            'chance': 0.05,
            'text': 'Вы нашли 100₽ на скамейке!',
            'effects': {'money': 100, 'vibe': 5},
        }],
        'choices': [
            {'text': 'Посидеть на скамейке', 'next': 'your_room_evening', 'effects': {'time': 30, 'vibe': 5}},
            {'text': 'Покормить голубей', 'next': 'park', 'effects': {'vibe': 2, 'time': 15}},
            {'text': 'Вернуться домой', 'next': 'your_room_evening', 'effects': {'time': 20}},
        ],
    },
    
    'bar': {
        'text': 'Бар "Утопленник". Запах пива и отчаяния.',
        'conditions': [
            {'check': lambda state: state['money'] < 50, 'text': 'У вас почти нет денег на выпивку.'},
        ],
        'choices': [
            {'text': 'Выпить пиво (50₽)', 'next': 'your_room_evening', 'effects': {'money': -50, 'vibe': 10, 'hungry': 5, 'time': 60}},
            {'text': 'Выпить виски (150₽)', 'next': 'your_room_evening', 'effects': {'money': -150, 'vibe': 20, 'time': 90, 'is_dirty': True}},
            {'text': 'Уйти', 'next': 'evening_street', 'effects': {'time': 5}},
        ],
    },
}

