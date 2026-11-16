# Agente de Preenchimento de Documentos com IA

Projeto em Python que usa o **Google Gemini** para ler um texto livre, extrair os dados de uma pessoa
e preencher automaticamente um modelo de documento em **Word (.docx)**.

> **Todos os dados deste repositório são fictícios.** O projeto foi inspirado em agentes de IA que
> desenvolvo no estágio para reduzir o trabalho manual com documentação, mas é independente: não usa
> dados, modelos ou sistemas de nenhuma empresa.

## O problema

Em muitos setores (cadastro, crédito, RH, atendimento) as pessoas passam parte do dia copiando dados
de mensagens e documentos para fichas e formulários. Isso é repetitivo, demorado e sujeito a erro.

## Como funciona

```
texto livre  ->  Gemini (extrai os campos em JSON)  ->  validação  ->  modelo .docx preenchido
                                                           |
                                                           +-> avisa o que falta ou está suspeito (revisão humana)
```

1. **Extração:** o texto é enviado ao Gemini com a lista de campos pedidos. O modelo devolve um JSON
   e é instruído a usar `null` quando a informação não existe, em vez de inventar.
2. **Validação:** o código confere formatos (CPF, data, e-mail) e marca campos ausentes como
   `NÃO INFORMADO`.
3. **Geração:** os marcadores `{{campo}}` do modelo Word são substituídos pelos valores.
4. **Revisão humana:** o programa lista no terminal o que precisa ser conferido. A IA acelera o
   trabalho, mas a pessoa continua responsável pelo resultado.

## Estrutura

```
src/campos.py       campos da ficha e validação
src/extrator.py     chamada ao Gemini e leitura do JSON
src/gerador.py      preenchimento do modelo Word
src/main.py         linha de comando
scripts/criar_modelo.py   gera o modelo Word de exemplo
exemplos/           entrada fictícia, modelo e saída de exemplo
tests/              testes automatizados
```

## Como rodar

Requisitos: Python 3.10+ e uma chave gratuita do Gemini (https://aistudio.google.com/apikey).

```bash
git clone https://github.com/SEU-USUARIO/agente-preenchimento-documentos.git
cd agente-preenchimento-documentos

python -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # no Windows: copy .env.example .env
# abra o arquivo .env e cole sua chave em GEMINI_API_KEY

python -m src.main
```

O resultado é salvo em `saida/ficha_preenchida.docx`. Para usar outros arquivos:

```bash
python -m src.main --entrada meu_texto.txt --modelo meu_modelo.docx --saida saida/resultado.docx
```

Para criar o seu próprio modelo, escreva um .docx com marcadores como `{{nome_completo}}`,
`{{cpf}}`, `{{renda_mensal}}` (veja `scripts/criar_modelo.py`).

## Exemplo

Entrada (`exemplos/entrada_ficticia.txt`):

> Olá, equipe de cadastro! Meu nome é Mariana Souza Lima, nasci em 14 de março de 1995.
> Meu CPF é 123.456.789-09 (...). Moro na Rua das Palmeiras, 250, Bairro Centro, Três Pontas - MG.
> Trabalho como analista administrativa e tenho renda mensal de R$ 3.850,00. (...)

Saída esperada (`exemplos/saida_exemplo.docx`): a ficha preenchida, com o e-mail marcado como
`NÃO INFORMADO` porque não aparece no texto, e o aviso no terminal pedindo conferência.

## Testes

```bash
python -m unittest discover -s tests -t . -v
```

Os testes cobrem validação de campos, leitura do JSON do modelo e geração do documento, sem precisar
de chave de API.

## Privacidade e segurança

- Use apenas dados fictícios ou com autorização. Textos enviados à API saem do seu computador.
- A chave fica no arquivo `.env`, que está no `.gitignore`. Nunca suba a chave para o GitHub.
- O prompt trata o conteúdo do documento como dados e manda ignorar instruções escritas nele
  (defesa básica contra *prompt injection*).

## Próximos passos

- [ ] Ler PDFs e imagens de documentos (o Gemini aceita entrada multimodal)
- [ ] Interface web simples com Streamlit
- [ ] Mais modelos de documento e campos configuráveis por arquivo
- [ ] Validação do dígito verificador do CPF
- [ ] Avaliar a precisão da extração com um conjunto de textos de teste

## Autora

Samid Giraldello de Oliveira – estudante de Ciência da Computação (Unis) e estagiária de T.I.
LinkedIn: https://www.linkedin.com/in/samid-giraldello-491427255/
