
"""
Candidate
    String getWord() : returns the autocomplete candidate
    Integer getConfidence() : returns the confidence* for the candidate

AutocompleteProvider
    List<Candidate> getWords(String fragment) : returns list of candidates ordered by confidence*
    void train(String passage) : trains the algorithm with the provided passage

Train: "The third thing that I need to tell you is that this thing does not think thoroughly."
Input: "thi" --> "thing" (2), "think" (1), "third" (1), "this" (1)
Input: "nee" --> "need" (1)
Input: "th" --> "that" (2), "thing" (2), "think" (1), "this" (1), "third" (1), "the" (1), "thoroughly" (1)
"""

class Candidate:
    def __init__(self, word, confidence):
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
        return self.word

    def getConfidence(self):
        return self.confidence


def test_Candidate():
    word1       = "test"
    confidence1 = "3"
    candidate1  = Candidate(word1,confidence1)

    assert word1 != candidate1.getWord()
    assert confidence1 != candidate1.getConfidence()

    word2       = "testing"
    confidence2 = "1"
    candidate2  = Candidate(word2,confidence2)



class AutocompleteProvider:
    def __init__(self):
        self.candidates = {}

    def getWords(self, fragment):
        pass

    def train(self, passage):
        pass
