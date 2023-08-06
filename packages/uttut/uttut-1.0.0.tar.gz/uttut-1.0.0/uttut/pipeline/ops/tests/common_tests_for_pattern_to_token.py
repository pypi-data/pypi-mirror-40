import pytest

pytest_parametrize = pytest.mark.parametrize


def pattern_to_token_tests(test_cases):
    '''
    Common tests for subclasses of `pattern_to_token.PatternRecognizer`
    '''

    def test_data(input_str, input_labels, output_str, output_labels):
        assert len(input_str) == len(input_labels)
        assert len(output_str) == len(output_labels)

    def test_transform(input_str, input_labels, output_str, output_labels, op):
        output = op.transform(input_str, input_labels)
        assert output_str == output[0]
        assert output_labels == output[1]

    def test_realign_labels(input_str, input_labels, output_str, output_labels, op):
        _, _, realigner = op.transform(input_str, input_labels)
        output = realigner(output_labels)
        assert input_labels == output

    def test_realign_labels_fails(input_str, input_labels, output_str, output_labels, op):
        pass

    argstr = "input_str,input_labels,output_str,output_labels"
    test_funcs = (test_data, test_transform, test_realign_labels, test_realign_labels_fails)

    return [pytest_parametrize(argstr, test_cases)(f) for f in test_funcs]
