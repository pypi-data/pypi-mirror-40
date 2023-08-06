from src import sample_python_package

def test_hello():
    hello = sample_python_package.hello()
    assert isinstance(hello, str) == True