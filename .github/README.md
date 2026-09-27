[![KEIKICHI DEN](/brand/logo-navy.png)](https://dkeikichi.com/)

# dkeikichi.com

田 慶吉（Keikichi Den）のポートフォリオサイトです。
Personal portfolio of Keikichi Den, IT engineer at ANA Systems — a static site on GitHub Pages with separate English and Japanese pages.

| | URL |
|---|---|
| 英語版 | https://dkeikichi.com/ |
| 日本語版 | https://dkeikichi.com/ja/ |

`main` ブランチに push すると、約1分でサイトに反映されます。

## 目次

1. [概要と仕組み](#1-概要と仕組み)
2. [ファイル構成](#2-ファイル構成)
3. [更新の基本手順](#3-更新の基本手順)
4. [テンプレートの書き方](#4-テンプレートの書き方)
5. [検索エンジン対策（SEO）](#5-検索エンジン対策seo)
6. [デザインのルール](#6-デザインのルール)
7. [JavaScript の動き](#7-javascript-の動き)
8. [画像](#8-画像)
9. [ロゴ・アイコン・共有画像](#9-ロゴアイコン共有画像)
10. [履歴書PDF](#10-履歴書pdf)
11. [アクセス解析](#11-アクセス解析)
12. [公開の仕組み（GitHub Pages）](#12-公開の仕組みgithub-pages)
13. [ブランチと作業の流れ](#13-ブランチと作業の流れ)
14. [アーカイブ](#14-アーカイブ)
15. [困ったとき](#15-困ったとき)
16. [更新履歴](#16-更新履歴)
17. [クレジット](#17-クレジット)

---

## 1. 概要と仕組み

- **構成**：HTML・CSS・JavaScript だけの静的サイトです。フレームワークやビルドツールは使っていません。
- **公開**：GitHub Pages（`main` ブランチのルート）＋独自ドメイン `dkeikichi.com`
- **外部サービス**：Google Fonts（文字）、Cloudflare Web Analytics（アクセス数）、Google Search Console（検索）

英語版と日本語版は、**1つのテンプレートから自動で作っています**。文章の修正は1か所で済みます。

```
_src/index.template.html  （英語と日本語を並べて書いた元ファイル）
          │
          │  python3 _src/build_pages.py
          ▼
  ├─ index.html        英語版（/）   … 英語だけを残し、英語用の <head> を付ける
  ├─ ja/index.html     日本語版（/ja/）… 日本語だけを残し、日本語用の <head> を付ける
  └─ sitemap.xml       Google 向けのページ一覧（更新日も自動で更新）
```

`styles.css`・`script.js`・画像は、英語版と日本語版で共通です。

---

## 2. ファイル構成

| パス | 内容 | 編集 |
|---|---|---|
| [`_src/index.template.html`](/_src/index.template.html) | **ページの元ファイル**（英語・日本語の両方） | ✅ 文章はここを直す |
| [`_src/build_pages.py`](/_src/build_pages.py) | 英語版・日本語版・サイトマップを作るスクリプト。検索結果のタイトル・説明文・構造化データもここ | ✅ SEO の文言を変えるとき |
| [`_src/og-image.html`](/_src/og-image.html) | SNS 共有画像（`brand/og-image.png`）の元ファイル | 共有画像を作り直すとき |
| `index.html` | 英語版（自動生成） | ❌ 直接編集しない |
| `ja/index.html` | 日本語版（自動生成） | ❌ 直接編集しない |
| `sitemap.xml` | サイトマップ（自動生成） | ❌ 直接編集しない |
| [`styles.css`](/styles.css) | デザイン（共通） | ✅ |
| [`script.js`](/script.js) | スクロール表示・言語の記憶（共通） | ✅ |
| `img/` | 表示用に縮小した写真とロゴ（WebP） | ✅ |
| `brand/` | ロゴ・ファビコン・共有画像と、ロゴを作るスクリプト | 必要なときだけ |
| `KeikichiDen_CV_EN.pdf` | 英文履歴書 | 同じ名前で差し替え |
| `KeikichiDen_Resume_JA.pdf` | 和文履歴書・職務経歴書 | 同じ名前で差し替え |
| `favicon.ico` | ブラウザ・Google 検索結果のアイコン（16/32/48px） | ❌ |
| `robots.txt` | 検索エンジン向けの案内（サイトマップの場所） | ❌ |
| `CNAME` | 独自ドメインの設定 | ❌ **消さない** |
| `google1739cd937b765b4b.html` | Google Search Console の所有者確認ファイル | ❌ **消さない**（消すと確認が外れる） |
| `.github/README.md` | このファイル | ✅ |
| `.gitignore` | Git に含めないファイル（`brand/.fonts/` など） | ❌ |
| `_archive*` | 以前のサイトの保存（[14章](#14-アーカイブ)） | ❌ |
| ルートの `IMG_1545.JPG`・`*_Logo*.png`・`tcu.png` など | 縮小前の元画像。`IMG_1545.JPG` は構造化データの写真として使用中 | ❌ |

> `_` で始まるフォルダ（`_src`、`_archive*`）と `.` で始まるフォルダ（`.github`）は、GitHub Pages では公開されません。

---

## 3. 更新の基本手順

1. **`_src/index.template.html` を編集する**（書き方は[4章](#4-テンプレートの書き方)）

2. **英語版・日本語版を作り直す**（Python 3 の標準機能だけで動きます）

   ```bash
   python3 _src/build_pages.py
   ```

   `index.html`・`ja/index.html`・`sitemap.xml` が更新されます。

3. **手元で表示を確認する**

   ```bash
   python3 -m http.server 8000
   ```

   http://localhost:8000/ と http://localhost:8000/ja/ を開きます。
   画像やCSSは `/` から始まるパスで読み込むため、HTMLファイルをダブルクリックで開くと崩れて見えます。必ずこの方法で確認してください。

4. **コミットして `main` に push する**
   テンプレートと、生成された3ファイルを一緒にコミットします。

> `styles.css`・`script.js`・画像・PDFだけを変えた場合は、手順2は不要です。

### push 前のチェックリスト

- [ ] 英語と日本語の**両方**を書いた（片方だけだと、もう一方のページから消えます）
- [ ] `python3 _src/build_pages.py` を実行した
- [ ] 英語版・日本語版の両方を、PC幅とスマホ幅（ブラウザの開発者ツール）で確認した
- [ ] リンク・画像のパスが `/` から始まっている

---

## 4. テンプレートの書き方

### 言語の書き分け

英語は `class="lang-en"`、日本語は `class="lang-ja"` を付けて、並べて書きます。
作り直すと、英語版からは `lang-ja` の要素が、日本語版からは `lang-en` の要素が丸ごと取り除かれます。

**ブロック単位**（段落・箇条書きなど）

```html
<li class="lang-en">Designed and maintained network infrastructure</li>
<li class="lang-ja">ネットワークインフラの設計および保守を担当</li>
```

**文中の一部**

```html
<a href="#about"><span class="lang-en">About</span><span class="lang-ja">自己紹介</span></a>
```

**複数段落**（自己紹介など）

```html
<div class="lang-en">
    <p>…</p>
    <p>…</p>
</div>
<div class="lang-ja">
    <p>…</p>
</div>
```

### 属性の書き分け

画像の代替テキストなど、属性の値を言語で変えるときは `data-ja-属性名` を続けて書きます。

```html
<img src="/img/logo-tcu.webp" alt="Tokyo City University" data-ja-alt="東京都市大学">
<nav aria-label="Sections" data-ja-aria-label="セクション">
```

英語版では `alt="Tokyo City University"`、日本語版では `alt="東京都市大学"` になります。

### 触らないもの

- `<head>` の中の `{{TITLE}}`・`{{DESCRIPTION}}` などの `{{…}}` は、スクリプトが言語ごとに埋める場所です。そのまま残してください（文言は `_src/build_pages.py` で変えます）。
- 右上の言語切り替え（`<nav class="lang-toggle">`）のリンク `/` と `/ja/` は変えないでください。

### パスのルール

日本語版は `/ja/` にあるため、画像・CSS・PDFへのパスは **必ず `/` から始めます**。

```html
<img src="/img/profile.webp">        <!-- ○ -->
<img src="img/profile.webp">         <!-- × 日本語版で表示されない -->
```

### ページの区切り

テンプレート内は、次のコメントで区切っています。

| 目印 | 内容 |
|---|---|
| `<!-- ============ NAV ============ -->` | 上部のヘッダー（ロゴ・メニュー・言語切り替え） |
| `<!-- ============ HERO ============ -->` | 写真・名前・キャッチコピー・履歴書ボタン |
| `<!-- ============ ABOUT ============ -->` | 自己紹介 |
| `<!-- ============ EXPERIENCE ============ -->` | 職務経歴（新しい順） |
| `<!-- ============ EDUCATION ============ -->` | 学歴 |
| `<!-- ============ FOOTER / CONTACT ============ -->` | お問い合わせ（LinkedIn・メール） |

ページの最後に、Cloudflare Web Analytics の計測コードがあります（[11章](#11-アクセス解析)）。

### 職歴を追加する

`EXPERIENCE` の `<ol class="timeline">` の先頭に、次のひな形を追加します。

```html
<!-- 会社名 -->
<li class="timeline-item reveal">
    <span class="timeline-marker" aria-hidden="true"></span>
    <article class="card job-card">
        <div class="job-header">
            <a href="https://example.com/" target="_blank" rel="noopener" class="job-logo-link">
                <img class="job-logo" src="/img/logo-example.webp" alt="Example" width="200" height="68" loading="lazy" decoding="async">
            </a>
            <div class="job-heading">
                <h3><a href="https://example.com/" target="_blank" rel="noopener"><span class="lang-en">Example Inc.</span><span class="lang-ja">株式会社エグザンプル</span></a></h3>
                <p class="job-role">
                    <span class="lang-en">IT Engineer</span>
                    <span class="lang-ja">ITエンジニア</span>
                </p>
            </div>
            <p class="job-date">
                <span class="lang-en">Apr 2027 — Present<br>Tokyo, Japan</span>
                <span class="lang-ja">2027年4月 — 現在<br>日本・東京</span>
            </p>
        </div>
        <ul class="job-bullets">
            <li class="lang-en">…</li>
            <li class="lang-ja">…</li>
        </ul>
    </article>
</li>
```

**現職の表示**：現職のカードだけ、次の3点を付けます。転職したら、前の会社のカードからは外してください。

- `<span class="timeline-marker current">` と、その中の飛行機の `<svg>`
- `<article class="card job-card current-job">`
- 社名の横の「Current／現職」バッジ `<span class="badge">…</span>`

あわせて、次の箇所も更新します。

- `_src/build_pages.py` の `PAGES`（タイトル・説明文）と `PERSON` の `worksFor`（所属）
- ヒーローの肩書き（`hero-kicker`：「IT Engineer · ANA Systems · Tokyo」）
- 自己紹介（`ABOUT`）

**職歴の書き方の目安**：英語は動詞の過去形で始め、日本語は体言止めにします。PC表示で1行に収まる長さ（英語で約85文字、日本語で約45文字）にそろえています。

---

## 5. 検索エンジン対策（SEO）

### 設定済みの内容

| 項目 | 場所 |
|---|---|
| ページごとのタイトル・説明文・SNS 共有時の文言 | `_src/build_pages.py` の `PAGES` |
| 構造化データ（名前・別名・所属・出身大学・LinkedIn・得意分野） | `_src/build_pages.py` の `PERSON` |
| 正規URL（canonical）と、英語版・日本語版の対応（hreflang：en / ja / x-default） | 自動生成（テンプレートの `<head>`） |
| サイトマップ（両ページと hreflang、更新日） | 自動生成（`sitemap.xml`） |
| クローラー向けの案内 | `robots.txt` |
| 画像の代替テキスト（英語・日本語） | テンプレートの `alt` / `data-ja-alt` |
| ファビコン（Google 検索結果のアイコン） | `favicon.ico`・`brand/mark.svg`・`brand/favicon-192.png` |

### Google Search Console

- **プロパティ**：`https://dkeikichi.com/`（URLプレフィックス）。この1つで `/ja/` も含めてすべてのページを扱えます。
- **所有者確認**：`google1739cd937b765b4b.html`（HTMLファイル方式）
- **サイトマップ**：`sitemap.xml` を1つだけ登録しています。

> ⚠️ `/ja/` 用のプロパティを別に作ったり、`/ja/sitemap.xml` を登録したりしないでください。そのファイルは存在しないため「Couldn't fetch（取得できませんでした）」になります。

### 内容を大きく変えたあと

Search Console の **URL検査** で次の2つを入力し、「インデックス登録をリクエスト」を押すと、Google への反映が早まります（1日の回数に上限があるので、各1回で十分です）。

- `https://dkeikichi.com/`
- `https://dkeikichi.com/ja/`

### 確認に使えるツール

- [リッチリザルトテスト](https://search.google.com/test/rich-results)：構造化データにエラーがないか
- [PageSpeed Insights](https://pagespeed.web.dev/)：表示速度と SEO の採点（2026年9月の Lighthouse 計測では、英語版・日本語版ともスマホで Performance / Accessibility / SEO が100点）
- Google で `site:dkeikichi.com` と検索：登録されているページの一覧

---

## 6. デザインのルール

### 色（`styles.css` の `:root`）

| 変数 | 色 | 用途 |
|---|---|---|
| `--ana-blue` | `#0b4d94` | メインの青（ボタン・現職の印） |
| `--deep` | `#062a56` | 濃紺（見出し・フッター） |
| `--sky` | `#2f7fe0` | 明るい青（箇条書きの印・アクセント） |
| `--sky-light` | `#7db9f0` | 淡い青（線・グラデーション） |
| `--bg` | `#f3f8fd` | ページの背景 |
| `--text` | `#16283c` | 本文 |
| `--muted` | `#54708c` | 補足の文字（日付など） |
| `--line` | `#dbe9f6` | カードの枠線 |

文字の読みやすさの基準（WCAG のコントラスト比 4.5:1）を満たすように、役職名は `#256ec9`、フッターの著作権表示は白の75%にしています。色を変えるときは、この基準を下回らないようにしてください。

### 文字

- 英語版：Inter（Google Fonts）
- 日本語版：Noto Sans JP（Google Fonts）
- 表示を速くするため、フォントの読み込みを待たずに先に文字を表示します（初回だけ、一瞬標準の書体で表示されることがあります）。

### 画面幅ごとの切り替え

| 画面幅 | 主な変化 |
|---|---|
| 901px 以上 | PC表示。ヘッダーにロゴ（高さ34px）・メニュー・言語切り替え |
| 900px 以下 | タブレット。ロゴを28pxにし、メニューの間隔を詰める |
| 720px 以下 | スマホ。メニューを隠し、言語切り替えを右端へ。職歴の日付を社名の下へ |
| 380px 以下 | ロゴを24pxに |
| 340px 以下 | ロゴを21pxに |
| 動きを減らす設定の端末 | アニメーションを止める |

320px 幅（小さいスマホ）まで、横スクロールが出ないことを確認済みです。

### スクロール時の表示

カード（職歴・学歴・自己紹介）は `reveal` クラスで、画面に入ったときにふわっと表示されます。JavaScript が動かない環境でも最初から表示されるよう、`<html>` に `js` クラスが付いたときだけ隠す仕組みです。

---

## 7. JavaScript の動き

| 場所 | 動き |
|---|---|
| 英語版の `<head>`（`_src/build_pages.py` の `head_script`） | 以前に「日本語」を選んだ人（ブラウザに `lang=ja` が保存されている人）が `/` を開くと、`/ja/` へ移動します |
| 両方の `<head>` | `<html>` に `js` クラスを付けます（スクロール表示用） |
| `script.js` | 言語切り替えのリンクを押したときに、選んだ言語をブラウザに保存します。カードのスクロール表示を行います |

ブラウザの言語設定による自動切り替えは、Google の推奨に従って**行っていません**。初めての人は、ブラウザが日本語でも英語版から始まり、右上の「日本語」で切り替えます。検索エンジンは常に英語版・日本語版をそれぞれ正しく読み込めます。

---

## 8. 画像

表示サイズの約2倍に縮小した WebP を `img/` に置いています。元の画像はルートに残しています。

| 表示用ファイル | 元画像 | 表示サイズ（PC） |
|---|---|---|
| `img/profile.webp`（336×448） | `IMG_1545.JPG` | 168px の円形 |
| `img/logo-lenovo.webp` | `Lenovo-Logo-scaled.webp` | 高さ34px |
| `img/logo-nx.webp` | `NX_logo.svg.png` | 高さ34px（最大幅130px） |
| `img/logo-agc.webp` | `AGC_Logo.svg.png` | 高さ34px |
| `img/logo-tcu.webp` | `tcu.png` | 高さ44px（最大幅130px） |
| `All_Nippon_Airways_Logo.svg.png`（そのまま使用） | ― | 高さ34px（元が小さいため縮小不要） |

### 画像を追加するとき

1. 表示サイズの2倍程度に縮小して WebP にします。例（Pillow）：

   ```bash
   python3 -c "from PIL import Image; im=Image.open('元画像.png'); im.thumbnail((260, 68)); im.save('img/logo-xxx.webp', lossless=True)"
   ```

2. `<img>` には次を付けます。
   - `width`・`height`（画像の縦横比。読み込み中に表示がずれるのを防ぐ）
   - `alt`（内容が分かる説明。日本語版用に `data-ja-alt`）
   - ページの下の方の画像には `loading="lazy" decoding="async"`

---

## 9. ロゴ・アイコン・共有画像

### デザイン

「North Star」ロゴ：斜体の極太文字「KEIKICHI DEN」（Archivo Expanded Black Italic）と、遠近感をつけた8方向の星（右上の光線だけ長く伸ばして進行方向を表現）の組み合わせ。星はオリジナルのデザインです。

### ファイルと用途

| ファイル | 用途 |
|---|---|
| `brand/logo.svg` / `logo-white.svg` | ロゴ全体（星が大きい版）。白背景用 / 青背景用。名刺・資料向け |
| `brand/logo-transparent.png` / `logo-white-transparent.png` | ロゴ全体の背景透過PNG（横3000px）。明るい背景用 / 暗い背景用。SVGが使えないアプリ・資料・SNS向け |
| `brand/logo-navy.png` | 紺背景（`#062a56`）に白ロゴのPNG（3000×860px）。この README のバナー。名刺・資料の表紙・署名向け |
| `brand/logo-compact.svg` / `logo-compact-white.svg` | 星を控えめにした版。サイトのヘッダー（黒）には白版 `logo-compact-white.svg` を使用 |
| `brand/mark.svg` | 星のアイコン（紺の角丸四角）。ファビコン |
| `brand/favicon-192.png` | ファビコン（192px） |
| `favicon.ico` | ファビコン（16/32/48px。Google 検索結果用） |
| `brand/apple-touch-icon.png` | iPhone のホーム画面アイコン（180px） |
| `brand/og-image.png` | SNS 共有画像（1200×630px） |

### 作り直し方

**SVG（ロゴ・アイコン）**

```bash
pip install fonttools uharfbuzz
python3 brand/build_logo.py
```

フォントは初回に Google Fonts から `brand/.fonts/` へ自動でダウンロードされます（Git には含めません）。星の大きさ・光線の長さ・色は `brand/build_logo.py` で調整できます。

**PNG・ICO**（SVG から書き出し。例として librsvg と Pillow を使う場合）

```bash
rsvg-convert -w 192 -h 192 brand/mark.svg -o brand/favicon-192.png
rsvg-convert -w 180 -h 180 -b '#0b4d94' brand/mark.svg -o brand/apple-touch-icon.png
python3 -c "from PIL import Image; Image.open('brand/favicon-192.png').save('favicon.ico', sizes=[(16,16),(32,32),(48,48)])"
```

**SNS 共有画像**：`_src/og-image.html` を Chrome で開き、開発者ツールで表示サイズを 1200×630 にして「スクリーンショットをキャプチャ」し、`brand/og-image.png` として保存します。

> SNS やブラウザは古い画像を覚えていることがあります。LinkedIn の共有画像は [Post Inspector](https://www.linkedin.com/post-inspector/) で `https://dkeikichi.com` を入れると更新できます。

---

## 10. 履歴書PDF

| ファイル | ボタン |
|---|---|
| `KeikichiDen_CV_EN.pdf` | 英文履歴書（CV (English)） |
| `KeikichiDen_Resume_JA.pdf` | 和文履歴書（CV (Japanese)） |

- 内容を更新するときは、**同じファイル名**で上書きして push します（HTMLの変更は不要）。
- ボタンを押すとダウンロードされます（`download` 属性）。
- 公開されているファイルなので、Google の検索結果にも表示されることがあります。

---

## 11. アクセス解析

**Cloudflare Web Analytics** を使っています（Cookie を使わない計測）。

- **見る場所**：Cloudflare → Analytics & Logs → Web Analytics → `dkeikichi.com`
- **分かること**：訪問数・表示回数・国・端末・ブラウザ・どこから来たか（Referers）・見られたページ（`/` と `/ja/`）
- **計測コード**：`_src/index.template.html` の最後（`static.cloudflareinsights.com/beacon.min.js`）。コード内の token は公開されても問題ないものです。
- 広告ブロッカーを使う人のアクセスは計測されないため、実際より少し少なめに出ます。ご自身の閲覧も数に含まれます。

Google 検索での表示回数・クリック数・検索キーワードは、Google Search Console の「検索パフォーマンス」で見られます。

---

## 12. 公開の仕組み（GitHub Pages）

- **設定**：リポジトリの Settings → Pages で、Source は「Deploy from a branch」（`main` / root）、Custom domain は `dkeikichi.com`、**Enforce HTTPS はオン**にしてください。
- **ドメイン**：`CNAME` ファイルと、ドメイン登録業者側のDNS設定で `dkeikichi.com` を GitHub Pages に向けています。
- **反映の確認**：GitHub の **Actions** → `pages build and deployment` が緑のチェックになれば公開完了です（約1分）。
- **キャッシュ**：GitHub Pages のページは最大10分ほどブラウザにキャッシュされます。変更が見えないときは、再読み込み（Ctrl+Shift+R / Cmd+Shift+R）かシークレットウィンドウで確認します。
- **公開されないもの**：`_` や `.` で始まるフォルダ・ファイル（`_src`、`_archive*`、`.github` など）。GitHub Pages が内部で使う Jekyll の仕様です。
- **README の置き場所**：このファイルは `.github/README.md` にあります。ルートに `README.md` を置くと、Jekyll がサイトのページ（`/README.html`）として公開してしまうためです。

---

## 13. ブランチと作業の流れ

**ブランチ**は、同じサイトのファイル一式を別々に並べて保存しておく仕組みです。本番に影響を与えずに修正を準備できます。

| ブランチ | 役割 |
|---|---|
| `main` | **本番用**。ここに入った内容が dkeikichi.com に公開されます |
| `claude/vibrant-johnson-n1lc3i` | **Claude Code の作業用**。修正をまずここに置き、確認してから `main` に反映します |
| `dependabot/…` | Dependabot が自動で作る更新依頼（PR）用。マージまたはクローズすると自動で消えます |

### 作業の流れ（Claude Code に依頼した場合）

```
修正 ─▶ 作業用ブランチに push ─▶ 確認（スクリーンショットなど）─▶ main に反映 ─▶ 約1分で公開
```

### Branches 画面の見方

リポジトリの **Code → Branches**（またはブランチ名のメニュー → View all branches）で開きます。

| 列 | 意味 |
|---|---|
| Updated | 最後に更新された時刻 |
| Check status | 自動チェック（サイトの公開処理など）の結果。✓ 3 / 3 なら3件すべて成功 |
| Behind / Ahead | Behind＝`main` にあってこのブランチにない変更の数、Ahead＝このブランチにあって `main` にない変更の数。**0 / 0 なら `main` と完全に同じ** |
| Pull request | 変更の取り込み依頼（PR）があれば表示 |

画面は次の区分に分かれています。同じブランチが複数の区分に表示されることがあります。

- **Default**：既定のブランチ（`main`）
- **Your branches**：自分のアカウントで push したブランチ。Claude Code はあなたのアカウントの権限で push するため、作業用ブランチもここに表示されます
- **Active branches**：最近更新されたブランチ

### 作業用ブランチは消してよいか

- **Behind / Ahead が 0 / 0 のとき**：内容はすべて `main` に入っているので、消しても何も失われません。行の右のゴミ箱アイコンで消せます。次に Claude Code に修正を頼んだときは、必要に応じて作り直されます。
- **Ahead が1以上のとき**：まだ `main` に入っていない変更があるので、消さないでください。

### GitHub の画面で直接直すとき

ブラウザ上では `python3 _src/build_pages.py` を実行できません。

- ✅ **直接直してよい**：`styles.css`、`script.js`、`.github/README.md`、PDF の差し替え
- ❌ **直接直さない**：`index.html`・`ja/index.html`・`sitemap.xml`（自動生成）。文章の修正は、テンプレートを直して作り直せる環境（手元のPC、または Claude Code）で行います

### Dependabot の更新依頼（PR）

`_archive` の古いプロジェクトについて、Dependabot がライブラリの更新依頼（PR）を自動で作ることがあります。`_archive` はサイトに公開されないので、マージしてもクローズしても**サイトの表示には影響しません**（マージすると公開処理が1回動きますが、表示は変わりません）。依頼自体を止めたい場合は、Settings → Code security で Dependabot を無効にします。

---

## 14. アーカイブ

以前のサイトを、フォルダごと保存しています。どれもサイトには公開されません。

| フォルダ | 内容 |
|---|---|
| `_archive` | 最初のデザイン（React / Create React App で作ったもの）と `index-legacy.html` |
| `_archive_2026-09-27` | 2026-09-27 の内容見直し前（ANA Systems の職歴を追加した直後） |
| `_archive_2026-09-27_v2` | 2回目の修正前（表記統一・会社名の日本語化などの前） |
| `_archive_2026-09-27_v3` | 英語版・日本語版を分ける前（1ページで言語を切り替えていた版。ロゴ・SEO対策済み） |

**手元で見るとき**（各フォルダは単体で表示できます）

```bash
cd _archive_2026-09-27_v3
python3 -m http.server 8000
```

> `_archive` の古いプロジェクト（`node_modules`）が原因で、GitHub の Dependabot のアラートや失敗通知が出ることがあります。サイトには公開されていないので影響はありません。不要なら Settings → Code security で Dependabot を止められます。

---

## 15. 困ったとき

| 症状 | 原因 | 対処 |
|---|---|---|
| 変更がサイトに出ない | 公開処理が未完了、またはキャッシュ | Actions の完了を待つ／再読み込み（Ctrl+Shift+R） |
| 片方の言語だけ文章が消えた | `lang-en` か `lang-ja` の片方しか書いていない | 両方を書いて作り直す |
| 日本語版だけ画像やCSSが出ない | パスが `/` から始まっていない | `src="/img/…"` のように直す |
| 手元で開くと表示が崩れる | HTMLファイルを直接開いている | `python3 -m http.server 8000` で確認する |
| `index.html` を直したのに元に戻った | 自動生成ファイルを直接編集した | テンプレートを直して作り直す |
| `/` を開くと日本語版に移動する | 以前「日本語」を選んだ記憶が残っている | 右上の「EN」を押すと英語版が記憶される |
| Search Console のサイトマップが「Couldn't fetch」 | 存在しないサイトマップを登録した | 「⋮」→「サイトマップを削除」。登録は `sitemap.xml` だけでよい |
| Google 検索のアイコンやタイトルが古い | Google がまだ読み直していない | URL検査でインデックス登録をリクエストし、数日〜数週間待つ |
| Cloudflare のアクセス数が0 | 公開直後、広告ブロッカー、キャッシュ | 数分待つ／ブロッカーのないスマホで開く |
| ロゴのスクリプトがフォントの取得に失敗 | ネットワーク制限 | Google Fonts に接続できる環境で実行する |
| Branches に見慣れないブランチがある | Claude Code の作業用、または Dependabot の更新依頼用 | [13章](#13-ブランチと作業の流れ)を参照。Behind / Ahead が 0 / 0 なら消してよい |

---

## 16. 更新履歴

**2026-09-27**
- ANA Systems の職歴を追加。職歴の書き方を他社とそろえ、PC表示で1行に
- 学位を B.Eng.（学士（工学））に修正、AGC の入社月・役職名を修正
- 自己紹介を段落分けし、日本語を体言止め・1文ごとの改行に
- 表記ゆれの統一、英語の文法修正、会社名の日本語表記
- スマホでの改行位置、文字のコントラスト、JavaScript がない環境での表示を改善
- 電話番号をフッターから削除、履歴書PDFのファイル名を変更
- 「North Star」ロゴを作成し、ヘッダー・ファビコン・SNS 共有画像に適用
- Google Search Console を設定（所有者確認・サイトマップ）
- Cloudflare Web Analytics を導入
- SEO 対策：タイトル・説明文、構造化データ、canonical、robots.txt、sitemap.xml、画像の軽量化、フォントの読み込み改善
- 英語版（`/`）と日本語版（`/ja/`）を別ページに分割（hreflang 対応）
- 共有画像（SNS・README のバナー）から勤務先を外し、名前を大きくして「IT ENGINEER · TOKYO」に
- ロゴの北極星をブライトブルーに（カラー版）。サイトのヘッダーを黒にして白ロゴを表示
- README を作成（`.github/README.md`）

---

## 17. クレジット

- フォント：[Inter](https://fonts.google.com/specimen/Inter)・[Noto Sans JP](https://fonts.google.com/noto/specimen/Noto+Sans+JP)・[Archivo](https://fonts.google.com/specimen/Archivo)（いずれも SIL Open Font License 1.1）
- 各社・大学のロゴは、それぞれの所有者の商標です。勤務先・出身校を示す目的で掲載しています。
