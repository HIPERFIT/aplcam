
⍝ Parameters: dims, image, degree

h ← dims[1]
b ← dims[2]

m ← h b 3 ⍴ image

m3 ← 3 1 2 ⍉ m

m2 ← ((3 × h) b) ⍴ m3

m2 ← ⌽ m2

m3 ← 3 h b ⍴ m2

m3 ← 2 3 1 ⍉ m3

image ← (h×b×3) ⍴ m3



