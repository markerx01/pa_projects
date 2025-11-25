number = int(input("Enter a number: "))
binary = format(number, '08b')
print(binary)

def to_minus_binary(binary):
    binary = list(str(binary))
    for i in range(len(binary)):
        if binary[i] == '0':
            binary[i] = '1'
        elif binary[i] == '1':
            binary[i] = '0'

    inverted = ''.join(binary)

    result = format(int(inverted, 2) + 1, '08b')
    print(result)


to_minus_binary(binary)