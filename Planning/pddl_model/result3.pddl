(cross-together f e i1 i2)
(cross-together b a i1 i2)
(pass-torch f b t2 i2)
(cross-together b a i2 i1)
(pass-torch a c t1 i1)
(cross-together d c i1 i2)
(cross-together b a i1 i2)
(cross-together c a i2 i3)
(pass-torch c a t1 i3)
(cross-alone a i3 i2)
(cross-together d a i2 i4)
(cross-alone a i4 i2)
(pass-torch a e t1 i2)
(cross-together f e i2 i4)
(cross-together b a i2 i3)
; cost = 33 (general cost)
