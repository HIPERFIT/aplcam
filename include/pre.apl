image ← ReadCSVInt 'image.txt'
dims ← ReadCSVInt 'dims.txt'
dims ← 2 ↑ dims
degree ← ReadCSVDouble 'degree.txt'
degree ← degree[1]
h ← dims[1]
w ← dims[2]

onChannels ← {
  m ← h w 3 ⍴ ⍵ 
  m ← 3 1 2 ⍉ m 
  m1 ← h w ⍴ m
  m2 ← h w ⍴ 1↓m
  m3 ← h w ⍴ 2↓m
  m ← (⍺⍺ m1) ⍪ (⍺⍺ m2) ⍪ ⍺⍺ m3
  (h×w×3) ⍴ 2 3 1 ⍉ 3 h w ⍴ m
}
