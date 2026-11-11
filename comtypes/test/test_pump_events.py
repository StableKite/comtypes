import gc
import unittest
from unittest import mock

from comtypes.client import PumpEvents, _events


class PumpEventsTest(unittest.TestCase):
    def test_callback_registration_and_removal_use_same_owner(self):
        native_set = _events._SetConsoleCtrlHandler
        calls = []

        def record(handler, add):
            calls.append((id(handler), add))
            return native_set(handler, add)

        with mock.patch.object(_events, "_SetConsoleCtrlHandler", record):
            PumpEvents(0.001)
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0], (calls[1][0], 1))
        self.assertEqual(calls[1][1], 0)

    def test_other_hresult_errors_are_still_raised(self):
        invalid_argument = -2147024809
        with mock.patch.object(
            _events, "_CoWaitForMultipleHandles", return_value=invalid_argument
        ):
            with self.assertRaises(OSError) as caught:
                PumpEvents(0.001)
        self.assertEqual(caught.exception.winerror, invalid_argument)

    def test_signaled_wait_still_raises_keyboard_interrupt(self):
        with mock.patch.object(_events, "_CoWaitForMultipleHandles", return_value=0):
            with self.assertRaises(KeyboardInterrupt):
                PumpEvents(0.001)

    def test_pump_events_doesnt_leak_cycles(self):
        gc.collect()
        for i in range(3):
            PumpEvents(0.05)
            ncycles = gc.collect()
            self.assertEqual(ncycles, 0)


if __name__ == "__main__":
    unittest.main()
