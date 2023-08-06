import argparse

from khaiii import KhaiiiApi
import os
'''
카카오 한글 형태소 분석기를 이용한 명사 추출기

'''



def kakao_postagger_nn_finder( summay_text):
    api = KhaiiiApi()
    api.open()
    nn_word_list = []
    for word in api.analyze(summay_text):
        morphs_str = ' + '.join([(m.lex + '/' + m.tag) for m in word.morphs])
        # print(f'{word.lex}\t{morphs_str}')

        morphs_str_list = morphs_str.split(" + ")

        complex_morphs = ""
        for mophs_item in morphs_str_list:
            if mophs_item.split("/")[1].startswith("N") or mophs_item.split("/")[1].startswith("MM") or \
                    mophs_item.split("/")[1].startswith("SN") or mophs_item.split("/")[1].startswith("SL"):
                complex_morphs = complex_morphs + mophs_item.split("/")[0]

        if len(complex_morphs) > 1:
            # print("->", complex_morphs)
            nn_word_list.append(complex_morphs)

    return nn_word_list


def extract_file_noun(input, output):
    input_file = open(input, mode='r', encoding='utf-8')
    open(output, mode='w', encoding='utf-8')
    output_file = open(output, mode='a', encoding='utf-8')
    line_number = 1
    while (True):
        line = input_file.readline()
        if not line:
            break;

        line = line.strip()
        word_list = kakao_postagger_nn_finder(line)

        if len(word_list):
            print(line_number, word_list)
            for word in word_list:
                output_file.write(word + os.linesep)
        line_number += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract File Noun word")
    parser.add_argument('--input', type=str, required=True, default='', help='Input File')
    parser.add_argument('--output', type=str, required=True, default='', help='Output File')
    args = parser.parse_args()

    if not args.input:
        print("input file is invalid!")
        exit(1)

    if not args.output:
        print("output file is invalid!")
        exit(1)

    input = str(args.input)
    output = str(args.output)

    extract_file_noun(input, output)

