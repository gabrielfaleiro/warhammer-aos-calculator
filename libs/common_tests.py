import unittest
import common

# Regular expression to match '1+', '3+', '6+' etc.
# Regular expression to match 'D3', 'D6', 'D10' etc.
# Regular expression to match '1D3', '2D6', '2D3' etc.
# Regular expression to match '1', '3', '6', '98' etc.
# Regular expression to match '2D3+3', '3D6+5', '1D6+1' etc.


data_set = [
    {
        "input": "1+",
        "output": 1
    },
    {
        "input": "3+",
        "output": 4/6
    },
    {
        "input": "6+",
        "output": 1/6
    },
    {
        "input": "D3",
        "output": 2
    },
    {
        "input": "D6",
        "output": 3.5
    },
    {
        "input": "D10",
        "output": 5.5
    },
    {
        "input": "2D3",
        "output": 2*2
    },
    {
        "input": "4D6",
        "output": 4*3.5
    },
    {
        "input": "6D10",
        "output": 6*5.5
    },
    {
        "input": "2D3+3",
        "output": 2*2+3
    },
    {
        "input": "3D6+5",
        "output": 3*3.5+5
    },
    {
        "input": "8D6+1",
        "output": 8*3.5+1
    },
    {
        "input": "6",
        "output": 6
    },
    {
        "input": "15",
        "output": 15
    },
    {
        "input": "98",
        "output": 98
    }
]

# TODO: complete tests with modifiers


class TestParseCharacteristic(unittest.TestCase):
    def test_parse_characteristic(self):
        for data in data_set:
            with self.subTest(data=data):
                self.assertEqual(common.parse_characteristic(data["input"]), data["output"])


if __name__ == '__main__':
    unittest.main()
