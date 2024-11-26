import re

from readBook import read_file


def ignore(c):
    return c == ' ' or c == '\n' or c == '\t' or c == '\r' or c == '\f' or c == '\v'


def get_index(text, pattern):
    n = len(text)
    m = len(pattern)

    def compute_next(pattern):
        next_array = [-1] * m
        j = 0
        for i in range(1, m):
            while j > 0 and pattern[i] != pattern[j]:
                j = next_array[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
                next_array[i] = j
            else:
                next_array[i] = 0

        return next_array

    next_array = compute_next(pattern)
    i = 0
    j = 0
    matches = []
    count = 0
    while i < n:
        if ignore(text[i]):
            i += 1
            count += 1
            continue

        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - j - count)
                j = next_array[j - 1]
                count = 0
        else:
            count = 0
            if j > 0:
                j = next_array[j - 1]
            else:
                i += 1
    return matches


def split_by_matches(text, matches):
    segments = []
    start_idx = 0
    for match in matches:
        result = re.sub(r"^[\s\v\f\r\n\t]+|[\s\v\f\r\n\t]+$", "", text[start_idx:match])
        segments.append(result)
        start_idx = match
    result = re.sub(r"^[\s\v\f\r\n\t]+|[\s\v\f\r\n\t]+$", "", text[start_idx:])
    segments.append(result)
    return segments


def split_and_save(text, patterns, nums):
    patterns = [re.sub(r"[\s\v\f\r\n\t]+", '', pattern).strip() for pattern in patterns]
    matches = set()
    for pattern in patterns:
        matches = matches.union(set(get_index(text, pattern)))
    matches = sorted(matches)
    splits = split_by_matches(text, matches)
    save_text = []
    for num in nums:
        if num > len(splits):
            continue
        save_text.append(splits[num - 1])
    for i, part in enumerate(save_text, 1):
        file_path = f'chapters/part_{i}.txt'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(part)
            print(f"保存成功: {file_path}")


if __name__ == "__main__":
    text = read_file('link.epub')
    patterns = [
        '第6链 幂律——复杂网络的分布规律40年前，埃尔德什和莱利将复杂网络放到“随机”灌木丛中，而幂律将复杂网络从中拉了出来，并将其放到色彩斑斓、内涵丰富的“自组织”舞台上。',
        '第7链 富者愈富——复杂网络的先发优势在我们不得不引入生长机制之前，经典模型的静态特性一直没有人注意；在幂律要求我们引入偏好连接之前，随机性也不是什么问题。',
        '第8链 爱因斯坦的馈赠——复杂网络的新星效应在大多数复杂系统中，每个节点都有各自的特性。']
    numbers = [2, 3]
    split_and_save(text, patterns, numbers)
