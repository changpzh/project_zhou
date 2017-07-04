wait until keyword succeeds  3x  2s  Test #会执行Test这个keyword3次（如果有一次成功，则停止执行，意思是最多执行3次），每次间隔2s

*** keywords ***
Test
    Sleep  4s
    should be true  1==0

wait until keyword succeeds  30  2s  Test #会执行Test这个keyword最多30s，执行完一次，间隔2s执行下一次，最多30s

*** keywords ***
Test
    Sleep  4s
    should be true  1==0