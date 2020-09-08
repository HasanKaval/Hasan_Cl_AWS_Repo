def int_to_roman(input):

    if type(input) != type(1):
        raise TypeError("expected integer, got" % type(input))
    if not 0 < input < 4000:
        raise ValueError("Argument must be between 1 and 3999")
    ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
    nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL', 'X','IX','V','IV','I')
    result = ""
    for i in range(len(ints)):
        count = int(input / ints[i])
        result += nums[i] * count

        input -= ints[i] * count
    print(result)


number = int(input("Please enter a number between 1 and 3999 : "))
int_to_roman(number)


#i=0
#1200
#1200/1000 = 1
#result = "" + (M * 1) --> M
#input = 1200 - (1000*1) --> 200

#i=1
#200
#200/900 = 0
#result = M + (CM * 0) --> M
#input = 200 - (900 * 0) -> 200

### i=2 ve i=3 icin de sonuclar 0 oldugu icin input hala 200, result ise hala M (string) degerine sahip 

#i = 4
#200
#200/100 = 2
#result = result + (C * 2) -> M + CC -> MCC
#input = 200 - (100 * 2) -> 200 -200 = 0

