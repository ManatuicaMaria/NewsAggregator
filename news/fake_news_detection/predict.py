from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, GlobalMaxPooling1D
from keras.layers import Conv1D, Embedding
from keras.models import Model
import pickle
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

PATH_CONV = dir_path + "/trained_models/weights.best-1.hdf5"
PATH_TOKENIZER = dir_path + "/trained_models/tokenizer.pickle"
PATH_MATRIX_WORD2VEC= dir_path + "/trained_models/embedding_matrix_word2vec"
MAX_SEQUENCE_LENGTH = 24256
EMBEDDING_DIM = 300  # size of word2vec vector


def load_tokenizer():
    with open(PATH_TOKENIZER, 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer


def load_convolutional_network(tokenizer):
    with open(PATH_MATRIX_WORD2VEC, 'r') as file:
        embedding_matrix = pickle.load(file)
    embedding_layer = Embedding(len(tokenizer.word_index) + 1,
                                EMBEDDING_DIM,
                                weights=[embedding_matrix],
                                input_length=MAX_SEQUENCE_LENGTH,
                                trainable=False)

    sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
    embedded_sequences = embedding_layer(sequence_input)
    x = Conv1D(128, 5, activation='relu')(embedded_sequences)
    x = GlobalMaxPooling1D()(x)
    x = Dense(128, activation='relu')(x)
    preds = Dense(2, activation='softmax')(x)
    model = Model(sequence_input, preds)
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',
                  metrics=['acc'])
    model.load_weights(PATH_CONV)
    return model


def predict_news(model, news, tokenizer):
    sequences = tokenizer.texts_to_sequences(news)
    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    return model.predict(data)


if __name__ == '__main__':
    tokenizer = load_tokenizer()
    model = load_convolutional_network(tokenizer)
    print "I've loaded models"
    news = ["After Vets Fight War", "An example of fake news", "Some real news"]
    results = predict_news(model, news, tokenizer)
    print str(results)
    print int(results[0][1] * 100)
