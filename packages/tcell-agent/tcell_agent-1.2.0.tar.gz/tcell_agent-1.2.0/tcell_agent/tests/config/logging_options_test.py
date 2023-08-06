import unittest

from tcell_agent.config.logging_options import LoggingOptions


class LoggingOptionsTest(unittest.TestCase):
    def none_dict_test(self):
        logging_options = LoggingOptions()

        self.assertEqual(logging_options["enabled"], True)
        self.assertEqual(logging_options["level"], "INFO")
        self.assertEqual(logging_options["filename"], "tcell_agent.log")

    def empty_dict_test(self):
        logging_options = LoggingOptions({})

        self.assertEqual(logging_options["enabled"], True)
        self.assertEqual(logging_options["level"], "INFO")
        self.assertEqual(logging_options["filename"], "tcell_agent.log")

    def enabled_values_test(self):
        logging_options = LoggingOptions({"enabled": False})
        self.assertEqual(logging_options["enabled"], False)

        logging_options = LoggingOptions({"enabled": True})
        self.assertEqual(logging_options["enabled"], True)

        logging_options = LoggingOptions({"enabled": "string"})
        self.assertEqual(logging_options["enabled"], False)

        logging_options = LoggingOptions({"enabled": None})
        self.assertEqual(logging_options["enabled"], True)

        logging_options = LoggingOptions({"enabled": ""})
        self.assertEqual(logging_options["enabled"], False)

        logging_options = LoggingOptions({"enabled": 1245})
        self.assertEqual(logging_options["enabled"], False)

    def level_values_test(self):
        logging_options = LoggingOptions({"level": None})
        self.assertEqual(logging_options["level"], "INFO")

        logging_options = LoggingOptions({"level": ""})
        self.assertEqual(logging_options["level"], "INFO")

        logging_options = LoggingOptions({"level": "UNKNOWN"})
        self.assertEqual(logging_options["level"], "INFO")

        logging_options = LoggingOptions({"level": True})
        self.assertEqual(logging_options["level"], "INFO")

        logging_options = LoggingOptions({"level": 12355})
        self.assertEqual(logging_options["level"], "INFO")

        logging_options = LoggingOptions({"level": "DEBUG"})
        self.assertEqual(logging_options["level"], "DEBUG")

    def filename_values_test(self):
        logging_options = LoggingOptions({"filename": None})
        self.assertEqual(logging_options["filename"], "tcell_agent.log")

        logging_options = LoggingOptions({"filename": ""})
        self.assertEqual(logging_options["filename"], "tcell_agent.log")

        logging_options = LoggingOptions({"filename": True})
        self.assertEqual(logging_options["filename"], "True")

        logging_options = LoggingOptions({"filename": 12355})
        self.assertEqual(logging_options["filename"], "12355")

        logging_options = LoggingOptions({"filename": "custom.log"})
        self.assertEqual(logging_options["filename"], "custom.log")

    def happy_path_test(self):
        logging_options = LoggingOptions({
            "enabled": False,
            "level": "DEBUG",
            "filename": "custom.log"
        })

        self.assertEqual(logging_options["enabled"], False)
        self.assertEqual(logging_options["level"], "DEBUG")
        self.assertEqual(logging_options["filename"], "custom.log")
