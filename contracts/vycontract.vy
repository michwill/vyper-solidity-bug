contract SolContract:
    def testTrueAfter() -> bool: modifying
    def testFalseAfter() -> bool: modifying
    def testTrue() -> bool: modifying
    def testFalse() -> bool: modifying

externalContract: public(address)


@public
def __init__(token: address):
    self.externalContract = token

@public
def test_true_after():
    assert SolContract(self.externalContract).testTrueAfter()

@public
def test_false_after():
    assert not SolContract(self.externalContract).testFalseAfter()

@public
def test_true():
    assert SolContract(self.externalContract).testTrue()

@public
def test_false():
    assert not SolContract(self.externalContract).testFalse()

@public
def test_transact():
    SolContract(self.externalContract).testTrue()
    SolContract(self.externalContract).testFalse()
