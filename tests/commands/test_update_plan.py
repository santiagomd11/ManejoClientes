import unittest
from unittest.mock import patch, MagicMock
from src.commands.update_plan import UpdateClientPlan
from src.errors.errors import NotFound, BadRequest
from src.models.client import Client, db, Plan

class TestUpdateClientPlan(unittest.TestCase):
    def setUp(self):
        self.valid_input = {
            'email': 'john.doe@example.com',
            'plan': Plan.EMPRENDEDOR
        }

    @patch('src.commands.update_plan.db.session.commit')
    @patch('src.commands.update_plan.Client.query.filter_by')
    def test_update_plan_success(self, mock_filter_by, mock_commit):
        mock_client = MagicMock()
        mock_filter_by.return_value.first.return_value = mock_client

        command = UpdateClientPlan(self.valid_input)
        command.execute()

        mock_filter_by.assert_called_once_with(email=self.valid_input['email'])
        self.assertEqual(mock_client.plan, self.valid_input['plan'])
        mock_commit.assert_called_once()

    @patch('src.commands.update_plan.Client.query.filter_by')
    def test_update_plan_client_not_found(self, mock_filter_by):
        mock_filter_by.return_value.first.return_value = None

        command = UpdateClientPlan(self.valid_input)
        with self.assertRaises(NotFound) as context:
            command.execute()
        self.assertEqual(str(context.exception), f"Client with email {self.valid_input['email']} not found")

    def test_update_plan_invalid_plan(self):
        invalid_input = self.valid_input.copy()
        invalid_input['plan'] = 'INVALID_PLAN'

        command = UpdateClientPlan(invalid_input)
        with self.assertRaises(BadRequest) as context:
            command.execute()
        self.assertEqual(str(context.exception), 'Invalid plan')

    @patch('src.commands.update_plan.db.session.rollback')
    @patch('src.commands.update_plan.db.session.commit', side_effect=Exception('DB Error'))
    @patch('src.commands.update_plan.Client.query.filter_by')
    def test_update_plan_db_error(self, mock_filter_by, mock_commit, mock_rollback):
        mock_client = MagicMock()
        mock_filter_by.return_value.first.return_value = mock_client

        command = UpdateClientPlan(self.valid_input)
        with self.assertRaises(Exception) as context:
            command.execute()
        self.assertEqual(str(context.exception), 'DB Error')
        mock_rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()