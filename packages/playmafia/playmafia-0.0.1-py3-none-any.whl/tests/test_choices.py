import unittest

from playmafia.choices import Choice, ChoiceError, ChoiceEvent

class TestChoice(unittest.TestCase):
    def check_choice(self, event):
        self.assertEqual(str(event.choice), 'Apple')

    def test_choice(self):
        choice = Choice('Fruit selection', ['Apple', 'Banana'], self.check_choice)
        choice.choose(0, None, None)
        self.assertRaises(ChoiceError, choice.choose, 2, None, None)

if __name__ == '__main__':
    unittest.main()
