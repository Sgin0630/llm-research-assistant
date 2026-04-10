# ⚛️ HEP arXiv アシスタント

高エネルギー物理学論文に特化したRAG（Retrieval-Augmented Generation）システム。  
BM25キーワード検索と密なベクトル検索を組み合わせたハイブリッド検索と、LaTeX方程式を保持するChunkingを実装しています。

---

## アーキテクチャ

```
ユーザークエリ（例：「NLOにおけるトップクォーク対生成のソフト異常次元は？」）
    │
    ▼
┌─────────────────────────────────────┐
│  ハイブリッド検索                      │
│  ┌───────────┐  ┌────────────────┐  │
│  │ BM25      │  │ 密なベクトル   │  │
│  │ (キーワード)│  │ (埋め込み)    │  │
│  └─────┬─────┘  └───────┬────────┘  │
│        └───────┬─────────┘           │
│     Reciprocal Rank Fusion           │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│  Claude API 生成                    │
│  - 物理学特化システムプロンプト      │
│  - 構造化arXiv引用 [arXiv:ID]        │
│  - LaTeX方程式レンダリング            │
└─────────────────┬───────────────────┘
                  ▼
        Streamlit UI + MathJax
```

---

## セットアップ方法

### 前提条件

- Docker と Docker Compose がインストール済みであること
- Anthropic API キーを取得済みであること

### 起動手順

```bash
# リポジトリをクローン
git clone https://github.com/Sgin0630/hep-arxiv-assistant.git
cd hep-arxiv-assistant

# APIキーを設定
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Dockerで起動
docker compose up
```

ブラウザで `http://localhost:8501` を開くとアプリが表示されます。

### ローカル環境での起動

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

streamlit run ui/app.py
```

---

## 評価結果

| 指標 | 値 |
|------|----|
| Precision@5 | — (評価実行後に更新) |
| キーワードカバレッジ | — |

評価を実行するには：

```bash
python eval/run_eval.py
```

詳細な結果は `eval/results.md` を参照してください。

---

## 技術的な工夫

### 物理学対応Chunking

LaTeXブロック（`$$...$$`、`\begin{equation}...\end{equation}` など）を検出し、  
方程式の途中でテキストを分割しないようにしています。

```python
LATEX_BLOCK = re.compile(
    r'(\$\$.*?\$\$|\\begin\{(equation|align|eqnarray)\}.*?\\end\{\2\})',
    re.DOTALL
)
```

### ハイブリッド検索（BM25 + 密なベクトル）

BM25によるキーワードマッチングと文埋め込みモデル（`all-MiniLM-L6-v2`）による  
意味的類似度検索を、Reciprocal Rank Fusion (RRF) で統合します。

```python
def reciprocal_rank_fusion(dense_ids, bm25_ids, k=60):
    scores = {}
    for rank, doc_id in enumerate(dense_ids):
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)
    for rank, doc_id in enumerate(bm25_ids):
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)
    return sorted(scores, key=scores.get, reverse=True)
```

### arXiv論文の自動取得

`arxiv`ライブラリを使用して、`hep-ph`（高エネルギー現象論）および  
`hep-th`（高エネルギー理論）カテゴリから最新論文を自動取得します。

---

## ディレクトリ構成

```
hep-arxiv-assistant/
├── ui/app.py              # Streamlit フロントエンド
├── src/
│   ├── ingest/            # arXiv取得・PDF抽出・Chunking
│   ├── retrieval/         # BM25・ベクトルストア・ハイブリッド検索
│   ├── generation/        # LLMチェーン・プロンプト・引用フォーマット
│   └── api/               # FastAPI エンドポイント
├── eval/                  # 評価スクリプトと20問の物理問題集
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/     # GCP Cloud Run へのCI/CD
```

---

## ライセンス

MIT License
