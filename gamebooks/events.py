from typing import Callable, Dict

from .models import ReadingSession, Paragraph

# Aqui mapeamos o nome da action para a função que a processa
EVENT_HANDLERS: Dict[str, Callable] = {}

def register_event(action_name):
    def decorator(func):
        EVENT_HANDLERS[action_name] = func
        return func
    return decorator

def process_paragraph_events(session: ReadingSession, paragraph: Paragraph):
    state = session.state or {}

    for event in paragraph.events:
        action = event.get('action')

        handler = EVENT_HANDLERS.get(action)
        if handler:
            handler(state, event)

    session.state = state
    session.save()

@register_event('choose_character')
def handle_choose_character(state: dict, event: dict):
    state['character_options'] = event.get('options', [])
    state['active_character'] = None

@register_event('damage')
def handle_damage(state: dict, event: dict):
    amount = event.get('amount', 0)
    state['health'] = max(0, state.get('health', 0) - amount)

@register_event('add_item')
def handle_add_item(state: dict, event: dict):
    inventory = state.get('inventory', [])
    inventory.append(event.get('item'))
    state['inventory'] = inventory

# Exemplo de futuro:
@register_event('test_luck')
def handle_test_luck(state: dict, event: dict):
    # Futuramente aqui virá a lógica de rolagem de dados
    pass
