from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
import nltk

nltk.download("averaged_perceptron_tagger")
st = StanfordNERTagger(
    "../Lib/english.all.3class.distsim.crf.ser.gz", "../Lib/stanford-ner.jar"
)


def stanfordNE2BIO(tagged_sent):
    bio_tagged_sent = []
    prev_tag = "O"
    for token, tag in tagged_sent:
        if tag == "O":  # O
            bio_tagged_sent.append((token, tag))
            prev_tag = tag
            continue
        if tag != "O" and prev_tag == "O":  # Begin NE
            bio_tagged_sent.append((token, "B-" + tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag == tag:  # Inside NE
            bio_tagged_sent.append((token, "I-" + tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag != tag:  # Adjacent NE
            bio_tagged_sent.append((token, "B-" + tag))
            prev_tag = tag

    return bio_tagged_sent


def stanfordNE2tree(ne_tagged_sent):
    bio_tagged_sent = stanfordNE2BIO(ne_tagged_sent)
    sent_tokens, sent_ne_tags = zip(*bio_tagged_sent)
    sent_pos_tags = [pos for token, pos in pos_tag(sent_tokens)]

    sent_conlltags = [
        (token, pos, ne)
        for token, pos, ne in zip(sent_tokens, sent_pos_tags, sent_ne_tags)
    ]
    ne_tree = conlltags2tree(sent_conlltags)
    return ne_tree


def get_ne_in_sent_from(sent):
    tokenized_text = word_tokenize(sent)
    classified_text = st.tag(tokenized_text)
    ne_tree = stanfordNE2tree(classified_text)
    ne_in_sent = []
    for subtree in ne_tree:
        if type(subtree) == Tree:  # If subtree is a noun chunk, i.e. NE != "O"
            ne_label = subtree.label()
            # ne_string = " ".join([token for token, pos in subtree.leaves()])
            # ne_in_sent.append((ne_string, ne_label))
            ne_in_sent.append(ne_label)
    return ne_in_sent


# print(get_ne_in_sent_from("Kim Jong Un"))
# print(get_ne_in_sent_from("person"))
# print(get_ne_in_sent_from("bacon"))