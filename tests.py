from module_finances import finances

transacao = finances.Transaction(56.25, "Comidas", "Hamburguer do NESFood")

print(transacao)

def test_instancia():
    assert transacao.amount == 56.25
    assert transacao.category == "Comidas"
    assert transacao.description == "Hamburguer do NESFood"

def test_tipos():
    assert type(transacao.amount) == float
    assert type(transacao.category) == str
    assert type(transacao.description) == str

def test_impressao():
    assert str(transacao) == "Transação: Hamburguer do NESFood R$56.25 (Comidas)"

def test_update():
    transacao.update(category="Food", description="Food from NES")
    assert transacao.category == "Food"
    assert transacao.description == "Food from NES"