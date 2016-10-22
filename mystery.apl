⍝ Parameters: dims, image, degree

h ← dims[1]
w ← dims[2]

onChannelRows ← {
  m2 ← ((3×h) w) ⍴ 2 3 1 ⍉ ⍵ 
  m2 ← ⍺⍺ m2
  3 1 2 ⍉ 3 h w ⍴ m2
}

onChannelCols ← {
  m ← h (3×w) ⍴ 1 3 2 ⍉ ⍵ 
  m ← ⍺⍺ m
  1 3 2 ⍉ h 3 w ⍴ m
}

image ←	⊖ onChannelCols ⌽ onChannelRows image


