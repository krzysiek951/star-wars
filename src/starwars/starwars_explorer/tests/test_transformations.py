from starwars.pages.utils.transformations import str_to_digit


def test_str_to_digit():
    """ Test whether string is properly converted to a number. If number is not detected - leave a string."""
    samples = {
        '10': 10,
        '10.0': 10,
        '10.2': 10.2,
        '1,000': 1000,
        '1.000': 1,
        '': '',
        'name': 'name',
    }
    for sample, expected in samples.items():
        result = str_to_digit(sample)
        assert result == expected
