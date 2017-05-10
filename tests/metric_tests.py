import unittest
import metricupload
import os.path
import jsonschema
import json

class TestMetricUpload(unittest.TestCase):
    def testJsonValidation(self):
        test_file = os.path.join(os.path.dirname(__file__), "files/example.json")
        with open(test_file, "r") as f:
            json_data = json.load(f)
        self.assertEqual(len(json_data["metrics"]), 2)
        self.assertEqual(len(json_data["metrics"][0].keys()), 4)
        self.assertEqual(len(json_data["metrics"][1].keys()), 3)

        # No exception is good...
        jsonschema.validate(json_data, metricupload.schema)

        # Add an unknown attribute
        json_data["metrics"][0]["foo"] = "Unknown"
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(json_data, metricupload.schema)
