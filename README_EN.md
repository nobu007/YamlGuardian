```
# YamlGuardian
YamlGuardian

## Integração Contínua

Este projeto utiliza o GitHub Actions para integração contínua. O fluxo de trabalho de CI é definido no arquivo `.github/workflows/ci.yml`. Ele executa testes em cada push e pull request para garantir que a base de código permaneça estável.

## Recurso de Auto-Merge

Adicionamos um novo recurso de auto-merge ao nosso fluxo de trabalho de CI. Este recurso mescla automaticamente pull requests se todas as verificações de CI forem aprovadas. O processo de auto-merge é tratado pela GitHub Action `peter-evans/merge`. Isso garante que apenas PRs que passem em todas as verificações sejam mesclados, mantendo a estabilidade da base de código.

## Instruções de Configuração

### Pré-requisitos

- Python 3.8 ou superior
- Poetry

### Instalando o Poetry

Se você não tiver o Poetry instalado, pode instalá-lo usando o seguinte comando:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### Configurando o Projeto

1. Clone o repositório:

```sh
git clone https://github.com/nobu007/YamlGuardian.git
cd YamlGuardian
```

2. Instale as dependências usando o Poetry:

```sh
poetry install
```

### Executando Testes

Você pode executar os testes usando o seguinte comando:

```sh
poetry run python -m unittest discover -s tests
```

### Executando Testes de Casos Limite

Para executar os testes de casos limite, use o seguinte comando:

```sh
poetry run python -m unittest tests/test_validate.py
```

### Analisando a Estrutura do Diretório

Para analisar a estrutura do diretório e identificar as mudanças necessárias, execute o seguinte script:

```sh
poetry run python yamlguardian/directory_analyzer.py
```

As mudanças identificadas serão salvas em um arquivo CSV chamado `directory_structure_changes.csv` no diretório raiz.

### Analisando e Salvando a Estrutura do Diretório

Para analisar a estrutura do diretório e salvar as alterações em um arquivo CSV, use o método `analyze_and_save_directory_structure` em `YamlGuardian`:

```python
from yamlguardian.core import YamlGuardian

guardian = YamlGuardian(schema_file='path/to/schema.yaml')
guardian.analyze_and_save_directory_structure(root_dir='path/to/root_dir', csv_file='path/to/output.csv')
```

### Executando o Servidor FastAPI

Para executar o servidor FastAPI usando `uvicorn`, use o seguinte comando:

```sh
uvicorn main:app --reload
```

### Validando Dados YAML

Para validar os dados YAML usando o endpoint `/validate`, envie uma requisição POST para `http://127.0.0.1:8000/validate` com o conteúdo YAML no corpo da requisição. Por exemplo:

```sh
curl -X POST "http://127.0.0.1:8000/validate" -H "Content-Type: application/json" -d '{"yaml_content": "name: John\nage: 30"}'
```

## Corrigindo Erros de CI

Se você encontrar erros de CI, siga estas etapas para resolvê-los:

1. **Verifique os logs de CI**: Revise os logs na aba GitHub Actions para identificar a causa do erro.
2. **Problemas comuns**:
   - **Problemas de dependência**: Certifique-se de que todas as dependências estejam corretamente especificadas em `pyproject.toml` e execute `poetry install` para instalá-las.
   - **Falhas nos testes**: Execute os testes localmente usando `poetry run python -m unittest discover -s tests` para identificar e corrigir quaisquer testes com falha.
   - **Erros de linting**: Certifique-se de que seu código adere às regras de linting do projeto. Execute `poetry run flake8` para verificar erros de linting e corrigi-los adequadamente.
3. **Re-execute o fluxo de trabalho de CI**: Após corrigir os problemas, envie suas alterações para acionar o fluxo de trabalho de CI novamente.

## Documentação de Design

Para documentação detalhada do design, consulte o arquivo [DESIGN.md](DESIGN.md).
```