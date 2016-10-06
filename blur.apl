blurOne ← {
  m1 ← 1 ⌽ ⍵
  m2 ← ¯1 ⌽ ⍵
  ⌈(⍵ + (m1+m2)÷2) ÷ 2
}

n ← ⌈degree

blur ← { ({⍉ blurOne ⍉ blurOne ⍵} ⍣ n) ⍵ }

image ← blur onChannels image