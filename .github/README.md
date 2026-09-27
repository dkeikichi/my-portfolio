# dkeikichi.com

田 慶吉（Keikichi Den）のポートフォリオサイトです。GitHub Pages で公開しています。

- 英語版：https://dkeikichi.com/
- 日本語版：https://dkeikichi.com/ja/

`main` ブランチに push すると、1分ほどで自動的にサイトへ反映されます。

---

## ファイル構成

| パス | 内容 | 直接編集 |
|---|---|---|
| [`_src/index.template.html`](/_src/index.template.html) | **ページの元ファイル**。英語と日本語の両方を1つのファイルに書いています | ✅ ここを編集 |
| [`_src/build_pages.py`](/_src/build_pages.py) | 元ファイルから英語版・日本語版・サイトマップを作るスクリプト。検索結果のタイトルや説明文、構造化データもここで設定しています | ✅ 検索向けの文言を変えるとき |
| `index.html` | 英語版ページ（自動生成） | ❌ 編集しない |
| `ja/index.html` | 日本語版ページ（自動生成） | ❌ 編集しない |
| `sitemap.xml` | Google 向けのページ一覧（自動生成） | ❌ 編集しない |
| `styles.css` | デザイン（英語版・日本語版で共通） | ✅ |
| `script.js` | スクロール時の表示アニメーション、言語の記憶（共通） | ✅ |
| `brand/` | ロゴ一式（SVG・ファビコン・SNS共有画像）と、ロゴを作るスクリプト | 必要なときだけ |
| `img/` | サイトで表示している写真とロゴ（表示サイズに縮小した WebP） | ✅ |
| `KeikichiDen_CV_EN.pdf` / `KeikichiDen_Resume_JA.pdf` | 英文・和文の履歴書 | 同じ名前で差し替え |
| `favicon.ico` | ブラウザのタブや Google 検索結果のアイコン | ❌ |
| `robots.txt` | 検索エンジン向けの案内 | ❌ |
| `CNAME` | 独自ドメイン（dkeikichi.com）の設定 | ❌ 消さない |
| `google1739cd937b765b4b.html` | Google Search Console の所有者確認ファイル | ❌ **消さない**（消すと確認が外れます） |
| `_archive*` | 以前のデザインの保存用。サイトには公開されません | ❌ |
| ルートの `IMG_1545.JPG`・各社ロゴ画像 | 元の画像（縮小前）。保存用に残しています | ❌ |

`_` で始まるフォルダ（`_src`、`_archive*`）と `.github` は、GitHub Pages では公開されません。

---

## ページの文章を直すとき

1. **`_src/index.template.html` を編集します。**
   英語と日本語は、次のように並べて書きます。

   ```html
   <li class="lang-en">Designed and maintained network infrastructure</li>
   <li class="lang-ja">ネットワークインフラの設計および保守を担当</li>
   ```

   画像の代替テキストなど、属性の値を言語で変えたい場合は、次のように書きます。

   ```html
   <img src="/img/logo-tcu.webp" alt="Tokyo City University" data-ja-alt="東京都市大学">
   ```

2. **英語版・日本語版を作り直します。**（Python 3 のみで動きます）

   ```bash
   python3 _src/build_pages.py
   ```

   `index.html`・`ja/index.html`・`sitemap.xml` が更新されます。

3. **手元で表示を確認します。**（任意）

   ```bash
   python3 -m http.server 8000
   ```

   ブラウザで http://localhost:8000/ と http://localhost:8000/ja/ を開きます。
   画像やCSSは `/` から始まるパスで読み込むため、HTMLファイルをダブルクリックで開くと表示が崩れます。必ずこの方法で確認してください。

4. **コミットして `main` に push します。**
   テンプレートと、生成された3つのファイルをまとめてコミットしてください。

> `styles.css` と `script.js` だけを直した場合は、手順2は不要です。

### 検索結果に出るタイトル・説明文を変えるとき

`_src/build_pages.py` の `PAGES`（英語版・日本語版それぞれのタイトル・説明文・SNS共有時の文言）と `PERSON`（Google 向けの構造化データ：名前、所属、出身大学、LinkedIn など）を編集し、手順2以降を行います。

---

## よくある作業

### 職歴を追加する
`_src/index.template.html` の `<!-- ============ EXPERIENCE ============ -->` の中で、既存の `<li class="timeline-item reveal">…</li>` を1つコピーして書き換えます。
最新の職歴には `timeline-marker current`（飛行機のマーク）と `current-job` を付け、1つ前の職歴からは外してください。
あわせて `_src/build_pages.py` の `PERSON` の `worksFor`（所属）も更新します。

### 履歴書PDFを差し替える
新しいPDFを **同じファイル名**（`KeikichiDen_CV_EN.pdf` / `KeikichiDen_Resume_JA.pdf`）で上書きして push します。HTMLの変更は不要です。

### 画像を追加・変更する
表示サイズの2倍程度に縮小した WebP を `img/` に置き、`<img>` に `width`・`height` を指定します。ページの下の方にある画像には `loading="lazy"` を付けます。

### ロゴを作り直す
```bash
pip install fonttools uharfbuzz
python3 brand/build_logo.py
```
`brand/` の SVG が作り直されます（フォントは初回に Google Fonts から `brand/.fonts/` へ自動ダウンロード）。PNG（`favicon-192.png`・`apple-touch-icon.png`・`og-image.png`）と `favicon.ico` は、SVG をブラウザで表示して書き出したものなので、必要なら別途作り直します。

---

## 公開と確認

| 確認したいこと | 場所 |
|---|---|
| サイトへの反映状況 | GitHub の **Actions** → `pages build and deployment`（緑のチェックで完了） |
| アクセス数・国・どこから来たか | Cloudflare → **Analytics → Web analytics → dkeikichi.com**（Cookie を使わない計測。計測コードは `_src/index.template.html` の末尾） |
| Google 検索での表示回数・クリック数・検索キーワード | [Google Search Console](https://search.google.com/search-console)（プロパティ `https://dkeikichi.com/`） |
| 表示速度・SEOの採点 | [PageSpeed Insights](https://pagespeed.web.dev/) に URL を入力 |

大きく内容を変えたときは、Search Console の **URL検査** で `https://dkeikichi.com/` と `https://dkeikichi.com/ja/` を入力し、「インデックス登録をリクエスト」を押すと、Google への反映が早まります。

---

## 注意点

- **言語の切り替え**：右上の EN／日本語 は `/` と `/ja/` を行き来するリンクです。選んだ言語はブラウザに記憶され、日本語を選んだ人が次に `/` を開くと `/ja/` に移動します。ブラウザの言語設定による自動切り替えは、Google の推奨に従い行っていません。
- **Dependabot の通知**：`_archive/` に残している古いプロジェクト（`node_modules`）が原因で、Dependabot のアラートや失敗通知が出ることがあります。サイトには公開されていないため、影響はありません。不要なら Settings → Code security で Dependabot を停止できます。
- **HTTPS**：Settings → Pages の「Enforce HTTPS」はオンのままにしてください。
