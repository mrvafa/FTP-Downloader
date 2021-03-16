import multiprocessing
import os
import urllib.parse
import urllib.request


def split_list_to_sub_list(input_list, number_sub_list):
    sub_lists = [[] for _ in range(number_sub_list)]

    index = 0
    for item in input_list:
        sub_lists[index].append(item)
        index = (index + 1) % number_sub_list

    return sub_lists


def download_url(url, filename, output_dir=''):
    url_head = url[:url.find('//')]
    url_body = urllib.parse.unquote(url[url.find('//'):])
    url = url_head + urllib.parse.quote(url_body)
    output = os.path.join(output_dir, filename) if output_dir else filename
    if not os.path.isfile(output):
        urllib.request.urlretrieve(url, filename=output)
    return output


def download_urls(urls, filenames, output_dirs):
    for index in range(len(urls)):
        download_url(urls[index], filenames[index], output_dirs[index])


def download_url_using_multi_processor(urls, filenames, output_dirs, cores=multiprocessing.cpu_count()):
    urls_sub_lists = split_list_to_sub_list(urls, cores)
    filenames_sub_lists = split_list_to_sub_list(filenames, cores)
    output_dirs_sub_lists = split_list_to_sub_list(output_dirs, cores)

    processes = []
    for core in range(cores):
        p = multiprocessing.Process(target=download_urls,
                                    args=(urls_sub_lists[core],
                                          filenames_sub_lists[core],
                                          output_dirs_sub_lists[core]))
        p.start()
        processes.append(p)

    for process in processes:
        process.join()


def get_name_from_url(url):
    url = url[url.rfind('/') + 1:]
    return urllib.parse.unquote(url)


if __name__ == '__main__':
    links = open('links.txt', 'r').readlines()
    download_output_dir = 'output'
    if not os.path.isdir(download_output_dir):
        os.mkdir(download_output_dir)
    download_url_using_multi_processor(links, [get_name_from_url(link) for link in links],
                                       [download_output_dir for _ in range(len(links))], cores=16)
