"""Preenchimento de um modelo Word (.docx) com marcadores {{campo}}."""
from pathlib import Path

from docx import Document


def _substituir_em_paragrafo(paragrafo, dados: dict) -> None:
    texto = paragrafo.text
    if "{{" not in texto:
        return
    for campo, valor in dados.items():
        texto = texto.replace("{{" + campo + "}}", valor)
    if texto == paragrafo.text or not paragrafo.runs:
        return
    # Mantém a formatação do primeiro trecho e limpa os demais.
    paragrafo.runs[0].text = texto
    for run in paragrafo.runs[1:]:
        run.text = ""


def _paragrafos(documento):
    yield from documento.paragraphs
    for tabela in documento.tables:
        for linha in tabela.rows:
            for celula in linha.cells:
                yield from celula.paragraphs


def preencher_modelo(caminho_modelo: str | Path, dados: dict, caminho_saida: str | Path) -> Path:
    """Gera um novo .docx com os marcadores substituídos pelos dados."""
    documento = Document(str(caminho_modelo))
    for paragrafo in _paragrafos(documento):
        _substituir_em_paragrafo(paragrafo, dados)

    caminho_saida = Path(caminho_saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    documento.save(str(caminho_saida))
    return caminho_saida
