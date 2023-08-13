class StateMachineStorage:

    def __init__(self):
        pass


state_machine_storage = StateMachineStorage()


def get_state_machine_storage() -> StateMachineStorage:
    return state_machine_storage
