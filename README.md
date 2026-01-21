# Vim DSL Keymap for Kinesis Advantage 360 Pro (ZMK)

このリポジトリは、**Kinesis Advantage 360 Pro** 用に作成された **Vim-first キーマップ**を収録しています。  
ZMK ファームウェア上で Vim の編集言語（DSL）をそのまま物理キーボードのレイヤーとして実装することで、Neovim・VSCode Vim・Terminal Vim など、エディタに依存しない統一的な操作感を実現します。

---

## 理念

- **Vim を物理言語として実装**：Insert レイヤーを通常入力、Nav レイヤーを Vim Normal モードとみなし、キーボード自身が Vim の文法を解釈します。
- **親指中心のモード制御**：Esc キーに頼らず、親指のホールドでモードを切り替えます。左親指の Space ホールドで Normal モード、右親指の Enter ホールドで Fn レイヤーに入ります。
- **役割の明確化**：左手はオペレータ（削除・変更・ヤンク等）、右手はモーション（hjkl・単語移動等）を担当。親指はモードと修飾キーの操作に徹します。

---

## ファイル構成

```
config/
├── adv360.keymap # メインのキーマップ（レイヤーとバインディング）
├── macros.dtsi # Vim 文法用マクロ定義
├── combos.dtsi # Vim ショートハンド用コンボ定義
└── adv360.conf # マクロ・コンボの有効化と Hold-Tap 設定
```

---

## レイヤー構成の概要

テキストベースでレイヤーの役割と親指の動きが分かるように図示しました。

```
────────────────────────────────────────────────────────
Kinesis Advantage 360 Pro — Logical Layer Model (Vim DSL)
────────────────────────────────────────────────────────

                    ┌───────────────────┐
                    │   Fn Layer (2)     │
                    │  F-keys / OS cmds │
                    │  (Hold Right Thumb)│
                    └─────────▲─────────┘
                              │
                              │ Hold Enter
                              │
┌───────────────────┐   ┌──────┴──────┐   ┌───────────────────┐
│  Base Layer (0)   │   │  Nav Layer  │   │  Base Layer (0)   │
│  Insert / Typing │◄──►│  Vim Normal│◄──►│  Insert / Typing │
│                   │   │  DSL Layer │   │                   │
│  Tap: Space       │   │  (Hold only)│   │  Release Space    │
└─────────▲─────────┘   └──────▲──────┘   └─────────▲─────────┘
          │                    │                    │
          │ Hold Space         │ Vim Grammar        │
          │                    │ (macros + combos) │
          │                    │                    │
          │         ┌───────────────────────────┐
          │         │  Vim DSL (Firmware Level) │
          │         │  d c y + motions           │
          │         │  dd gg iw ap (macros)     │
          │         │  jk df gh (combos)        │
          │         └───────────────────────────┘


Thumb Responsibilities
────────────────────────────────────────────────────────
Left Thumb:
  - Space (Hold) → Enter Vim Normal (Nav)
  - Ctrl         → Vim / Terminal control
  - Alt          → Meta / Option

Right Thumb:
  - Enter (Hold) → Fn layer
  - Cmd          → macOS commands
  - Shift        → Capital / selection

Mental Model:
  Hold Space = Vim Normal
  Left hand = verbs (operators)
  Right hand = motions
  Thumbs = modes and control

```


---

## チートシート

### モード制御

- **Normal へ入る**：左親指の Space を押し続ける  
- **Insert へ戻る**：Space を離す  
- **Esc**：`j` と `k` を同時押し  

### モーション（右手）

- `h` `j` `k` `l`：← ↓ ↑ →  
- `w`：次の単語へ  
- `b`：前の単語へ  
- `e`：単語の終わりへ  
- `0`：行頭  
- `$`：行末  
- `gg`：ファイル先頭  
- `G`：ファイル末尾  

### オペレータ（左手）

- `d`：削除  
- `c`：変更  
- `y`：ヤンク  
- `x`：1文字削除  
- `p`：貼り付け  
- `u`：Undo  
- `Ctrl+r`：Redo  

### テキストオブジェクト（マクロ）

- `iw`：単語の内側  
- `aw`：単語を含む全体  
- `ip`：段落の内側  
- `ap`：段落全体  

### ファームウェアレベルのマクロ

- `dd`：行削除  
- `cc`：行変更  
- `yy`：行ヤンク  
- `gg`：ファイル先頭へ移動  

### コンボ（Nav レイヤーのみ）

- `j + k`：Esc  
- `d + f`：`dd` (行削除)  
- `g + h`：`gg` (ファイル先頭)  
- `u + i`：`iw` (単語の内側)  
- `u + o`：`aw` (単語を含む全体)  

---

## ビルドと書き込み

1. このリポジトリを fork し、変更を push すると GitHub Actions により自動でファームウェアがビルドされます。  
2. Actions の Artifacts から `left.uf2` と `right.uf2` をダウンロードします。  
3. 左右のモジュールをブートローダーモードでマウントし、それぞれ対応する `.uf2` をドラッグ＆ドロップして書き込みます。  

---

この README の内容を参考に、Vim DSL キーマップを最大限に活用してください。

