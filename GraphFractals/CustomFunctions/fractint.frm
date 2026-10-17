comment {
 This iteration of FRACTINT.FRM was first released with Fractint 19.0

 The formulas at the beginning of this file are from Mark Peterson, who
 built this fractal interpreter feature.  The rest are grouped by contributor.
 Formulas by unidentified authors are grouped at the end.

 If you would like to contribute formulas for future versions of this file,
 please contact one of the authors listed in FRACTINT.DOC.
 All contributions are assumed to belong to the public domain.

 There are several hard-coded restrictions in the formula interpreter:

 1) The fractal name through the open curly bracket must be on a single line.
 2) There is a hard-coded limit of 2000 formulas per formula file, only
    because of restrictions in the prompting routines.
 3) Formulas can contain at most 250 operations (references to variables and
    arithmetic); this is bigger than it sounds.
 4) Comment blocks can be set up using dummy formulas with no formula name
    or with the special name "comment".

 Note that the builtin "cos" function had a bug which was corrected in
 version 16.  To recreate an image from a formula which used cos before
 v16, change "cos" in the formula to "cosxx" which is a new function
 provided for backward compatibility with that bug.
 }
{--- Carl Sansfacon}
Carl1 {; Mark Peterson
  ; Classical fractal showing LastSqr speedup
  z = Pixel, z = (z+p1) ^ z - 1:  ; Start with z**2 to initialize LastSqr
  param2 = (p2 == 0)
   z = fn1(z - p1)
   y = x + y ^ param2
   x = fn2((z + p1 - y) * z)
   |z| <= 4

  }

Carl2 {

z = Pixel :
z = z * sin(z) + 1


}

Carl3 {
z=Pixel:
u =  Pixel +p1

p = fn1(u + pixel)-p1

z = (P / U) * z
|z| <= 4


}
carl4{
z=Pixel:
z=fn1( fn2(z*z/(z - 1))/((z+1)/(z*z))*(z*z/(z + 1))/((z-1)/(z*z))   /   fn3(z*z/(z + 1))/((z-1)/(z*z))*(z*z/(z - 1))/((z+1)/(z*z)) ) +P1
;try fn1 = sin,fn2 = recip, fn3 = sin ,p1=(,)
;try fn1 = ,fn2 = , fn3 = ,p1=(,)

}
carl5{
z=Pixel:
z= (z*z/(z - 1))/((z+1)/(z*z))

}
carl6{
z=Pixel:
z= (z*z/(z - 1))/((z+1)/(z*z))*(z*z/(z + 1))/((z-1)/(z*z))   /   (z*z/(z + 1))/((z-1)/(z*z))*(z*z/(z - 1))/((z+1)/(z*z)) + 1

}

carl7{
z=Pixel,c=1,n=0:
c = (c * 2+1)/((c * 2-1)) * P1
cpos = (c > 0) + fn3(P1* P1 - n)
cneg = (c <= 0) - fn3(P1* P1 - n *2)
c = cpos + cneg
z= fn1(z*z/(z - 1))/((z+1)/(z*z))*(z*z/(z + 1))/((z-1)/(z*z))   /   fn2(z*z/(z + 1))/((z-1)/(z*z))*(z*z/(z - 1))/((z+1)/(z*z)) + n - c
n=n+1
}

Carl8 {
;(pour créer des variantes :)
z = Pixel, w = 2*3.14159265358979*real(P1):
R = real(z)

C = -imag(z)*(1/(w*imag(P2)))
L = imag(z)*w * imag(P3)
z = R + C + L
}

Carl9 {
; exp, flip,tan
z = Pixel, w = 2*3.14159265358979*600000,defaultp1 = (.3,.3),defaultp2 = (6,6):
R = real(z)
myp1 = (imag(P1) !=0) * imag(P1) + (imag(P1) == 0) * imag(defaultp1)

myp2 = (imag(P2) !=0) * imag(P2) + (imag(P2) == 0) * imag(defaultp2)

C = fn1(-imag(z)*(1/(w*myp1)))
L = fn2(imag(z)*w * myp2)
z = fn3(R + 1/(1/C + 1/L))
;z = fn3(R + C + L)

|z| <= 4
}

Carl10 {
; log, sin, Cosxx ou tan

z = Pixel, w = 2*3.14159265358979,defaultp1 = (5,.3),defaultp2 = (6,6):
R = 50
myp1 = (P1 != (0,0)) * P1 + (P1 == (0,0)) * defaultp1

myp2 = (P2 !=(0,0)) * P2 + (P2 == (0,0)) * defaultp2

C = fn1(-z*(1/(w*myp1)))
L = fn2( z* w * myp2)
z = fn3(R+ 1/(1/C + 1/L))
;z = fn3(R + C + L)

|z| <= 4
}

Carl11 {
; log, sin, Cosxx ou tan

z = Pixel, w = 2*3.14159265358979*10,defaultp1 = (5,.3),defaultp2 = (6,6):
R = 50
myp1 = (P1 != (0,0)) * P1 + (P1 == (0,0)) * defaultp1

myp2 = (P2 !=(0,0)) * P2 + (P2 == (0,0)) * defaultp2

C = fn1(z*(1/(w*myp1)))
L = fn2( -z* w * myp2)
z = fn3(((C+L)/(C*L+R))/((C+L)/(C*L-R)))
;z = fn3(R + C + L)

|z| <= 4
}

Carl12 {
; log, sin, Cosxx ou tan

z = Pixel, w = 2*3.14159265358979*10,defaultp1 = (5,.3),defaultp2 = (6,6):
R = 50
myp1 = (P1 != (0,0)) * P1 + (P1 == (0,0)) * defaultp1

myp2 = (P2 !=(0,0)) * P2 + (P2 == (0,0)) * defaultp2

C = fn1(z*(1/(w*myp1)))
L = fn2( -z* w * myp2)
z = fn3(((C+L)/(C*L+R))/((C+L)/(C*L-R))*((C+L)/(C*L+R))/((C+L)/(C*L-R))-((C+L)/(C*L+R))/((C+L)/(C*L-R)))
;z = fn3(R + C + L)

|z| <= 4
}
Carl13 {
; log, sin, Cosxx ou tan

z = Pixel, w = 2*3.14159265358979*10,defaultp1 = (5,.3),defaultp2 = (6,6):
R = 50
myp1 = (P1 != (0,0)) * P1 + (P1 == (0,0)) * defaultp1

myp2 = (P2 !=(0,0)) * P2 + (P2 == (0,0)) * defaultp2

C = fn1(z*(1/(w*myp1)))
L = fn2( -z* w * myp2)
z = fn3(((C+L)/(C*L+R))/((C+L)/(C*L-R))*((C+L)/(C*L+R))/((C+L)/(C*L-R))-((C+L)/(C*L+R))/((C+L)/(C*L-R))*((C+L)/(C*L+R))/((C+L)/(C*L-R))*((C+L)/(C*L+R))/((C+L)/(C*L-R))-((C+L)/(C*L+R))/((C+L)/(C*L-R))-((C+L)/(C*L+R))/((C+L)/(C*L-R))*((C+L)/(C*L+R))/((C+L)/(C*L-R))-((C+L)/(C*L+R))/((C+L)/(C*L-R)))
;z = fn3(R + C + L)

|z| <= 4
}

Carl14 {
z = Pixel,defaultp1 = (5,.3),defaultp2 = (1.5,.1):
; Attenuator
myp1 = (P1 != (0,0)) * P1 + (P1 == (0,0)) * defaultp1
myp2 = (P2 !=(0,0)) * P2 + (P2 == (0,0)) * defaultp2
parallelc1r1 = (imag(myp1) * real(myp1))/(imag(myp1) + real(myp1)) + z
parallelc2r2 = (imag(myp2) * real(myp2))/(imag(myp2) + real(myp2)) + z
z = fn1(parallelc1r1*parallelc2r2)/(parallelc1r1+parallelc2r2)

|z| <= 4
}
Carl15 {
z = Pixel,defaultp1 = (5,.3),defaultp2 = (1.5,.1):
; Attenuator 2eme ordre
myp1 = (P1 != (0,0)) * P1 + (P1 == (0,0)) * defaultp1
myp2 = (P2 !=(0,0)) * P2 + (P2 == (0,0)) * defaultp2
parallelc1r1 = (imag(myp1) * real(myp1))/(imag(myp1) + real(myp1))
parallelc2r2 = (imag(myp2) * real(myp2))/(imag(myp2) + real(myp2))
attenuateurR = (parallelc1r1*parallelc2r2)/(parallelc1r1+parallelc2r2)
attenuateurI = ( parallelc1r1*parallelc2r2)*(parallelc1r1+parallelc2r2)
parallelattenuateurR = (imag(attenuateurR) * real(attenuateurR))/(imag(attenuateurR) + real(attenuateurR)) + z
parallelattenuateurI = (imag(attenuateurI) * real(attenuateurI))/(imag(attenuateurI) + real(attenuateurI)) + z
z = fn1(parallelattenuateurR*parallelattenuateurI)/(parallelattenuateurR+parallelattenuateurI)



|z| <= 4
}

Carl16 {
z = Pixel,defaultp1 = (5,.3),defaultp2 = (1.5,.1):
; Attenuator 3eme ordre modif
myp1 = (P1 != (0,0)) * P1 + (P1 == (0,0)) * defaultp1
myp2 = (P2 !=(0,0)) * P2 + (P2 == (0,0)) * defaultp2
parallelc1r1 = (imag(myp1) * real(myp1))/(imag(myp1) + real(myp1))
parallelc2r2 = (imag(myp2) * real(myp2))/(imag(myp2) + real(myp2))
attenuateurR = (parallelc1r1*parallelc2r2)/(parallelc1r1+parallelc2r2)
attenuateurI = ( parallelc1r1*parallelc2r2)*(parallelc1r1+parallelc2r2)
parallelattenuateurR = (imag(attenuateurR) * real(attenuateurR))/(imag(attenuateurR) + real(attenuateurR)) + z
parallelattenuateurI = (imag(attenuateurI) * real(attenuateurI))/(imag(attenuateurI) + real(attenuateurI)) + z

parallelattenuateurR2 = (imag(parallelattenuateurR) * real(parallelattenuateurI))/(imag(parallelattenuateurR) + real(parallelattenuateurI)) + z
parallelattenuateurI2 = (imag(parallelattenuateurI) * real(parallelattenuateurR))/(imag(parallelattenuateurI) + real(parallelattenuateurR)) + z

z = fn1(parallelattenuateurR2*parallelattenuateurI2)/(parallelattenuateurR2+parallelattenuateurI2)



|z| <= 4
}

Carl17 {
z = Pixel,defaultp1 = (5,.3),defaultp2 = (1.5,.1):
; Attenuator 3eme ordre modif
myp1 = (P1 != (0,0)) * P1 + (P1 == (0,0)) * defaultp1
myp2 = (P2 !=(0,0)) * P2 + (P2 == (0,0)) * defaultp2
parallelc1r1 = (imag(myp1) * real(myp1))/(imag(myp1) + real(myp1))
parallelc2r2 = (imag(myp2) * real(myp2))/(imag(myp2) + real(myp2))
attenuateurR = (parallelc1r1*parallelc2r2)/(parallelc1r1+parallelc2r2)  + z
attenuateurI = ( parallelc1r1*parallelc2r2)*(parallelc1r1+parallelc2r2)  + z
parallelattenuateurR = (imag(attenuateurR) * real(attenuateurR))/(imag(attenuateurR) + real(attenuateurR))
parallelattenuateurI = (imag(attenuateurI) * real(attenuateurI))/(imag(attenuateurI) + real(attenuateurI))

attenuateurR2 = (attenuateurR*attenuateurI)/(attenuateurR+attenuateurI) - z

attenuateurI2 = ( attenuateurR*attenuateurI)*(attenuateurR+attenuateurI) - z
parallelattenuateurR2 = (imag(attenuateurR2) * real(attenuateurR2))/(imag(attenuateurR2) + real(attenuateurR2))
parallelattenuateurI2 = (imag(attenuateurI2) * real(attenuateurI2))/(imag(attenuateurI2) + real(attenuateurI2))


z = fn1(parallelattenuateurR2*parallelattenuateurI2)/(parallelattenuateurR2+parallelattenuateurI2)



|z| <= 4
}

Carl18 {
; MOSFET Drain current ohmic region
z = Pixel,defaultp1 = (5,2),defaultp1 = (6,5) :
myp1 = (P1 != (0,0)) * P1 + (P1 == (0,0)) * defaultp1
myp2 = (P2 !=(0,0)) * P2 + (P2 == (0,0)) * defaultp2
z = z * fn1(2*(1-myp1/myp2)*(z*z/-myp2)-fn2(z*z/myp2)*fn3(z*z/myp2))
}
Carl19 {
; Op-Amp negative feedback
z = Pixel :
z = fn1(P1*fn2(P2 - P3 * z))
|z| <= 4

}
Carl20 {
; Op-Amp negative feedback 2ème ordre
z = Pixel :
z = fn1(P1*fn2(P2 - P3 * z))
z = fn1(z) - fn2(-P2 + P3 / sqr(z))
|z| <= 4

}
Carl21 {
; Op-Amp positive feedback 2ème ordre
z = Pixel :
z = fn1(P1*( P2 * z))
;z = fn1(z) + fn2( P2 / sqr(z))
|z| <= 4

}
Carl22 {
; Op-Amp variations
z = Pixel :
z = (((P1 * 3.14159 * z * z) - z)/((P1 * 3.14159 * z * z) + z))  *  (((P1 * 3.14159 * z * z) + z)/(P1 * 3.14159 * z * z) - z)

|z| <= 4

}

Carl23 {

z = Pixel ,c = 2:
z = (z*(c)*(c-1))/(c+.01)
c =  fn1((c +.1)*(-c +.1) - (z*(z-1)))

|z| <= 4

}
Carl24 {

z = Pixel ,c = P1:
z = z*(c*c)*(c*(c-1))/(c*c+.0001)
c =  fn1((c +.1)*(-c +.1) - (z*(z-.1)))*fn2(z^2)

|z| <= 4

}
Carl25 {

z = Pixel ,c = P1:
z = z*(c*c)*(c*(c-1))/(c*c+.0001)+z*(c*c)/(c*(c+1))*(c*c-.0001)
c =  fn1((c +.1)/(-c +.1) - (z/(z-.1)))+ fn2(z^2)

|z| <= 4

}
Carl26 {

z = Pixel ,c = P1:
z = fn2((((z+z)*(z))*((z+z)*(z/z-.000001)))/(((z+z)/(z*z+.000001))*((z)/(z*z+.0001)))) - c
c = fn1(c+1)

;|z| <= 4

}

Carl27 {

z = Pixel :
z = (z * z + z / (z - 1))*(z * z - z / (z - 1))


;|z| <= 4

}
Carl28 {

z = Pixel :
z = fn3(fn1(z * z + z / (z - 1))*fn2(z * z - z / (z - 1)))*fn3(fn1(z * z + z / (z - 1))*fn2(z * z - z / (z + 1)))


;|z| <= 4

}
Carl29 {

z = Pixel :
z = fn3(fn1(z * z + z / (z - 1))*fn2(z * z - z / (z - 1)))*fn3(fn1(z * z + z / (z - 1))*fn2(z * z - z / (z + 1)))/fn3(fn1(z * z + z / (z + 1))*fn2(z * z - z / (z + 1)))*fn3(fn1(z * z + z / (z + 1))*fn2(z * z - z / (z - 1)))


;|z| <= 4

}

Carl30 {

z = Pixel :
z = fn3(fn2(z * z + z / (z - 1))*fn2(z * z - z / (z - 1)))*fn3(fn2(z * z + z / (z - 1))*fn1(z * z - z / (z + 1)))/fn3(fn1(z * z + z / (z + 1))*fn2(z * z - z / (z + 1)))*fn3(fn1(z * z + z / (z + 1))*fn2(z * z - z / (z - 1)))


;|z| <= 4

}

Carl31 {

z = Pixel ,c=.0265125 :
z = fn3(fn2(z * z + z / (z - c))*fn2(z * z - z / (z - c)))*fn3(fn2(z * z + z / (z - c))*fn1(z * z - z / (z + c)))/fn3(fn1(z * z + z / (z + c))*fn2(z * z - z / (z + c)))*fn3(fn1(z * z + z / (z + c))*fn2(z * z - z / (z - c)))


;|z| <= 4

}
Carl32 {

z = Pixel, c = p1  :
z = fn3(fn2(z * z/(z + z * c))-fn1(z * z/(z - z * c)))*(fn2(z * z/(z - z * c))-fn1(z * z/(z + z * c)))


|z| <= 4

}
Carl33 {

z = Pixel, c = P1  :
z = fn3(fn2(z * c/(z + z * c))-fn1(z * z/(z - z - c)))*(fn2(z * z/(z - z * c))-fn1(z * c/(z + z - c)))


|z| <= 4

}
Carl34 {

z = Pixel, c = p1  :
z = fn3(fn1((z*z-c)*(z*z+c))/fn2((z*z+c)*(z*z+c)) + z)

|z| <= 4

}
Carl35 {

z = Pixel, c = p1 , b =.5  :
z = fn2(fn1(z * (z + b)) / fn3(c + (c + b))) * fn1((z / (z - b)) / fn3(c * (c - b )))

|z| <= 4

}

Carl36 {

z = Pixel ,c1=p1,c2=p2:
z = fn1(z * sqrt(1/2*z*z*c1) + z * sqrt(1/2*z*z*c2))

|z| <= 4

}

Carl37 {

z = Pixel ,c1=p1,c2=p2:
z = fn1((z * fn2(1/2*z*z*c1) + z * fn3(1/2*z*z*c2)) * (z * fn2(1/2*z*z*c1) + z * fn4(1/2*z*z*c2)))

|z| <= 4

}

Carl38 {

z = Pixel ,c1=p1:
z = fn1((z * fn2(1/2*z*z*c1+c1) + z * fn3(1/2*z*z*c1)) / ((z * fn2(1/2*z*z*c1) + z * fn4(1/2*z*z*c1+c1))+1))

|z| <= 4

}
Carl39 {
;mutual resonnance
z = Pixel ,c1=p1:
l2 = 1 / l2 + real(z)
l1 = 1 / l1 + imag(z)
z =  c1 * sqrt(l2/l1)
|z| <= 16

}
Carl40 {
;mutual resonnance
z = Pixel ,c1=p1:
l2 = 1 / l2 + real(z)
l1 = 1 / l1 + imag(z)
z =  fn1(c1 * sqrt(l2/l1))
|z| <= 16

}
Carl41 {
;mutual resonnance
z = Pixel ,c1=p1:
l2 = fn2(1 / l2 + real(z))
l1 = fn3(1 / l1 + imag(z))
z =  fn1(c1 * sqrt(l2/l1))
|z| <= 16

}
Carl42 {
; mutual resonnance
z = Pixel ,c1=p1:
l2 = fn2(1 / l2 + z) + 1
l1 = fn3(1 / l1 + z) + 1
z =  fn1(c1 * sqrt(l2/l1))
|z| <= 16

}
Carl42rand {
; mutual resonnance
z = Pixel ,c1=rand*5:
l2 = fn2(1 / l2 + z) + 1
l1 = fn3(1 / l1 + z) + 1
z =  fn1(c1 * sqrt(l2/l1))
|z| <= 16

}
Carl43{
; mutual resonnance
z = Pixel ,c1=P1:
l2 = fn2(1 / l2 + z) + 1
l1 = fn3(1 / l1 + z) + 1
z =  fn1(c1 * sqrt(l2/l1))
z = z * z
|z| <= 16

}
Carl44{
; mutual resonnance
z = Pixel ,c1=P1:
l2 = fn2(1 / l2 + z) + 1
l1 = fn3(1 / l1 + z) + l2
l2 = l2 + fn3(1 / l1 + z)
z =  fn1(c1 * sqrt(l2/l1))
|z| <= 16

}

Carl45{
; mutual resonnance
z = Pixel ,c1=P1, c2=P2, c3 = P3:
Vgs = c1 * z
Vt = c2 * z
Vds = fn1(Vgs+Vt)/(Vgs*Vt)
z = 0.5*(Vgs-Vt)*(Vgs-Vt)*(1 + c3 * Vds )
;|z| <= 16

}
Carl46{

z = Pixel ,c1=P1, c2=P2, c3 = P3:
Vgs = c1 + (z-1)*(z+1)
Vt = c2 + (z-1)*(z+1)
Vds = fn1(Vgs+Vt)/(Vgs*Vt)
z = 0.5*(Vgs-Vt)*(Vgs-Vt)*(1 + c3 * Vds )
;|z| <= 16

}
Carl47{
z = Pixel ,c1=2.25431683245, c2=.3869433691248, c3 = 3.14159128349663:
Vgs = c1 + (z-1)*(z+1)
Vt = c2 + (z-1)*(z+1)
Vds = fn1(Vgs+Vt)/(Vgs*Vt)
z = fn2(0.5*(Vgs-Vt)*fn3(Vgs-Vt)*(1 + c3 * Vds ))
;|z| <= 16

}
Carl48{
z = Pixel ,c1=p1, c2=p2, c3 = 0.3561356663,c4 =1.13457:
Vgs = c1 + ((z-c4)*(z+c4))
Vt = c2 + ((z-c4)*(z+c4))
Vds = fn1(real(Vgs+Vt)/imag(Vgs*Vt)-c4)*fn1(imag(Vgs+Vt)/real(Vgs*Vt)+c4)
z = fn2(c4/2*(Vgs-Vt)*fn3(Vgs-Vt)*(c4 + c3 * Vds ))
|z| <= 4

}
Carl49{
z = Pixel ,c1=p1, c2=p2, c3 = 0.3561356663,c4 =1.13457:
Vgs = c1 + ((z-c4)*(z+c4))
Vt = c2 + ((z-c4)*(z+c4))
Vds = fn1(real(Vgs+Vt)/imag(Vgs*Vt)-c4)*fn1(imag(Vgs+Vt)/real(Vgs*Vt)+c4)
z = fn2(c4/2*(Vgs-Vt)*fn3(Vgs-Vt)*(c4 + c3 * Vds ))*sqr(z)
|z| <= 4

}
Carl50{
z = Pixel ,c1=p1, c2=p2, c3 = 0.3561356663,c4 =1.13457:
Vgs = c1 - ((z-c4)*(z+c4))
Vt = c2 - ((z-c4)*(z+c4))
Vds = fn1((Vgs+Vt)-(Vgs*Vt)-c4)*fn1((Vgs+Vt)-(Vgs*Vt)+c4)
z = fn2(-(Vgs-Vt*Vt)*fn3(Vgs-Vt-1)*(c4 + c3 * Vds ))+sqr(z)
|z| <= 4

}

Carl51{
z = Pixel ,c1=P1:
z = fn1(fn2(fn3(z * c1 - z)*(z * c1 - z))*((z * c1 + z)*(z * c1 + z))  + ((z * c1 - z)*(z * c1 - z))*((z * c1 + z)*(z * c1 + z)))
;|z| <= 4

}
Carl52{
z = Pixel ,c1=P1:
z = fn1(fn2(fn3(z * c1 - z)*fn3(z * c1 - z))*fn2(fn3(z * c1 + z)*fn3(z * c1 + z))  + fn2(fn3(z * c1 - z)*fn3(z * c1 - z))*fn2(fn3(z * c1 + z)*fn3(z * c1 + z)))
|z| <= 16

}
Carl53{
z = Pixel ,c1=P1:
z = fn3(- z  + c1)
if (z > 0)
  z=fn1(z-1)*z
else
  z=fn2(z+1)*z
end if




|z| <= 16

}
Carl54{
z = Pixel ,c1=P1,c2=P2:
z = fn3(- z  + c1)
if (z > c2)
  z=fn1(z-c1)*z
else
  z=fn2(z+c1)*z
end if




|z| <= 16

}
Carl55{
z = Pixel ,c1=P1,c2=P2:
z = fn3(- z  + c1)
if (z > c2)
  z=fn1(z-c1)*z
  c2 = c2 - c1
else
  z=fn2(z+c1)*z
  c2 = c2 + c1
end if




|z| <= 16

}

Carl56 {
; MOSFET Drain current ohmic region with if
z = Pixel :
if (z < 0)
z = fn3(z)
else
z = fn3(-z)
end if
z = z * fn1(2*(1-p1/p2)*(z*z/-p2)-fn2(z*z/p2)*fn2(z*z/p2))
}

Carl57 {
; MOSFET Drain current ohmic region with if
z = Pixel :
if (z < P3)
z = fn3(z)
else
z = fn3(-z)
end if
z = z * fn1(2*(1-p1/p2)*(z*z/-p2)-fn2(z*z/p2)*fn2(z*z/p2))
}
Carl58 {
; MOSFET Drain current ohmic region with if
z = Pixel :
if (whitesq)
z = fn3(z)
else
z = fn3(-z)
end if
z = z * fn1(2*(1-p1/p2)*(z*z/-p2)-fn2(z*z/p2)*fn2(z*z/p2))
}
Carl59 {
; MOSFET Drain current ohmic region with if
z = Pixel :
if (z>abs(z+1))
z = -fn3(z)
else
z = fn3(-z)
end if
z = z * fn1(2*(1-p1/p2)*(z*z/-p2)-fn2(z*z/p2)*fn2(z*z/p2))
|z| <= 16

}
Carl60 {
; MOSFET Drain current ohmic region with if
z = Pixel :
if (z>abs(z+1))
z = -fn3(-z)
else
z = fn3(z)
end if
z = z * fn1(2*fn2(1.01-p1/p2)*(z*z/-p2)-(z*z/p2)*fn2(z*z/p2 + 1))+.00000000001
|z| <= 16

}
Carl61 {
z = Pixel :
if (fn4(sqr(z)) > P1)
z = (z - 1)/(z + 1)
else
z = (z + 1)/(z - 1)
end if
z = fn1((fn2(z * (z - 1)-1)+fn3(z * (z - 1) + 1))*(fn2(z * (z + 1)-1)+fn3(z * (z + 1) - 1)))
;|z| <= 16

}

Carl62 {
z = Pixel :
z = fn1(z) * z + P1 * whitesq
z = -z * (fn2(z) * z + P1 * ( whitesq -1) )

|z| <= 16

}
Carl63 {
z = Pixel,c=1.4816213168904 :
z = fn1(z) * z + P1 - c
z = -z * (fn2(z) * fn3(z) + sqr(P1 * ( c - 1 )) )

|z| <= 16

}
Carl64 {
z = Pixel,e= P1:
z = e * (z-1)+P2
z = fn3((fn1(z + z-P2) + fn2(z + z+P2))/(fn2(z * z+P2) - fn1(z - z-P2)))
|z| <= 4

}

Carl65 {
z = Pixel,pip = 3.14159128349663:
z = z + pip
if(fn2(z) > P1)
z = fn1(z) + P2
end if


|z| <= 4

}

Carl66 {
z = Pixel,pip = 3.14159128349663:
z = 2 * pip * fn1(sqr(fn2(P1)*fn3(P2))) * z + 1


|z| <= 4

}
Carl67 {
z = Pixel,pip = 3.14159128349663,pii = 1.386094:
z = fn1(2 * pip * sqr(z*z*(-z + P1)) * z ) + z - P1/2


|z| <= 4

}
Carl68 {
z = Pixel,pip = 3.14159128349663,pii = 1.386094:
z = (fn1(2 * pip * sqr(z*z*(-z + P1)) * z ) + z - P1/2)*(fn1(2 / pip / sqr(z/z/(z + P1)) / z ) - z + P1)
if (z < 0 )
z = z + 1
end if


}
Carl69 {
z = Pixel,pip = 3.14159128349663,pii = 1.386094:
z = (fn1(2 * pip * sqr(z*z*(-z + P1)) * z ) + z - P1/2)*((2 / pip / sqr(z/z/(z + P1)) / z ) - z + P1)
if (z < 0 )
z = z * z + 1
else
z = - z + 1
end if


}
Carl70 {
z = Pixel:
z = z + z
z = fn1(z * z)
z = fn2(z + (z * z))
z = fn3(z * (z + z))

}

Carl71 {
z = Pixel:
z = z + z
z = fn1(z * (z + z))
z = fn2(z + (z * z)) + .5
z = fn3(z * z)

}
Carl72 {
z = Pixel:
z = fn1(z * (z + z + z))
z = fn2(-z + (z * z / 2)) + (3.141592653589793238462643383279,1.414213562373095048801688724209)
z = fn3(z * z + (0, 2.718281828459045235360287471352) )
z = z + z
}
Carl73 {
z = Pixel:
z = fn1(z * (z + z + z))
z = 1/fn2(-z + (z * z / 2)) + P1
z = fn3(z * z + P1 )
z = 1/((z * z) + (z - 1 ))/ ( -(z + z) + (z + 1 )*(z + z - sqr(2)))
|z| <= 4

}
Carl74 {
z = Pixel:
z = fn3(1/sqrt(fn2(fn1(2*3.141592653589793238462643383279*z)*p1)))

}
Carl75 {
z = Pixel:
z = fn3(fn2(fn1(z/2+p1)*fn1(z/2-p1))/fn2(fn1(z/2+p1)*fn1(z/2-p1)))
|z| <= 16
}
Carl76 {
z = Pixel:
c1 = (3.141678345267,.04357347)
z = fn1(fn2(fn3(z * (z - c1 )) - (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 )))    /   ( (z * (z - c1 )) + (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 ))))


|z| <= 4
}
Carl77 {
z = Pixel:
c1 = (1.1718293416698,.04357347)
z = fn1(fn2(fn3(z * (z - c1 )) - (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 )))    /   ( (z * (z - c1 )) + (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 ))))
z = fn2(fn2(fn2(z * (z - c1 )) - (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 )))    /   ( (z * (z - c1 )) + (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 ))))
z = fn3(fn2(fn1(z * (z - c1 )) - (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 )))    /   ( (z * (z - c1 )) + (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 ))))
z = fn1(fn3(fn3(z * (z - c1 )) - (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 )))    /   ( (z * (z - c1 )) + (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 ))))
z = fn2(fn2(fn3(z * (z - c1 )) - (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 )))    /   ( (z * (z - c1 )) + (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 ))))
z = fn1(fn3(fn3(z * (z - c1 )) - (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 )))    /   ( (z * (z - c1 )) + (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 ))))
z = fn2(fn3(fn3(z * (z - c1 )) - (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 )))    /   ( (z * (z - c1 )) + (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 ))))


|z| <= 4
}
Carl78 {
z = Pixel:
c1 = (1.1718293416698,.04357347)
z = fn1(fn2(fn3(z * (z - c1 )) - (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 )))    /   ( (z * (z - c1 )) + (z * (z + c1 ))* (z * (z + c1 )) - (z * (z - c1 ))))
z = ((z / (z - c1 )) - (z / (z + c1 ))* (z / (z + c1 )) - (z / (z - c1 )))    +   ( (z / (z - c1 )) + (z / (z + c1 ))* (z / (z + c1 )) - (z / (z - c1 )))
z = (z + 1)*z
|z| <= 4
}
Carl79 {
z = Pixel:
c1 = (1.221683914,0.124)
z = fn3(fn1(z + c1)^fn2(z*2 + c1))
|z| <= 4
}
Carl80 {
z = Pixel:
c1 = (0.2663345788843245,-0.4235115672388)
z = fn1(1/fn2(fn3(39.5*z^2)*c1))
|z| <= 4
}
Carl81 {
z = Pixel:
c1 = p1;(1.2663345788843245,0.4235115672388)
z = fn1((|z| - c1) * z)
z = fn2(-(-z + c1) / z)

|z| <= 4
}

Carl82 {
z = Pixel, m1 = (1,0.02356), m2 = (5,.743556):
;Gravity 1
g = (1,.000000000066743)
R = fn1(((z - 1)*(z + 1))/((z * 1)+(z * -1)))
z = (g * m1 * m2) / (R * R)


|z| <= 4
}
Carl83 {
z = Pixel, g = p1:
;Gravity 2
z = sqr((fn1(z)*fn2(z)*g)/fn3(z))

|z| <= 4
}
Carl84 {
z = Pixel, g = p1:
;Gravity 3
z = fn2(sqr((real(z)*imag(z)*g)/fn1(z)))
z = (z + z)/( z * z)
|z| <= 4
}
Carl85 {
z = Pixel, g = p1:
;Gravity 3
z = fn2(sqr((real(z)*imag(z)*g)/fn1(z)))
z = ( z * z)/(z + z)
|z| <= 4
}
Carl86 {
z = Pixel, g = p1 , g2 = (1.67733,.77436), g3 = (0.36733,.17436):
;Gravity 3
z = fn2(sqr((real(z)*imag(z)*g)/fn1(z)))
z = ( z * z)/(z + z)
z = fn2(sqr((real(z)*imag(z)*g2)/fn1(z)))
z = ( z * z)/(z + z)
z = fn2(sqr((real(z)*imag(z)*g3)/fn1(z)))
z = ( z * z)/(z + z)
|z| <= 4
}
Carl87 {
z = Pixel, g = (3.14158,.17436) , g2 = (1.67733,.77436), g3 = p1:
;Gravity 3
z = fn2(sqr((real(z)*imag(z)*g)/fn1(z)))
z = ( z * z)/(z + z)
z = fn2(sqr((real(z)*imag(z)*g2)/fn1(z)))
z =(z + z) / (z * z)
z = fn2(sqr((real(z)*imag(z)*g3)/fn1(z)))
z = ( z * z)/(z + z)
|z| <= 4
}
Carl88 {
z = Pixel, g = (3.14158,.17436) , g2 = (1.67733,.77436), g3 = p1:
;Gravity 3
z = fn2(sqr((real(z)*imag(z)*g)/fn1(z)))
z = fn2(sqr((real(z)*imag(z)*g2)/fn1(z)))
z = fn2(sqr((real(z)*imag(z)*g3)/fn1(z)))
|z| <= 4
}
Carl89 {
z = Pixel, g = (3.14158,.17436) , g2 = (1.67733,.77436), g3 = p1:
;Gravity 4
if (whitesq)
z = fn2(sqr((real(z)*imag(z)*g)/fn1(z)))
z = fn2(sqr((real(z)*imag(z)*g2)/fn1(z)))
z = fn2(sqr((real(z)*imag(z)*g3)/fn1(z)))
else
z = fn3(sqr((real(z)*imag(z)*g)/fn1(z)))
z = fn3(sqr((real(z)*imag(z)*g2)/fn1(z)))
z = fn3(sqr((real(z)*imag(z)*g3)/fn1(z)))
end if

|z| <= 4
}
Carl90 {
z = Pixel, g = (3.14158,.17436) , g2 = (1.67733,.77436), g3 = p1:
;Gravity 4
if (whitesq)
z = fn2(sqr((real(z)*imag(z)*g)/fn1(z)))
z = 1 / fn2(sqr((real(z)*imag(z)*g2)/fn2(z))) + 1
z = fn2(sqr((real(z)*imag(z)*g3)/fn1(z)))
else
z = fn3(sqr((real(z)*imag(z)*g)/fn1(z)))
z = 1 /  fn3(sqr((real(z)*imag(z)*g2)/fn3(z))) + 1
z = fn3(sqr((real(z)*imag(z)*g3)/fn1(z)))
end if

|z| <= 4
}
Carl91 {
z = Pixel, g = (3.14158,.17436) , g2 = (1.67733,.77436), g3 = p1:
;Gravity 4
if (whitesq)
z = fn2(sqr((real(z)*imag(z)*g)/fn2(z)))
z = 1 / fn2(sqr((real(z)*imag(z)*g2)/fn2(z))) + 1
z = fn3(sqr((real(z)*imag(z)*g3)/fn1(z)))
else
z = fn2(sqr((real(z)*imag(z)*g)/fn1(z)))
z = 1 /  fn3(sqr((real(z)*imag(z)*g2)/fn3(z))) + 1
z = fn3(sqr((real(z)*imag(z)*g3)/fn3(z)))
end if

|z| <= 4
}
Carl92 {
z = Pixel, g = p1 , g2 = p2:
; Et si ?
if (whitesq)
z = (z * (z-1)^g)
else
z = (z * (z-1)^g2)

end if

|z| <= 4
}
Carl93 {
z = Pixel, g = p1 , g2 = p2:
; Et si ?
if (whitesq)
z = fn1(z * fn2(z-1)^g)
else
z = fn1(z * fn2(z-1)^g2)

end if

|z| <= 4
}
Carl94 {
z = Pixel, g = p1 , g2 = p2:
; Et si ?
if (whitesq)
z = fn1(z * fn2(z-1)^g)
else
z = fn2(z * fn1(z-1)^g2)

end if

|z| <= 4
}
Carl95 {
z = Pixel, g = p1 , temp = flip(Pixel):
; Et si ?
if (whitesq)
z = z + fn1(z ^ g)
else
z = temp + fn1(temp ^ g) + z
end if

|z| <= 4
}
Carl96 {
z = Pixel, g = p1 , deviation = (1.78655578663,.925437865):
; Et si ?
if (whitesq)
z = fn2(z + fn1(z-g)^2)
else
z = fn2(z + fn1(z-g+deviation)^2)
end if

|z| <= 4
}
Carl97 {
z = Pixel, g = p1 , deviation = (0.08655578663,.925437865):
; Et si ?
if (whitesq)
z = fn2(z + fn2(z-g-deviation)^2)
else
z = fn1(z + fn1(z-g+deviation)^2)
end if

|z| <= 4
}
Carl98 {
z = Pixel, g = p1:
; Et si ?
if (whitesq)
z = z ^ (z - 1) + z
else
z = z ^ (z + 1) + z
end if

|z| <= 4
}
Carl99 {
z = Pixel:
; Et si ?
if (whitesq)
z = fn1(z ^ (z - 1) + z)
else
z = fn1(z ^ (z + 1) + z)
end if

|z| <= 4
}
Carl100 {
z = Pixel:
; Et si ?
if (whitesq)
z = ((z ^ (z - 1) + z)*(z ^ (z - 1) + z)) * ((z ^ (z + 1) + z)*(z ^ (z - 1) - z))
else
z = ((z ^ (z + 1) + z)*(z ^ (z - 1) + z)) * ((z ^ (z + 1) + z)*(z ^ (z - 1) - z + 1))
end if

|z| <= 4
}
Carl101 {
z = Pixel:
; Et si ?
if (whitesq)
z = fn1((z ^ (z - 1) + z)*(z ^ (z - 1) + z)) * ((z ^ (z + 1) + z)*fn2(z ^ (z - 1) - z))
else
z = fn1((z ^ (z + 1) + z)*(z ^ (z - 1) + z)) * ((z ^ (z + 1) + z)*fn2(z ^ (z - 1) - z + 1))
end if

|z| <= 4
}
Carl102 {
z = Pixel:
; Et si ?
if (whitesq)
z = ((z ^ (z + 1) / (z + 1)) + (z ^ (z * -(z + 1) ) + z/3)) * ((z ^ (1 / (z + 1)) - z) * fn2(z))
else
z = ((z ^ (z + 1) - z)-(z ^ (z + 1) + z/2)) / ((z ^ (z + 1))*fn1(z ^ (z ) + z - 1))
end if

|z| <= 4
}
Carl103 {
z = Pixel,c=(3.34673,2.347893467),e=(1.0345684,1.0012466778):
; A amours de sois
if (whitesq)
z = ((z + fn1(z * e))+(z ^ (z / c)))/((z + (z - e))+(z + (z * e)))
else
z = ((z + (z - e))+(z ^ (z + e)))/((z + (z * e))+(z + fn2(z * c)))
end if

|z| <= 4
}
Carl104 {
z = Pixel,c=(3.34673,2.347893467),e=(1.0345684,1.0012466778):
; A amours de sois
if (whitesq)
z = ((z + fn1(z * e))+(z ^ (z + c)))/((z + (z - e))+(z + (z * e)))
else
z = ((z + (z - e))+(z ^ (z + e)))/((z + (z * e))+(z + fn2(z * c)))
end if

|z| <= 4
}
Carl105 {
z = Pixel,c=(1.34673,0.347893467),e=(1.3345684,1.1012466778):

z = fn2((z + fn1(z * e))^(z - (z * e)))



|z| <= 4
}
Carl106 {
z = Pixel,c=(1.34673,0.347893467),e=(0.03345684,1.1012466778):
if(z < c)
z = fn2((z + fn1(z * e))^(z - (z * e - 1)))
else
z = fn2((z + fn1(z * e))^(z - (z * e + 1)))

end if


|z| <= 4
}
Carl107 {
z = Pixel,c=(1.0034673,0.11147893467),e=(0.16345684,0.1012466778):
if(z < c)
z = fn2((z + fn1(z - e))^(z - (z * e - c)))
else
z = fn2((z * fn1(z - e))^(z - (z * e + c)))

end if

|z| <= 8

}
Carl108 {
z = Pixel,c=(1.2034673,3.11147893467),e=(0.46345684,0.1012466778):
if(z < sqrt(c))
z = fn2((z + fn1(z - e))^(z - (z * e - c)))+1
else
z = fn2((z * fn1(z - e))^(z - (z * e + c)))-1

end if

|z| <= 8

}
Carl109 {
z = Pixel,c=(0.2034673,3.11147893467),e=(0.46345684,0.1012466778):
if(z < sqrt(c)-1)
z = fn2((z * fn1(z - e)))
else
z = fn3((z * fn1(z - e)))

end if

|z| <= 8

}
Carl110 {
z = Pixel,c=(0.2865,0.37754),e=(1.29675546,0.8346):
if(z < sqrt(c)-1)
z = fn2((z * fn1(z - e)))^(.5)
else
z = fn2((z * fn1(z + e)))^(.65)

end if

|z| <= 4

}
Carl111 {
z = Pixel,c=(0.1865,0.47754),e=(1.59675546,0.2346):
z = (fn1(fn2(fn3(z)*z)/z) + fn1(fn2(fn3(z)*z)*z)+1)/(fn1(fn2(fn3(z)*z)/z) + fn1(fn2(fn3(z)*z)*z)-1)

|z| <= 4

}
Carl112 {
z = Pixel,c=(0.001865,0.047754),e=(0.015774,0.02346):
z = (fn1(fn2(fn3(z)*z)/(z+.0001)) + fn1(fn2(fn3(z)*z)*z)+1)/(fn1(fn2(fn3(z)*z)/(z+.001)) + fn1(fn2(fn3(z)*z)*z+.0001)-1)

|z| <= 4

}

Carl113 {
z = Pixel,c=(0.2501865,0.347754):
z = (z * z + c)/(z ^ z - c)



}
Carl114 {
z = Pixel,c=(0.2501865,0.347754),c2=(0.1501865,0.547754):
z = (z * z + c)/(z ^ z - c2)



}
Carl115 {
z = Pixel,c=(0.72531865,0.366654),c2=(1.1501865,1.547754):
z = (z * z + c)/(z ^ z - c2)
z = (z * z - c2)/(z ^ z + c +0.0000001)



}
Carl116 {
z = Pixel,c=(0.22531865,0.0000366654),c2=(0.000000000501865,0.2547754):
z = (2 * z + c + 0.00001)
x = (z + c2)
y = ((z * c1)- (z / (c2 + 1)))
x = tan(y - x)
y = (x - y*y)
z = (z - (x/(y-c))/2)
|z| <= 512

}
Carl117 {
z = Pixel,c=(0.3786865,0.4006654),c2=(0.8400000000501865,0.1547754),scale=(2,1.5):
epi = (2.718281828459045235360287471352,3.141592653589793238462643383279)/scale
pie =  (3.141592653589793238462643383279,2.718281828459045235360287471352)/scale
z = (2 * z + c )*epi / 3.141592653589793238462643383279
x = (z - c2)
y = 1/((z * c1)- (z / (c2 + 1)))
x = asin(y - x) 
y = (x / y*y*y)
z = (z - (x/(y-c))/pie)
|z| <= 512
}
Carl118 {
z = Pixel,c=(0.5786865,0.4006654),c2=(0.8400000000501865,0.1547754),scale=(1,1):
epi = (2.718281828459045235360287471352,3.141592653589793238462643383279)/scale
pie =  (3.141592653589793238462643383279,2.718281828459045235360287471352)/scale
z = (((z * (epi/pie))+(z / (epi/pie + 1))-c)*((z * (epi/pie))+(z / (epi/pie + 1))+c2))/(((z * (pie/epi))+(z / (pie/epi + 1))+c)/((z * (pie/epi))+(z / (pie/epi + 1))-c2))
|z| <= 512
}
Carl119p1 {
z = Pixel:
z = z+ z*z +z
z = z*(z+z)*z
z = z*(z+z)*z
z = z+ z*z +z
;|z| <= 512
}
Carl119p2 {
z = Pixel:
z = z*z 
z = z^z
z = z^z
z = z*z
;|z| <= 512
}
Carl119p3 {
z = Pixel:
z = z*fn1(z+z)*z 
z = fn1(z+z)+fn1(z+z)
z = fn1(z+z)+fn1(z+z)
z = z*fn1(z+z)*z
;|z| <= 512
}
Carl119p4 {
z = Pixel:
z =      z + z*z + z
z =      z *fn1(z+z)* z
z =  z+(z)+z+fn1(z*z)+z+(z)+z
z = fn2(fn1(z)+z+fn1(z))*(fn1(z)+z+fn1(z))
z = fn2(fn1(z)+z+fn1(z))*(fn1(z)+z+fn1(z))
z =  z+fn1(z)+z+fn1(z*z)+z+fn1(z)+z
z =      z *fn1(z+z)* z
z =      z + z*z + z
;|z| <= 512
}
Carl119p4distonie {
z = Pixel,c=(1.5644,1.523567):
z =      z + z*z + z                    /       c
z =      z *fn1(z+z)* z                 /   z+fn1(z)+z
z =  z+fn1(z)+z+fn1(z*z)+z+fn1(z)+z     / fn1(z)*z*fn1(z) 
z = (fn1(z)+z+fn2(z))*(fn1(z)+z+fn1(z)) /  z+fn1(z)+z
z = (fn1(z)+z+fn1(z))*(fn2(z)+z+fn1(z)) / fn1(z)*z*fn1(z) 
z =  z+fn1(z)+z+fn1(z*z)+z+fn1(z)+z     /  z+fn1(z)+z
z =      z *fn1(z+z)* z                 / fn1(z)*z*fn1(z) 
z =      z + z*z + z                    *       c
;|z| <= 512
}
Carl120 {
z = Pixel,c=(0.05644,0.823567):
z = z*fn1(z)*fn2(z)-z*fn3(z) + z + c

;|z| <= 512
}
Carl121 {
z = Pixel,c=(0.45644,0.223567):
z = z*fn1(z)*fn2(z)-z*fn1(z) + z + c
z = (z*fn1(z)*fn2(z)-z*fn1(z)) * (|z|>fn3(z))*(z - c)
;|z| <= 512
}

Carl122 {
z = Pixel,c=(0.45644,0.243567):
z = z*fn1(z+ c *(1-z/2 > 0) )*fn2(z)-z*fn1(z-(fn2(z)<.20345)*imag(c)) + z + c 
z = (z*fn1(z)*fn2(z)-z*fn1(z)) * (|z|>fn3(z))*(z - c)
;|z| <= 512
}
Carl123 {
z = Pixel,c=(0.75644,0.643467):
z = fn3((z / (z - c))*(z / (z + c)))
z = fn2(z + (|z|>fn1(z)) * c - (|z|<fn1(z)) * c)
|z| <= 512
}
Carl124 {
z = Pixel,c=(0.75644,0.643467):
z = fn2(z + (|z|>fn1(z)) * c - (|z|<fn1(z)) * c) ^ z 
|z| <= 512
}
Carl125 {
z = Pixel,c=(0.05644,0.8943467):
z = fn2(z + (|z|>fn1(z)) / c - (|z|<fn1(z)) * c)
z = (z + fn1(z))*(z - fn1(z)-c)

|z| <= 512
}
Carl126 {
z = Pixel,c=(0.423911,0.51157889345):
z = fn1((real(z)-(z-1)) * (imag(z) + z)) * fn2(z)
z = z * (z+1) - z * (imag(z)-1)

|z| <= 512
}
Carl127 {
z = Pixel,c=(0.423911,0.51157889345):
z = fn1((z*(z-1)) * (z + z)) * fn2(z)
z = z * (z+1) - z * (z-1)

;|z| <= 512
;|z| <= 1024
}

Carl128 {
z = Pixel,c=(0.423911,0.51157889345):
z = fn1((z*(z+1)) * (z * ((z-1)/z))*((1-z)/z)) * fn2(z)
z = z * (z+1) - z * (z-1)

;|z| <= 512
;|z| <= 1024
}
Carl129 {
z = Pixel,c=(0.123911,0.51157889345):
z = fn1((z*(z+1.1)) * (z * ((z-1.1)/z)))*(((1-z)/z) * fn2(z))
z = z * (z+1) - z * (z-1)

;|z| <= 512
;|z| <= 1024
}
Carl130 {
z = Pixel,c=(0.423911,0.51157889345):
z = fn1((z*(z+1.1)) / (z * ((z-1.1)/z)))/(((1-z)/z) + fn2(z))
z = z * (z+1) + z * (z-1)

;|z| <= 512
;|z| <= 1024
}
Carl131 {
z = Pixel,c=(0.423911,0.51157889345):
z = fn1((z)) / (z * ((z-1.1)/z))*(((1-z)+z) / fn2(z))
z = z / (z+1) * z * (z-1)

;|z| <= 512
;|z| <= 1024
}
Carl132 {
z = Pixel,c=(0.523911,0.31157889345):
z = (sin(z)+z)+c
z = fn1(z * z)
z = fn2(z*(z-1))

;|z| <= 512
;|z| <= 1024
}
Carl133 {
z = Pixel,c=(0.523911,1.31157889345):
z = fn1(z + c)*fn2(z * z)
z = fn3(z * z)

;|z| <= 512
;|z| <= 1024
}


{--- MARK PETERSON -------------------------------------------------------}

  Mandelbrotsimple(XAXIS) {; Mark Peterson
    ; Classical fractal showing LastSqr speedup
    z = Pixel  ; Start with z**2 to initialize LastSqr
     z = z + Pixel

    }
Dragon (ORIGIN) {; Mark Peterson
  z = Pixel:
   z = sqr(z) + (-0.74543, 0.2)
    |z| <= 4
  }

Daisy (ORIGIN) {; Mark Peterson
  z = pixel:
   z = z*z + (0.11031, -0.67037)
    |z| <= 4
  }

InvMandel (XAXIS) {; Mark Peterson
  c = z = 1 / pixel:
   z = sqr(z) + c
    |z| <= 4
  }

DeltaLog(XAXIS) {; Mark Peterson
  z = pixel, c = log(pixel):
   z = sqr(z) + c
    |z| <= 4
  }

Newton4(XYAXIS)[float=y] {; Mark Peterson
  ; Note that floating-point is required to make this compute accurately
  z = pixel, Root = 1:
   z3 = z*z*z
   z4 = z3 * z
   z = (3 * z4 + Root) / (4 * z3)
    .004 <= |z4 - Root|
  }

{--- DON ARCHER ----------------------------------------------------------}

DAFRM01 {;  Don Archer, 1993
  z = pixel :
   z = z ^ (z - 1) * (fn1(z) + pixel)
    |z| <= 4
  }

DAFRM07 {
  z = pixel, c = p1 :
   z = z ^ (z - 1) * fn1(z) + pixel
    |z| <= 4
  }

DAFRM09 {
  z = pixel, c = z + z^ (z - 1):
   tmp = fn1(z)
   real(tmp) = real(tmp) * real(c) - imag(tmp) * imag(c)
   imag(tmp) = real(tmp) * imag(c) - imag(tmp) * real(c)
   z = tmp + pixel + 12
    |z| <= 4
  }

dafrm21 {
  z = pixel:
   x = real(z), y = imag(z)
   x1 = -fn1((x*x*x + y*y*y - 1) - 6*x)*x/(2*x*x*x + y*y*y - 1)
   y1 = -fn2((x*x*x + y*y*y - 1) + 6*x)*y/(2*x*x*x + y*y*y - 1)
   x2 = x1*x1*x1 - y1*y1*y1 + p1 + 5
   y2 = 4*x*y - 18
   z = x2 + flip(y2)
    |z| <= 100
  }

3daMand01 {; Mandelbrot/Zexpe via Lee Skinner
  ; based on 4dFRACT.FRM by Gordon Lamb (CIS: 100272,3541)
  z=real(pixel)+flip(imag(pixel)*p1)
  c=p2+p1*real(pixel)+flip(imag(pixel)):
   z=z^2.71828182845905 + c
    |z|<=100
  }

3daMand02 {; Mandelbrot/Xexpe/Feigenbaum's alpha constant=exponent
  ; based on 4dFRACT.FRM by Gordon Lamb (CIS: 100272,3541)
  z=real(pixel)+flip(imag(pixel)*p1)
  c=p2+p1*real(pixel)+flip(imag(pixel)):
   z=z^2.502907875095 + c
    |z|<=100
  }

{--- RON BARNETT ---------------------------------------------------------}

Julike { ; Ron Barnett, 1993
  ; a Julia function based upon the Ikenaga function
  z = Pixel:
   z = z*z*z + (P1-1)*z - P1
    |z| <= 4
  }

Mask [float=y] { ; Ron Barnett, 1993
  ; try fn1 = log, fn2 = sinh, fn3 = cosh
  ;P1 = (0,1), P2 = (0,1)
  ;Use floating point
  z = fn1(pixel):
   z = P1*fn2(z)^2 + P2*fn3(z)^2 + pixel
    |z| <= 4
  }

JMask {  ; Ron Barnett, 1993
  z = fn1(pixel):
   z = P1*fn2(z)^2 + P2
    |z| <= 4
  }

PseudoZeePi {; Ron Barnett, 1993
  z = pixel:
   x = 1-z^p1;
   z = z*((1-x)/(1+x))^(1/p1) + p2
    |z| <= 4
  }

ZeePi {  ; Ron Barnett, 1993
  ; This Julia function is based upon Ramanujan's iterative
  ; function for calculating pi
  z = pixel:
   x = (1-z^p1)^(1/p1)
   z = z*(1-x)/(1+x) + p2
    |z| <= 4
  }

IkeNewtMand {; Ron Barnett, 1993
  z = c = pixel:
   zf = z*z*z + (c-1)*z - c
   zd = 3*z*z + c-1
   z = z - p1*zf/zd
    0.001 <= |zf|
  }

Frame-RbtM(XAXIS) {; Ron Barnett, 1993
  ; from Mazes for the Mind by Pickover
  z = c = pixel:
   z = z*z*z/5 + z*z + c
    |z| <= 100
  }

FrRbtGenM {; Ron Barnett, 1993
  z = pixel:
   z = p1*z*z*z + z*z + pixel
    |z| <= 100
  }

FlipLambdaJ { ; Ron Barnett, 1993
  z = pixel:
   z = p1*z*(1-flip(z)*flip(z))
    |z| <= 100
  }

REBRefInd2[float=y] {  ; Ron Barnett, 1993
  ; Use floating point
  z = pixel:
   z = (z*z-1)/(z*z+2)*fn1(z)*fn2(z) + p1
    |z| <= 100
  }

GopalsamyFn {
  z = pixel:
   x = real(z), y = imag(z)
   x1 = fn1(x)*fn2(y)
   y1 = fn3(x)*fn4(y)
   x2 = -2*x1*y1 + p1
   y = y1*y1 - x1*x1
   z = x2 + flip(y)
    |z| <= 100
  }

REB004A {; Ron Barnett, 1993
  z = pixel:
   z =p1*fn1(z) + p1*p1*fn2(p2*z) + pixel
    |z| <= 100
  }

REB004K[float=y] {; Ron Barnett, 1993
  ; floating point required
  z = pixel:
   x = flip(pixel + fn1(3/z - z/4))
   z = x*z + p1
    |z| <= 100
  }

REB004L[float=y] {; Ron Barnett, 1993
  ; floating point required
  z = pixel:
   x = flip(pixel + fn1(p1/z - z/(p2+1)))
   z = x*z + pixel
    |z| <= 100
  }

REB004M[float=y] {; Ron Barnett, 1993
  ; floating point required
  z = pixel:
   x = real(z), y = imag(z)
   const = x*x + y*y
   x1 = -fn1(const - 12*x)*x/(4*const)
   y1 = -fn2(const + 12*x)*y/(4*const)
   x2 = x1*x1 - y1*y1 + p1
   y2 = 2*x*y
   z = x2 + flip(y2)
    |z| <= 100
  }

REB005A[float=y] {; Ron Barnett, 1993
  ; floating point required
  z = pixel:
   x = real(z), y = imag(z)
   const = x*x + y*y
   x1 = -fn1(const - 12*x)*x/(4*const)
   y1 = -fn2(const + 12*y)*y/(4*const)
   x2 = x1*x1 - y1*y1 + p1
   y2 = 2*x1*y1
   z = x2 + flip(y2)
    |z| <= 100
  }

REB005E[float=y] {; Ron Barnett, 1993
  ; floating point required
  z = pixel:
   x = real(z), y = imag(z)
   const = x*x + y*y
   x1 = -fn1((const - x)*x/const)
   y1 = -fn2((const + y)*y/const)
   x2 = x1*x1 - y1*y1 + p1
   y2 = 2*x1*y1
   z = x2 + flip(y2)
    |z| <= 100
  }

REB005F[float=y] {; Ron Barnett, 1993
  ; floating point required
  z = pixel:
   x = real(z), y = imag(z)
   const = x*x + y*y
   x1 = -fn1((const - 12*x)*x/(4*const))
   y1 = -fn2((const + 12*y)*y/(4*const))
   x2 = x1*x1 - y1*y1 + p1
   y2 = 2*x1*y1
   z = x2 + flip(y2)
    |z| <= 100
  }

REB005G[float=y] {; Ron Barnett, 1993
  ; floating point required
  z = pixel:
   x = real(z), y = imag(z)
   const = x*x + y*y
   x1 = -fn1(const + p1*x)*y/const
   y1 = -fn2(const + y)*x/const
   x2 = x1*x1 - y1*y1 + p2
   y2 = 2*x1*y1
   z = x2 + flip(y2)
    |z| <= 100
  }


{--- BRADLEY BEACHAM -----------------------------------------------------}

OK-01 { ;TRY P1 REAL = 10000, FN1 = SQR
  z = 0, c = pixel:
   z = (c^z) + c
   z = fn1(z)
    |z| <= (5 + p1)
  }

OK-04 { ;TRY FN2 = SQR, DIFFERENT FUNCTIONS FOR FN1
  z = 0, c = fn1(pixel):
   z = fn2(z) + c
    |z| <= (5 + p1)
  }

OK-08 {
  z = pixel, c = fn1(pixel):
   z = z^z / fn2(z)
   z = c / z
    |z| <= (5 + p1)
  }

OK-21 {
  z = pixel, c = fn1(pixel):
   z = fn2(z) + c
    fn3(z) <= p1
  }

OK-22 {
  z = v = pixel:
   v = fn1(v) * fn2(z)
   z = fn1(z) / fn2(v)
    |z| <= (5 + p1)
  }

OK-32 {
  z = y = x = pixel, k = 1 + p1:
   a = fn1(z)
   b = (a <= y) * ((a * k) + y)
   e = (a > y) * ((a * k) + x)
   x = y
   y = z
   z = b + e
    |z| <= (5 + p2)
  }

OK-34 {
  z = pixel, c = (fn1(pixel) * p1):
   x = abs(real(z))
   y = abs(imag(z))
   a = (x <= y) * (fn2(z) + y + c)
   b = (x > y) * (fn2(z) + x + c)
   z = a + b
    |z| <= (10 + p2)
  }

OK-35 {
  z = pixel, k = 1 + p1:
   v = fn1(z)
   x = (z*v)
   y = (z/v)
   a = (|x| <= |y|) * ((z + y) * k)
   b = (|x| > |y|) * ((z + x) * k)
   z = fn2((a + b) * v) + v
    |z| <= (10 + p2)
  }

OK-36 { ; DISSECTED MANDELBROT
  ; TO GENERATE "STANDARD" MANDELBROT, SET P1 = 0,0 & ALL FN = IDENT
  z = pixel, cx = fn1(real(z)), cy = fn2(imag(z)), k = 2 + p1:
   zx = real(z), zy = imag(z)
   x = fn3(zx*zx - zy*zy) + cx
   y = fn4(k * zx * zy) + cy
   z = x + flip(y)
    |z| <  (10 + p2)
  }

OK-38 { ; DISSECTED CUBIC MANDELBROT
  ; TO GENERATE "STANDARD" CUBIC MANDELBROT, SET P1 = 0,0 & ALL FN = IDENT
  z = pixel,  cx = fn1(real(pixel)), cy = fn2(imag(pixel)), k = 3 + p1:
   zx = real(z), zy = imag(z)
   x = fn3(zx*zx*zx - k*zx*zy*zy) + cx
   y = fn4(k*zx*zx*zy - zy*zy*zy) + cy
   z =  x + flip(y)
    |z| <  (4 + p2)
  }

OK-42 { ; MUTATION OF FN + FN
  z = pixel, p1x = real(p1)+1, p1y = imag(p1)+1
  p2x = real(p2)+1, p2y = imag(p2)+1:
   zx = real(z), zy = imag(z)
   x = fn1(zx*p1x - zy*p1y) + fn2(zx*p2x - zy*p2y)
   y = fn3(zx*p1y + zy*p1x) + fn4(zx*p2y + zy*p2x)
   z = x + flip(y)
    |z| <= 20
  }

OK-43 { ; DISSECTED SPIDER
  ; TO GENERATE "STANDARD" SPIDER, SET P1 = 0,0 & ALL FN = IDENT
  z = c = pixel, k = 2 + p1:
   zx = real(z), zy = imag(z)
   cx = real(c), cy = imag(c)
   x = fn1(zx*zx - zy*zy) + cx
   y = fn2(k*zx*zy) + cy
   z = x + flip(y)
   c = fn3((cx + flip(cy))/k) + z
    |z| <  (10 + p2)
  }

Larry { ; Mutation of 'Michaelbrot' and 'Element'
  ; Original formulas by Michael Theroux [71673,2767]
  ; For 'Michaelbrot', set FN1 & FN2 =IDENT and P1 & P2 = default
  ; For 'Element', set FN1=IDENT & FN2=SQR and P1 & P2 = default
  ; p1 = Parameter (default 0.5,0), real(p2) = Bailout (default 4)
  z = pixel
  ; The next line sets c=default if p1=0, else c=p1
  c = ((0.5,0) * (|p1|<=0) + p1)
  ; The next line sets test=4 if real(p2)<=0, else test=real(p2)
  test = (4 * (real(p2)<=0) + real(p2) * (0<p2)):
   z = fn1(fn2(z*z)) + c
    |z| <= test
  }

Moe { ; Mutation of 'Zexpe'.
  ; Original formula by Lee Skinner [75450,3631]
  ; For 'Zexpe', set FN1 & FN2 =IDENT and P1 = default
  ; real(p1) = Bailout (default 100)
  s = exp(1.,0.), z = pixel, c = fn1(pixel)
  ; The next line sets test=100 if real(p1)<=0, else test=real(p1)
  test = (100 * (real(p1)<=0) + real(p1) * (0<p1)):
   z = fn2(z)^s + c
    |z| <= test
  }

Groucho { ; Mutation of 'Fish2'.
  ; Original formula by Dave Oliver via Tim Wegner
  ; For 'Fish2', set FN1 & FN2 =IDENT and P1 & P2 = default
  ; p1 = Parameter (default 1,0), real(p2) = Bailout (default 4)
  z = c = pixel
  ; The next line sets k=default if p1=0, else k=p1
  k = ((1,0) * (|p1|<=0) + p1)
  ; The next line sets test=4 if real(p2)<=0, else test=real(p2)
  test = (4 * (real(p2)<=0) + real(p2) * (0<p2)):
   z1 = c^(fn1(z)-k)
   z = fn2(((c*z1)-k)*(z1))
    |z| <= test
  }

Zeppo { ; Mutation of 'Liar4'.
  ; Original formula by Chuck Ebbert [76306,1226]
  ; For 'Liar4' set FN1 & FN2 =IDENT and P1 & P2 = default
  ; p1 & p2 = Parameters (default 1,0 and 0,0)
  z = pixel
  ; The next line sets p=default if p1=0, else p=p1
  p = (1 * (|p1|<=0) + p1):
   z =fn1(1-abs(imag(z)*p-real(z)))+flip(fn2(1-abs(1-real(z)-imag(z))))-p2
    |z| <= 1
  }

inandout02 {
  ;p1 = Parameter (default 0), real(p2) = Bailout (default 4)
  ;The next line sets test=4 if real(p2)<=0, else test=real(p2)
  test = (4 * (real(p2)<=0) + real(p2) * (0<p2))
  z = oldz = pixel:
   a = (|z| <= |oldz|) * (fn1(z)) ;IN
   b = (|oldz| < |z|) * (fn2(z))  ;OUT
   oldz = z
   z = a + b + p1
    |z| <= test
  }

inandout03 {
  ;p1 = Parameter (default 0), real(p2) = Bailout (default 4)
  ;The next line sets test=4 if real(p2)<=0, else test=real(p2)
  test = (4 * (real(p2)<=0) + real(p2) * (0<p2))
  z = oldz = c = pixel:
   a = (|z| <= |oldz|) * (c)    ;IN
   b = (|oldz| < |z|)  * (z*p1) ;OUT
   c = fn1(a + b)
   oldz = z
   z = fn2(z*z) + c
    |z| <= test
  }

inandout04 {
  ;p1 = Parameter (default 1), real(p2) = Bailout (default 4)
  ;The next line sets k=default if p1=0, else k=p1
  k = ((1) * (|p1|<=0) + p1)
  ;The next line sets test=4 if real(p2)<=0, else test=real(p2)
  test = (4 * (real(p2)<=0) + real(p2) * (0<p2))
  z = oldz = c = pixel:
   a = (|z| <= |oldz|) * (c)   ;IN
   b = (|oldz| < |z|)  * (c*k) ;OUT
   c = a + b
   oldz = z
   z = fn1(z*z) + c
    |z| <= test
  }


{--- PIETER BRANDERHORST -------------------------------------------------}

{ The following resulted from a FRACTINT bug. Version 13 incorrectly
  calculated Spider (see above). We fixed the bug, and reverse-engineered
  what it was doing to Spider - so here is the old "spider" }

Wineglass(XAXIS) {; Pieter Branderhorst
  c = z = pixel:
   z = z * z + c
   c = (1+flip(imag(c))) * real(c) / 2 + z
    |z| <= 4
  }

{--- JM COLLARD-RICHARD --------------------------------------------------}

{ These are the original "Richard" types sent by Jm Collard-Richard. Their
  generalizations are tacked on to the end of the "Jm" list below, but
  we felt we should keep these around for historical reasons.}

Richard1 (XYAXIS) {; Jm Collard-Richard
  z = pixel:
   sq=z*z, z=(sq*sin(sq)+sq)+pixel
    |z|<=50
  }

Richard2 (XYAXIS) {; Jm Collard-Richard
  z = pixel:
   z=1/(sin(z*z+pixel*pixel))
    |z|<=50
  }

Richard3 (XAXIS) {; Jm Collard-Richard
  z = pixel:
   sh=sinh(z), z=(1/(sh*sh))+pixel
    |z|<=50
  }

Richard4 (XAXIS) {; Jm Collard-Richard
  z = pixel:
   z2=z*z, z=(1/(z2*cos(z2)+z2))+pixel
    |z|<=50
  }

Richard5 (XAXIS) {; Jm Collard-Richard
  z = pixel:
   z=sin(z*sinh(z))+pixel
    |z|<=50
  }

Richard6 (XYAXIS) {; Jm Collard-Richard
  z = pixel:
   z=sin(sinh(z))+pixel
    |z|<=50
  }

Richard7 (XAXIS) {; Jm Collard-Richard
  z=pixel:
   z=log(z)*pixel
    |z|<=50
  }

Richard8 (XYAXIS) {; Jm Collard-Richard
  ; This was used for the "Fractal Creations" cover
  z=pixel,sinp = sin(pixel):
   z=sin(z)+sinp
    |z|<=50
  }

Richard9 (XAXIS) {; Jm Collard-Richard
  z=pixel:
   sqrz=z*z, z=sqrz + 1/sqrz + pixel
    |z|<=4
  }

Richard10(XYAXIS) {; Jm Collard-Richard
  z=pixel:
   z=1/sin(1/(z*z))
    |z|<=50
  }

Richard11(XYAXIS) {; Jm Collard-Richard
  z=pixel:
   z=1/sinh(1/(z*z))
    |z|<=50
  }

{ These types are generalizations of types sent to us by the French
  mathematician Jm Collard-Richard. If we hadn't generalized them
  there would be --ahhh-- quite a few. With 26 possible values for
  each fn variable, Jm_03, for example, has 456,976 variations! }

Jm_01 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=(fn1(fn2(z^pixel)))*pixel
    |z|<=t
  }

Jm_02 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=(z^pixel)*fn1(z^pixel)
    |z|<=t
  }

Jm_03 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1((fn2(z)*pixel)*fn3(fn4(z)*pixel))*pixel
    |z|<=t
  }

Jm_03a {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1((fn2(z)*pixel)*fn3(fn4(z)*pixel))+pixel
    |z|<=t
  }

Jm_04 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1((fn2(z)*pixel)*fn3(fn4(z)*pixel))
    |z|<=t
  }

Jm_05 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(fn2((z^pixel)))
    |z|<=t
  }

Jm_06 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(fn2(fn3((z^z)*pixel)))
    |z|<=t
  }

Jm_07 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(fn2(fn3((z^z)*pixel)))*pixel
    |z|<=t
  }

Jm_08 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(fn2(fn3((z^z)*pixel)))+pixel
    |z|<=t
  }

Jm_09 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(fn2(fn3(fn4(z))))+pixel
    |z|<=t
  }

Jm_10 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(fn2(fn3(fn4(z)*pixel)))
    |z|<=t
  }

Jm_11 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(fn2(fn3(fn4(z)*pixel)))*pixel
    |z|<=t
  }

Jm_11a {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(fn2(fn3(fn4(z)*pixel)))+pixel
    |z|<=t
  }

Jm_12 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(fn2(fn3(z)*pixel))
    |z|<=t
  }

Jm_13 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(fn2(fn3(z)*pixel))*pixel
    |z|<=t
  }

Jm_14 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(fn2(fn3(z)*pixel))+pixel
    |z|<=t
  }

Jm_15 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   f2=fn2(z),z=fn1(f2)*fn3(fn4(f2))*pixel
    |z|<=t
  }

Jm_16 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   f2=fn2(z),z=fn1(f2)*fn3(fn4(f2))+pixel
    |z|<=t
  }

Jm_17 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(z)*pixel*fn2(fn3(z))
    |z|<=t
  }

Jm_18 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(z)*pixel*fn2(fn3(z)*pixel)
    |z|<=t
  }

Jm_19 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(z)*pixel*fn2(fn3(z)+pixel)
    |z|<=t
  }

Jm_20 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(z^pixel)
    |z|<=t
  }

Jm_21 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(z^pixel)*pixel
    |z|<=t
  }

Jm_22 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   sq=fn1(z), z=(sq*fn2(sq)+sq)+pixel
    |z|<=t
  }

Jm_23 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(fn2(fn3(z)+pixel*pixel))
    |z|<=t
  }

Jm_24 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z2=fn1(z), z=(fn2(z2*fn3(z2)+z2))+pixel
    |z|<=t
  }

Jm_25 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(z*fn2(z)) + pixel
    |z|<=t
  }

Jm_26 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   z=fn1(fn2(z)) + pixel
    |z|<=t
  }

Jm_27 {; generalized Jm Collard-Richard type
  z=pixel,t=p1+4:
   sqrz=fn1(z), z=sqrz + 1/sqrz + pixel
    |z|<=t
  }

Jm_ducks(XAXIS) {; Jm Collard-Richard
  ; Not so ugly at first glance and lot of corners to zoom in.
  ; try this: corners=-1.178372/-0.978384/-0.751678/-0.601683
  z=pixel,tst=p1+4,t=1+pixel:
   z=sqr(z)+t
    |z|<=tst
  }

Gamma(XAXIS) { ; first order gamma function from Prof. Jm
  ; "It's pretty long to generate even on a 486-33 comp but there's a lot
  ; of corners to zoom in and zoom and zoom...beautiful pictures :)"
  z=pixel,twopi=6.283185307179586,r=10:
   z=(twopi*z)^(0.5)*(z^z)*exp(-z)+pixel
    |z|<=r
  }

ZZ(XAXIS)[float=y] { ; Prof Jm using Newton-Raphson method
  ; use floating point with this one
  z=pixel,solution=1:
   z1=z^z
   z2=(log(z)+1)*z1
   z=z-(z1-1)/z2
    0.001 <= |solution-z1|
  }

ZZa(XAXIS)[float=y] { ; Prof Jm using Newton-Raphson method
  ; use floating point with this one
  z=pixel,solution=1:
   z1=z^(z-1)
   z2=(((z-1)/z)+log(z))*z1
   z=z-((z1-1)/z2)
    .001 <= |solution-z1|
  }

GenInvMand1_N { ; Jm Collard-Richard
  c=z=1/pixel:
   z=fn1(z)*fn2(z)+fn3(fn4(c))
    |z|<=4
  }


{--- W. LEROY DAVIS ------------------------------------------------------}

{ These are from: "AKA MrWizard W. LeRoy Davis;SM-ALC/HRUC"
      davisl@sm-logdis1-aflc.af.mil
  The first 3 are variations of:
         z
     gamma(z) = (z/e) * sqrt(2*pi*z) * R
}

Sterling(XAXIS) {; davisl
  z = Pixel:
   z = ((z/2.7182818)^z)/sqr(6.2831853*z)
    |z| <= 4
  }

Sterling2(XAXIS) {; davisl
  z = Pixel:
   z = ((z/2.7182818)^z)/sqr(6.2831853*z) + pixel
    |z| <= 4
  }

Sterling3(XAXIS) {; davisl
  z = Pixel:
   z = ((z/2.7182818)^z)/sqr(6.2831853*z) - pixel
    |z| <= 4
  }

PsudoMandel(XAXIS) {; davisl - try center=0,0/magnification=28
  z = Pixel:
   z = ((z/2.7182818)^z)*sqr(6.2831853*z) + pixel
    |z| <= 4
  }

{--- ROB DEN BRAASEM -----------------------------------------------------}

J_TchebychevC3 {
  c = pixel, z = P1:
   z = c*z*(z*z-3)
    |z|<100
  }

J_TchebychevC7 {
  c = pixel, z = P1:
   z = c*z*(z*z*(z*z*(z*z-7)+14)-7)
    |z|<100
  }

J_TchebychevS4 {
  c = pixel, z = P1:
   z = c*(z*z*(z*z-3)+1)
    |z|<100
  }

J_TchebychevS6 {
  c = pixel, z = P1:
   z = c*(z*z*(z*z*(z*z-5)+6)-1)
    |z|<100
  }

J_TchebychevS7 {
  c = pixel, z = P1:
   z = c*z*(z*z*(z*z*(z*z-6)+10)-4)
    |z|<100
  }

J_Laguerre2 {
  c = pixel, z = P1:
   z = (z*(z - 4) +2 ) / 2 + c
    |z| < 100
  }

J_Laguerre3 {
  c = pixel, z = P1:
   z = (z*(z*(-z + 9) -18) + 6 ) / 6 + c
    |z| < 100
  }

J_Lagandre4 {
  c = pixel, z = P1:
   z = (z*z*(35 * z*z - 30) + 3) / 8 + c
    |z| < 100
  }

M_TchebychevT5 {
  c = P1, z = Pixel:
   z = c*(z*(z*z*(16*z*z-20)+5))
    |z|<100
  }

M_TchebychevC5 {
  c = P1, z = Pixel:
   z = c*z*(z*z*(z*z-5)+5)
    |z|<100
  }

M_TchebychevU3 {
  c = P1, z = Pixel:
   z = c*z*(8*z*z-4)
    |z|<100
  }

M_TchebychevS3 {
  c = P1, z = Pixel:
   z = c*z*(z*z-2)
    |z|<100
  }

M_Lagandre2 {
  c = P1, z = Pixel:
   z = (3 * z*z - 1) / 2 + c
    |z| < 100
  }

M_Lagandre6 {
  c = P1, z = Pixel:
   z = (z*z*(z*z*(231 * z*z - 315)  + 105 ) - 5) / 16 + c
    |z| < 100
  }


{--- CHUCK EBBERT & JON HORNER -------------------------------------------}

comment {
  Chaotic Liar formulas for FRACTINT. These formulas reproduce some of the
  pictures in the paper 'Pattern and Chaos: New Images in the Semantics of
  Paradox' by Gary Mar and Patrick Grim of the Department of Philosophy,
  SUNY at Stony Brook. "...what is being graphed within the unit square is
  simply information regarding the semantic behavior for different inputs
  of a pair of English sentences:"
  }

Liar1 { ; by Chuck Ebbert.
  ; X: X is as true as Y
  ; Y: Y is as true as X is false
  ; Calculate new x and y values simultaneously.
  ; y(n+1)=abs((1-x(n) )-y(n) ), x(n+1)=1-abs(y(n)-x(n) )
  z = pixel:
   z = 1 - abs(imag(z)-real(z) ) + flip(1 - abs(1-real(z)-imag(z) ) )
    |z| <= 1
  }

Liar3 { ; by Chuck Ebbert.
  ; X: X is true to P1 times the extent that Y is true
  ; Y: Y is true to the extent that X is false.
  ; Sequential reasoning.  P1 usually 0 to 1.  P1=1 is Liar2 formula.
  ; x(n+1) = 1 - abs(p1*y(n)-x(n) );
  ; y(n+1) = 1 - abs((1-x(n+1) )-y(n) );
  z = pixel:
   x = 1 - abs(imag(z)*real(p1)-real(z) )
   z = flip(1 - abs(1-real(x)-imag(z) ) ) + real(x)
    |z| <= 1
  }

Liar4[float=y] { ; by Chuck Ebbert.
  ; X: X is as true as (p1+1) times Y
  ; Y: Y is as true as X is false
  ; Calculate new x and y values simultaneously.
  ; Real part of p1 changes probability.  Use floating point.
  ; y(n+1)=abs((1-x(n) )-y(n) ), x(n+1)=1-abs(y(n)-x(n) )
  z = pixel, p = p1 + 1:
   z = 1-abs(imag(z)*p-real(z))+flip(1-abs(1-real(z)-imag(z)))
    |z| <= 1
  }

F'Liar1 { ; Generalization by Jon Horner of Chuck Ebbert formula.
  ; X: X is as true as Y
  ; Y: Y is as true as X is false
  ; Calculate new x and y values simultaneously.
  ; y(n+1)=abs((1-x(n) )-y(n) ), x(n+1)=1-abs(y(n)-x(n) )
  z = pixel:
   z = 1 - abs(imag(z)-real(z) ) + flip(1 - abs(1-real(z)-imag(z) ) )
    fn1(abs(z))<p1
  }

M-SetInNewton(XAXIS)[float=y] {; use float=yes
  ; jon horner 100112,1700, 12 feb 93
  z = 0,  c = pixel,  cminusone = c-1:
   oldz = z, nm = 3*c-2*z*cminusone, dn = 3*(3*z*z+cminusone)
   z = nm/dn+2*z/3
    |(z-oldz)|>=|0.01|
  }

F'M-SetInNewtonA(XAXIS)[float=y] {; use float=yes
  ; jon horner 100112,1700, 12 feb 93
  z = 0,  c = fn1(pixel),  cminusone = c-1:
   oldz = z, nm = p1*c-2*z*cminusone, dn = p1*(3*z*z+cminusone)
   z = nm/dn+2*z/p1
    |(z-oldz)|>=|0.01|
  }

F'M-SetInNewtonC(XAXIS)[float=y periodicity=0] { ; same as F'M-SetInNewtonB except for bailout
  ; use float=yes, periodicity=no
  ; (3 <= p1 <= ?) and (1e-30 < p2 < .01)
  z=0, c=fn1(pixel), cm1=c-1, cm1x2=cm1*2, twoop1=2/p1, p1xc=c*real(p1):
   z = (p1xc - z*cm1x2 )/( (sqr(z)*3 + cm1 ) * real(p1) ) + z*real(twoop1)
    abs(|z| - real(lastsqr) ) >= p2
  }


{--- CHRIS GREEN ---------------------------------------------------------}

comment {
  These fractals all use Newton's or Halley's formula for approximation of
  a function.  In all of these fractals, p1 real is the "relaxation
  coefficient". A value of 1 gives the conventional newton or halley
  iteration. Values <1 will generally produce less chaos than values >1.
  1-1.5 is probably a good range to try.  P1 imag is the imaginary
  component of the relaxation coefficient, and should be zero but maybe a
  small non-zero value will produce something interesting.  Who knows?
  For more information on Halley maps, see "Computers, Pattern, Chaos, and
  Beauty" by Pickover.
  }

Halley (XYAXIS) [float=y] {; Chris Green. Halley's formula applied to x^7-x=0.
  ; P1 real usually 1 to 1.5, P1 imag usually zero. Use floating point.
  ; Setting P1 to 1 creates the picture on page 277 of Pickover's book
  z=pixel:
   z5=z*z*z*z*z
   z6=z*z5
   z7=z*z6
   z=z-p1*((z7-z)/ ((7.0*z6-1)-(42.0*z5)*(z7-z)/(14.0*z6-2)))
    0.0001 <= |z7-z|
  }

CGhalley (XYAXIS) [float=y] {; Chris Green -- Halley's formula
  ; P1 real usually 1 to 1.5, P1 imag usually zero. Use floating point.
  z=(1,1):
   z5=z*z*z*z*z
   z6=z*z5
   z7=z*z6
   z=z-p1*((z7-z-pixel)/ ((7.0*z6-1)-(42.0*z5)*(z7-z-pixel)/(14.0*z6-2)))
    0.0001 <= |z7-z-pixel|
  }

halleySin (XYAXIS) [float=y] {; Chris Green. Halley's formula applied to sin(x)=0.
  ; Use floating point.
  ; P1 real = 0.1 will create the picture from page 281 of Pickover's book.
  z=pixel:
   s=sin(z), c=cos(z)
   z=z-p1*(s/(c-(s*s)/(c+c)))
    0.0001 <= |s|
  }

NewtonSinExp (XAXIS) [float=y] {; Chris Green
  ; Newton's formula applied to sin(x)+exp(x)-1=0.
  ; Use floating point.
  z=pixel:
   z1=exp(z)
   z2=sin(z)+z1-1
   z=z-p1*z2/(cos(z)+z1)
    .0001 < |z2|
  }

CGNewtonSinExp (XAXIS) {
  z=pixel:
   z1=exp(z)
   z2=sin(z)+z1-z
   z=z-p1*z2/(cos(z)+z1)
    .0001 < |z2|
  }

CGNewton3 [float=y] {; Chris Green -- A variation on newton iteration.
  ; The initial guess is fixed at (1,1), but the equation solved
  ; is different at each pixel ( x^3-pixel=0 is solved).
  ; Use floating point.
  ; Try P1=1.8.
  z=(1,1):
   z2=z*z
   z3=z*z2
   z=z-p1*(z3-pixel)/(3.0*z2)
    0.0001 < |z3-pixel|
  }

HyperMandel [float=y] {; Chris Green.
  ; A four dimensional version of the mandelbrot set.
  ; Use P1 to select which two-dimensional plane of the
  ; four dimensional set you wish to examine.
  ; Use floating point.
  a=(0,0),b=(0,0):
   z=z+1
   anew=sqr(a)-sqr(b)+pixel
   b=2.0*a*b+p1
   a=anew
    |a|+|b| <= 4
  }

OldHalleySin (XYAXIS) {
  z=pixel:
   s=sin(z)
   c=cosxx(z)
   z=z-p1*(s/(c-(s*s)/(c+c)))
    0.0001 <= |s|
  }


{--- RICHARD HUGHES ------------------------------------------------------}

phoenix_m { ; Mandelbrot style map of the Phoenix curves
  z=x=y=nx=ny=x1=y1=x2=y2=0:
   x2 = sqr(x), y2 = sqr(y)
   x1 = x2 - y2 + real(pixel) + imag(pixel) * nx
   y1 = 2 * x * y + imag(pixel) * ny
   nx=x, ny=y, x=x1, y=y1, z=x + flip(y)
    |z| <= 4
  }


{--- GORDON LAMB ---------------------------------------------------------}

SJMAND01 {;Mandelbrot
  z=real(pixel)+flip(imag(pixel)*p1)
  c=p2+p1*real(pixel)+flip(imag(pixel)):
   z=z*z+c
    |z|<=64
  }

3RDIM01 {;Mandelbrot
  z=p1*real(pixel)+flip(imag(pixel))
  c=p2+real(pixel)+flip(imag(pixel)*p1):
   z=z*z+c
    |z|<=64
  }

SJMAND03 {;Mandelbrot function
  z=real(pixel)+p1*(flip(imag(pixel)))
  c=p2+p1*real(pixel)+flip(imag(pixel)):
   z=fn1(z)+c
    |z|<=64
  }

SJMAND05 {;Mandelbrot lambda function
  z=real(pixel)+flip(imag(pixel)*p1)
  c=p2+p1*real(pixel)+flip(imag(pixel)):
   z=fn1(z)*c
    |z|<=64
  }

3RDIM05 {;Mandelbrot lambda function
  z=p1*real(pixel)+flip(imag(pixel))
  c=p2+real(pixel)+flip(imag(pixel)*p1):
   z=fn1(z)*c
    |z|<=64
  }

SJMAND10 {;Mandelbrot power function
  z=real(pixel),c=p2+flip(imag(pixel)):
   z=(fn1(z)+c)^p1
    |z|<=4
  }

SJMAND11 {;Mandelbrot lambda function - lower bailout
  z=real(pixel)+flip(imag(pixel)*p1)
  c=p2+p1*real(pixel)+flip(imag(pixel)):
   z=fn1(z)*c
    |z|<=4
  }


{--- KEVIN LEE -----------------------------------------------------------}

LeeMandel1(XYAXIS) {; Kevin Lee
  z=Pixel:
;; c=sqr(pixel)/z, c=z+c, z=sqr(z),  this line was an error in v16
   c=sqr(pixel)/z, c=z+c, z=sqr(c)
    |z|<4
  }

LeeMandel2(XYAXIS) {; Kevin Lee
  z=Pixel:
   c=sqr(pixel)/z, c=z+c, z=sqr(c*pixel)
    |z|<4
   }

LeeMandel3(XAXIS) {; Kevin Lee
  z=Pixel, c=Pixel-sqr(z):
   c=Pixel+c/z, z=c-z*pixel
    |z|<4
  }

{--- RON LEWEN -----------------------------------------------------------}

RCL_Cross1 [float=y] { ; Ron Lewen
  ; Try p1=(0,1), fn1=sin and fn2=sqr.  Set corners at
  ; -10/10/-7.5/7.5 to see a cross shape.  The larger
  ; lakes at the center of the cross have good detail
  ; to zoom in on.
  ; Use floating point.
  z=pixel:
   z=p1*fn1(fn2(z+p1))
    |z| <= 4
  }

RCL_Pick13 [float=y] { ; Ron Lewen
  ;  Formula from Frontpiece for Appendix C
  ;  and Credits in Pickover's book.
  ;  Set p1=(3,0) to generate the Frontpiece
  ;  for Appendix C and to (2,0) for Credits
  ;  Use Floating Point
  z=.001:
   z=z^p1+(1/pixel)^p1
    |z| <= 100
  }

RCL_1 (XAXIS) [float=y] { ; Ron Lewen
  ;  An interesting Biomorph inspired by Pickover's
  ;  Computers, Pattern, Choas and Beauty.
  ;  Use Floating Point
  z=pixel:
   z=pixel/z-z^2
    |real(z)| <= 100 || |imag(z)| <= 100
  }

RCL_Cosh (XAXIS) [float=y] { ; Ron Lewen, 76376,2567
  ; Try corners=2.008874/-3.811126/-3.980167/3.779833/
  ; -3.811126/3.779833 to see Figure 9.7 (P. 123) in
  ; Pickover's Computers, Pattern, Chaos and Beauty.
  ; Figures 9.9 - 9.13 can be found by zooming.
  ; Use floating point
  z=0:
   z=cosh(z) + pixel
    abs(z) < 40
  }

Mothra (XAXIS) { ; Ron Lewen, 76376,2567
  ; Remember Mothra, the giant Japanese-eating moth?
  ; Well... here he (she?) is as a fractal!
  z=pixel:
   a=z^5 + z^3 + z + pixel
   b=z^4 + z^2 + pixel
   z=b^2/a,
    |real(z)| <= 100 || |imag(z)| <= 100
  }

RCL_10 { ; Ron Lewen, 76376,2567
  z=pixel:
   z=flip((z^2+pixel)/(pixel^2+z))
    |z| <= 4
  }


{--- JONATHAN OSUCH ------------------------------------------------------}

BirdOfPrey (XAXIS_NOPARM) { ; Optimized by Sylvie Gallet
  z = p1 :
   z = cosxx(sqr(z) + pixel) + pixel
    |z| <= 4
  }

; Original version
; BirdOfPrey(XAXIS_NOPARM) {
;  z=p1, x=1:
;   (x<10)*(z=sqr(z)+pixel)
;   (10<=x)*(z=cosxx(z)+pixel)
;   x=x+1
;    |z|<=4
;  }

FractalFenderCa(XAXIS_NOPARM) {;Spectacular!
  z=p1,x=|z|:
   if (0.9999999999 < x)
      z=cosh(z)+pixel
   endif
   z=sqr(z)+pixel,x=|z|
    x<=4
  }

{--- LEE SKINNER ---------------------------------------------------------}

MTet (XAXIS) {; Mandelbrot form 1 of the Tetration formula --Lee Skinner
  z = pixel:
   z = (pixel ^ z) + pixel
    |z| <= (P1 + 3)
  }

AltMTet(XAXIS) {; Mandelbrot form 2 of the Tetration formula --Lee Skinner
  z = 0:
   z = (pixel ^ z) + pixel
    |z| <= (P1 + 3)
  }

JTet (XAXIS) {; Julia form 1 of the Tetration formula --Lee Skinner
  z = pixel:
   z = (pixel ^ z) + P1
    |z| <= (P2 + 3)
  }

AltJTet (XAXIS) {; Julia form 2 of the Tetration formula --Lee Skinner
  z = P1:
   z = (pixel ^ z) + P1
    |z| <= (P2 + 3)
  }

Cubic (XYAXIS) {; Lee Skinner
  p = pixel, test = p1 + 3
  t3 = 3*p, t2 = p*p
  a = (t2 + 1)/t3, b = 2*a*a*a + (t2 - 2)/t3
  aa3 = a*a*3, z = 0 - a :
   z = z*z*z - aa3*z + b
    |z| < test
 }

Fzppfnre {; Lee Skinner
  z = pixel, f = 1./(pixel):
   z = fn1(z) + f
    |z| <= 50
  }

Fzppfnpo {; Lee Skinner
  z = pixel, f = (pixel)^(pixel):
   z = fn1(z) + f
    |z| <= 50
  }

Fzppfnsr {; Lee Skinner
  z = pixel, f = (pixel)^.5:
   z = fn1(z) + f
    |z| <= 50
  }

Fzppfnta {; Lee Skinner
  z = pixel, f = tan(pixel):
   z = fn1(z) + f
    |z|<= 50
  }

Fzppfnct {; Lee Skinner
  z = pixel, f = cos(pixel)/sin(pixel):
   z = fn1(z) + f
    |z|<= 50
  }

Fzppfnse {; Lee Skinner
  z = pixel, f = 1./sin(pixel):
   z = fn1(z) + f
    |z| <= 50
  }

Fzppfncs {; Lee Skinner
  z = pixel, f = 1./cos(pixel):
   z = fn1(z) + f
    |z| <= 50
  }

Fzppfnth {; Lee Skinner
  z = pixel, f = tanh(pixel):
   z = fn1(z)+f
    |z|<= 50
  }

Fzppfnht {; Lee Skinner
  z = pixel, f = cosh(pixel)/sinh(pixel):
   z = fn1(z)+f
    |z|<= 50
  }

Fzpfnseh {; Lee Skinner
  z = pixel, f = 1./sinh(pixel):
   z = fn1(z) + f
    |z| <= 50
  }

Fzpfncoh {; Lee Skinner
  z = pixel, f = 1./cosh(pixel):
   z = fn1(z) + f
    |z| <= 50
  }

Zexpe (XAXIS) {
  s = exp(1.,0.), z = Pixel:
   z = z ^ s + pixel
    |z| <= 100
  }

comment { s = log(-1.,0.) / (0.,1.)   is   (3.14159265358979, 0.0 }

Exipi (XAXIS) {
  s = log(-1.,0.) / (0.,1.), z = Pixel:
   z = z ^ s + pixel
    |z| <= 100
  }

Fzppchco {
  z = pixel, f = cosxx (pixel):
   z = cosh (z) + f
    |z| <= 50
  }

Fzppcosq {
  z = pixel, f = sqr (pixel):
   z = cosxx (z)  + f
    |z| <= 50
  }

Fzppcosr {
  z = pixel, f = (pixel) ^ 0.5:
   z = cosxx (z)  + f
    |z| <= 50
  }

Leeze (XAXIS) {
  s = exp(1.,0.), z = Pixel, f = Pixel ^ s:
   z = cosxx (z) + f
    |z| <= 50
  }

OldManowar (XAXIS) {
  z0 = 0
  z1 = 0
  test = p1 + 3
  c = pixel :
   z = z1*z1 + z0 + c
   z0 = z1
   z1 = z
    |z| < test
  }

ScSkLMS(XAXIS) {
  z = pixel, TEST = (p1+3):
   z = log(z) - sin(z)
    |z|<TEST
  }

ScSkZCZZ(XYAXIS) {
  z = pixel, TEST = (p1+3):
   z = (z*cosxx(z)) - z
    |z|<TEST
  }

TSinh (XAXIS) {; Tetrated Hyperbolic Sine - Improper Bailout
  z = c = sinh(pixel):
   z = c ^ z
    z <= (p1 + 3)
  }

{--- SCOTT TAYLOR --------------------------------------------------------}

{ The following is from Scott Taylor.
  Scott says they're "Dog" because the first one he looked at reminded him
  of a hot dog. This was originally several fractals, we have generalized it. }

FnDog(XYAXIS) {; Scott Taylor
  z = Pixel, b = p1+2:
   z = fn1( z ) * pixel
    |z| <= b
  }

Ent {; Scott Taylor
  ; Try params=.5/.75 and the first function as exp.
  ; Zoom in on the swirls around the middle.  There's a
  ; symmetrical area surrounded by an asymmetric area.
  z = Pixel, y = fn1(z), base = log(p1):
   z = y * log(z)/base
    |z| <= 4
  }

Ent2 {; Scott Taylor
  ; try params=2/1, functions=cos/cosh, potential=255/355
  z = Pixel, y = fn1(z), base = log(p1):
   z = fn2( y * log(z) / base )
    |z| <= 4
  }

{--- MICHAEL THEROUX & RON BARNETT ---------------------------------------}

test3 {; Michael Theroux [71673,2767]
  ;fix and generalization by Ron Barnett [70153,1233]
  ;=phi
  ;try p1 = 2.236067977 for the golden mean
  z = ((p1 + 1)/2)/pixel:
   z =  z*z + pixel*((p1 + 1)/2)/((p1 - 1)/2)
    |z| <= 4
  }

{--- TIMOTHY WEGNER ------------------------------------------------------}

Newton_poly2 [float=y] { ; Tim Wegner - use float=yes
  ; fractal generated by Newton formula z^3 + (c-1)z - c
  ; p1 is c in above formula
  z = pixel, z2 = z*z, z3 = z*z2:
   z = (2*z3 + p1) / (3*z2 + (p1 - 1))
   z2 = z*z
   z3 = z*z2
   .004 <= |z3 + (p1-1)*z - p1|
  }

Newt_ellipt_oops [float=y periodicity=0] { ; Tim Wegner - use float=yes and periodicity=0
  ; fractal generated by Newton formula  (z^3 + c*z^2 +1)^.5
  ; try p1 = 1 and p2 = .1
  ; if p2 is small (say .001), converges very slowly so need large maxit
  ; another "tim's error" - mistook sqr for sqrt (see next)
  z = pixel, z2 = z*z, z3 = z*z2:
   num = (z3 + p1*z2 + 1)^.5      ; f(z)
   denom = (1.5*z2 + p1*z)/num    ; f'(z)
   z = z - (num/denom)            ; z - f(z)/f'(z)
   z2 = z*z
   z3 = z*z2
    p2 <= |z3 + p1*z2 + 1|  ; no need for sqrt because sqrt(z)==0 iff z==0
  }

Newton_elliptic [float=y periodicity=0] { ; Tim Wegner - use float=yes and periodicity=0
  ; fractal generated by Newton formula f(z) = (z^3 + c*z^2 +1)^2
  ; try p1 = 1 and p2 = .0001
  z = pixel, z2 = z*z, z3 = z*z2:
   z = z - (z3 + p1*z2 + 1)/(6*z2 + 4*p1*z)      ; z - f(z)/f'(z)
   z2 = z*z
   z3 = z*z2
    p2 <= |z3 + p1*z2 + 1|  ; no need for sqr because sqr(z)==0 iff z==0
  }

{--- TIM WEGNER & MARK PETERSON ------------------------------------------}

comment {
  These are a few of the examples from the book, Fractal Creations, by Tim
  Wegner and Mark Peterson.
  }

MyFractal {; Fractal Creations example
  c = z = 1/pixel:
   z = sqr(z) + c
    |z| <= 4
  }

Bogus1 {; Fractal Creations example
  z = 0; z = z + * 2
   |z| <= 4 }

MandelTangent {; Fractal Creations example (revised for v.16)
  z = pixel:
   z = pixel * tan(z)
    |real(z)| < 32
  }

Mandel3 {; Fractal Creations example
  z = pixel, c = sin(z):
   z = (z*z) + c
   z = z * 1/c
    |z| <= 4
  }


{--- AUTHORS UNKNOWN -----------------------------------------------------}

moc {
	z=0, c=pixel:
   z=sqr(z)+c
   c=c+p1/c
    |z| <= 4
	}

Bali {;The difference of two squares
  z=x=1/pixel, c= fn1 (z):
   z = (x+c) * (x-c)
   x=fn2(z)
    |z| <=3
  }

Fatso {;
  z=x=1/pixel, c= fn1 (z):
   z = (x^3)-(c^3)
   x=fn2(z)
    |z| <=3
  }

Bjax {;
  z=c=2/pixel:
   z =(1/((z^(real(p1)))*(c^(real(p2))))*c) + c
}

ULI_4 {
  z = Pixel:
   z = fn1(1/(z+p1))*fn2(z+p1)
    |z| <= p2
  }

ULI_5 {
  z = Pixel, c = fn1(pixel):
   z = fn2(1/(z+c))*fn3(z+c)
    |z| <= p1
  }

ULI_6 {
  z = Pixel:
   z = fn1(p1+z)*fn2(p2-z)
    |z| <= p2+16
  }
