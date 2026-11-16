"""Cria o modelo Word de exemplo com marcadores {{campo}}.

Uso: python scripts/criar_modelo.py
"""
import sys
from pathlib import Path

from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.campos import CAMPOS  # noqa: E402

ROTULOS = {
    "nome_completo": "Nome completo",
    "cpf": "CPF",
    "data_nascimento": "Data de nascimento",
    "email": "E-mail",
    "telefone": "Telefone",
    "endereco": "Endereço",
    "profissao": "Profissão",
    "renda_mensal": "Renda mensal",
}


def main() -> None:
    documento = Document()
    documento.add_heading("Ficha Cadastral (modelo de exemplo)", level=1)
    documento.add_paragraph("Documento gerado automaticamente. Todos os dados são fictícios.")
    for campo in CAMPOS:
        documento.add_paragraph(f"{ROTULOS[campo]}: {{{{{campo}}}}}")

    destino = Path("exemplos/modelo_ficha.docx")
    destino.parent.mkdir(parents=True, exist_ok=True)
    documento.save(str(destino))
    print(f"Modelo criado em {destino}")


if __name__ == "__main__":
    main()
