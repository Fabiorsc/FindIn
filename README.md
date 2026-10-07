# FindIn — Busca Profunda de Conteúdo

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Brand](https://img.shields.io/badge/developed%20by-Devbrax-orange)

FindIn é uma aplicação desktop desenvolvida em Python e Tkinter projetada para realizar buscas rápidas e profundas de termos e trechos de texto em arquivos locais.

---

## Download do Executável (.exe)

Se você deseja apenas utilizar o aplicativo no Windows sem precisar instalar o Python ou configurar dependências:

[Clique aqui para baixar a versão executável (.exe) na seção de Releases](../../releases)

---

## Funcionalidades

- Busca Recursiva: Localize palavras e expressões em arquivos de texto, PDF, documentos Word e planilhas Excel dentro de diretórios e subdiretórios.
- Processamento Assíncrono: Uso de múltiplas threads para manter a interface responsiva durante buscas intensas.
- Interface Intuitiva: Desenvolvida em Tkinter para uma experiência leve e ágil.
- Visualização Clara: Exibição estruturada dos resultados e caminhos de arquivos encontrados.

---

## Tecnologias e Bibliotecas Utilizadas

- Linguagem: Python 3
- Interface Gráfica: Tkinter
- Concorrência: Threading (processamento em segundo plano)
- Leitura de Arquivos: PyPDF2 / pdfplumber (PDFs), python-docx (documentos Word), openpyxl (planilhas Excel)
- Compilação Executável: PyInstaller

---

## Como Executar o Código Fonte

Caso queira rodar o projeto diretamente do código-fonte:

### Pré-requisitos
- Python 3.8 ou superior instalado.

### Passo a passo
1. Clone este repositório:
```bash
git clone [https://github.com/Fabiorsc/FindIn.git](https://github.com/Fabiorsc/FindIn.git)
```

2. Acesse a pasta do projeto:
```bash
cd FindIn
```

3. Execute o script principal:
```bash
python main.py
```

---

## Como Gerar o Executável (.exe)

O projeto inclui o arquivo de especificação do PyInstaller (findin.spec). Para compilar o executável por conta própria:

1. Instale o PyInstaller:
```bash
pip install pyinstaller
```

2. Execute a compilação utilizando o arquivo .spec:
```bash
pyinstaller findin.spec
```

3. O executável será gerado na pasta dist/.

---

## Licença

Este projeto está licenciado sob a MIT License — consulte o arquivo [LICENSE](LICENSE) para obter mais detalhes.

---

## Contato e Suporte

Desenvolvido por Devbrax.

- E-mail: devbrax.software@gmail.com
- GitHub: https://github.com/Fabiorsc
