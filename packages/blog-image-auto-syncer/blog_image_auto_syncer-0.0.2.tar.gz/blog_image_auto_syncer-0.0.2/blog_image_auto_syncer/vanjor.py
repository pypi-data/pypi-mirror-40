import re
import urllib.request

# http|https://(*?.jpg|png|jpeg|gif|bmp)
regex = "(http|https)://[^)]{1,200}/([^/)]{1,100}.jpg|png|jpeg|gif|bmp)"
pattern = re.compile(regex)


def get_content_from_file(file_path):
    with open(file_path) as f:
        file_content = f.read()
    return file_content


def get_image_links_from_content(content):
    dic = {}
    for match in pattern.finditer(content):
        key = match.group(2)
        url = match.group(0)
        dic[key] = {'key': key, 'url': url}
    return dic


def download_images(image_list, local_dir_path):
    for item in image_list.values():
        print(item)
        print('start download image: ' + item['url'])
        urllib.request.urlretrieve(item['url'], local_dir_path + item['key'])


file_path = "/Users/rujiw/Documents/GitHub/VanjorBlogWebsite/source/_posts/2016/05/git-complete-user-guide.md"

content = get_content_from_file(file_path)
image_list = get_image_links_from_content(content)
download_images(image_list, '')

