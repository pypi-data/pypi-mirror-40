import unittest

from playmafia.core import Alignment, Phase, Player, Role, StateEvent

class InvincibleRole(Role):
    @classmethod
    def setup(cls, player):
        def invincible(state_event):
            return False # instruct to not set state
        player.on_state_changed(Player.STATE_ALIVE, invincible)

    @classmethod
    def get_choices(cls, phase, participants):
        return []

    @classmethod
    def get_alignment(cls, current_player):
        return []

class TestCore(unittest.TestCase):
    def setUp(self):
        self.player = Player(0xbadf00d, InvincibleRole)
        self.assertEqual(self.player.get_state(Player.STATE_ALIVE), True)
        self.assertEqual(self.player.get_state(Player.STATE_ROLE_REVEALED), False)

    def test_player(self):
        # try to kill the player with the invincible role
        self.player.set_state(Player.STATE_ALIVE, False, [self.player])
        self.assertEqual(self.player.get_state(Player.STATE_ALIVE), True)
        # try to set some other state unaffected by the role
        self.player.set_state(Player.STATE_ROLE_REVEALED, True, [self.player])
        self.assertEqual(self.player.get_state(Player.STATE_ROLE_REVEALED), True)

if __name__ == '__main__':
    unittest.main()
