from module_finances import finances

cliente1 = finances.Client("Rodrigo")
cliente1.add_account("Banco NES")
cliente1.accounts[0].add_transaction(5000, "Bolsa de Estudos")
print(cliente1.accounts[0].get_transactions(category = "Bolsa")[0].category)
print(cliente1.accounts[0].balance)

inv_cdb = finances.Investment(cliente1, "Renda Fixa CDB", 180.50, 1.03)
cliente1.add_investment(inv_cdb)

print(cliente1.get_new_worth())

finances.generate_report(cliente1)
finances.future_value_report(cliente1)