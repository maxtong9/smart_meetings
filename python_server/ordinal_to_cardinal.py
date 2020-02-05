ordinals = {
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninenth": 9,
    "tenth": 10,
    "eleventh": 11,
    "twelfth": 12,
    "thirteenth": 13,
    "fourteenth": 14,
    "fifteenth": 15,
    "sixteenth": 16,
    "seventeenth": 17,
    "eighteenth": 18,
    "nineteenth": 19,
    "twentieth": 20,
    "thirtieth": 30
}

cardinals = {
    "twenty": 20,
    "thirty": 30
}

class OrdinalToCardinal:
    def convert(self, arr):
        num = 0
        if len(arr) == 1:
            num = ordinals[arr[0]]
        else:
            num += cardinals[arr[0]]
            num += ordinals[arr[1]]
        return str(num)

    def convert_string(self, words_arr):
        print(str(words_arr))
        for i in range(len(words_arr)-1, 1, -1):
            print(words_arr[i])
            if (words_arr[i].isalpha()):
                if words_arr[i] in ordinals:
                    print("ordinal: " + words_arr[i])
                    if words_arr[i-1] in cardinals:
                        print("cardinal: " + words_arr[i-1])
                        words_arr[i-1] = self.convert([words_arr[i-1], words_arr[i]])
                        del words_arr[i]
                    else:
                        words_arr[i] = self.convert([words_arr[i]])
        print(str(words_arr))
        return ' '.join(words_arr)
        