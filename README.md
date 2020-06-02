StartBound Frackin' Universe日本語化ツール
===

# 内容

* このリポジトリは`StarBound`の大型拡張MOD`Frackin' Universe`(以降`FU`)の日本語化ツールです
* `FU`を直接翻訳するツールであり、MODは作成しません
* 翻訳に`Google App Sctipt`(以降`GAS`)を利用します

# 補足

* `GAS`を無料枠で利用する場合、1日に翻訳できる回数に限界があります
* つまり、`FU`全体を翻訳する場合、完了までに数日かかります

# 注意事項

* このツールを起因としたいかなる障害においても、作者は一切の責任を負わないものとします
* 自己責任で利用し、問題の解決は自身で行ってください
* 上記承諾できない方は、利用対象外とさせていただきます

# 開発環境

* OS: `Windows 10`
* IDE: `Visual Studio Code 1.45.1`
* ターミナル: `WSL`
* docker-ce: `19.03.8`
* docker-compose: `1.25.4`
* Python: `3.7.7`

# 必須要件

* Python: `3.7.7`
* GAS

# 使用方法

# 1. リポジトリクローン

```bash
# 任意の作業ディレクトリ移動
$ cd /path/to/workspace/

# Gitクローン
$ git clone git@github.com:rog-works/sb-fu-jp.git
```

## 2. GASに翻訳APIを設置

1. `GAS`を利用するユーザーで`Google`にログイン
1. [GAS](https://script.google.com/home)にアクセス
1. 左ペインの「新しいプロジェクト」を押下し、プロジェクトを作成
1. プロジェクト画面にて、最上部の「無題のプロジェクト」を押下
1. 表示されたダイアログにプロジェクト名を設定し、「OK」を押下
1. `コード.gs`のソースペインに、リポジトリ内の`gas/main.gs`の全文をコピー＆ペースト
1. 上部ツールバーの「公開」＞「ウェブアプリケーションとして導入」を押下
1. 表示されたダイアログ内の「Who has access to the app」の選択ボックスで「Anyone, even anonymous」を選択し、「Deploy」を押下
1. デプロイ後に表示されたURLは後で利用するのでコピーしておく

## 3. `config.py`内の`GAS_URL`に(2)で作成したWebAPIのURLを設定

```bash
$ cd /path/to/workspace/sb-fu-jp

# `GAS_URL`を変更
$ vim config.py

config = {
    'GAS_URL': 'https://script.google.com/macros/s/xxxx/exec',  # 設定例
}
```

## 5. FUのMODデータをアンパック

```bash
# アンパックツールが存在するディレクトリに移動
$ cd /path/to/steamapps/common/Starbound/win32/

# FUのMODデータをコピー
$ cp /path/to/steamapps/workshop/content/211820/729480149/contents.pak ./

# FUのMODデータをバックアップ
$ cp contents.pak ./contents.pak.bak

# MODデータのアンパック
$ asset_unpack.exe contents.pak fu_assets/
```

## 2. アンパックしたMODデータを作業ディレクトリに移動

```bash
# 作業ディレクトリにアンパックしたMODデータを移動
$ mv fu_assets/ /path/to/workspace/sb-fu-jp/

# 翻訳後の出力ディレクトリにもMODデータをコピー
$ cp -R /path/to/workspace/fu_assets/ /path/to/workspace/sb-fu-jp/dest/

# パックツール類を出力ディレクトリにコピー
$ cp asset_packer.exe /path/to/workspace/sb-fu-jp/dest/
$ cp *.dll /path/to/workspace/sb-fu-jp/dest/
```

## 3. MODデータを翻訳

```bash
$ cd /path/to/workspace/sb-fu-jp/

# クエストの翻訳
$ bash 1-quest-trans.sh

# アイテムの翻訳
$ bash 2-item-trans.sh
```

## 4. 翻訳済みのMODデータ再パック

```bash
# 出力ディレクトリに移動
$ cd /path/to/workspace/sb-fu-jp/dest/

# 翻訳後のMODデータを再パック
$ asset_packer.exe fu_assets contents.pak
```

## 5. 翻訳済みのMODデータで元データを上書き

```bash
$ mv contents.pak /path/to/steamapps/workshop/content/211820/729480149/
```

## 6. `Star Bound`を起動

正常にゲームが起動すれば成功！
