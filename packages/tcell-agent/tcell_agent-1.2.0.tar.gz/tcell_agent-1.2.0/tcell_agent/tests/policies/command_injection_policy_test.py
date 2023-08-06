import unittest

from tcell_agent.policies.command_injection_policy import CommandInjectionPolicy
from tcell_agent.rust.native_agent import create_native_agent
from tcell_agent.tests.support.builders import ConfigurationBuilder, ContextBuilder
from tcell_agent.tests.support.free_native_agent import free_native_agent


class CommandInjectionPolicyTest(unittest.TestCase):
    def setUp(self):
        configuration = ConfigurationBuilder().build()
        self.native_agent = create_native_agent(configuration)

    def tearDown(self):
        free_native_agent(self.native_agent.agent_ptr)

    def classname_test(self):
        self.assertEqual(CommandInjectionPolicy.api_identifier, "cmdi")

    def blank_command_rules_block_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "command_rules": []
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertFalse(policy.block_command("cat /etc/passwd && grep root", context))

    def ignore_all_command_rules_block_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "command_rules": [{"rule_id": "1", "action": "ignore"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertFalse(policy.block_command("cat /etc/passwd && grep root", context))

    def block_all_command_rules_block_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "collect_full_commandline": True,
                    "command_rules": [{"rule_id": "1", "action": "block"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertTrue(policy.block_command("cat /etc/passwd && grep root", context))

    def ignore_all_ignore_cat_command_rules_block_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "collect_full_commandline": True,
                    "command_rules": [
                        {"rule_id": "1", "action": "ignore"},
                        {"rule_id": "2", "action": "ignore", "command": "cat"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertFalse(policy.block_command("cat /etc/passwd && grep root", context))

    def ignore_all_report_cat_command_rules_block_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "command_rules": [
                        {"rule_id": "1", "action": "ignore"},
                        {"rule_id": "2", "action": "report", "command": "cat"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertFalse(policy.block_command("cat /etc/passwd && grep root", context))

    def ignore_all_block_cat_command_rules_block_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "command_rules": [
                        {"rule_id": "1", "action": "ignore"},
                        {"rule_id": "2", "action": "block", "command": "cat"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertTrue(policy.block_command("cat /etc/passwd && grep root", context))

    def report_all_ignore_cat_command_rules_block_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "command_rules": [
                        {"rule_id": "1", "action": "report"},
                        {"rule_id": "2", "action": "ignore", "command": "cat"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertFalse(policy.block_command("cat /etc/passwd && grep root", context))

    def report_all_report_cat_command_rules_block_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "command_rules": [
                        {"rule_id": "1", "action": "report"},
                        {"rule_id": "2", "action": "report", "command": "cat"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertFalse(policy.block_command("cat /etc/passwd && grep root", context))

    def report_all_block_cat_command_rules_block_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "command_rules": [
                        {"rule_id": "1", "action": "report"},
                        {"rule_id": "2", "action": "block", "command": "cat"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertTrue(policy.block_command("cat /etc/passwd && grep root", context))

    def block_all_ignore_cat_command_rules_block_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "command_rules": [
                        {"rule_id": "1", "action": "block"},
                        {"rule_id": "2", "action": "ignore", "command": "cat"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertTrue(policy.block_command("cat /etc/passwd && grep root", context))

    def block_all_report_cat_command_rules_block_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "command_rules": [
                        {"rule_id": "1", "action": "block"},
                        {"rule_id": "2", "action": "report", "command": "cat"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertTrue(policy.block_command("cat /etc/passwd && grep root", context))

    def block_all_block_cat_command_rules_block_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "command_rules": [
                        {"rule_id": "1", "action": "block"},
                        {"rule_id": "2", "action": "block", "command": "cat"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertTrue(policy.block_command("cat /etc/passwd && grep root", context))

    def ignore_one_command_compound_statement_rules_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "compound_statement_rules": [
                        {"rule_id": "1", "action": "ignore"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertFalse(policy.block_command("cat /etc/passwd", context))

    def ignore_two_command_compound_statement_rules_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "compound_statement_rules": [
                        {"rule_id": "1", "action": "ignore"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertFalse(policy.block_command("cat /etc/passwd && grep root", context))

    def report_one_command_compound_statement_rules_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "compound_statement_rules": [
                        {"rule_id": "1", "action": "report"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertFalse(policy.block_command("cat /etc/passwd", context))

    def report_two_command_compound_statement_rules_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "compound_statement_rules": [
                        {"rule_id": "1", "action": "report"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertFalse(policy.block_command("cat /etc/passwd && grep root", context))

    def block_one_command_compound_statement_rules_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "compound_statement_rules": [
                        {"rule_id": "1", "action": "block"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertFalse(policy.block_command("cat /etc/passwd", context))

    def block_two_command_compound_statement_rules_test(self):
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "compound_statement_rules": [
                        {"rule_id": "1", "action": "block"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertTrue(policy.block_command("cat /etc/passwd && grep root", context))

    def multiple_compound_statements_block_two_command_compound_statement_rules_test(self):
        # multiple compound statements present only first one is taken
        policies_rsp = self.native_agent.update_policies({
            "cmdi": {
                "policy_id": "policy_id",
                "version": 1,
                "data": {
                    "compound_statement_rules": [
                        {"rule_id": "1", "action": "block"}, {"rule_id": "2", "action": "ignore"}]
                }
            }
        })

        policy = CommandInjectionPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().build()
        self.assertTrue(policy.block_command("cat /etc/passwd && grep root", context))

        # test empty context
        self.assertTrue(policy.block_command("cat /etc/passwd && grep root", None))
