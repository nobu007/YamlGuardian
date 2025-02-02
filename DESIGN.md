# YamlGuardian Design Document

## 1. システムの目的
YamlGuardianは、YAMLファイルに基づいてデータの検証を行うツールです。このシステムは、特にフォームの検証や設定の管理を行う際に、定義されたルールに従ってデータが正しいかどうかを確認するために使用されます。これにより、データの整合性や正確性を保証し、エラーの早期発見を促します。

## 2. 機能
### 主な機能
#### YAMLファイルの読み込み
スキーマファイル、関係ファイル、共通定義ファイルを読み込み、データを構造化する。

#### データ検証
指定されたデータがYAMLスキーマに基づいて正しいかどうかを検証する。
必須フィールドが欠けている場合や、ルールに違反している場合にエラーメッセージを返す。

#### ルールの適用
各ルールに基づいて、条件に従った適切な検証を行う。

### 追加機能
- 検証結果のログ出力
- エラーの詳細なトレース
- CLIインターフェースの提供

## 3. アーキテクチャ
### 3.1 モジュール構成
- `core.py`: YamlGuardianのコア機能を提供し、YAMLファイルの読み込みとデータ検証を管理する。
- `validator.py`: YAMLのルールに基づいてデータを検証するためのモジュール。
- `rules.py`: ルールを管理し、検証を行うためのモジュール。
- `utils.py`: ユーティリティ関数を含むモジュール。例えば、フィールドの存在確認など。

### 3.2 データ構造
#### スキーマ構造
```yaml
root_element:
  - name: "FormA"
    type: "form"
    description: "このフォームはラベルとラジオボタンの関係を定義します。"
    attributes:
      action: "/submit"
      method: "post"
    elements:
      - name: AAA
        type: label
        required: true
        ...
```

#### 関係構造
```yaml
root_element_relations:
  - source: "FormA"
    target: "FormB"
    condition: "exists"
```

#### 共通要素構造
```yaml
common_elements:
  - name: commonLabel
    type: label
    required: true
    ...
```

## 4. データフロー
### YAMLファイルの読み込み
ユーザーはYamlGuardianにスキーマファイル、関係ファイル、共通定義ファイルのパスを提供します。
YamlGuardianはこれらのファイルを読み込み、データ構造を作成します。

### データ検証
ユーザーは検証したいデータを提供します。
YamlGuardianは、読み込んだスキーマと関係に基づいてデータを検証します。

### エラー報告
検証結果がエラーであれば、エラーメッセージを生成し、ユーザーに返します。

## 5. エラーハンドリング
### 必須フィールドエラー
必須フィールドが欠けている場合、"フィールド名が存在しません。"というメッセージを返します。

### 禁止フィールドエラー
禁止されているフィールドが存在する場合、"フィールド名は選択できません。"というメッセージを返します。

### YAML読み込みエラー
YAMLファイルの読み込みに失敗した場合、適切なエラーメッセージを表示します。

## 6. 拡張性
### 新しいルールの追加
ルールに関する新しい機能を追加することが容易であり、rules.pyに新しい検証ロジックを組み込むことで拡張できます。

### 新しいYAMLフォーマットのサポート
追加のYAMLフォーマットをサポートするために、読み込み機能を拡張することが可能です。

## 7. 今後の展望
### GUIインターフェースの追加
ユーザーがより直感的にデータを検証できるように、GUIを開発することを検討します。

### CI/CD統合
自動化されたテストと統合を行うことで、データの整合性を継続的にチェックできるようにします。

## 8. Validation Stages
### Stage 1: Schema validation using `validate_openapi_schema`
In this stage, the input YAML data is validated against the OpenAPI schema to ensure it conforms to the defined structure and rules.

### Stage 2: User-defined YAML validation
In this stage, the input YAML data is validated against user-defined schemas to ensure it meets the specific requirements defined by the user.

### Stage 3: User-provided YAML validation
In this stage, the input YAML data is validated against the schemas provided by the user to ensure it adheres to the expected format and rules.

## 9. CLIインターフェースとその使用法
CLIインターフェースは、コマンドラインからデータを検証するためのツールです。以下のコマンドを使用して、YAMLデータを検証できます。

```sh
python -m yamlguardian.cli <data_file> <schema_file>
```

このコマンドは、指定されたデータファイルとスキーマファイルを読み込み、データがスキーマに準拠しているかどうかを検証します。検証結果は、成功またはエラーメッセージとして表示されます。

## 10. FastAPIサーバーとエンドポイント
FastAPIサーバーは、HTTPリクエストを受け付けてデータを検証するためのエンドポイントを提供します。以下は、主要なエンドポイントの説明です。

### `/schema` エンドポイント
このエンドポイントは、スキーマをJSON形式で公開します。GETリクエストを送信すると、スキーマが返されます。

### `/validate` エンドポイント
このエンドポイントは、YAMLデータを検証します。POSTリクエストを送信し、リクエストボディにYAMLデータを含めると、検証結果が返されます。

## 11. ディレクトリ構造の解析とCSVファイルへの変更保存
ディレクトリ構造を解析し、変更をCSVファイルに保存する機能を提供します。以下のコマンドを使用して、ディレクトリ構造を解析し、変更を保存できます。

```sh
python -m yamlguardian.analyze_directory_structure <root_directory>
```

このコマンドは、指定されたルートディレクトリを解析し、変更を`directory_structure_changes.csv`ファイルに保存します。

## 12. Validation Stagesの実装
`yamlguardian/validate.py`ファイルには、以下の検証ステージが実装されています。

### Stage 1: Schema validation using `validate_openapi_schema`
このステージでは、入力されたYAMLデータがOpenAPIスキーマに準拠しているかどうかを検証します。

### Stage 2: User-defined YAML validation
このステージでは、入力されたYAMLデータがユーザー定義のスキーマに準拠しているかどうかを検証します。

### Stage 3: User-provided YAML validation
このステージでは、入力されたYAMLデータがユーザー提供のスキーマに準拠しているかどうかを検証します。

## 13. 今後の展望
### GUIインターフェースの追加
ユーザーがより直感的にデータを検証できるように、GUIを開発することを検討します。

### CI/CD統合
自動化されたテストと統合を行うことで、データの整合性を継続的にチェックできるようにします。
