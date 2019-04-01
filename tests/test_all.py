def test_truefalse(w3, vycontract):
    vycontract.test_true()
    vycontract.test_false()


def test_trueafter(w3, vycontract):
    vycontract.test_true_after()


def test_falseafter(w3, vycontract):
    vycontract.test_false_after()


def test_transact(w3, vycontract):
    vycontract.test_transact()
