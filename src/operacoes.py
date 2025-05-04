#Saque, depósito, extrato
from datetime import datetime
from database import carregar_usuarios, salvar_usuarios

def consultar_saldo(conta: str) -> None:
    """Exibe o saldo atual da conta do usuário."""
    usuarios = carregar_usuarios()
    print(f"\nSaldo atual: R$ {usuarios[conta]['saldo']:.2f}")

def sacar(conta: str) -> None:
    """Realiza operação de saque com validações."""
    usuarios = carregar_usuarios()
    
    try:
        valor = float(input("\nValor do saque: R$ "))
        
        # Validações
        if valor <= 0:
            print("Erro: Valor deve ser positivo!")
            return
            
        if valor > usuarios[conta]["saldo"]:
            print("Erro: Saldo insuficiente!")
            return
            
        # Atualiza saldo e histórico
        usuarios[conta]["saldo"] -= valor
        transacao = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: Saque de R$ {valor:.2f}"
        usuarios[conta]["historico"].append(transacao)
        
        salvar_usuarios(usuarios)  # Salva os dados atualizados
        print("\n✅ Saque realizado com sucesso!")
        
    except ValueError:
        print("Erro: Valor inválido! Use números (ex: 150.50).")

def depositar(conta: str) -> None:
    """Realiza operação de depósito com validações."""
    usuarios = carregar_usuarios()  # Carrega os dados aqui
    
    try:
        valor = float(input("\nValor do depósito: R$ "))
        
        # Validações
        if valor <= 0:
            print("Erro: Valor deve ser positivo!")
            return
            
        # Atualiza saldo e histórico
        usuarios[conta]["saldo"] += valor
        transacao = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: Depósito de R$ {valor:.2f}"
        usuarios[conta]["historico"].append(transacao)
        
        salvar_usuarios(usuarios)  # Salva os dados atualizados
        print("\n✅ Depósito realizado com sucesso!")
        
    except ValueError:
        print("Erro: Valor inválido! Use números (ex: 300.75).")

def extrato(conta: str) -> None:
    """Exibe as últimas 10 transações da conta."""
    usuarios = carregar_usuarios()  # Carrega os dados aqui
    
    print("\n" + "=" * 40)
    print("           EXTRATO BANCÁRIO           ")
    print("=" * 40)
    
    if not usuarios[conta]["historico"]:
        print("\nNenhuma transação registrada.")
        return
    
    # Mostra últimas 10 transações em ordem reversa
    for transacao in reversed(usuarios[conta]["historico"][-10:]):
        print(f"- {transacao}")
    
    print(f"\nSaldo atualizado: R$ {usuarios[conta]['saldo']:.2f}")
    print("=" * 40)

def transferir(conta_origem: str) -> None:
    """Realiza transferência para outra conta com validações."""
    usuarios = carregar_usuarios()  # Carrega os dados aqui
    
    try:
        conta_destino = input("\nNúmero da conta destino: ").strip()
        valor = float(input("Valor da transferência: R$ "))
        
        # Validações
        if valor <= 0:
            print("Erro: Valor deve ser positivo!")
            return
            
        if conta_destino not in usuarios:
            print("Erro: Conta destino não encontrada!")
            return
            
        if usuarios[conta_origem]["saldo"] < valor:
            print("Erro: Saldo insuficiente!")
            return
            
        # Executa a transferência
        usuarios[conta_origem]["saldo"] -= valor
        usuarios[conta_destino]["saldo"] += valor
        
        # Registra transações em ambas as contas
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M')
        usuarios[conta_origem]["historico"].append(
            f"{data_hora}: Transferência para {conta_destino} de R$ {valor:.2f}"
        )
        usuarios[conta_destino]["historico"].append(
            f"{data_hora}: Transferência recebida de {conta_origem} de R$ {valor:.2f}"
        )
        
        salvar_usuarios(usuarios)  # Salva os dados atualizados
        print("\n✅ Transferência realizada com sucesso!")
        
    except ValueError:
        print("Erro: Valor inválido!")