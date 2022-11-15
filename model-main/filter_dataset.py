import torchtext

from tokenizer import Language, Tokenizer

model_en = torchtext.vocab.FastText("en")
model_fr = torchtext.vocab.FastText("fr") # Nigger can you run this?

en_tokenizer = Tokenizer(Language.EN)
fr_tokenizer = Tokenizer(Language.FR)


with open("english.txt", "r", encoding="utf8") as en_f, open("french.txt", "r", encoding="utf8") as fr_f:
    lines = zip(en_f.readlines(), fr_f.readlines())

    with open("english_filtered.txt", "w", encoding="utf8") as en_ff, open("french_filtered.txt", "w", encoding="utf8") as fr_ff:
        for i, (en_line, fr_line) in enumerate(lines):
            en_tokens = en_tokenizer.tokenize(en_line)
            fr_tokens = fr_tokenizer.tokenize(fr_line)

            case_1 = all([token in model_en.stoi for token in en_tokens])
            case_2 = all([token in model_fr.stoi for token in fr_tokens])

            if case_1 and case_2:
                en_ff.write(en_line)
                fr_ff.write(fr_line)
            
            print(f"{i}/700000")