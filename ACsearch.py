import os
import re
from readBook import read_file
from collections import deque


def ignore(c):
    return c == ' ' or c == '\n' or c == '\t' or c == '\r' or c == '\f' or c == '\v'


class TrieNode:
    def __init__(self):
        self.children = {}
        self.fail = None
        self.output = []


class AC:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, pattern, index):
        node = self.root
        for char in pattern:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.output.append(index)

    def build(self):
        queue = deque()
        for char, node in self.root.children.items():
            node.fail = self.root
            queue.append(node)
        while queue:
            current_node = queue.popleft()
            for char, child_node in current_node.children.items():
                fail_node = current_node.fail
                while fail_node is not None and char not in fail_node.children:
                    fail_node = fail_node.fail
                if fail_node is None:
                    child_node.fail = self.root
                else:
                    child_node.fail = fail_node.children[char]
                    child_node.output.extend(child_node.fail.output)
                queue.append(child_node)

    def search(self, text, patterns):
        node = self.root
        matches = set()
        count = 0
        for i in range(len(text)):
            if ignore(text[i]):
                i += 1
                count += 1
                continue
            while node is not None and text[i] not in node.children:
                node = node.fail
                count = 0
            if node is None:
                node = self.root
                count = 0
                continue
            node = node.children[text[i]]
            if node.output:
                for pattern_index in node.output:
                    matches.add(i - len(patterns[pattern_index]) + 1 - count)
                count = 0
        return sorted(list(matches))


def split_by_matches(text, matches):
    segments = []
    start_idx = 0
    for match in matches:
        result = re.sub(r"^[\s\v\f\r\n\t]+|[\s\v\f\r\n\t]+$", "", text[start_idx:match])
        if result != '':
            segments.append(result)
        start_idx = match
    result = re.sub(r"^[\s\v\f\r\n\t]+|[\s\v\f\r\n\t]+$", "", text[start_idx:])
    segments.append(result)
    return segments


def split_and_save(text, patterns, nums):
    patterns = [re.sub(r"[\s\v\f\r\n\t]+", '', pattern).strip() for pattern in patterns]
    nums = sorted(nums)
    ac = AC()
    for i, pattern in enumerate(patterns):
        ac.insert(pattern, i)
    ac.build()
    matches = ac.search(text, patterns)
    splits = split_by_matches(text, matches)
    save_text = []
    for num in nums:
        if num > len(splits):
            continue
        save_text.append(splits[num - 1])
    if len(save_text) == 0:
        save_text = [text]
    file_dir = 'chapters'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    for i, part in enumerate(save_text, 1):
        file_path = os.path.join(file_dir, f'part_{i}.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(part)
            print(f"保存成功: {file_path}")


if __name__ == "__main__":
    text = read_file('D:\pythonProject\AI_PPT\实验成果\测试书籍资料\链接\链接.pdf')
    patterns = [
        '第1链 网络让世界变得不同“人们曾经拆卸过宇宙，却不知道该如何将它再拼起来。',
        '第2链 随机宇宙网络的构造和结构是理解复杂世界的关键。',
        '第3链 六度分隔研究表明，社交网络上任何一对节点之间平均相隔6个链接；任意两个网页之间平均相隔19次点击。',
        '第4链 小世界无论是找工作、获取消息、开餐馆，还是传播新潮流，弱关系在我们和外部世界互通消息方面发挥着至关重要的作用。',
        '第5链 枢纽节点和连接者——复杂网络的关键要素如果万维网是一个随机网络，我们被看到和听到的机会应该是相等的。',
        '第6链 幂律——复杂网络的分布规律40年前，埃尔德什和莱利将复杂网络放到“随机”灌木丛中，而幂律将复杂网络从中拉了出来，并将其放到色彩斑斓、内涵丰富的“自组织”舞台上。',
        '第7链 富者愈富——复杂网络的先发优势在我们不得不引入生长机制之前，经典模型的静态特性一直没有人注意；在幂律要求我们引入偏好连接之前，随机性也不是什么问题。',
        '第8链 爱因斯坦的馈赠——复杂网络的新星效应在大多数复杂系统中，每个节点都有各自的特性。',
        '第9链 阿喀琉斯之踵——复杂网络的健壮性与脆弱性人造的东西通常都会出现错误和故障，但生态系统具有令人惊叹的对错误和故障的容忍性，即便面临诸如造成恐龙等数万种物种灭绝的尤卡坦陨石冲击这样的极端事件，也能安然无恙。',
        '第10链 病毒和时尚之前，人们一直把枢纽节点视为特殊现象，并不清楚它们为什么存在、究竟有多少。',
        '第11链 觉醒中的互联网虽然互联网是人造系统，但从结构上来看，却更像是一个生态系统。',
        '第12链 分裂的万维网万维网远非由节点和链接组成的一个匀质的海洋，它分裂成四块大陆，其中每块大陆上又有许多的村庄和城市，它们以重叠社区的形式出现。',
        '第13链 生命的地图虽然所有的生物体都具有同样的枢纽节点，但不同生物体中连通度较小的分子却各不相同。',
        '第14链 网络新经济从网络的角度去理解宏观经济的相互依赖性，能帮助我们预见和控制未来的危机。',
        '第15链 一张没有蜘蛛的网遮盖细节可以提高我们的感知和观察能力。',
        '注释第1链 网络让世界变得不同媒体就MafiaBoy的故事进行了广泛讨论。'
    ]
    numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    split_and_save(text, patterns, numbers)
