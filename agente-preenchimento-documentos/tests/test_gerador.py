import tempfile
import unittest
from pathlib import Path

from docx import Document

from src.campos import NAO_INFORMADO, normalizar
from src.extrator import _limpar_json, montar_prompt
from src.gerador import preencher_modelo


class TestCampos(unittest.TestCase):
    def test_campos_faltando_viram_nao_informado(self):
        dados, faltando, _ = normalizar({"nome_completo": "Ana Teste"})
        self.assertEqual(dados["email"], NAO_INFORMADO)
        self.assertIn("email", faltando)
        self.assertNotIn("nome_completo", faltando)

    def test_formato_suspeito(self):
        _, _, suspeitos = normalizar(
            {"cpf": "12345678909", "data_nascimento": "31/02/2000", "email": "sem-arroba"}
        )
        self.assertEqual(set(suspeitos), {"cpf", "data_nascimento", "email"})

    def test_formatos_validos(self):
        _, _, suspeitos = normalizar(
            {"cpf": "123.456.789-09", "data_nascimento": "14/03/1995", "email": "a@b.com"}
        )
        self.assertEqual(suspeitos, [])


class TestExtrator(unittest.TestCase):
    def test_limpar_json_com_cerca(self):
        self.assertEqual(_limpar_json('```json\n{"cpf": "1"}\n```'), {"cpf": "1"})

    def test_limpar_json_puro(self):
        self.assertEqual(_limpar_json('{"a": null}'), {"a": None})

    def test_prompt_contem_texto_e_campos(self):
        prompt = montar_prompt("texto de teste")
        self.assertIn("texto de teste", prompt)
        self.assertIn("nome_completo", prompt)


class TestGerador(unittest.TestCase):
    def test_preenche_marcadores(self):
        with tempfile.TemporaryDirectory() as pasta:
            modelo = Path(pasta) / "modelo.docx"
            saida = Path(pasta) / "saida" / "ficha.docx"
            doc = Document()
            doc.add_paragraph("Nome: {{nome_completo}}")
            doc.add_paragraph("CPF: {{cpf}}")
            doc.save(str(modelo))

            preencher_modelo(modelo, {"nome_completo": "Ana Teste", "cpf": "111.111.111-11"}, saida)

            textos = [p.text for p in Document(str(saida)).paragraphs]
            self.assertIn("Nome: Ana Teste", textos)
            self.assertIn("CPF: 111.111.111-11", textos)


if __name__ == "__main__":
    unittest.main()
