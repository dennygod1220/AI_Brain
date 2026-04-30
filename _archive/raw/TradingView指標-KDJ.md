```
study("KDJ", shorttitle="KDJ")
ilong = input(9, title="period")
isig = input(3, title="signal")

bcwsma(s,l,m) => 
    _s = s
    _l = l
    _m = m
    _bcwsma = (_m*_s+(_l-_m)*nz(_bcwsma[1]))/_l
    _bcwsma
    
c = close
h = highest(high, ilong)
l = lowest(low,ilong)
RSV = 100*((c-l)/(h-l))
pK = bcwsma(RSV, isig, 1)
pD = bcwsma(pK, isig, 1)
pJ = 3 * pK-2 * pD

plot(pK, color= #1E88E5,transp=0)
plot(pD, color=#FF6F00,transp=0)
plot(pJ, color=black,transp=0)
bgcolor(pJ>pD? green : red, transp=75)
h0 = hline(80)
h1 = hline(20)
```