# ARCHITECTURE_JA.md

## 1. 概要

このドキュメントは、YamlGuardian プロジェクトのアーキテクチャについて概説します。明確な責務の分離とモジュール化された設計に焦点を当てています。このシステムは、定義済みのルールとスキーマに基づいて YAML データを検証するように設計されています。このアーキテクチャは、テスト容易性、保守性、および拡張性を優先します。

## 2. システムアーキテクチャ

このアーキテクチャは、修正されたクリーンアーキテクチャに基づいており、責務の分離と依存性逆転を強調するために、ヘキサゴナルアーキテクチャの要素を取り入れています。

```plaintext
YamlGuardian
├── Application     # システム全体のユースケースを定義
│   └── validation_usecase.py # YAML検証ユースケース
├── Orchestration   # ユースケースの処理をオーケストレーション
│   └── validation_orchestrator.py # YAML検証オーケストレーター
├── Validation      # 検証機能
│   ├── __init__.py     # パッケージの初期化
│   ├── validation_facade.py # 検証処理のFacade
│   ├── Schema        # スキーマ定義の管理
│   │   ├── __init__.py  # パッケージの初期化
│   │   ├── common      # スキーマの共通処理、I/Oに依存しない
│   │   │   └── schema_utils.py # スキーマ操作ユーティリティ
│   │   │   └── schema_converter.py # スキーマ変換
│   │   ├── input     # 検証に必要なスキーマ情報を受け取る (ロジック側)
│   │   │   └── schema_loader.py # スキーマ読み込み
│   │   ├── logic   # スキーマの検証、操作 (ロジック側)
│   │   │   └── schema_validator.py # スキーマ検証
│   │   │   └── schema_modifier.py # スキーマ操作 (例: デフォルト値の適用)
│   │   └── output    # 検証済みスキーマを提供する (ロジック側)
│   │   │   └── schema_cache.py # スキーマキャッシュ
│   │   └── schema_definition.py # スキーマ定義 (データクラス)
│   ├── Rule          # 検証ルール管理
│   │   ├── __init__.py  # パッケージの初期化
│   │   ├── common      # ルールの共通処理、I/Oに依存しない
│   │   │   └── rule_utils.py # ルール操作ユーティリティ
│   │   ├── input     # 検証に必要なルール情報を受け取る (ロジック側)
│   │   │   └── rule_loader.py # ルール読み込み
│   │   ├── logic   # ルールの検証、適用 (ロジック側)
│   │   │   └── rule_validator.py # ルール検証
│   │   │   └── rule_applier.py # ルール適用
│   │   └── output    # 検証済みルールを提供する (ロジック側)
│   │   │   └── N/A
│   │   └── N/A
│   ├── Data          # 検証対象データ管理
│   │   ├── __init__.py  # パッケージの初期化
│   │   ├── common      # データの共通処理、I/Oに依存しない
│   │   │   └── data_utils.py # データ操作ユーティリティ
│   │   ├── input     # 検証に必要なデータを受け取る (ロジック側)
│   │   │   └── data_loader.py # データ読み込み
│   │   ├── logic   # データの検証 (ロジック側)
│   │   │   └── data_validator.py # データ検証
│   │   └── output    # 検証結果を提供する (ロジック側)
│   │   │   └── result_formatter.py # 検証結果の整形
├── Presentation    # 外部インターフェース (CLI、API、プレゼンター)
│   ├── Input          # 入力処理
│   │   ├── __init__.py  # パッケージの初期化
│   │   ├── common      # 入力データの共通処理
│   │   │   └── N/A
│   │   ├── prepare      # 入力データの受付、パース (インタラクション側)
│   │   │   └── cli_handler.py # CLIからの入力を処理
│   │   │   └── api_handler.py # APIからの入力を処理
│   │   ├── logic       # 入力データの検証、変換 (インタラクション側)
│   │   │   └── input_validator.py # 入力検証
│   │   └── postprocess  # 検証済みデータの Application への受け渡し (インタラクション側)
│   │   │   └── input_transformer.py # データ変換
│   ├── Output         # 出力処理
│   │   ├── __init__.py  # パッケージの初期化
│   │   ├── common      # 出力データの共通処理
│   │   │   └── N/A
│   │   ├── prepare      # 出力データの整形 (インタラクション側)
│   │   │   └── cli_formatter.py # CLIへの出力を整形
│   │   │   └── api_formatter.py # APIへの出力を整形
│   │   ├── logic       # 出力データの検証、変換 (インタラクション側)
│   │   │   └── output_validator.py # 出力検証
│   │   └── postprocess  # 出力処理 (インタラクション側)
│   │   │   └── output_sender.py # 出力送信
├── Commons         # 共通コンポーネント
│   ├── CrossCutting# ロギング、セキュリティ、例外処理
│   │   └── logger.py # ロギング
│   │   └── exception_handler.py # 例外処理
│   ├── Utilities   # 汎用的なユーティリティクラス
│   │   └── string_utils.py # 文字列操作
│   │   └── file_utils.py # ファイル操作
├── Infrastructure
│   ├── FrameworkAdapter # フレームワーク固有の処理の抽象化
│   │   └── file_system.py # ファイルシステムアクセス
│   └── ExternalAdapter # 外部サービス連携の抽象化
│   │   └── json_schema.py # JSONスキーマ検証
```

## 3. モジュールの責務

### 3.1 アプリケーション (Application)

- システムの全体的なユースケースを定義し、外部からのリクエストを処理します。
- `validation_usecase.py`: YAML 検証ユースケースを実装します。ユースケースは、検証処理を呼び出し、結果を整形して Presentation 層に提供します。

### 3.2 オーケストレーション (Orchestration)

- 特定のユースケースの処理をオーケストレーションします。
- `validation_orchestrator.py`: YAML 検証のオーケストレーションを実装します。オーケストレーションは、ValidationFacade を呼び出し、Presentation 層に渡すデータを準備します。

### 3.3 検証 (Validation)

このパッケージには、データの検証に関連するすべての機能が含まれています。コア向きの処理を行います。

- **validation_facade.py**:

  - `ValidationFacade` クラス: 検証処理のエントリポイントを提供します。
  - スキーマのロード、ルールの適用、データの検証を統括します。
  - `run`メソッドは、検証に必要なすべての手順をまとめ、結果を返します。

- **Schema**:

  - スキーマ定義を管理します。
  - `schema_definition.py`:
    - `SchemaDefinition` クラス: スキーマのデータ構造を定義します。
    - スキーマの種類、データ、ソースパスを保持します。
  - `common`: スキーマの共通処理、I/O に依存しない処理を提供します。
    - `schema_utils.py`: スキーマ操作に関するユーティリティ関数を提供します。
    - スキーマの正規化やコピーなどの処理を行います。
    - `schema_converter.py`: スキーマ形式を変換する機能を提供します (例: YAML -> JSON Schema)。
  - `input`: 検証に必要なスキーマ情報を受け取る (コア向き)。
    - `schema_loader.py`: スキーマを YAML ファイルなどから読み込む機能を提供します。
    - ファイルシステムからスキーマを読み込み、内部データ構造に変換します。
  - `logic`: スキーマの検証、操作処理を提供します (コア向き)。
    - `schema_validator.py`: スキーマの構造や内容を検証する機能を提供します。
    - 定義されたルールに従ってスキーマを検証します。
    - `schema_modifier.py`: スキーマを修正する機能を提供します (例: デフォルト値の適用)。
  - `output`: 検証済みスキーマを提供する (コア向き)。
    - `schema_cache.py`: 検証済みスキーマをキャッシュに保存する機能を提供します。

- **Rule**:

  - 検証ルールを管理します。
  - `rule_utils.py`: ルール操作に関するユーティリティ関数を提供します。
  - `rule_loader.py`: ルールを YAML ファイルなどから読み込む機能を提供します。
  - `rule_validator.py`: ルールの構文や意味を検証する機能を提供します。
  - `rule_applier.py`: データを検証するために、ロードされたルールを適用する機能を提供します。

- **Data**:
  - 検証対象データを管理します。
  - `data_utils.py`: データ操作に関するユーティリティ関数を提供します。
  - `data_loader.py`: YAML ファイルなどから検証対象データを読み込む機能を提供します。
  - `data_validator.py`: スキーマとルールに基づいてデータを検証する機能を提供します。
  - `result_formatter.py`: 検証結果を見やすい形式 (例: テキスト) に整形する機能を提供します。

### 3.4 プレゼンテーション (Presentation)

CLI、API、プレゼンテーションロジックなどの外部インターフェースを処理します。インタラクション向きの処理を行います。

- **Input**:
  - `cli_handler.py`: CLI からの入力を受け付け、処理する機能を提供します (インタラクション向き)。
  - `api_handler.py`: API からの入力を受け付け、処理する機能を提供します (インタラクション向き)。
  - `input_validator.py`: 入力データの形式や内容を検証する機能を提供します (インタラクション向き)。
  - `input_transformer.py`: 入力データを UseCase が扱いやすい形式に変換する機能を提供します (インタラクション向き)。
- **Output**:
  - `cli_formatter.py`: 検証結果を CLI 向けに整形する機能を提供します (インタラクション向き)。
  - `api_formatter.py`: 検証結果を API 向けに整形する機能を提供します (インタラクション向き)。
  - `output_validator.py`: 出力データの形式や内容を検証する機能を提供します (インタラクション向き)。
  - `output_sender.py`: 検証結果を外部に送信する機能を提供します (インタラクション向き)。

### 3.5 共通コンポーネント (Commons)

システム全体で共有されるコンポーネントが含まれています。

- `logger.py`: ロギング機能を提供します。
- `exception_handler.py`: 例外処理機能を提供します。
- `string_utils.py`: 文字列操作に関するユーティリティ関数を提供します。
- `file_utils.py`: ファイル操作に関するユーティリティ関数を提供します。

### 3.6 インフラストラクチャ (Infrastructure)

外部依存関係の抽象化レイヤーを提供します。

- `file_system.py`: ファイルシステムアクセスを抽象化する機能を提供します。
- `json_schema.py`: JSON Schema バリデーションを抽象化する機能を提供します。
