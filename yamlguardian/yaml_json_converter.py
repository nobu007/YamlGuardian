import json
from pathlib import Path

from ruamel.yaml import YAML, CommentedMap


class YamlJsonConverter:
    def __init__(self):
        self.yaml = YAML()

    def yaml_to_json(self, yaml_input: CommentedMap | str | Path, output_file=None):
        """YAMLをJSONに変換

        Args:
            yaml_input: YAML文字列またはファイルパス
            output_file: 出力JSONファイルパス（オプション）

        Returns:
            JSON文字列または辞書オブジェクト
        """
        # 入力処理
        if isinstance(yaml_input, (str, Path)) and Path(yaml_input).is_file():
            with open(yaml_input, "r", encoding="utf-8") as f:
                data = self.yaml.load(f)
        else:
            try:
                data = yaml_input
            except Exception as e:
                raise ValueError(f"Invalid YAML input: {e}")

        # 出力処理
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return data
        else:
            return json.dumps(data, ensure_ascii=False, indent=2)

    def json_to_yaml(self, json_input, output_file=None):
        """JSONをYAMLに変換

        Args:
            json_input: JSON文字列、ファイルパス、または辞書オブジェクト
            output_file: 出力YAMLファイルパス（オプション）

        Returns:
            YAML文字列または辞書オブジェクト
        """
        # 入力処理
        if isinstance(json_input, dict):
            data = json_input
        elif isinstance(json_input, (str, Path)) and Path(json_input).is_file():
            with open(json_input, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = json.loads(json_input)

        # 出力処理
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                self.yaml.dump(data, f)
            return data
        else:
            from io import StringIO

            stream = StringIO()
            self.yaml.dump(data, stream)
            return stream.getvalue()
