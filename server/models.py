from pydantic import BaseModel
from typing import List, Optional

class TournamentCreate(BaseModel):
    name: str

class UserJoin(BaseModel):
    username: str
    tournament_name: str

class UserMove(BaseModel):
    username: str
    tournament_name: str
    x : int
    y : int

class MatchResult(BaseModel):
    tournament_name: str
    winner: Optional[str]
    loser: Optional[str]
    draw: bool
    board: List[List[int]]
    piece_diff: int

class WinnerRequest(BaseModel):
    tournament_name: str
    username: str

class PlayerUpdate(BaseModel):
    tournament_name: str
    player_name: str
    wins: int
    draws: int
    losses: int