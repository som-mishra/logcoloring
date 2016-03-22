#!/usr/bin/python

import unittest
import re

import color_cole_file

class TestParseTestResults(unittest.TestCase):

	def test_get_all_tokens_valid1(self):
		test_line1 = "2016-03-07 23:08:02.956 26887 WARNING oslo_reports.guru_meditation_report [-] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."
		self.assertEqual( #fill in with expected value
			, color_cole_file.get_all_tokens(test_line1))

	def test_get_all_tokens_valid1(self):
		test_line1 = "2016-03-07 23:08:02.956 26887 WARNING oslo_reports.guru_meditation_report [-] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."
		self.assertEqual( #fill in with expected value
			, color_cole_file.get_all_tokens(test_line1))

	def test_get_all_tokens_valid1(self):
		test_line1 = "2016-03-07 23:08:02.956 26887 WARNING oslo_reports.guru_meditation_report [-] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."
		self.assertEqual( #fill in with expected value
			, color_cole_file.get_all_tokens(test_line1))
