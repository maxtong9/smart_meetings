nums = {
    "first": 1, "one": 1,
    "second": 2, "two": 2,
    "third": 3, "three": 3,
    "fourth": 4, "four": 4,
    "fifth": 5, "five": 5,
    "sixth": 6, "six": 6,
    "seventh": 7, "seven": 7,
    "eighth": 8, "eight": 8,
    "ninenth": 9, "nine": 9,
    "tenth": 10, "ten": 10,
    "eleventh": 11, "eleven": 11,
    "twelfth": 12, "twelve": 12,
    "thirteenth": 13, "thirteen": 13,
    "fourteenth": 14, "fourteen": 14,
    "fifteenth": 15, "fifteen": 15,
    "sixteenth": 16, "sixteen": 16,
    "seventeenth": 17, "seventeen": 17,
    "eighteenth": 18, "eighteen": 18,
    "nineteenth": 19, "nineteen": 19,
    "twentieth": 20, "twenty": 20,
    "thirtieth": 30, "thirty": 30
}

class WordToNum:
    def convert(self, arr):
        num = 0
        if len(arr) == 1:
            num = nums[arr[0]]
        else:
            num += nums[arr[0]]
            num += nums[arr[1]]
        print(num)
        return str(num)

    def convert_string(self, words_arr):
        print(str(words_arr))
        for i in range(len(words_arr)-1, 0, -1):
            print("attempting to convert \"" + words_arr[i] + "\"")
            if (words_arr[i].isalpha()):
                print("is alpha")
                if words_arr[i] in nums:
                    print("words[i]: " + words_arr[i])
                    if words_arr[i-1] in nums:
                        print("words[i-1]: " + words_arr[i-1])
                        words_arr[i-1] = self.convert([words_arr[i-1], words_arr[i]])
                        del words_arr[i]
                    else:
                        words_arr[i] = self.convert([words_arr[i]])
            else:
                print("not alpha")
        
        print(str(words_arr))
        return words_arr
        