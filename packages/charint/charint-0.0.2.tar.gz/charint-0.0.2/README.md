# charint

charint とはエクセルやスプレッドシートの `A` や `AZ` 等の表現を整数に変換したり、逆に整数を文字列に変換できるライブラリです

## 使い方

### 文字列から整数に変換

```python
from charint import chars2num

char = 'Z'
chars_radix_type = 'ALPHABET' # chars.py の CHARS_RADIXES の列挙の中から選択する

print(chars2num(char, chars_radix_type)) # 25

```

### 整数から文字列に変換

```python
from charint import num2chars

num = 25
chars_radix_type = 'ALPHABET' # chars.py の CHARS_RADIXES の列挙の中から選択する

print(num2chars(num, chars_radix_type))

```

## 拡張

`JAPANESE` の名前で文字基数 `あかさたなはまやらわ` を追加

```python
from charint import CHARS_RADIXES

class MyCHARS_RADIXES(CHARS_RADIXES):
    JAPANESE = 'あかさたなはまやらわ'
    
```
