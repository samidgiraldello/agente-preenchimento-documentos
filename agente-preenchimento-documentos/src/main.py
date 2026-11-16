"""Linha de comando: texto -> Gemini -> ficha cadastral em Word."""
import argparse
from pathlib import Path

from dotenv import load_dotenv

from .campos import CAMPOS, normalizar
from .extrator import extrair_campos
from .gerador import preencher_modelo


def executar(entrada: Path, modelo: Path, saida: Path) -> int:
    texto = entrada.read_text(encoding="utf-8")

    print("Extraindo dados com o Gemini...")
    extraidos = extrair_campos(texto)
    dados, faltando, suspeitos = normalizar(extraidos)

    arquivo = preencher_modelo(modelo, dados, saida)
    print(f"Documento gerado: {arquivo}")

    # Revisão humana: o agente avisa o que precisa ser conferido.
    if faltando:
        print("\nCampos não encontrados (conferir manualmente):")
        for campo in faltando:
            print(f"  - {campo}: {CAMPOS[campo]}")
    if suspeitos:
        print("\nCampos com formato suspeito (conferir):")
        for campo in suspeitos:
            print(f"  - {campo}: {dados[campo]}")
    if not faltando and not suspeitos:
        print("Todos os campos foram preenchidos e estão no formato esperado.")
    return 0


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Agente de preenchimento de documentos com IA (Gemini).")
    parser.add_argument("--entrada", type=Path, default=Path("exemplos/entrada_ficticia.txt"))
    parser.add_argument("--modelo", type=Path, default=Path("exemplos/modelo_ficha.docx"))
    parser.add_argument("--saida", type=Path, default=Path("saida/ficha_preenchida.docx"))
    args = parser.parse_args()
    return executar(args.entrada, args.modelo, args.saida)


if __name__ == "__main__":
    raise SystemExit(main())
