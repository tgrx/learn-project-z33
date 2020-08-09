from utils import normalize_path

input_data_set = ["", "/", "hello", "hello/"]
expected_data_set = ["/", "/", "hello/", "hello/"]


def test_normalize_path():
    for i in range(len(input_data_set)):
        input_data = input_data_set[i]
        expected_data = expected_data_set[i]
        output_data = normalize_path(input_data)

        assert \
            output_data == expected_data, \
            f"path `{input_data}` normalized to `{output_data}`, while `{expected_data}` expected"
