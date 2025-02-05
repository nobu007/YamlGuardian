import json
from pathlib import Path


def from_json(json_input: dict | str | Path) -> dict:
    """JSONファイルまたはJSON文字列を辞書にする

    Args:
        json_input: 入力データ（JSON文字列、ファイルパス、または辞書オブジェクト）

    Returns:
        辞書オブジェクト
    """

    if isinstance(json_input, dict):
        data = json_input
    elif isinstance(json_input, (str, Path)) and Path(json_input).is_file():
        with open(json_input, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.loads(json_input)
    return data


def to_json(data: dict, output_file: str = None):
    """JSONファイルまたはJSON文字列にする

    Args:
        data: 辞書オブジェクト
        output_file: 出力JSONファイルパス（オプション）

    Returns:
        JSON文字列または辞書オブジェクト
    """

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return data
    else:
        return json.dumps(data, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    data_ = {"aa": "bb"}
    print(to_json(data_))
