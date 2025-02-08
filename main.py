import sys

import jsonschema
import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from yamlguardian.validate import validate_yaml_data


# スキーマのロード関数
def load_schema(schema_path: str):
    """YAMLスキーマファイルを読み込む"""
    with open(schema_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# スキーマを読み込む（本番環境用）
schema = load_schema("schema.yaml")

# FastAPI アプリケーションのセットアップ
app = FastAPI()


class YamlInput(BaseModel):
    yaml_content: str


@app.get("/schema", response_class=JSONResponse)
def get_schema():
    """スキーマを JSON 形式で公開するエンドポイント"""
    return schema


@app.post("/validate")
def validate_yaml_endpoint(input_data: YamlInput):
    """YAML データをバリデーションするエンドポイント"""
    try:
        validation_result = validate_yaml_data(input_data.yaml_content)
        if validation_result["message"] == "Validation failed":
            return JSONResponse(status_code=400, content=validation_result)

        return {"message": "Validation successful"}
    except jsonschema.exceptions.ValidationError as e:
        return JSONResponse(status_code=422, content={"message": "Validation error", "detail": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal server error", "detail": str(e)})


# コマンドライン実行時
if __name__ == "__main__":
    if len(sys.argv) > 1:
        validate_yaml_local(sys.argv[1])
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)
