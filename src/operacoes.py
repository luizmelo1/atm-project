#Saque, depósito, extrato
from datetime import datetime
from database import carregar_usuarios, salvar_usuarios

def consultar_saldo(conta: str) -> float:
    """Retorna o saldo atual da conta."""
    return carregar_usuarios()[conta]["saldo"]

def sacar(conta: str, valor: float) -> None:
    """Realiza um saque, atualizando saldo e histórico."""
    usuarios = carregar_usuarios()
    if usuarios[conta]["saldo"] < valor:
        raise ValueError("Saldo insuficiente.")
    usuarios[conta]["saldo"] -= valor
    usuarios[conta]["historico"].append(
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: Saque de R$ {valor:.2f}"
    )
    salvar_usuarios(usuarios)

def depositar(conta: str, valor: float) -> None:
    """Realiza um depósito, atualizando saldo e histórico."""
    usuarios = carregar_usuarios()
    usuarios[conta]["saldo"] += valor
    usuarios[conta]["historico"].append(
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: Depósito de R$ {valor:.2f}"
    )
    salvar_usuarios(usuarios)

def extrato(conta: str) -> list:
    """Retorna as últimas 10 transações da conta."""
    return carregar_usuarios()[conta]["historico"][-10:]

def transferir(conta_origem: str, conta_destino: str, valor: float) -> None:
    """Realiza uma transferência entre contas."""
    usuarios = carregar_usuarios()
    if conta_destino not in usuarios:
        raise ValueError("Conta destino não encontrada.")
    if usuarios[conta_origem]["saldo"] < valor:
        raise ValueError("Saldo insuficiente.")
    
    # Atualiza saldos
    usuarios[conta_origem]["saldo"] -= valor
    usuarios[conta_destino]["saldo"] += valor
    
    # Registra transações
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M")
    usuarios[conta_origem]["historico"].append(
        f"{data_hora}: Transferência para {conta_destino} de R$ {valor:.2f}"
    )
    usuarios[conta_destino]["historico"].append(
        f"{data_hora}: Transferência recebida de {conta_origem} de R$ {valor:.2f}"
    )
    
    salvar_usuarios(usuarios)