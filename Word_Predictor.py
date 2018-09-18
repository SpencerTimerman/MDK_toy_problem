
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

import unittest
class TestCandidate(unittest.TestCase):

    def test_creation(self):
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
        with self.assertRaises(ValueError):
            Candidate(word = "test", confidence = 0)

        with self.assertRaises(ValueError):
            Candidate(word = "test", confidence = -1)

        with self.assertRaises(ValueError):
            Candidate(word = "test", confidence = -100)




class AutocompleteProvider:
    def __init__(self):
        self.candidates = {}

    def getWords(self, fragment):
        pass

    def train(self, passage):
        pass


if __name__ == "__main__":
    unittest.main()
