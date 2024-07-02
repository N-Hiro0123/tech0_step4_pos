# tech0_step4_pos

## アプリ概要

- フロントエンド：Next.js、バックエンドをFastAPI、データベースにAzure MySQLを使用したPOSアプリ

## 準備

- バックエンド
  - python仮想環境に対して、requirements.txtの内容をインストール
    - pip install -r requirements.txt
  - /backendに、.envファイルを作成
    - Azureの設定
      - AZURE_MY_SERVER
      - AZURE_MY_ADMIN
      - AZURE_MY_PASSWORD
      - AZURE_MY_DATABASE
    - JWT認証の設定
      - SECRET_KEY
      - ALGORITHM
  - /backend/db_controlに、SSL認証に必要なファイルをおく
    - SSLパブリック証明書:DigiCertGlobalRootCA.crt.pem
- フロントエンド
  - /frontendにおいて、"npm install"を実行し、package.jsonの内容をインストール
  - /frontendに、.env.localファイルを作成
    - バックエンドのURLの設定
      - NEXT_PUBLIC_API_ENDPOINT

## 実行方法

- AzureのMySQLサーバーの立ち上げ
- バックエンドの立ち上げ
  - /backendにおいて、"uvicorn main:app --reload"
- フロントエンドの立ち上げ
  - /frontendにおいて、"npm run dev"
- webブラウザでフロントエンドにアクセス
  - /register：ユーザー登録画面
  - /login：ログイン画面
  - /purchase：購入画面
- DBに登録されており、商品コード読み込みが通るものは以下のファイルを参照
  - /backend/db_control/make_dummy_db.py
    - 1234567890123, 2345678901234, ... , 01234567890123
