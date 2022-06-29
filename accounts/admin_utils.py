from stocks_app.models import Stock


class SingletonMeta(object):

    _instances: dict["SingletonMeta", "Trie"] = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class TrieNode:
    def __init__(self) -> None:
        self.letters: dict[str, TrieNode] = {}


class Trie(SingletonMeta):
    root = TrieNode()
    stocks = Stock.objects.all()

    def alternatives(self, word):
        """
        provides name suggestions in case of typos. Does not work for cases where first letter is wrong.
        """

        current_node = self.root
        matched = ""

        # if first letter is wrong counter will be 0 and we can return None rightaaway
        counter = 0
        for char in word:
            if current_node.letters.get(char):
                matched += char
                current_node = current_node.letters.get(char)
                counter += 1
            else:
                # if current character isnt found among the current node's letters
                # collect the suffixes from current char get n of them and output concatenated
                # with already matched string
                if counter != 0:
                    word = self.collect_all_words(current_node)[:2]  # nb of suggestions can be adjusted.
                    output = [matched + w for w in word]
                    return output
                else:
                    return None

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
