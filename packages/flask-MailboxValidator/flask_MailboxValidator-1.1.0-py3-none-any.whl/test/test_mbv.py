from unittest import TestCase
import flask_MailboxValidator

class TestMBV(TestCase):
    def test_getting_results(self):
        mbv = flask_MailboxValidator.SingleValidation('PASTE_API_KEY_HERE')
        # check if the function is returning correct validation results for this email : example@example.com
        results = mbv.ValidateEmail('example@example.com')
        self.assertEqual('', results['error_code'])
        self.assertEqual('', results['error_message'])
        self.assertEqual('example@example.com', results['email_address'])
        self.assertEqual('example.com', results['domain'])
        self.assertEqual('False', results['is_free'])
        self.assertEqual('True', results['is_syntax'])
        self.assertEqual('False', results['is_domain'])
        self.assertEqual('-', results['is_smtp'])
        self.assertEqual('-', results['is_verified'])
        self.assertEqual('-', results['is_server_down'])
        self.assertEqual('-', results['is_greylisted'])
        self.assertEqual('True', results['is_disposable'])
        self.assertEqual('True', results['is_suppressed'])
        self.assertEqual('False', results['is_role'])
        self.assertEqual('False', results['is_high_risk'])
        self.assertEqual('Unknown', results['is_catchall'])
        self.assertEqual('False', results['status'])

