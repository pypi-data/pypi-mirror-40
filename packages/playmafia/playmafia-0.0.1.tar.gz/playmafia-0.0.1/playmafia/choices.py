"""
Provides the base choice and the most common choices.
"""

class ChoiceError(Exception):
    """
    Is raised if an invalid choice was made. An attempt to do so may be audited as hack attempt.
    """
    def __init__(self, pick, maximum):
        super().__init__(f'Failed to choose index {pick}, expected: 0 < x < {maximum}')

class ChoiceEvent:
    """
    Defines an event that is fired as soon as a :class:`.Player` makes a choice. Firing can occur
    either immediately or delayed (meeting at night).

    :ivar Any choice: The object associated with the choice made.
    :ivar Player player: The player who made the choice.
    :ivar List[Player] participants: All the players in the game.

    :vartype participants: A list of :class:`.Player` objects.
    :remark: Use functions from playmafia.filters to filter the participants.
    """
    def __init__(self, choice, player, participants):
        """
        Initializes a new choice event.
        """
        self.choice = choice
        self.player = player
        self.participants = participants


class Choice:
    """
    Defines a choice a player can choose from. Note: The callback receives all participants. Filter
    them using the playmafia.filters module.

    .. code-block:: python
       def print_choice(choice, player, participants):
           print(f'Picked choice {choice}')
       choice = Choice(title: 'Fruit meeting', items: ['Apple', 'Banana'], on_choose: print_choice)
       choice.choose(0, None, None)
    """
    def __init__(self, title, items, on_choose, is_immutable = False, is_shared = False):
        """
        Creates a choice.

        :param str title: The title of the choice.
        :param List[Any] items: List of objects to appear as choice items.
        :param Callable[ChoiceEvent] on_choose: The function to call as soon as a choice was made.
        :param bool is_immutable: True to indicate that the choice is unchangeable once made.
        :param bool is_shared: True to indicate that the choice is shared among players with the
            same role.

        :type items: A list of arbitrary objects that implement __str__().
        :type on_choose: A callable of signature void(ChoiceEvent).
        """
        self.title = title
        self.items = items
        self.is_immutable = is_immutable
        self._on_choose = on_choose

    def choose(self, index, issuer, participants):
        """
        Performs a choice and calls the on_choose event handler.

        :param int index: The index of the chosen item.
        :param Player issuer: The one who did the choice.
        :param List[Player] participants: All players in the game.

        :type issuer: An instance of Player who made the choice.
        :type participants: A list of :class:`.Player` objects.
        """
        if index < 0 or index >= len(self.items):
            raise ChoiceError(index, len(self.items))
        self._on_choose(ChoiceEvent(self.items[index], issuer, participants))
