from absl import app
from lib.word_transform import *


def main(argv):
    del argv

    if FLAGS.vocabulary:
        load_vocabulary(FLAGS.vocabulary)

    if FLAGS.prefixes:
        load_prefixes(FLAGS.prefixes)

    if FLAGS.suffixes:
        load_suffixes(FLAGS.suffixes)

    if FLAGS.supertags:
        load_supertags(FLAGS.supertags)

    if FLAGS.bases:
        load_superbases(FLAGS.bases)

    methods = [get_method(identifier) for identifier in FLAGS.features]

    with open(FLAGS.input, "r") as ifile:
        with open(FLAGS.output, "w") as ofile:
            for line in ifile:
                line = line if line[-1] != "\n" else line[:-1]
                res = [apply_methods(w, methods = methods) for w in line.split(" ")]
                res = " ".join(res)+ "\n"
                ofile.write(res)
                
if __name__ == "__main__":
    app.run(main)