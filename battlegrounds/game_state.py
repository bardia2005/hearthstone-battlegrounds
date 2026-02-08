from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from .player import BGPlayer
from .minion import BGMinion


class GamePhase(Enum):
    LOBBY = "lobby"
    RECRUIT = "recruit"
    COMBAT = "combat"
    RESULT = "result"
    GAME_OVER = "game_over"


@dataclass
class GameState:
    """Complete game state for Battlegrounds"""
    match_id: str = "local-001"
    phase: GamePhase = GamePhase.LOBBY
    turn: int = 1
    players: Dict[str, BGPlayer] = field(default_factory=dict)
    current_player_id: str = "p1"
    combat_log: List[Dict[str, Any]] = field(default_factory=list)
    event_log: List[str] = field(default_factory=list)
    combat_events: List[Dict[str, Any]] = field(default_factory=list)
    combat_index: int = 0
    pairing: List[str] = field(default_factory=list)
    first_attacker: str = ""
    winner: Optional[str] = None
    
    def add_log(self, message: str):
        self.event_log.append(message)
        if len(self.event_log) > 100:
            self.event_log.pop(0)
    
    def get_player(self, player_id: str) -> Optional[BGPlayer]:
        return self.players.get(player_id)
    
    def get_current_player(self) -> Optional[BGPlayer]:
        return self.players.get(self.current_player_id)
    
    def get_opponent(self, player_id: str) -> Optional[BGPlayer]:
        for pid in self.players:
            if pid != player_id:
                return self.players[pid]
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "match_id": self.match_id,
            "phase": self.phase.value,
            "turn": self.turn,
            "players": [p.to_dict() for p in self.players.values()],
            "current_player_id": self.current_player_id,
            "event_log": self.event_log[-20:],
            "pairing": self.pairing,
            "first_attacker": self.first_attacker
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameState':
        state = cls(
            match_id=data.get("match_id", "local-001"),
            phase=GamePhase(data.get("phase", "recruit")),
            turn=data.get("turn", 1)
        )
        
        for p_data in data.get("players", []):
            player = BGPlayer.from_dict(p_data)
            state.players[player.player_id] = player
        
        if state.players:
            state.current_player_id = list(state.players.keys())[0]
        
        return state
    
    @classmethod
    def from_mock_state(cls, data: Dict[str, Any]) -> 'GameState':
        """Load from mock_state.json format"""
        return cls.from_dict(data)
    
    @classmethod
    def from_combat_start(cls, data: Dict[str, Any]) -> 'GameState':
        """Load from combat_start.json format"""
        state = cls(
            match_id=data.get("match_id", "combat-001"),
            phase=GamePhase.COMBAT,
            pairing=data.get("pairing", []),
            first_attacker=data.get("first_attacker", "")
        )
        
        boards = data.get("boards", {})
        for player_id, minions in boards.items():
            player = BGPlayer(
                player_id=player_id,
                hero=f"Hero_{player_id}",
                health=40
            )
            for m_data in minions:
                minion = BGMinion.from_dict(m_data)
                player.board.append(minion)
            state.players[player_id] = player
        
        if state.pairing:
            state.current_player_id = state.pairing[0]
        
        return state
