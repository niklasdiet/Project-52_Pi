import pytest


@pytest.fixture()
def testData():
    return {"": ""}

def test(testData):
    assert(testData == {"": ""})