"""
Provides filters to strip a list of players.

Since each filter returns a new list, calls can be chained:
.. code-block:: python
   # select all alive players that are not part of the mafia
   choices = select_alive(select_not_party(Mafia, participants))
   meeting = Choice('Mafia meeting', choices, ...)

More complicated things should be done manually through a single list comprehension.
"""

from playmafia.core import Player

def select_alive(players):
    """
    Selects all alive players.

    :param List[Player] players: The list of players to use for the selection process.
    :return: A new list of alive players.
    """
    return [x for x in players if x.get_state(Player.STATE_ALIVE)]

def select_dead(players):
    """
    Selects all dead players.

    :param List[Player] players: The list of players to use for the selection process.
    :return: A new list of dead players.
    """
    return [x for x in players if not x.get_state(Player.STATE_ALIVE)]

def select_role(role_type, players):
    """
    Selects all players that have a certain role.

    :param Type[Role] role_type: The role type to select.
    :param List[Player] players: The list of players to use for the selection process.
    :return: A new list of players with the given role type.
    """
    return [x for x in players if x.role_type is role_type]

def select_party(party, players):
    """
    Selects all players that are members of a certain party.

    :param Type[Role] party: The role type of the party to select.
    :param List[Player] players: The list of players to use for the selection process.
    :return: A new list of players that are members of the given party.
    :remark: A role that inherits from the given role type is considered a member of the party.
    """
    return [x for x in players if issubclass(x.role_type, party)]

def select_not_party(party, players):
    """
    Selects all players that are not members of a certain party.

    :param Type[Role] party: The role type of the party to not select.
    :param List[Player] players: The list of players to use for the selection process.
    :return: A new list of players that are not members of the given party.
    :remark: A role that inherits from the given role type is considered a member of the party.
    """
    return [x for x in players if not issubclass(x.role_type, party)]

def exclude_one(player, players):
    """
    Excludes one player from a list of players.

    :param Player player: The player to exclude.
    :param List[Player] players: The list of players to use for the selection process.
    :return: A new list without the given player.
    """
    return [x for x in players if x is not player]

def exclude_many(excludes, players):
    """
    Excludes many players from a list of players.

    :param List[Player] excludes: The list of players to exclude.
    :param List[Player] players: The list of players to use for the selection process.
    :return: A new list without the given players.
    """
    return [x for x in players if x not in excludes]
