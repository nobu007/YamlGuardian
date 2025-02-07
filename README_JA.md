# YamlGuardian
YamlGuardian

## 継続的インテグレーション

このプロジェクトでは、継続的インテグレーションに GitHub Actions を使用しています。CI ワークフローは、`.github/workflows/ci.yml` ファイルで定義されています。すべてのプッシュおよびプルリクエストでテストを実行し、コードベースが安定していることを確認します。

## 自動マージ機能

CI ワークフローに新しい自動マージ機能を追加しました。この機能は、すべての CI チェックに合格した場合にプルリクエストを自動的にマージします。自動マージプロセスは、`peter-evans/merge` GitHub Action によって処理されます。これにより、すべてのチェックに合格した PR のみがマージされ、コードベースの安定性が維持されます。

## セットアップ手順

### 前提条件

- Python 3.8 以降
- Poetry

### Poetry のインストール

Poetry がインストールされていない場合は、次のコマンドを使用してインストールできます。

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### プロジェクトのセットアップ

1. リポジトリをクローンします。

```sh
git clone https://github.com/nobu007/YamlGuardian.git
cd YamlGuardian
```

2. Poetry を使用して依存関係をインストールします。

```sh
poetry install
```

### テストの実行

次のコマンドを使用してテストを実行できます。

```sh
poetry run python -m unittest discover -s tests
```

### エッジケーステストの実行

エッジケーステストを実行するには、次のコマンドを使用します。

```sh
poetry run python -m unittest tests/test_validate.py
```

### ディレクトリ構造の分析

ディレクトリ構造を分析し、必要な変更を特定するには、次のスクリプトを実行します。

```sh
poetry run python yamlguardian/directory_analyzer.py
```

特定された変更は、ルートディレクトリにある `directory_structure_changes.csv` という名前の CSV ファイルに保存されます。

### ディレクトリ構造の分析と保存

ディレクトリ構造を分析し、変更を CSV ファイルに保存するには、`YamlGuardian` の `analyze_and_save_directory_structure` メソッドを使用します。

```python
from yamlguardian.core import YamlGuardian

guardian = YamlGuardian(schema_file='path/to/schema.yaml')
guardian.analyze_and_save_directory_structure(root_dir='path/to/root_dir', csv_file='path/to/output.csv')
```

### FastAPI サーバーの実行

`uvicorn` を使用して FastAPI サーバーを実行するには、次のコマンドを使用します。

```sh
uvicorn main:app --reload
```

### YAML データの検証

`/validate` エンドポイントを使用して YAML データを検証するには、リクエスト本文に YAML コンテンツを含めて `http://127.0.0.1:8000/validate` に POST リクエストを送信します。次に例を示します。

```sh
curl -X POST "http://127.0.0.1:8000/validate" -H "Content-Type: application/json" -d '{"yaml_content": "name: John\nage: 30"}'
```

## CI エラーの修正

CI エラーが発生した場合は、次の手順に従って解決してください。

1. **CI ログの確認**: GitHub Actions タブでログを確認し、エラーの原因を特定します。
2. **一般的な問題**:
   - **依存関係の問題**: すべての依存関係が `pyproject.toml` で正しく指定されていることを確認し、`poetry install` を実行してインストールします。
   - **テストの失敗**: `poetry run python -m unittest discover -s tests` を使用してローカルでテストを実行し、失敗しているテストを特定して修正します。
   - **Lint エラー**: コードがプロジェクトの Lint ルールに準拠していることを確認します。`poetry run flake8` を実行して Lint エラーを確認し、それに応じて修正します。
3. **CI ワークフローの再実行**: 問題を修正した後、変更をプッシュして CI ワークフローを再度トリガーします。

## 設計ドキュメント

詳細な設計ドキュメントについては、[DESIGN.md](DESIGN.md) ファイルを参照してください。
