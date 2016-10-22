image ← ReadCSVInt 'image.txt'
dims ← ReadCSVInt 'dims.txt'
dims ← 2 ↑ dims
degree ← ReadCSVDouble 'degree.txt'
degree ← degree[1]
h ← dims[1]
w ← dims[2]

image ← h w 3 ⍴ image

onChannels ← {
  m ← 2 3 1 ⍉ ⍵                    ⍝ inv 3 1 2 -→ 2 3 1 (inverse indexing in APL)
  m1 ← h w ⍴ m
  m2 ← h w ⍴ 1↓m
  m3 ← h w ⍴ 2↓m
  m ← (⍺⍺ m1) ⍪ (⍺⍺ m2) ⍪ ⍺⍺ m3
  3 1 2 ⍉ 3 h w ⍴ m                ⍝ inv 2 3 1 -→ 3 1 2
}
