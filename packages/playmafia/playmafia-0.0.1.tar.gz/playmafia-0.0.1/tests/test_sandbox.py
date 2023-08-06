import unittest

from playmafia.sandbox import Sandbox, SandboxError, SandboxRunner

class TestSandbox(unittest.TestCase):
    def test_positive(self):
        sandbox = Sandbox('tests.sandbox.plugin3', ['sys'])
        with sandbox.run():
            self.assertEqual(sandbox.get_attribute('get_plugin_name')(), 'plugin3')

    def test_importtime_imports(self):
        sandbox = Sandbox('tests.sandbox.plugin1')
        with self.assertRaises(SandboxError):
            with sandbox.run():
                assert False

    def test_runtime_imports(self):
        sandbox = Sandbox('tests.sandbox.plugin2')
        with self.assertRaises(SandboxError):
            with sandbox.run():
                sandbox.get_attribute('plugin_function')()

    def test_runtime_vulnerabilities(self):
        with SandboxRunner(__import__):
            with self.assertRaises(NameError):
                compile('print(0)', 'none', 'single')
            with self.assertRaises(NameError):
                with open('dummy', 'w') as handle:
                    handle.write('I should not be here!')
        # test restore functionality
        self.assertEqual(eval(compile('0', 'none', 'eval')), 0)

if __name__ == '__main__':
    unittest.main()
