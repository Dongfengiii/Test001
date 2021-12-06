def encode(posting_list):
    def number_byte(num):
        '''
        convert decimal into byte list
        '''
        lst = []
        while num > 0:
            digit = num % 256
            lst = [digit] + lst
            num = num // 256
        if lst == []:
            lst = [0]
        return lst
            
    def code_group(lst4):
        '''
        encode a group of 4 number
        '''
        bytes0 = number_byte(lst4[0])
        bytes1 = number_byte(lst4[1])
        bytes2 = number_byte(lst4[2])
        bytes3 = number_byte(lst4[3])
        prefix = ((len(bytes0) - 1) << 6) + ((len(bytes1) - 1) << 4) + ((len(bytes2) - 1) << 2) + ((len(bytes3) - 1) << 0)
        return [prefix] + bytes0[::-1] + bytes1[::-1] + bytes2[::-1] + bytes3[::-1]

    # calculate the differ between 2 value
    diff_lst = []
    for i in range(len(posting_list)):
        diff = posting_list[i]
        if i % 4 != 0:
            diff = posting_list[i] - posting_list[i - 1]
        diff_lst.append(diff)

    # fix posting_list, so that its length can be divide by 4
    while len(diff_lst) % 4 != 0:
        diff_lst.append(0)

    # encode each group
    lst = []
    for i in range(0, len(diff_lst), 4):
        lst4 = diff_lst[i : i + 4] 
        lst += code_group(lst4)
    return bytearray(lst)
    


def decode(encoded_list):

    def byte_num(bytes_lst):
        '''
        convert bytes into decimal number
        '''
        num = 0
        for b in bytes_lst:
            num = num * 256 + b
        return num
    
    def split_prefix(value):
        '''
        prefix -> length list
        '''
        length0 = ((value >> 6) & 3) + 1
        length1 = ((value >> 4) & 3) + 1
        length2 = ((value >> 2) & 3) + 1
        length3 = ((value >> 0) & 3) + 1
        return length0, length1, length2, length3

    diff_lst = []
    i = 0
    while i < len(encoded_list):

        # process prefix
        length0, length1, length2, length3 = split_prefix(encoded_list[i])
        i = i + 1

        # process byte 0
        bytes0 = encoded_list[i : i + length0]
        i = i + length0

        # process byte 1
        bytes1 = encoded_list[i : i + length1]
        i = i + length1

        # process byte 2
        bytes2 = encoded_list[i : i + length2]
        i = i + length2

        # process byte 3
        bytes3 = encoded_list[i : i + length3]
        i = i + length3

        diff_lst += [byte_num(bytes0[::-1]), byte_num(bytes1[::-1]), byte_num(bytes2[::-1]), byte_num(bytes3[::-1])]

    # convert diff into original list
    lst = []
    for i in range(len(diff_lst)):
        value = diff_lst[i]
        if i % 4 != 0:
            value = diff_lst[i] + lst[-1]
        lst.append(value)

    return lst

def evaluation(rel_list, total_rel_doc):

    tp = sum(rel_list)
    fp = len(rel_list) - tp

    f1 = tp / fp

    map = 0
    for i in range(len(rel_list)):
        if rel_list[i] == 1:
            sub = rel_list[: i + 1]
            ap = sum(sub) / len(sub)
            map += ap
    map /= total_rel_doc

    return round(f1, 2), map







    