# Spotify Tootプログラム
Spotifyの楽曲情報をMastodonに投稿するプログラムです。楽曲情報データはGoogle Cloud PlatformのFirestoreへの追加もしています。

## 前提
### 各種アカウント、APIの登録
* Spotify APIの登録
* Mastodonのアカウント作成、Mastodon APIの登録
* Mastodonの自分のアカウントだけを追加したリストの作成、リストIDのメモ
* Firestoreのアカウント登録
* Firebaseからサービスアカウントを作成し、JSON秘密鍵の作成（[参考](https://firebase.google.com/docs/app-distribution/authenticate-service-account?hl=ja)）
### Firestoreのコレクション作成
以下のコレクション、フィールドが必要になります。
以下のコレクションを作成し、playlistについては以下のフィールドを持つ必要なドキュメントを追加してください。
* **playlist**
  * id (String) ("consumed"など自分の好きなIDをつけてください)
  * root_toot_id (String) (Mastodonのトゥートのスレッドの一番上（根？）になるトゥートのid)
  * spotify_url (String) (SpotifyのプレイリストのURL)
  * title (String) (メモ用、Spotifyのリスト名を入れてます)
* **musics_(playlistのid)**
  * artist (list\[String\])
  * date (String)
  * id (String) (トゥートのID)
  * title (String) (楽曲名)
  * url (String) (Spotifyの楽曲URL)
### APIキーなどの環境変数の登録
connfig/config.pyで環境変数を取得しています。以下を環境変数に追加してください。
* SPOTIFY_CLIENT_ID
* SPOTIFY_CLIENT_SECRET
* MASTODON_CLIENT_ID
* MASTODON_CLIENT_SECRET
* MASTODON_ACCESS_TOKEN

また、spotify_introduction.pyに記載の通り、環境変数'GOOGLE_APPLICATION_CREDENTIALS'にFirebaseで取得したservice account（jsonファイル）のパスを入れてください。

## 使い方
`pipenv run python spotify_introduction.py`
