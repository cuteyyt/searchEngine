def vb_encoding(ori):
    ori = bin(ori)[2:]
    target = (7 - len(ori) % 7) * '0' + ori
    tem = list(target)
    count = 0
    for i in range(len(target) // 7):
        if i == len(target) // 7 - 1:
            tem.insert(7 * i + count, '1')
        else:
            tem.insert(7 * i + count, '0')
            count += 1
    encoded = ''.join(tem)
    # print(encoded)
    return encoded


def vb_decoding(encoded):
    # encoded is supposed to be a string
    tem_list = list()
    for i in range(len(encoded) // 8):
        tem_list.append(encoded[i * 8:(i + 1) * 8][1:])

    for k in range(len(tem_list[0])):
        if tem_list[0][k] != '0':
            tem_list[0] = tem_list[0][k:]
            break
    tem = ''.join(tem_list)
    decoded = int(tem, 2)
    # print(decoded)
    return decoded


def gamma_encoding(ori):
    offset = bin(ori)[3:]
    length = ''.join(['1' for _ in range(len(offset))]) + '0'
    print(length + offset)


def gamma_decoding(encoded):
    pos = encoded.find('0')
    decoded = int('1' + encoded[pos + 1:], 2)
    # print(decoded)
    return decoded


if __name__ == '__main__':
    # vb_decoding('10000101')
    # vb_decoding('000011010000110010110001')
    gamma_decoding('1110101')
    # gamma_decoding()
