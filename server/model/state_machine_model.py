import logging
from abc import ABC, abstractmethod
from typing import Dict, Optional, List

from model.base import Context

logger = logging.getLogger(__name__)


class State(ABC):

    state_id: str

    @abstractmethod
    def __init__(self, state_id: str):
        self.state_id = state_id

    @abstractmethod
    def evaluate(self, action_context: Optional[Context]) -> str:
        raise NotImplementedError


class StateMachine(ABC):

    states: Dict[str, State]
    transitions: Dict[str, Dict[str, str]]
    current_state_id: str

    @abstractmethod
    def __init__(self, states: List[State], transitions: Dict[str, Dict[str, str]], initial_state: str):
        self.states = {}

        for state in states:
            self.states[state.state_id] = state

        self.transitions = transitions
        self.current_state_id = initial_state

    def action(self, action_context: Optional[Context] = None):
        action = self.states[self.current_state_id].evaluate(action_context)
        next_state_id = self.transitions[self.current_state_id][action]
        print(f"[{self.current_state_id}] --[{action}]--> [{next_state_id}]")
        self.current_state_id = next_state_id
