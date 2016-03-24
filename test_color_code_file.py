import unittest
import re

import color_code_file
from collections import namedtuple


Fields = namedtuple('Fields', ['date', 'time', 'pid', 'loglevel', 'modulename', 'request', 'message'])

class TestParseTestResults(unittest.TestCase):

	def test_get_all_tokens_valid1(self):
		test_line1 = "2016-03-07 23:08:02.956 26887 WARNING oslo_reports.guru_meditation_report [joain[-]wion] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-03-07', time='23:08:02.956', pid='26887', loglevel='WARNING', modulename='oslo_reports.guru_meditation_report', request='[joain[-]wion]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))


	def test_get_all_tokens_valid2(self):
		test_line1 = "2016-03-07 23:08:02.956 26887 DEBUG oslo_reports.something.blah [joaiwion] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-03-07', time='23:08:02.956', pid='26887', loglevel='DEBUG', modulename='oslo_reports.something.blah', request='[joaiwion]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))


	def test_get_all_tokens_valid3(self):
		test_line1 = "2016-04-07 23:08:02.123 26887 WARNING guru_meditation_report [joain[-]wion] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='26887', loglevel='WARNING', modulename='guru_meditation_report', request='[joain[-]wion]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))

	def test_get_all_tokens_valid4(self):
		test_line1 = "2016-03-07 23:08:51.738 27883 DEBUG oslo_service.service [-] oslo_messaging_rabbit.kombu_reconnect_delay = 1.0 log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2341"
		expectedtuple = Fields(date='2016-03-07', time='23:08:51.738', pid='27883', loglevel='DEBUG', modulename='oslo_service.service', request='[-]', message='oslo_messaging_rabbit.kombu_reconnect_delay = 1.0 log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2341')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))

	def test_get_all_tokens_valid5(self):
		test_line1 = "2016-04-07 23:08:02.123 26887 WARNING guru_meditation_report [joain[-]wion] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='26887', loglevel='WARNING', modulename='guru_meditation_report', request='[joain[-]wion]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))

	def test_get_all_tokens_valid6(self):
		test_line1 = "2016-04-07 23:08:02.123 26880970987 DEBUG guru_meditation_report [joain[-]] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='26880970987', loglevel='DEBUG', modulename='guru_meditation_report', request='[joain[-]]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))








if __name__ == '__main__':
	unittest.main()