import json, os, nltk, gensim, string, nltk, datetime
from num2words import num2words
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from gensim import corpora, models
from gensim.utils import tokenize, simple_preprocess
from gensim.similarities import Similarity
nltk.download('stopwords')
stop_words = stopwords.words('english')
stemmer = PorterStemmer()
punc = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~Æôö\n\r'
punc_remover = str.maketrans(punc, ' ' * len(punc))

def to_json_lines(paperID, title, abstract, keywords, fos):
    string = '{"paperID": ' + str(paperID) + ', '
    string += '"title": "' + title + '", '
    string += '"abstract": "' + abstract + '", '
    string += '"keywords": "' + keywords + '", '
    string += '"fosNames": "' + fos + '"}'
    return string


def string_to_list(string):
    string = string.lower()
    li = list(string.split(' '))
    return li


def remove_stopwords(string_list):
    newString_list = []
    for word in string_list:
        if word not in stop_words:
            newString_list.append(word)

    return newString_list


def remove_punctuation(string_list):
    newString_list = []
    for word in string_list:
        newString_list.append(word.translate(punc_remover))

    return newString_list


def remove_single_characters(string_list):
    newString_list = []
    for word in string_list:
        if len(word) > 1:
            newString_list.append(word)

    return newString_list


def lemmatize_string(string_list):
    newString_list = []
    for word in string_list:
        stemmedWord = stemmer.stem(word)
        newString_list.append(stemmedWord)

    return newString_list


def convert_numbers(string_list):
    for x, word in enumerate(string_list):
        try:
            wordAsInt = int(word)
            numtoString = num2words(wordAsInt)
            string_list[x] = numtoString
        except ValueError:
            pass

    return string_list


def list_to_string(string_list):
    newString = ''
    for word in string_list:
        newString += word + ' '

    return newString


def clean_string(string):
    string_list = string_to_list(string)
    string_list = remove_stopwords(string_list)
    string_list = remove_punctuation(string_list)
    string_list = remove_single_characters(string_list)
    string_list = lemmatize_string(string_list)
    string = list_to_string(string_list)
    string_list = string_to_list(string)
    string_list = convert_numbers(string_list)
    string_list = remove_stopwords(string_list)
    string_list = remove_punctuation(string_list)
    string_list = remove_single_characters(string_list)
    string_list = lemmatize_string(string_list)
    cleanedString = list_to_string(string_list)
    return cleanedString


def text_preprocessing(inputDir, outputDir, splits):
    """
    Preprocess the textual dataset for use in the recommender system.
    Takes in multiple files and outputs two: a list of the IDs and the text content
    
    inputDir (string): Location of the split textual content dataset
    outputDir (string): Location for the cleaned file
    splits (integer): Number of times the original DBLP dataset was split
    """
    first = True
    fileNo = 1
    inputPrefix = inputDir + 'Split_DBLP_Text_'
    inputSuffix = '.json'
    idFile = outputDir + 'AbsID.csv'
    textFile = outputDir + 'Text.csv'
    
    print(str(datetime.datetime.now()) + ": Text preprocessing initiated.")
    
    for x in range(splits):
        inputFile = inputPrefix + str(fileNo) + inputSuffix
        with open(inputFile, encoding='utf-8') as (iFile):
            for line in iFile:
                jsonLine = json.loads(line)
                paperID = str(jsonLine['paperID'])
                title = clean_string(jsonLine['title'])
                fosNames = ''
                try:
                    fosNames = clean_string(jsonLine['fosNames'])
                except KeyError:
                    pass

                abstract = ''
                try:
                    abstract = clean_string(jsonLine['abstract'])
                except KeyError:
                    pass

                textContent = title + ' ' + fosNames + ' ' + abstract
                if first:
                    with open(textFile, 'w', encoding='utf-8') as (oFile):
                        oFile.write(textContent)
                        oFile.write('\n')
                    with open(idFile, 'w', encoding='utf-8') as (oFile):
                        oFile.write(paperID)
                        oFile.write('\n')
                    first = False
                else:
                    with open(textFile, 'a', encoding='utf-8') as (oFile):
                        oFile.write(textContent)
                        oFile.write('\n')
                    with open(idFile, 'a', encoding='utf-8') as (oFile):
                        oFile.write(paperID)
                        oFile.write('\n')

        print(str(datetime.datetime.now()) + ": File " + str(x + 1) + " cleaned.")
        
    print(str(datetime.datetime.now()) + ": Text preprocessing completed.")


def create_dictionary(textFile, outputDir):
    """"
    Creates a Gensim dictionary object from a specified text file and saves it
    
    textFile (string): Location of the specified text file used in dictionary generation
    outputDir (string): Location to save the dictionary
    """
    outputFile = outputDir + 'DBLP_Dictionary.dict'
    dictionary = corpora.Dictionary((tokenize(line) for line in open(textFile, encoding='utf-8')))
    dictionary.save(outputFile)
    print('Dictionary created and stored at: ' + outputFile)
    return dictionary


def create_bow_corpus(textFile, dictionary, outputDir):
    """"
    Creates a Gensim bag-of-words corpus from a Gensim dictionary and saves it
    
    textFile (string): Location of the specified text file used in dictionary generation
    dictionary (Gensim dictionary object): Dictionary object used in corpus generation
    outputDir (string): Location to save the corpus
    """
    outputFile = outputDir + 'DBLP_Corpus.mm'
    with open(textFile, encoding='utf-8') as (iFile):
        corpus = [dictionary.doc2bow((tokenize(line)), allow_update=True) for line in iFile]
    corpora.MmCorpus.serialize(outputFile, corpus)
    print('Corpus created and stored at: ' + outputFile)
    return corpus


def create_tfidf_model(corpus, outputDir, weighting):
    """"
    Creates a Gensim TF-IDF model and saves it
    
    corpus (Gensim corpus object): Corpus used for TF-IDF generation
    outputDir (string): Location to save the model
    """
    outputFile = outputDir + 'TF-IDF'
    tfidf = models.TfidfModel(corpus, smartirs=weighting)
    tfidf.save(outputFile)
    print('TF-IDF model created and stored at: ' + outputFile)
    return tfidf


def create_sim_matrix(tfidf, corpus, dictionary, outputDir):
    """"
    Creates a Gensim simiariry matrix for document similarity comparison and saves it
    
    tfidf (Gensim tfidf model): Gensim tfidf model
    corpus (Gensim corpus object): Gensim corpus
    dictionary (Gensim dictionary object): Gensim dictionary
    outputDir (string): Location to save matrix
    """
    indicesFile = outputDir + 'indices'
    simFile = outputDir + 'Index'
    sims = Similarity(indicesFile, tfidf[corpus], num_features=(len(dictionary)))
    sims.close_shard()
    sims.save(simFile)
    print('Similarity matrix created and stored at: ' + simFile)


def generate_recommender(textFile, outputDir, weighting="ntc", dictExists=False, corpusExists=False, tfidfExists=False, createSimMatrix=True):
    """
    Generates all the essential parts of the recommender system
    Uses default parameter (ntc) for SMART-IRS TF-IDF weighting:
        Term frequency weighting: raw
        Document frequency weighting: idf
        Document normailizatio: cosine
    
    textFile (string): Location of the specified text file used in dictionary generation
    outputDir (string): Location to save recommender parts
    weighting (string): SMART-IRS TF-IDF weighting, default is ntc
    dictExists (boolean): Whether the Gensim dictionary exists already, default is False
    corpusExists (boolean): Whether the Gensim corpus exists already, default is False
    tfidfExists (boolean): Whether the Gensim TF-IDF model exists already, default is False
    createSimMatrix (boolean): Whether to create a disk based version of the similarity matrix, default is true
    """
    
    print(str(datetime.datetime.now()) + ": Recommender generation initiated.")
    
    if dictExists:
        dictionary = corpora.Dictionary.load(outputDir + "DBLP_Dictionary.dict")
        print(str(datetime.datetime.now()) + ": Dictionary retrieved.")
    else:
        dictionary = create_dictionary(textFile, outputDir)
        print(str(datetime.datetime.now()) + ": Dictionary generated.")
    
    if corpusExists:
        corpus = corpora.MmCorpus(outputDir + "DBLP_Corpus.mm")
        print(str(datetime.datetime.now()) + ": Corpus retrieved.")
    else:
        corpus = create_bow_corpus(textFile, dictionary, outputDir)
        print(str(datetime.datetime.now()) + ": Corpus generated.")
        
    if tfidfExists:
        tfidf = models.TfidfModel().load(outputDir + "TF-IDF")
        print(str(datetime.datetime.now()) + ": TF-IDF model retrieved.")
    else:
        tfidf = create_tfidf_model(corpus, outputDir, weighting)
        print(str(datetime.datetime.now()) + ": TF-IDF model generated.")
        
    if createSimMatrix:
        create_sim_matrix(tfidf, corpus, dictionary, outputDir)
        print(str(datetime.datetime.now()) + ": Simialrity matrix generated.")
    
    print(str(datetime.datetime.now()) + ": Recommender generation completed.")