from prof_checker import output_results

def test_output_predict():
    test_strings = ["Hello World!", "Fuck U"]
    assert(output_results(test_strings, [("test.py", 1), ("test.py", 2)], None) == -1)


def test_output_probability():
    test_strings = ["Hello World!", "Fuck U"]
    assert(output_results(test_strings, [("test.py", 1), ("test.py", 2)], 0.5) == -1)
