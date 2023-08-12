# ADV360-PRO-ZMK

![PXL_20230403_144852246](https://user-images.githubusercontent.com/92862731/229546810-cf623a0a-2c2f-45e3-b710-8f3eaecbc795.jpg)

## Build

```bash
make
cp ./firmware/*-left.uf2  /Volumes/ADV360PRO/.
cp ./firmware/*-right.uf2  /Volumes/ADV360PRO/.
```

---
# TODO

## 移植

ghの横を使う

```js
{
    description: "アプリ一覧(現在のスペース",
    from: {
      key_code: keyMap.lr_rl,
    },
    type: "basic",
    to: [
      {
        key_code: "tab",
        modifiers: ["option"],
      },
    ],
  },
  {
    description: "アプリ一覧(すべてのスペース",
    from: {
      key_code: keyMap.ll_rr,
    },
    type: "basic",
    to: [
      {
        key_code: "tab",
        modifiers: ["option", "control"],
      },
    ],
  },
```

---




- Figmgaが使いにくいので
  - del, tab を左
  - alt, ctrl を押しやすく
  - このレイヤーが参考になるかも？
    - https://github.com/manna-harbour/miryoku/tree/master

- マウスとの相性が悪いので
  - モディファイキーを即発火
- かえうちも視野
- Grabshell 届いたら
- charybdis も試す