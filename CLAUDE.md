# neteye-client — Claude Code Instructions

## Project Overview

neteye-client は Neteye REST API の Python クライアントライブラリ。ネットワーク機器管理システム Neteye に対して、Node・Interface・ARP・Serial・Cable などのリソースを CRUD 操作するための SDK。

## Tech Stack

- **言語**: Python 3.10+
- **HTTP**: requests (セッションベース認証)
- **型チェック**: dataclasses + type hints
- **テスト**: pytest

## Directory Structure

```
neteye_client/
  neteye_client.py       # NeteyeClient — メインエントリポイント
  base/
    rest_client.py       # RestClient + APIError — HTTP 基底クラス
    api_resource.py      # APIResource — CRUD 共通ロジック + バリデーション
  node/
    node.py              # Node モデル + node リソースクラス
  interface/
    interface.py         # Interface モデル + interface リソースクラス
  arp/
    arp.py               # Arp モデル + arp リソースクラス
  serial/
    serial.py            # Serial モデル + serial リソースクラス
  cable/
    cable.py             # Cable モデル + cable リソースクラス
tests/
  test_neteye_client.py  # pytest テストスイート
```

## Common Commands

```shell
# テスト実行
python -m pytest tests/

# テスト (カバレッジあり)
python -m pytest tests/ --cov=neteye_client --cov-report=term-missing
```

## Architecture Patterns

**リソース追加の手順** — 新しい API リソースを追加する場合は次の順序で:

1. `neteye_client/<resource>/<resource>.py` にモデル (dataclass) とリソースクラスを作成
2. リソースクラスは `APIResource` を継承し `PATH`・`MODEL`・`VALIDATOR` クラス変数を定義
3. 同ファイルにモジュールレベル関数 `_validate_<resource>_data(data: dict) -> None` を実装
4. `neteye_client.py` の `NeteyeClient.__init__()` にリソースを登録

**モデルクラス** — 各モデルは dataclass で実装し、`from_dict()` と `to_dict()` を必ず実装する:
- `to_dict()` は必須フィールドを常に含め、オプションフィールドは値が存在する場合のみ含める
- `ip_address` は `IPv4Address` 型を使用し、`to_dict()` では `str()` に変換する

**バリデーション** — クライアント側バリデーションは各リソースファイルのモジュールレベル関数 `_validate_<resource>_data(data: dict) -> None` に実装し、リソースクラスの `VALIDATOR` クラス変数に代入する。`APIResource._validate_data()` が `type(self).__dict__.get('VALIDATOR')` 経由で呼び出す。`ValueError` はフレームワーク内で `APIError(status_code=400)` に変換される。

**フィルタ** — リソースのフィルタ API は `filter?field=<field>&filter_str=<value>` パターン:
```python
def filter_by_hostname(self, hostname: str):
    path = f"{self.PATH}/filter?field=hostname&filter_str={hostname}"
    response = self.client.get(path)
    return [self.MODEL.from_dict(item) for item in response]
```

## Testing

- `DummySession` で `requests.Session` を monkeypatch してテストする (実際の HTTP リクエストは発生しない)
- モデルの `from_dict` / `to_dict` の往復テストも必ず書く
- テストファイルは `tests/` ディレクトリ配下に配置

## Code Quality Standards

- `print()` 不使用 — デバッグ出力が必要な場合は `logging` を使う
- type hints 必須
- 空文字と `None` を除外する: `to_dict()` のオプションフィールドは `if value is not None and value != '':` で判定し、`0` や `False` などの falsy な値は正しく含める

## Git Workflow

- `git checkout -b <branch>` を作業前に実行する
- main ブランチへの直接コミットは禁止
- ブランチ命名: `fix/`, `feature/`, `refactor/`, `docs/`
- PR を作成して main にマージする

## Commit Messages

- `Co-Authored-By` 行を含めない
- コミット前に変更サマリーと `git diff` を提示してユーザー確認を待つ

## Proposing Recommendations

選択肢を提案する際は以下の3視点から評価し、推奨案を明示する:

1. **Network Engineer 視点**: 運用・設計上の考慮事項
2. **Software Engineer 視点**: コード品質・保守性・セキュリティ
3. **Critical 視点**: 上記二つのトレードオフ・リスク・盲点

→ **Recommendation**: `<option>` — `<一文の根拠>`
