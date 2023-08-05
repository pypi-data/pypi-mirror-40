import csv
import os

def list_save(content, filename, mode='a'):
    # Try to save a list  into txt file.
    # content:list  filename:path and txt name to save as txt such as : "list.txt"
    if os.path.exists(filename):   # filename could existence or not but i will remove it haha
        os.remove(filename)
    file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()


def text_read(filename):
    # Try to read a txt file and return a list.Return [] if there was a mistake.
    try:
        file = open(filename, 'r')
    except IOError:
        error = []
        return error
    content = file.readlines()

    for i in range(len(content)):
        content[i] = content[i][:len(content[i])-1]

    file.close()
    return content

def save_csv(name, contexts):
    """
    :param name:  要保存的csv文件名， 如：F:\\gps.csv
    :param context:  要保存的文本信息，是一个列表形式：
    gps = [('latitude', 'longitude'), (30.745143, 103.927407), (30.746547, 103.928599), (30.749746, 103.931295),
           (30.750127, 103.931342), (30.751341, 103.931125), (30.752604, 103.932138), (30.752697, 103.931692),
           (30.753472, 103.930368), (30.753892, 103.929642), (30.753959, 103.929286), (30.753958, 103.928148),
           (30.754166, 103.927795), (30.751983, 103.926809), (30.751603, 103.926540), (30.751210, 103.926172),
           (30.751116, 103.925485), (30.750434, 103.925374), (30.749645, 103.925309), (30.748532, 103.925310),
           (30.746889, 103.924647), (30.746662, 103.924997), (30.744803, 103.924260), (30.744162, 103.925255),
           (30.745062, 103.926010), (30.744874, 103.926327), (30.744812, 103.926753), (30.744970, 103.927213)]
           第一行表示名称，后面是值
    :return: 返回一个新的csv文件
    """
    with open(name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for context in contexts:
            csv_writer.writerow(context)


def read_csv(csv_name):
    context = csv.reader(open(csv_name, 'r'))
    cont_list = []
    for file in context:
        cont_list.append(file)
    return cont_list


# ------------------------------------------------------------------------------
