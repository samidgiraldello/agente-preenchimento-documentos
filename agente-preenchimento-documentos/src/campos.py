"""Definição e validação dos campos da ficha cadastral.

Todos os dados usados neste projeto são FICTÍCIOS.
"""
import re
from datetime import datetime

NAO_INFORMADO = "NÃO INFORMADO"

# campo -> instrução enviada ao modelo
CAMPOS = {
    "nome_completo": "Nome completo da pessoa",
    "cpf": "CPF no formato 000.000.000-00",
    "data_nascimento": "Data de nascimento no formato DD/MM/AAAA",
    "email": "Endereço de e-mail",
    "telefone": "Telefone com DDD, no formato (00) 00000-0000",
    "endereco": "Endereço completo (rua, número, bairro, cidade e UF)",
    "profissao": "Profissão ou ocupação",
    "renda_mensal": "Renda mensal em reais, no formato R$ 0.000,00",
}

_REGEX_CPF = re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")
_REGEX_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _data_valida(valor: str) -> bool:
    try:
        datetime.strptime(valor, "%d/%m/%Y")
        return True
    except ValueError:
        return False


_VALIDADORES = {
    "cpf": lambda v: bool(_REGEX_CPF.match(v)),
    "data_nascimento": _data_valida,
    "email": lambda v: bool(_REGEX_EMAIL.match(v)),
}


def normalizar(dados: dict) -> tuple[dict, list[str], list[str]]:
    """Garante todos os campos e separa o que precisa de revisão humana.

    Retorna (dados_completos, campos_faltando, campos_com_formato_suspeito).
    """
    completos: dict[str, str] = {}
    faltando: list[str] = []
    suspeitos: list[str] = []

    for campo in CAMPOS:
        valor = dados.get(campo)
        if valor is None or not str(valor).strip():
            completos[campo] = NAO_INFORMADO
            faltando.append(campo)
            continue

        valor = str(valor).strip()
        completos[campo] = valor
        validador = _VALIDADORES.get(campo)
        if validador and not validador(valor):
            suspeitos.append(campo)

    return completos, faltando, suspeitos
