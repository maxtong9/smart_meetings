from nltk.tokenize import word_tokenize #Tokenizer
from nltk.probability import FreqDist
'''
    Demo Stuff revolving around nltk
'''
stringExample = "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)."

# Tokenizing Strings
tokenized = word_tokenize(stringExample)
print('Tokenized: \n')
print(tokenized)
# Frequency distribution of tokenized words
freq_dist = FreqDist(tokenized)
print("Frequency Distribution: \n")
print(freq_dist)

print(freq_dist.most_common(5)) # Displays 'n' most common tokens with frequency






print('Hello, World! ')
