"""
Provides the core components of playmafia.
"""

from enum import Enum

class Phase(Enum):
    """
    Defines an enumerator for all different phases of the game.
    """
    MORNING = 0 # chat, no lynch
    DAY = 1 # chat, lynch
    DAWN = 2 # party meetings without action
    NIGHT = 3 # party meetings with action

class Alignment(Enum):
    """
    Defines an enumerator for all different alignments of the game.
    """
    TOWN = 0
    MAFIA = 1
    THIRD = 2

class Role:
    """
    Defines a role that gives its possessing player choices during different phases of the game.
    The role is only a trait; it just defines what it does and contains no data whatsoever. This
    design requires the role creator to store possible states in the associated player instance
    (exposed through the 'issuer' parameter of the choice callback). The benefit of this approach is
    the possibility to exchange states between two or more roles.
    """
    def __init__(self):
        """
        Disabled due to role being a trait.
        """
        raise NotImplementedError('Role is just a trait and does not contain data')

    @classmethod
    def setup(cls, player):
        """
        Performs a role setup for the given player. Override this method with @classmethod and
        register handlers for possible state changes of the player.

        :param Type[Role] cls: The Role class type.
        :param Player player: The player to perform the setup on.

        :type player: An instance of :class:`.Player`.
        """
        pass

    @classmethod
    def get_choices(cls, phase, participants):
        """
        Retrieves the choices for this role during a particular phase of the game. Sub-classes of
        :class:`.Role` must decorate this method with @classmethod and take the class type as first
        parameter. Do not forget to call the super implementation to retrieve base choices such as
        meetings for specific parties.

        :param Type[Role] cls: The Role class type.
        :param Phase phase: The phase the game is currently in.
        :param List[Player] participants: All players in the game.

        :type participants: A list of :class:`.Player` objects.
        :return: A list of Choice instances presented to the player in this phase.
        """
        raise NotImplementedError('Role::get_choices() needs to be overridden')

    @classmethod
    def get_alignment(cls, current_player):
        """
        Retrieves the alignment of the role. This is usually done in the first sub-class, but some
        roles such as Turncoat have alternating alignments and might override the value based on
        some player states. Must decorate this method with @classmethod and take the class type as
        first parameter.

        :param Type[Role] cls: The Role class type.
        :param Player current_player: A player with this role.
        :return: The alignment of the given player.
        :rtype: :class:`.Alignment`
        """
        raise NotImplementedError('Role::get_alignment() needs to be overridden')

class StateEvent:
    """
    Defines an event that monitors the change of a player's state.

    :ivar Any old_value: Old value of the state.
    :ivar Any new_value: New value of the state.
    :ivar Player player: The player whose state changed.
    :ivar List[Player] participants: A list containing all participants in the game.
    :ivar int reason: The reason the state was changed.

    :vartype participants: A list of :class:`.Player` objects.
    """
    def __init__(self, old_value, new_value, player, participants, reason):
        """
        Initializes a new state event.
        """
        self.old_value = old_value
        self.new_value = new_value
        self.player = player
        self.participants = participants
        self.reason = reason

class Player:
    """
    Defines a human player with a role and some states.

    :cvar STATE_ALIVE: The name of the state that determines whether the player is alive.
    :cvar STATE_ROLE_REVEALED: The name of the state that determines whether the player's role is
        visible to everyone.
    :cvar REASON_NONE: There was no specific reason for a state change.
    :cvar REASON_LYNCH: A state changed due to a lynch at daytime.
    :cvar REASON_NIGHT_KILL: A state changed due to a kill at night.
    """
    STATE_ALIVE = 'alive' # boolean
    STATE_ROLE_REVEALED = 'revealed' # boolean
    REASON_NONE = 0
    REASON_LYNCH = 1
    REASON_NIGHT_KILL = 2

    def __init__(self, player_id, role_type):
        """
        Creates a new player with the given ID and role.

        :param int player_id: The unique identifier of the player.
        :param Type[Role] role_type: The class type of the role to use.
        """
        self.player_id = player_id
        self.role_type = role_type
        self._states = dict()
        self._states[self.STATE_ALIVE] = True
        self._states[self.STATE_ROLE_REVEALED] = False
        self._event_handlers = dict()
        self.role_type.setup(self)

    def get_state(self, name):
        """
        Retrieves a state of the player or None if not found.

        :param str name: The name of the state.

        :return: The object associated to the state.
        :rtype: Any
        """
        return self._states.get(name)

    def set_state(self, name, value, participants, reason = 0):
        """
        TODO: Add reason parameter? Could be useful for Bulletproof to determine whether he was
              shot or killed through other means.

        Specifies the value of a state. This triggers all event handlers associated with the state.
        If one event handler returns false, the new state is not set.

        :param str name: The name of the state to change.
        :param Any value: The new value of the state.
        :param List[Player] participants: All players in the game.
        :param int reason: The reason this state is changed.

        :type participants: A list of :class:`.Player` objects.
        """
        old_value = self._states.get(name)
        if old_value is not value:
            request_skip = False
            if self._event_handlers.get(name) is not None:
                for handler in self._event_handlers[name]:
                    if not handler(StateEvent(old_value, value, self, participants, reason)):
                        request_skip = True
            if not request_skip:
                self._states[name] = value

    def on_state_changed(self, name, handler):
        """
        Registers a handler that is called before the specified state changes.

        :param str name: The name of the state to intercept.
        :param Callable[StateEvent] handler: The function that handles the event.

        :type handler: A callable of signature bool(StateEvent). If it returns False, the new state
            is not set.
        """
        if self._event_handlers.get(name) is None:
            self._event_handlers[name] = list()
        self._event_handlers[name].append(handler)
