__author__ = 'changpzh'
import math

def number2timestr(number):
    '''
    #convert number to time string
    #number: int
    '''

    h = int(number/3600)
    m = int(number%3600/60)
    s = int(number%3600%60/1)

    h=str(h)
    if m<10:
        m='0'+str(m)
    else:
        m=str(m)
    if s<10:
        s='0'+str(s)
    else:
        s=str(s)
    timestr = h+':'+m+':'+s
    if timestr == '0:00:00':
        timestr = '-'
    return timestr

def main():
    my_number = int(input("Please input the second to change time string:"))
    print("my input number is:%s and timestr is:%s" % (my_number, number2timestr(my_number)))

if __name__ == '__main__':
    main()
