import json
import numpy as np
import itertools
import re


def data_generator(x_train_feature_dir, y_train_filename, thershold_of_occurences):

    # Load data
    f = open(y_train_filename)
    print('start loading data')
    y_train = json.load(f)

    video_id = []
    feature_list = []
    captions = []
    num_of_captions_list = []

    for label_data in y_train:
        feature = np.load(x_train_feature_dir + '/feat/' +
                          label_data['id']+'.npy')
        feature_list.append(feature)
        num_of_caption = len(label_data['caption'])
        num_of_captions_list.append(num_of_caption)
        video_id.append(label_data['id'])

        for caption in label_data['caption']:
            captions.append(re.sub(r'[^a-zA-Z0-9 ]', '', caption.lower()))

    print('start encoding')
    # init dictonary
    dic = {}
    word_to_idx = {
        'BOS': 0,
        'EOS': 1,
        'UWK': 2,
        'PAD': 3
    }
    next_word_id = 4
    idx_to_word = None

    for caption in captions:
        for word in caption.split():
                dic[word] = dic.get(word, 0) + 1

    for item in dic.items():
        if item[1] > thershold_of_occurences:
                word_to_idx[item[0]] = next_word_id
                next_word_id += 1

    idx_to_word = dict((reversed(item) for item in word_to_idx.items()))

    captions = list(map(str.split, captions))
    captions = [[word_to_idx.get(word, 2) for word in caption]
                for caption in captions]

    print('start convert to np array')
    features = np.repeat([feature_list[0]], num_of_captions_list[0], axis=0)
#     print(features.shape)
    i = 0
    for item in zip(feature_list[1:], num_of_captions_list[1:]):
        features = np.concatenate((features, np.repeat([item[0]], item[1], axis=0)), axis=0)
        print('the n th: ' + str(i))
        i += 1

    captions=np.array(captions)

    max_length=max([len(caption) for caption in captions]) + 1
    sequence_length=np.array([len(caption) + 1 for caption in captions])

    y_inputs=np.array([[word_to_idx['BOS']] + y + [word_to_idx['PAD']]
                         * (max_length - len(y) - 1) for y in captions])
    y_targets=np.array([y + [word_to_idx['EOS']] + [word_to_idx['PAD']]
                          * (max_length - len(y) - 1) for y in captions])

    # print('y_inputs: ', y_inputs)
    # print('y_targets: ', y_targets)
    print('Done data generation!')

    print(features.shape, y_inputs.shape, y_targets.shape, len(word_to_idx), len(
        idx_to_word), next_word_id, max_length, sequence_length)

    # print('features[0]: ', features[0])
    # print('y_inputs: ', y_inputs)
    # print('y_targets: ', y_targets)
    # print('word_to_idx: ', word_to_idx)
    # print('idx_to_word: ', idx_to_word)
    # print('sequence_length: ', sequence_length)

    return features, y_inputs, y_targets, word_to_idx, idx_to_word, next_word_id, max_length, sequence_length


def generate_batch(X, y_inputs, y_targets, word_idx, sequence_length, batch_size):

    idx=np.random.choice(len(X), batch_size)

    X_batch=X[idx]
    y_inputs_batch=y_inputs[idx]
    y_targets_batch=y_targets[idx]
    sequence_length_batch=sequence_length[idx]
    return X_batch, y_inputs_batch, y_targets_batch, sequence_length_batch


if __name__ == '__main__':
    X, y_inputs, y_targets, word_idx, idx_word, _, _, sequence_length=data_generator(
        './data/training_data', './data/training_label.json', 2)

    generate_batch(X, y_inputs, y_targets, word_idx, sequence_length, 128)
