from lib.word_transform import apply_methods, get_method, get_word
import kenlm
from absl import flags, app

FLAGS = flags.FLAGS
flags.DEFINE_string('model1', None, 'Model path.')
flags.DEFINE_string('model2', None, 'Model path.')
flags.DEFINE_string('test_file', None, 'Model path.')
flags.DEFINE_string('identifier', None, 'Input sentences.')


def main(argv):
    del argv
    model1 = kenlm.LanguageModel(FLAGS.model1)
    model2 = kenlm.LanguageModel(FLAGS.model2)
    
    N = 0
    res = 0.

    transform_method = get_method(FLAGS.identifier)
    with open(FLAGS.test_file, "r") as ifile:
        for line in ifile:
            words = line.split(" ")
            transformed_words = [transform_method(w) for w in words]
            transformed_line = " ".join(transformed_words)
            transformed_words = ["<s>"] + transformed_words + ["</s>"]
            full_words = [apply_methods(w, [transform_method, get_word]) for w in words]
            for i, (prob, length, oov) in enumerate(model1.full_scores(transformed_line)):
                N+=1
                bigram = transformed_words[i+2-length:i+2]
                res += prob
                if bigram[-1] == "<\s>" or oov:
                    continue
                full_word = full_words[i]
                full_scores = model2.full_scores(full_word)
                res += full_scores[1][0]
    
    print(f"Perplexity: {10**(res/N)}")


if __name__ == "__main__":
    app.run(main)