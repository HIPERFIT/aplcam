square ← {
  offset ← ⌈(w-h)÷2 
  ⍉ h h ⍴ offset↓⍉⍵ 
}

fromSquare ← {
  left ← ⌈(w-h)÷2
  right ← w-(left+h)
  (h left ⍴ 0) , ⍵ , h right ⍴ 0
}

n ← ⌈degree
rot ← { ({⊖⍉⍵} ⍣ n) ⍵ }

fun ← { fromSquare rot square ⍵ }

image ← fun onChannels image