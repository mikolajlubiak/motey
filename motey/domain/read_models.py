from dataclasses import dataclass


@dataclass(init=True, frozen=True)
class Emote:
    id: int
    name: str
    location: str
    times_used: int
