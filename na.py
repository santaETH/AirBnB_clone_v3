def test_states_endpoint(self):
    """Test that states endpoint returns a list of states"""
    r = requests.get("http://0.0.0.0:5050/api/v1/states")
    self.assertEqual(r.status_code, 200)
    self.assertIsInstance(r.json(), list)
