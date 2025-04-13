import unittest
import cv2
from unittest.mock import patch, MagicMock
from inference.py import DatabaseManager, get_most_frequent_count 

class TestDatabaseManager(unittest.TestCase):
    
    @patch('your_module.mariadb.connect')
    def setUp(self, mock_connect):
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        mock_connect.return_value = self.mock_connection

        self.db_manager = DatabaseManager({
            "host": "localhost",
            "user": "root",
            "port": 3306,
            "password": "root",
            "database": "robertodb"
        })
        self.db_manager.connect()
    
    def test_get_last_sample_id_success(self):
        self.mock_cursor.fetchone.return_value = (5,)
        sample_id = self.db_manager.get_last_sample_id()
        self.assertEqual(sample_id, 5)

    def test_get_last_sample_id_no_records(self):
        self.mock_cursor.fetchone.return_value = (None,)
        sample_id = self.db_manager.get_last_sample_id()
        self.assertEqual(sample_id, 0)

    def test_get_last_sample_id_exception(self):
        self.mock_cursor.execute.side_effect = Exception("Database error")
        sample_id = self.db_manager.get_last_sample_id()
        self.assertEqual(sample_id, 0)

    def test_save_batch_success(self):
        self.mock_cursor.rowcount = 1
        success = self.db_manager.save_batch(1, 10, 100, 95)
        self.assertTrue(success)
        self.mock_cursor.execute.assert_called()
    
    def test_save_batch_failure(self):
        self.mock_cursor.execute.side_effect = Exception("Insertion error")
        success = self.db_manager.save_batch(1, 10, 100, 95)
        self.assertFalse(success)
    
    def test_close(self):
        self.db_manager.close()
        self.mock_cursor.close.assert_called()
        self.mock_connection.close.assert_called()

class TestUtilityFunctions(unittest.TestCase):
    def test_get_most_frequent_count_empty(self):
        hashmap = {}
        result = get_most_frequent_count(hashmap)
        self.assertEqual(result, 0)

    def test_get_most_frequent_count_single(self):
        hashmap = {5: 10}
        result = get_most_frequent_count(hashmap)
        self.assertEqual(result, 5)
    
    def test_get_most_frequent_count_multiple(self):
        hashmap = {2: 1, 3: 5, 4: 3}
        result = get_most_frequent_count(hashmap)
        self.assertEqual(result, 3)

class TestCamera(unittest.TestCase):
    def test_camera_connection(self):
        cap = cv2.VideoCapture(0)
        self.assertTrue(cap.isOpened(), "Camera failed to open")
        cap.release()

    def test_camera_frame_capture(self):
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            self.assertTrue(ret, "Failed to capture frame")
            self.assertIsNotNone(frame, "Captured frame is None")
        cap.release()

if __name__ == '__main__':
    unittest.main()