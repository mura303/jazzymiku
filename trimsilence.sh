sox $1 tmp1.wav silence 1 0.1 0.1%
sox tmp1.wav tmp2.wav reverse
sox tmp2.wav tmp3.wav silence 1 0.1 0.1%
sox tmp3.wav $2 reverse
rm tmp1.wav tmp2.wav tmp3.wav
