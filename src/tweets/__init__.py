"""Custom types for annotations."""

from typing import Dict, List, Union

UserType = Dict[str, Union[int, str]]
TwitType = Dict[str, Union[int, str, List[str]]]

HashtagStatType = Dict[str, Union[str, int]]
UsersStatType = Dict[str, Union[str, int]]
