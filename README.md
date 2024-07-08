# チュパ音生成API(Cloud Run用)

[チュパ音合成デモ](https://huggingface.co/spaces/votepurchase/sbv2_chupa_demo)をウェブAPIで使うためのスクリプト(Cloud Run用)

ベースURL

```
https://chupa-api-omc3n2et7a-an.a.run.app
```

## エンドポイント

### ランダムにサンプルテキスト生成

```
/generate_random
```

**リクエスト**

```
curl -X GET https://chupa-api-omc3n2et7a-an.a.run.app/generate_random
```

**レスポンス**

```
{
  "random_result": "あ……ふぁ……。ちゅ。んちゅ……ちゅ……！ちゅっちゅっ"
}
```

### チュパ音生成

**リクエスト**

```
curl -X POST -H "Content-Type: application/json" -d '{"text":"わかりました……ではこのまま……んっ……ちゅっ……れろっ……んちゅっ……"}' https://chupa-api-omc3n2et7a-an.a.run.app/generate_sound
```

**レスポンス**

Base64エンコードされたMP4動画が返される。プレフィックス`data:video/mp4;base64,`はつかない。

```
{
  "video_result": "AAAAIGZ0eXBpc29tAAACAGlzb21pc28yYXZjMW1wNDEAAAAIZnJlZQAUHFJtZGF0AAACvwYF//+73EXpvebZSLeWLNgg2SPu73gy..."
}
```

## ファイル説明

- chupa_api.py: Cloud Run用
- generate.py: 必要な関数
- test.py: ローカルで動画生成関数を動かす用
- test_generate_video.py: チュパ音生成APIテスト用(生成された動画をローカルに保存して確認したい場合に使用)
- base_image.png: 動画にする際のプレースホルダー画像