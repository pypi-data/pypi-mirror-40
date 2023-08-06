import unittest

from tcell_agent.policies.login_policy import LoginPolicy
from tcell_agent.tests.support.builders import ConfigurationBuilder, ContextBuilder
from tcell_agent.rust.native_agent import create_native_agent
from tcell_agent.tests.support.free_native_agent import free_native_agent


class LoginPolicyTest(unittest.TestCase):
    def classname_test(self):
        self.assertEqual(LoginPolicy.api_identifier, "login")

    def setUp(self):
        configuration = ConfigurationBuilder().build()
        self.native_agent = create_native_agent(configuration)

    def tearDown(self):
        free_native_agent(self.native_agent.agent_ptr)

    def login_success_test(self):
        policies_rsp = self.native_agent.update_policies({
            "login": {
                "policy_id": "00a1",
                "version": 1,
                "data": {
                    "options": {
                        "login_failed_enabled": True,
                        "login_success_enabled": True
                    }
                }
            }
        })

        login_policy = LoginPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().update_attribute("user_id", "user-id").build()
        response = login_policy.report_login_success(
            user_id="user-id",
            header_keys=["user-agent", "content-length"],
            tcell_context=context
        )

        self.assertEqual(response, {"events_created": 1})

    def login_failed_test(self):
        policies_rsp = self.native_agent.update_policies({
            "login": {
                "policy_id": "00a1",
                "version": 1,
                "data": {
                    "options": {
                        "login_failed_enabled": True,
                        "login_success_enabled": True
                    }
                }
            }
        })

        login_policy = LoginPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().update_attribute("user_id", "user-id").build()
        response = login_policy.report_login_failure(
            user_id="user-id",
            password="password",
            header_keys=["user-agent", "content-length"],
            user_valid=False,
            tcell_context=context
        )

        self.assertEqual(response, {"events_created": 1})

    def disabled_login_policy_login_success_test(self):
        policies_rsp = self.native_agent.update_policies({
            "login": {
                "policy_id": "00a1",
                "version": 1,
                "data": {
                    "options": {
                        "login_failed_enabled": True,
                        "login_success_enabled": False
                    }
                }
            }
        })

        login_policy = LoginPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().update_attribute("user_id", "user-id").build()
        response = login_policy.report_login_success(
            user_id="user-id",
            header_keys=["user-agent", "content-length"],
            tcell_context=context
        )

        self.assertEqual(response, {"events_created": 0})

    def disabled_login_policy_login_failed_test(self):
        policies_rsp = self.native_agent.update_policies({
            "login": {
                "policy_id": "00a1",
                "version": 1,
                "data": {
                    "options": {
                        "login_failed_enabled": False,
                        "login_success_enabled": True
                    }
                }
            }
        })

        login_policy = LoginPolicy(self.native_agent, policies_rsp["enablements"], None)
        context = ContextBuilder().update_attribute("user_id", "user-id").build()
        response = login_policy.report_login_failure(
            user_id="user-id",
            password="password",
            header_keys=["user-agent", "content-length"],
            user_valid=False,
            tcell_context=context
        )

        self.assertEqual(response, {"events_created": 0})
