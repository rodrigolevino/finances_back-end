from datetime import datetime
import re

class Transaction:
    def __init__(self, amount: float, category: str, 
                 description: str = "") -> None:
        """ Inicializa um objeto Transaction

        Args:
            amount (float): Valor da transação feita
            category (str): Indetificador da categoria
            description (str): Descrição da transação
        """
        self.amount = amount
        self.category = category
        self.description = description
        self.date = datetime.now()
    
    def __str__(self) -> str:
        """ Formata uma descrição para retornar

        Returns:
            str: Retorna uma mensagem sobre as informações da transição
        """
        return (
        f"Transação: {self.description} "
        f"R${self.amount:,.2f} "
        f"({self.category})"
    )

    def update(self, **atributes) -> None:
        """ Altera informações da transação

        Args:
            **atributes: Os atributos para alterar, e seus novos valores
        """
        for chave, valor in atributes.items():
            setattr(self, chave, valor)


class Account:
    def __init__(self, client: 'Client', name: str) -> None:
        """ Inicializa uma nova conta

        Args:
            client (Client): Cliente dono da conta
            name (str): Nome da conta
        """
        self.client = client
        self.name = name
        self.balance = 0
        self.transactions = []
    
    def add_transaction(self, amount: float, category: str, 
                        description: str = "") -> Transaction:
        """ Adiciona um objeto transação a lista da conta e altera o saldo

        Args:
            amount (float): Valor da transação feita
            category (str): Indetificador da categoria
            description (str): Descrição da transação
        
        returns:
            Transaction: Retorna o objeto da transação criado, na lista
        """
        self.transactions.append(Transaction(amount, category, description))
        self.balance += amount
    
    def get_transactions(self, start_date: datetime = datetime.min,
                         end_date: datetime = datetime.max,
                         category: str = None) -> list[Transaction]:
        """ Retorna uma lista de transações filtradas

        Args:
            start_date (datetime): A data inicial da filtragem
            end_date (datetime): A data final da filtragem
            category (str): A categoria para filtrar
        
        Returns:
            list[Transaction]: Lista filtrada com base nos filtros acima
        """
        lista_filtrada = []
        # Verifica pra cada transação se está entre as datas, e é da categoria
        for transacoes in self.transactions:
            if start_date <= transacoes.date and end_date >= transacoes.date:
                if re.search(category, transacoes.category, re.IGNORECASE):
                    lista_filtrada.append(transacoes)
        
        return lista_filtrada
    

class Investment:
    def __init__(self, client: 'Client', inv_type: str, amount: float,
                  rate_of_return: float) -> None:
        """ Inicializa um investimento

        Args:
            client (Client): Cliente dono do investimento
            inv_type (str): Tipo de investimento
            initial_amount (float): Capital inicial de investimento
            rate_of_return (float): Taxa de retorno mensal
        """
        self.client = client
        self.type = inv_type
        self.initial_amount = amount
        self.date_purchase = datetime.now()
        self.rate_of_return = rate_of_return
    
    def calculate_value(self) -> float:
        """ Calcula o valor do investimento até o momento

        Returns:
            float: Valor que foi obtido durante o investimento
        """
        atual = datetime.now()
        meses_investido = (atual.year - self.date_purchase.year) * 12
        meses_investido += (atual.month - self.date_purchase.month)
        # Se não tiver chegado no dia do mês da data do 
        # investimento retira esse mês
        if atual.day < self.date_purchase.day:
            meses_investido -= 1
        return self.initial_amount * self.rate_of_return**meses_investido
    
    def sell(self, account: Account) -> None:
        """ Vende o investimento, somando na conta referida

        Args:
            account (Account): Conta a qual vai ser passada o valor total
        """
        total =self.calculate_value()
        account.add_transaction(total, "Investiment", self.type)
        self.initial_amount = 0


class Client:
    def __init__(self, name: str) -> None:
        """ Inicializa um cliente

        Args:
            name (str): Nome do cliente
        """
        self.name = name
        self.accounts = []
        self.investments = []
    
    def add_account(self, account_name: str) -> None:
        """ Adiciona uma conta à lista de contas do cliente

        Args:
            account_name (str): Nome da conta
        """
        self.accounts.append(Account(self, account_name))
    
    def add_investment(self, investment: Investment) -> None:
        """ Adiciona um investimento à lista de investimentos do cliente

        Args:
            investment (Investment): Investimento que vai ser adicionado
        """
        self.investments.append(investment)
    
    def get_new_worth(self) -> float:
        """ Calcula o valor da conta

        Returns:
            float: Valor somado de todas as contas e investimentos
        """
        valor_da_conta = 0
        for contas in self.accounts:
            valor_da_conta += contas.balance
        for investimentos in self.investments:
            valor_da_conta += investimentos.calculate_value()
        return valor_da_conta


def generate_report(client: Client) -> str:
    """ Exibe informações de cada investimento do cliente

    Args:
        client (Client): Cliente o qual vai ser analisado
    
    Returns:
        str: Texto contendo informações sobre os investimentos do cliente
    """
    for investimento in client.investments:
        print("-" * 20)
        print(f"Data de compra: {investimento.date_purchase}\n"
              f"Tipo de investimento: {investimento.type}\n"
              f"Rendimento Anual: {investimento.rate_of_return * 12:.2f}%\n"
              f"Dinheiro investido: R${investimento.initial_amount:,.2f}\n"
              f"Valor atual do investimento: R${investimento.calculate_value():,.2f}")
        print("-" * 20)

def future_value_report(client: Client) -> str:
    """ Gera um relatório de projeção de investimentos

    Args:
        client (Client): Cliente que vai ser analisado
    
    Returns:
        str: Texto contendo relatório da projeção dos investimentos
    """
    for investimento in client.investments:
        valor_atual = investimento.calculate_value()
        print("-" * 20)
        print(f"Tipo do investimento: {investimento.type}\n"
              f"Valor investido inicialmente: {investimento.initial_amount:,.2f}\n"
              f"Valor Atual: {valor_atual:,.2f}\n"
              f"Valor em um ano: {valor_atual*(investimento.rate_of_return**12):,.2f}\n"
              f"Valor em 5 anos: {valor_atual*(investimento.rate_of_return**60):,.2f}")
        print("-" * 20)