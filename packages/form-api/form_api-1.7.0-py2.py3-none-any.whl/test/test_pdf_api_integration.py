# coding: utf-8
# Note - this file is just used to generate a scaffold for the tests
# We overwrite it with test_pdf_api.py

"""
    API V1

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    OpenAPI spec version: v1
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import form_api
from form_api.api.pdf_api import PDFApi  # noqa: E501
from form_api.rest import ApiException
from pprint import pprint


class TestPDFApi(unittest.TestCase):
    """PDFApi unit test stubs"""

    def setUp(self):
        # Configure HTTP basic authorization: api_token_basic
        configuration = form_api.Configuration()
        configuration.api_token_id = 'api_token123'
        configuration.api_token_secret = 'testsecret123'
        configuration.host = 'api.formapi.local:31337/api/v1'

        # create an instance of the API class
        self.api = form_api.PDFApi(form_api.ApiClient(configuration))

    def tearDown(self):
        pass

    def test_batch_generate_pdfs(self):
        """Test case for batch_generate_pdfs

        Generates multiple PDFs  # noqa: E501
        """
        template_id = 'tpl_000000000000000001'  # str |
        api_response = self.api.batch_generate_pdfs({
            'template_id': template_id,
            'metadata': { 'user_id' : 123 },
            'test': True,
            'submissions': [
                {
                    'data': {
                        'title': 'Test PDF',
                        'description': 'This PDF is great!',
                    }
                },
                {
                    'data': {
                        'title': 'Test PDF 2',
                        'description': 'This PDF is also great!',
                    }
                }
            ]
        })

        self.assertEquals(api_response.status, 'success')
        batch = api_response.submission_batch
        self.assertRegexpMatches(batch.id, '^sbb_')
        self.assertEquals(batch.state, 'pending')
        self.assertEquals(batch.metadata['user_id'], 123)
        self.assertEquals(batch.total_count, 2)
        self.assertEquals(batch.pending_count, 2)
        self.assertEquals(batch.error_count, 0)
        self.assertEquals(batch.completion_percentage, 0)

        submissions = api_response.submissions
        self.assertEquals(len(submissions), 2)
        first_response = submissions[0]
        self.assertEquals(first_response.status, 'success')
        submission = first_response.submission
        self.assertRegexpMatches(submission.id, '^sub_')
        self.assertEquals(submission.expired, False)
        self.assertEquals(submission.state, 'pending')

    def test_combine_submissions(self):
        """Test case for combine_submissions

        Merge generated PDFs together  # noqa: E501
        """
        api_response = self.api.combine_submissions(
            combined_submission_data={
                'submission_ids': ['sub_000000000000000001', 'sub_000000000000000002']
            })
        self.assertEquals(api_response.status, 'success')
        self.assertRegexpMatches(api_response.combined_submission.id, '^com_')

    def test_expire_combined_submission(self):
        """Test case for expire_combined_submission

        Expire a combined submission  # noqa: E501
        """
        combined_submission_id = 'com_000000000000000001'  # str |
        api_response = self.api.expire_combined_submission(
            combined_submission_id)
        self.assertEquals(api_response.expired, True)

    def test_expire_submission(self):
        """Test case for expire_submission

        Expire a PDF submission  # noqa: E501
        """
        submission_id = 'sub_000000000000000001'  # str |
        api_response = self.api.expire_submission(submission_id)
        self.assertEquals(api_response.expired, True)

    def test_generate_pdf(self):
        """Test case for generate_pdf

        Generates a new PDF  # noqa: E501
        """
        template_id = 'tpl_000000000000000001'  # str |
        api_response = self.api.generate_pdf(
            template_id, {
              'data': {
                'title': 'Test PDF',
                'description': 'This PDF is great!'
              }
            })
        self.assertEquals(api_response.status, 'success')
        submission = api_response.submission
        self.assertRegexpMatches(submission.id, '^sub_')
        self.assertEquals(submission.expired, False)
        self.assertEquals(submission.state, 'pending')

    def test_generate_pdf_with_data_requests(self):
        """Test case for generate_pdf with data_requests

        Generates a new PDF with data_requests # noqa: E501
        """
        template_id = 'tpl_000000000000000001'  # str |
        api_response = self.api.generate_pdf(
            template_id, {
                'data': {
                    'title': 'Test PDF',
                },
                "data_requests": [
                    {
                        'name': 'John Smith',
                        'email': 'jsmith@example.com',
                        'fields': ['description'],
                        'order': 1,
                        'metadata': {
                            'user_id': 123
                        },
                        'auth_type': 'email_link'
                    }
                ]
            })
        self.assertEquals(api_response.status, 'success')
        submission = api_response.submission
        self.assertRegexpMatches(submission.id, '^sub_')
        self.assertEquals(submission.expired, False)
        self.assertEquals(submission.state, 'waiting_for_data_requests')

        data_requests = submission.data_requests
        self.assertEquals(len(data_requests), 1)
        data_request = data_requests[0]

        self.assertRegexpMatches(data_request.id, '^drq_')
        self.assertEquals(data_request.state, 'pending')
        self.assertEquals(data_request.fields, ['description'])
        self.assertEquals(data_request.order, 1)
        self.assertEquals(data_request.name, 'John Smith')
        self.assertEquals(data_request.email, 'jsmith@example.com')

    def test_get_combined_submission(self):
        """Test case for get_combined_submission

        Check the status of a combined submission (merged PDFs)  # noqa: E501
        """
        combined_submission_id = 'com_000000000000000001'  # str |
        api_response = self.api.get_combined_submission(combined_submission_id)
        self.assertRegexpMatches(api_response.id, '^com_')

    def test_get_submission(self):
        """Test case for get_submission

        Check the status of a PDF  # noqa: E501
        """
        submission_id = 'sub_000000000000000001'  # str |
        api_response = self.api.get_submission(submission_id)
        self.assertRegexpMatches(api_response.id, '^sub_')

    def test_get_templates(self):
        """Test case for get_templates

        Get a list of all templates  # noqa: E501
        """
        page = 1  # int | Default: 1 (optional)
        per_page = 10  # int | Default: 50 (optional)
        api_response = self.api.get_templates(page=page, per_page=per_page)
        self.assertEquals(len(api_response), 2)
        self.assertRegexpMatches(api_response[0].id, '^tpl_')

    def test_test_authentication(self):
        """Test case for test_authentication

        Test Authentication  # noqa: E501
        """
        api_response = self.api.test_authentication()
        self.assertEquals(api_response.status, 'success')


if __name__ == '__main__':
    unittest.main()
