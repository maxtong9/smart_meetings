import ssl
import nltk

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context



#nltk.download('all')

# For the tokenizers
nltk.download('punkt')
nltk.download('stopwords')
# Missing Probability but couldn't find a package, I believe it comes with nltk

nltk.download('averaged_perceptron_tagger')
