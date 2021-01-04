import kenlm
from absl import flags, app

FLAGS = flags.FLAGS
flags.DEFINE_string('model', None, 'Model path.')
flags.DEFINE_string('input', None, 'Input sentences.')

def main(argv):
    del argv
    with open(FLAGS.input, 'r') as file:
        data = file.read().replace('\n', '</s>')

    model=kenlm.Model(FLAGS.model) 
    per=model.perplexity(data)

    print(per)


if __name__ == "__main__":
    app.run(main)