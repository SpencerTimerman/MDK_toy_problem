

#Imported libraries (all standard with python 2.7)

# collections is a built-in library focussing on High-performance
#  container types. We use is for collections.Counter
import collections

# re is Python's built in regular expression library. We use it
#  for re.findall and re.match
import re

# unittest is one of Python's unit testing frameworks, we use it
#  as the basis for the testing included in this code.
import unittest



"""
Overview of the Application:

Candidate
    String getWord() : returns the autocomplete candidate
    Integer getConfidence() : returns the confidence* for the candidate

AutocompleteProvider
    List<Candidate> getWords(String fragment) : returns list of candidates ordered by confidence*
    void train(String passage) : trains the algorithm with the provided passage


Example Data:
Train: "The third thing that I need to tell you is that this thing does not think thoroughly."
Input: "thi" --> "thing" (2), "think" (1), "third" (1), "this" (1)
Input: "nee" --> "need" (1)
Input: "th" --> "that" (2), "thing" (2), "think" (1), "this" (1), "third" (1), "the" (1), "thoroughly" (1)
"""

class Candidate:
    def __init__(self, word, confidence):
        """
        Candidate data object represents a potential autocomplete candidate
        Data members:
          `word`: String representing the autocompleted word
          `confidence`: Integer (greater than 0) that represents the confidence 
                         that `word` is the correct autocomplete.
        Functions:
          String  getWord():     returns Candidate.word
          Integer getConfidence: returns Candidate.confidence
        """
        #Check to ensure that `word` is a string
        if not isinstance(word,str):
            raise TypeError("Candidate.word must be of type `str`!")
        #Check that `confidence` is an integer
        if not isinstance(confidence,int):
            raise TypeError("Candidate.confidence must be of type `int`!")
        #Given how we use confidence, we want to ensure that it is a positive integer
        if confidence <= 0:
            raise ValueError("Candidate.confidence must have a positive value")

        #If we've reached this far, the values are acceptable and we can store them
        self.word       = word
        self.confidence = confidence

    #Simple "getter" functions (Technically in Python we do no need these, but I
    # want to follow the specification.
    def getWord(self):
        """
        Returns the autocomplete candidate string, the literal word.
        """
        return self.word

    def getConfidence(self):
        """
        Returns the confidence for the candidate string, represented as an integer.
        """
        return self.confidence

    #We are overwriting the comparison operator so that we can sort on both the
    # confidence and the word
    def __cmp__(self,other):
        conf_difference = self.confidence - other.getConfidence()
        if conf_difference != 0:
            return conf_difference
        #otherwise they are equal
        # so we compare their words
        return cmp(other.getWord(), self.word)


class TestCandidate(unittest.TestCase):

    def test_creation(self):
        """
        Tests simple creation of Candidate objects as they were meant to be created.
        """
        word_1       = "test"
        confidence_1 = 3
        candidate_1  = Candidate(word = word_1, confidence = confidence_1)
        self.assertEqual(candidate_1.getWord(),word_1)
        self.assertEqual(candidate_1.getConfidence(),confidence_1)
 
        word_2       = "testing"
        confidence_2 = 1
        candidate_2  = Candidate(word = word_2, confidence = confidence_2)
        self.assertEqual(candidate_2.getWord(),word_2)
        self.assertEqual(candidate_2.getConfidence(),confidence_2)

    def test_type_errors(self):
        """
        Tests numerous ways in which the Candidate object could be created with invalid
         data types supplied to them.
        """
        with self.assertRaises(TypeError):
            Candidate(word = 1, confidence = 1)

        with self.assertRaises(TypeError):
            Candidate(word = 1, confidence = "no")

        with self.assertRaises(TypeError):
            Candidate(word = "yes", confidence = "1")

        with self.assertRaises(TypeError):
            Candidate(word = "test", confidence = {})

        with self.assertRaises(TypeError):
            Candidate(word = "fire", confidence = None)

        with self.assertRaises(TypeError):
            Candidate(word = {}, confidence = 1)

        with self.assertRaises(TypeError):
            Candidate(word = None, confidence = 1)


    def test_value_errors(self):
        """
        Tests ways in which the Candidate.confidence could be provided with an invalid 
         value. (It is required to be a positive integer)
        """
        with self.assertRaises(ValueError):
            Candidate(word = "test", confidence = 0)

        with self.assertRaises(ValueError):
            Candidate(word = "test", confidence = -1)

        with self.assertRaises(ValueError):
            Candidate(word = "test", confidence = -100)




class AutocompleteProvider:
    def __init__(self):
        #collections.Counter is built in class to support convenient and rapid
        # tallies. This seems the most effective way to store the data, especially
        # if it is going to be run on a large dataset (such as the first time it is
        # installed on a phone and would need to ingest their entire SMS history)
        self.model = collections.Counter()

    def getWords(self, fragment):
        #Force the fragment to be lowercase, because the model and requirements
        # list this application as being case insensitive.
        fragment = fragment.lower()

        #First find which words we have start with the same letters as the fragment
        # List comprehensions are very fast within python, and re.match tries to 
        # match the regular expression from the start of the word, so we won't need 
        # a leading "^" in the regex.
        candidate_words = [ word for word in self.model if re.match(fragment,word) ]

        #Now we construct Candidate objects to return to the user
        candidates = [ Candidate(word, self.model[word]) for word in candidate_words ]

        #The candidate list must be sorted by confidence, (and then alphabetically by 
        # the word?) we will use the python built-in function to sort, and use the 
        # Candidate class's overwitten comparator function to ensure the Candidated are
        # sorted primarily by confidence and secondarily alphabetically. We need to 
        # reverse it, as `sorted` naturally sorts low to high.
        sorted_candidates = sorted(candidates,reverse=True)

        return sorted_candidates

    def train(self, passage):
        #This uses a regular expression to extract all sequential sections of
        # alphanumeric characters (usually equivalent to "[^a-zA-Z0-9_]")
        # The `.lower()` call will lowercase all the characters before the 
        # regular expression runs on the passage.
        words = re.findall(r'\w+', passage.lower())
        self.model.update(words)


class TestAutocompleteProvider(unittest.TestCase):
    """
    Example Data:
    Train: "The third thing that I need to tell you is that this thing does not think thoroughly."
    Input: "thi" --> "thing" (2), "think" (1), "third" (1), "this" (1)
    Input: "nee" --> "need" (1)
    Input: "th" --> "that" (2), "thing" (2), "think" (1), "this" (1), "third" (1), "the" (1), "thoroughly" (1)
    """
    def test_on_example_data(self):
        autocomplete_provider = AutocompleteProvider()
        training_data = "The third thing that I need to tell you is that this thing does not think thoroughly."
        autocomplete_provider.train(training_data)

        #Input: "thi" --> "thing" (2), "think" (1), "third" (1), "this" (1)
        thi = autocomplete_provider.getWords("thi")
        thi_words = [ cand.getWord() for cand in thi]
        self.assertEqual(thi_words, ["thing","think","third","this"])
        thi_confs = [ cand.getConfidence() for cand in thi]
        self.assertEqual(thi_confs, [2,1,1,1])


        #Input: "nee" --> "need" (1)
        nee = autocomplete_provider.getWords("nee")
        nee_words = [ cand.getWord() for cand in nee]
        self.assertEqual(nee_words, ["need"])
        nee_confs = [ cand.getConfidence() for cand in nee]
        self.assertEqual(nee_confs, [1])


        #Input: "th" --> "that" (2), "thing" (2), "think" (1), "this" (1), "third" (1), "the" (1), "thoroughly" (1)
        th = autocomplete_provider.getWords("th")
        th_words = [ cand.getWord() for cand in th]
        self.assertEqual(th_words, ["that","thing","the","think","third","this","thoroughly"])
        th_confs = [ cand.getConfidence() for cand in th]
        self.assertEqual(th_confs, [2,2,1,1,1,1,1])

if __name__ == "__main__":
    unittest.main()
