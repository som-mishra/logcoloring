#!/usr/bin/env python

from collections import namedtuple
import re
import unittest

import color_code_file


Fields = namedtuple('Fields', ['date', 'time', 'pid', 'loglevel', 'modulename', 'request', 'message'])

class TestParseTestResults(unittest.TestCase):

	# Request has [] and and [] nested, and also has other characters
	def test_get_all_tokens_valid_nestedbrackets(self):
		test_line1 = "2016-03-07 23:08:02.956 26887 WARNING oslo_reports.guru_meditation_report [joain[-]wion] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-03-07', time='23:08:02.956', pid='26887', loglevel='WARNING', modulename='oslo_reports.guru_meditation_report', request='[joain[-]wion]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))

	# Changed the module name, removed the nested [] from module
	def test_get_all_tokens_changed_modname_nonesting(self):
		test_line1 = "2016-03-07 23:08:02.956 26887 DEBUG oslo_reports.something.blah [joaiwion] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-03-07', time='23:08:02.956', pid='26887', loglevel='DEBUG', modulename='oslo_reports.something.blah', request='[joaiwion]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))

	# There is nested [] and also nested [] in the message as well. Shouldn't make a difference. 
	def test_get_all_tokens_nestedbrackets_message(self):
		test_line1 = "2016-04-07 23:08:02.123 26887 WARNING guru_meditation_report [joain[-]wion] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='26887', loglevel='WARNING', modulename='guru_meditation_report', request='[joain[-]wion]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))

	# The request field is "empty". So it is [-], as in many lines
	def test_get_all_tokens_empty_module(self):
		test_line1 = "2016-03-07 23:08:51.738 27883 DEBUG oslo_service.service [-] oslo_messaging_rabbit.kombu_reconnect_delay = 1.0 log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2341"
		expectedtuple = Fields(date='2016-03-07', time='23:08:51.738', pid='27883', loglevel='DEBUG', modulename='oslo_service.service', request='[-]', message='oslo_messaging_rabbit.kombu_reconnect_delay = 1.0 log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2341')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))

	# reuqest if empty
	def test_get_all_tokens_request_field_empty(self):
		test_line1 = "2016-04-07 23:08:02.123 26887 WARNING guru_meditation_report [joain[-]wion] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='26887', loglevel='WARNING', modulename='guru_meditation_report', request='[joain[-]wion]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))

	# Request is nested, but it there is no other text. 
	def test_get_all_tokens_request_nested_notext(self):
		test_line1 = "2016-04-07 23:08:02.123 26880970987 DEBUG guru_meditation_report [[-]] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [req-a17d69b8-066c-4482-a865-4347872504af None None] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='26880970987', loglevel='DEBUG', modulename='guru_meditation_report', request='[[-]]', message="Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [req-a17d69b8-066c-4482-a865-4347872504af None None] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.")
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))












	# No pid in line
	def test_get_all_tokens_nopid(self):
		test_line1 = "2016-04-07 23:08:02.123 DEBUG guru_meditation_report [-] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid = '', loglevel='DEBUG', modulename='guru_meditation_report', request='[-]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))



	# No pid and nested request field
	def test_get_all_tokens_nopid_nestedrequest(self):
		test_line1 = "2016-04-07 23:08:02.123 DEBUG guru_meditation_report [[-]] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='', loglevel='DEBUG', modulename='guru_meditation_report', request='[[-]]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))



	# No pid, and nested request with other characters too
	def test_get_all_tokens_nopid_nested_withmessage(self):
		test_line1 = "2016-04-07 23:08:02.123 HELLO guru_meditation_report [oin[-]] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='', loglevel='HELLO', modulename='guru_meditation_report', request='[oin[-]]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))


	# No pid, Nested [] in request, and also nested [] in messsage portion. 
	def test_get_all_tokens_nopid_nested_inside_message(self):
		test_line1 = "2016-04-07 23:08:02.123 DEBUG guru_meditation_report [[-fasd]] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='', loglevel='DEBUG', modulename='guru_meditation_report', request='[[-fasd]]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))







	# Request has spaces with None None
	def test_get_all_tokens_nopid_reqnumber_none(self):
		test_line1 = "2016-04-07 23:08:02.123 26880970987 DEBUG guru_meditation_report [req-a17d69b8-066c-4482-a865-4347872504af None None] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='26880970987', loglevel='DEBUG', modulename='guru_meditation_report', request='[req-a17d69b8-066c-4482-a865-4347872504af None None]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))


	# Request has spaces with None None
	def test_get_all_tokens_short_reqnumber(self):
		test_line1 = "2016-04-07 23:08:02.123 DEBUG guru_meditation_report [req-a17d69b8-066c-4482-a865-4347872504af None None] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='', loglevel='DEBUG', modulename='guru_meditation_report', request='[req-a17d69b8-066c-4482-a865-4347872504af None None]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))


	# Request has spaces with None None
	def test_get_all_tokens_hello_request_none(self):
		test_line1 = "2016-04-07 23:08:02.123 DEBUG guru_meditation_report [hello None None] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='', loglevel='DEBUG', modulename='guru_meditation_report', request='[hello None None]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))

	# Request has spaces with None None
	def test_get_all_tokens_no_pid_long_logname(self):
		test_line1 = "2016-04-07 23:08:02.123 LOGLEVELRANDOMCAPS guru_meditation_report [req-a17d69b8-872504af None None] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='', loglevel='LOGLEVELRANDOMCAPS', modulename='guru_meditation_report', request='[req-a17d69b8-872504af None None]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))

	# Request has spaces with None None
	def test_get_all_tokens_short_requestnumber_nopid(self):
		test_line1 = "2016-04-07 23:08:02.123 DEBUG guru_meditation_report [req-a17d69b8-872504af None None] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='', loglevel='DEBUG', modulename='guru_meditation_report', request='[req-a17d69b8-872504af None None]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))


	# Request has spaces with None None
	def test_get_all_tokens_nopid_weirdloglevel(self):
		test_line1 = "2016-04-07 23:08:02.123 BOOM guru_meditation_report [req-a17d69b8-872504af None None] Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports."
		expectedtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='', loglevel='BOOM', modulename='guru_meditation_report', request='[req-a17d69b8-872504af None None]', message='Guru mediation \
            now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer \
            be registered in a future release, so please use SIGUSR2 to generate reports.')
		self.assertEqual(expectedtuple, color_code_file.get_all_tokens(test_line1))







	# Testing color_line with no pid
	def test_color_line_nopid(self):
		inputtuple = Fields(date='2034-02-07', time='23:08:02.123', pid='', loglevel='DEBUG', modulename='guru_meditation_report', request='[-]', message='Guru mediation \
        now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
        be registered in a future release, so please use SIGUSR2 to generate reports.')
		return color_code_file.color_line(inputtuple)


	# With a 4 digit pid and a non-empty request
	def test_color_line_4digit_nonemptyrequest(self):
		inputtuple = Fields(date='2016-04-07', time='23:08:02.123', pid='1234', loglevel='DEBUG', modulename='guru_meditation_report', request='[-fasd]', message='Guru mediation \
        now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
        be registered in a future release, so please use SIGUSR2 to generate reports.')
		return color_code_file.color_line(inputtuple)

	# Different log level and no pid
	def test_color_line_differentloglevel_nopid(self):
		inputtuple = Fields(date='2016-04-09', time='23:08:02.123', pid='', loglevel='HELLO', modulename='guru_meditation_report', request='[[-fasd]]', message='Guru mediation \
        now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
        be registered in a future release, so please use SIGUSR2 to generate reports.')
		return color_code_file.color_line(inputtuple)


	# Unusually large pid and nested request field
	def test_color_line_largepid_nestedrequest(self):
		inputtuple = Fields(date='2124-11-12', time='23:08:02.123', pid='0997980790970', loglevel='DEBUG', modulename='guru_meditation_report', request='[[-]]', message='Guru mediation \
        now registers SIGUSR1 and SIGUSR2 by [-ga[]sdhj] default for backward compatibility. SIGUSR1 will no longer \
        be registered in a future release, so please use SIGUSR2 to generate reports.')
		return color_code_file.color_line(inputtuple)








if __name__ == '__main__':
	unittest.main()
	
	# print test_color_line_valid1()