# Note: currently horribly unoptimized and has several bugs
# needs serious work before it is usable


class BPETokenizer:

    def __init__(self):
        self.vocab = {}             # maps sub-words -> tokens
        self.inverse_vocab = {}     # maps tokens ->  sub-words
        self.byte_mappings = {}     # shows merged tokens (token1, token2) -> token3

    def train(self, text, vocab_size):

        # replace spaces with Ġ from gpt-2
        preprocessed_text = "".join(["Ġ" if c == " " else c for c in text])

        # add all of the characters in text to a list as well as any chr(i) [0, 255] 
        chars = [chr(i) for i in range(256)]
        chars += (char for char in set(preprocessed_text) if char not in chars)
        if ('Ġ' not in chars):
            chars.append('Ġ')

        # add the characters from this to the vocab
        self.vocab = {i: char for i, char in enumerate(chars)}
        self.inverse_vocab = {char: i for i, char in enumerate(chars)}

        tokens = [self.inverse_vocab[c] for c in preprocessed_text]
        while (len(self.vocab) < vocab_size):

            count = {}
            for i in range(len(tokens)-1):
                pair = (tokens[i], tokens[i+1])
                count[pair] = 1 + count.get(pair, 0)

            # check if count is empty
            if (not bool(count)):
                break
            # get vals
            max_pair = max(count, key=count.get)
            new_token = len(self.vocab)
            new_subword = self.vocab[max_pair[0]] + self.vocab[max_pair[1]]

            # update class vars
            self.vocab[new_token] = new_subword
            self.inverse_vocab[new_subword] = new_token
            self.byte_mappings[max_pair] = new_token

            # update tokens
            updated_tokens = []
            i = 0
            while (i < len(tokens)):

                if (i < len(tokens)-1 and max_pair == (tokens[i], tokens[i+1])):
                    updated_tokens.append(new_token)
                    i += 2
                else:
                    updated_tokens.append(tokens[i])
                    i += 1

            tokens = updated_tokens


        print(f"Vocab: {self.vocab}")

        print(f"inverse vocab: {self.inverse_vocab}")

        print(f"mappings: {self.byte_mappings}")