from bpe import BPETokenizer

if __name__ == "__main__":

    tokenizer = BPETokenizer()
    tokenizer.train("testing this shit out lets go!!!!", 512)