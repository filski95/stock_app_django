from black import out
from stocks_app.models import Stock


class TrieNode:
    def __init__(self) -> None:
        self.letters: dict[str, TrieNode] = {}


class Trie:
    root = TrieNode()
    stocks = Stock.objects.all()

    def alternatives(self, word):
        current_node = self.root
        matched = ""

        for char in word:
            if current_node.letters.get(char):
                matched += char
                current_node = current_node.letters.get(char)
            else:
                # if current character isnt found among the current node's letters
                # collect the suffixes from current char get n of them and output concatenated
                # with already matched string
                word = self.collect_all_words(current_node)[:2]  # nb of suggestions can be adjusted.
                output = [matched + w for w in word]
                return output

        if "*" not in current_node.letters.keys():
            # if "word" typed in by the user is not a fully fledged word
            # we add 1 to it and use autocorrect again
            # adding number makes the for loop not finish and lets the function deploy self.collect_all_words
            word_suggestion = matched + str(1)
            word_suggestion = self.alternatives(word_suggestion)
            return word_suggestion
        return word

    def insert_word(self, word):
        current_node = self.root

        for char in word:
            if current_node.letters.get(char):
                current_node = current_node.letters[char]
            else:
                new_node = TrieNode()
                current_node.letters[char] = new_node
                current_node = new_node

        current_node.letters["*"] = 0

    def collect_all_words(self, node=None, word="", words=None):
        if words is None:
            words = []

        current_node = node or self.root
        for child_key, child_node in current_node.letters.items():
            # if the current key is * we hit the end of the word and can append it to words
            if child_key == "*":
                words.append(word)

            else:
                # otherwise we call the function recursively -> words [] is a list -> mutable so will contain all the new words.
                self.collect_all_words(child_node, word + child_key, words)
        return words
