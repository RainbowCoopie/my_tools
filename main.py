"""
this is Rainbow's Tool
"""

__author__ = "RainbowCookie"
__email__ = "2572504750@qq.com"


""" 导出环境依赖, 下载离线依赖文件(whl), 安装离线包 """
# 一键导出环境依赖及安装环境依赖
# pip3 freeze > requirements.txt

# 从当前环境的网络中下载requirements.txt中写的包，下载到当前目录下的pip_packages目录中，这时候你会发现，里面有很多依赖，还有一些whl文件
# pip download  -r requirements.txt  -d  ./pip_packages

# 安装离线包 --find-links指定的是包文件的存放地址，-r指定的是txt文件的位置
# pip install --no-index --find-links=E:\／／knowledge-base／／\python三方库本地源 -r requirements.txt


def get_program_path(program_name=None):
    """
    获取计算机下所有程序的路径, 并找到需要查询的那个程序的路径
    example: chrome_path = get_program_path(program_name="chrome.exe")
    """
    import win32api
    import win32con
    import os
    sub_keys = [
        r'Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store',
        r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths'
    ]
    programs = {}
    for sub_key in sub_keys:
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, sub_key, 0, win32con.KEY_READ)
        info = win32api.RegQueryInfoKey(key)
        for index in range(0, info[1]):
            _path = win32api.RegEnumValue(key, index)[0]
            _name = os.path.basename(_path)

            if program_name:
                if program_name.casefold() == _name.casefold():
                    return _path
            programs[_name] = _path
    return programs


def get_chrome_version():
    """ 获取 chrome 版本信息"""
    import os
    dos = r'reg query "HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome"'
    stream = os.popen(dos)
    output = stream.read()
    try:
        google_version = ''
        KEY = 'DisplayVersion    REG_SZ'
        for letter in output[output.rindex(KEY) + len(KEY):]:
            if letter != '\n':
                google_version += letter
            else:
                break
        return google_version.strip()
    except TypeError:
        return None


def get_chrome_driver_url(chrome_version):
    """
    获取指定 chrome 版本的 chrome driver
    example: chrome_driver_url = get_chrome_driver_url("125.0.6422.113")
    """
    import requests
    version = ""
    response = requests.get(r"https://registry.npmmirror.com/-/binary/chrome-for-testing/")
    if response.status_code == 200:
        data = response.json()
        for _ in reversed(data):
            if ".".join(_["name"].split(".")[:-1]) in chrome_version:
                version = _["name"]
                break
    url = f"https://registry.npmmirror.com/-/binary/chrome-for-testing/{version}win64/chromedriver-win64.zip"
    return url if version else False


def compress_zip(file_path: str, zip_path: str, mode=None):
    """
    document: 本函数功能为将指定目录文件件打包压缩为 zip 文件
    param file_path: 需要进行打包压缩的文件夹目录
    param zip_path: 输出 zip 文件路径
    param mode: zip 文件打开或创建模式
    return: True
    example: compress_zip(r"E:\_example", r"E:\_example.zip")
    """
    import zipfile
    import os
    mode = "x" if not mode else mode
    with zipfile.ZipFile(file=zip_path, compression=zipfile.ZIP_STORED, mode=mode, allowZip64=True) as zip:
        """
        # allowZip64 = True  指定 Zip 文件在必要情况下是否可以使用 Zip64 格式来支持超过 4GB 的文件
        
        # mode = "x"  以排它方式进行 Zip 文件的创建, 若文件已经存在, 则会引发 FileExistsError 异常
        # mode = "w"  以覆盖方式打开 Zip 文件, 若目标 Zip 文件已经存在, 则该文件将被覆盖, 若目标文件尚不存在，则创建它
        # mode = "r"  mode 参数的 默认值 为 r, 表示以只读方式打开 zip 文件, 如果文件不存在, 则会引发异常 FileNotFoundError
        # mode = "a"  以追加方式打开 Zip 文件, 若文件已经存在，则在该文件的末尾进行文件的写入, 若目标文件尚不存在，则创建它
        
        # compression = zipfile.ZIP_STORED  不进行任何压缩, 直接存储原始数据, 通常使用该压缩算法对文件进行归档
        # compression = ZIP_DEFLATED  提供比较高的压缩率和较快的压缩和解压速度
        # compression = ZIP_BZIP2  比 Deflate 更高的压缩率, 但压缩和解压速度较慢
        # compression = ZIP_LZMA  比 Bzip2 更高的压缩率, 但压缩和解压速度更慢
        """
        if os.path.isdir(file_path):
            root_len = len(os.path.dirname(file_path))
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    if os.path.join(root, file) == zip_path:
                        continue
                    arcname = os.path.join(root, file)[root_len:].strip(os.sep)
                    zip.write(os.path.join(root, file), arcname)
        else:
            zip.write(file_path, file_path.split(os.sep)[-1])
        return True


def unpack_zip(zip_path: str, unzip_path: str, keep_structure=False):
    """
    document: 本函数功能为将指定zip文件解压到指定位置
    param zip_path: 需要进行解压的文件路径
    param unzip_path: 解压到的文件目录
    param keep_structure: 是否保留 zip 文件中的文件结构, 默认为False
    return: True
    example: unpack_zip(r"D:\example\example.zip", r"D:\example")
    """
    import zipfile
    import os
    with zipfile.ZipFile(zip_path) as zf:
        for zip_file_info in zf.infolist():
            if zip_file_info.filename[-1] == "/":
                continue
            if not keep_structure:
                zip_file_info.filename = os.path.basename(zip_file_info.filename)  # 不保留zip文件目录结构

            unzip_file_path = os.path.join(unzip_path, zip_file_info.filename)  # 解压后文件路径
            if os.path.exists(unzip_file_path):  # 如果已经有了该文件
                if not os.path.isdir(unzip_file_path):
                    for index in range(1, 20):  # 则反复尝试(20次) 进行重命名
                        salt = index * "_"  # 每次尝试重命名的变量不同
                        new_unzip_file_path = salt.join(os.path.splitext(unzip_file_path))  # 新名字
                        try:
                            os.renames(unzip_file_path, new_unzip_file_path)  # 如果重命名成功
                            break  # 跳出循环
                        except Exception:
                            pass  # 重命名失败
            zf.extract(zip_file_info, unzip_path)  # 解压文件
    return True


def compress_tar(file_path: str, tar_path: str, mode=None):
    """
    document: 本函数功能为将指定目录文件件打包压缩为 tar 文件
    param file_path: 需要进行打包压缩的文件夹目录
    param tar_path: 输出 tar 文件路径
    param mode: zip 文件打开或创建模式
    return: True
    example: compress_tar(r"E:\example", r"E:\example.tar")
    """
    import tarfile
    import os
    mode = "x" if not mode else mode
    with tarfile.open(tar_path, mode=mode) as tar:
        """
        # mode = "x"  以排它方式进行 Zip 文件的创建, 若文件已经存在, 则会引发 FileExistsError 异常
        # mode = "w"  以覆盖方式打开 Zip 文件, 若目标 Zip 文件已经存在, 则该文件将被覆盖, 若目标文件尚不存在，则创建它
        # mode = "r"  mode 参数的 默认值 为 r, 表示以只读方式打开 zip 文件, 如果文件不存在, 则会引发异常 FileNotFoundError
        # mode = "a"  以追加方式打开 Zip 文件, 若文件已经存在，则在该文件的末尾进行文件的写入, 若目标文件尚不存在，则创建它
        """
        if os.path.isdir(file_path):
            root_len = len(os.path.dirname(file_path))
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    arcname = os.path.join(root, file)[root_len:].strip(os.sep)
                    tar.add(os.path.join(root, file), arcname)
        else:
            tar.add(file_path)
        return True


def check_tar(tar_path):
    """
    document: 本函数功能为校验 tar 文件的完整性
    param tar_path: tar 文件路径
    return: True
    example: check_tar(r"D:\tempOutput\sample21.tar")
    """
    import tarfile
    BLOCK_SIZE = 1024
    with tarfile.open(tar_path) as tar:
        for member in tar.getmembers():
            with tar.extractfile(member.name) as target:
                for chunk in iter(lambda: target.read(BLOCK_SIZE), b''):
                    pass
    return True


def get_suffix(file_dir: str, display_suffix: list = None) -> list:
    """
    document: 本函数功能为获取目录下每种文件格式数量 (通过后缀)
    param file_dir: 需要获取的文件夹目录
    return: 指定目录下每种文件格式数量
    example: get_suffix(r"E:\example")
    """
    import os
    import operator
    suffix_dict = {"count": 0}
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            suffix_dict["count"] += 1
            suffix = file.split(".")[-1]
            display_suffix = display_suffix if display_suffix else []
            if suffix in display_suffix:  # ["7z", "7Z", "zip", "ZIP", "rar", "RAR"]:  # 打印压缩文件路径
                print(os.path.join(root, file))

            suffix_dict[suffix] = suffix_dict.get(suffix, 0) + 1
    suffix_list = sorted(suffix_dict.items(), key=operator.itemgetter(1), reverse=True)
    return suffix_list


def rule_dir(check_dir: str) -> str:
    """
    document: 本函数功能为将路径规范化, 不合法的字符被删除
    param check_dir: 需要进行规范化的路径
    return: 规范化后的路径
    example: rule_dir(r"E:\exam?ple")
    """
    import os
    import re
    intab = r'[?*/\|:><"]'
    path_tier_list = os.path.normpath(check_dir).split(os.sep)
    print(path_tier_list)
    for index in range(len(path_tier_list)):
        path_tier_list[index] = re.sub(intab, "",
                                       path_tier_list[index]).strip() if index > 0 else f"{path_tier_list[index]}\\"
        print(path_tier_list)
        while path_tier_list[index][-1] == ".":
            path_tier_list[index] = path_tier_list[index][0:-1]
    return os.path.join(*(base_name for base_name in path_tier_list))


def create_dir(generate_dir: str) -> str:
    """
    document: 本函数功能为规范化逐层创建目录
    param generate_dir: 需要进行规范化逐层创建的路径
    return: 成功创建的路径
    example: create_dir(r"E:\exam?ple")
    """
    import os
    generate_dir = rule_dir(generate_dir)
    path_tier_list = os.path.normpath(generate_dir).split(os.sep)
    generate_dir = f"{path_tier_list[0]}\\"
    for path_tier in path_tier_list[1:]:
        generate_dir = os.path.join(generate_dir, path_tier)
        if os.path.exists(generate_dir):
            if os.path.isdir(generate_dir):
                continue
        os.mkdir(generate_dir)
    return generate_dir


def download_url(url: str, path: str):
    """
    document: 本函数功能为将 url 中的文件下载到本地 path 路径
    param url: 需要下载文件的 url 网址
    param path: 下载到本地的的 ptah 路径
    return: 下载是否成功(True/False)
    example: download_url(r"https://ww.example.com/example/example.jpg", r"D:\example\example.jpg")
    """
    """ 下载url文件到, file_path"""
    import requests
    import os
    import datetime
    import sys
    try:
        response = requests.get(url, stream=True)
        """
        请求关键参数：stream=True。 默认情况下，当你进行网络请求后，响应体会立即被下载。 你可以通过 stream 参数覆盖这个行为，推迟下载响应体直到访问 Response.content 属性
        """
        try:
            file_size = int(requests.head(url).headers['Content-Length'])  # 获取到文件标识的大小, 不一定是文件的实际大小
            # file_size = len(response.content)  # 获取到文件的实际大小, 此方法虽然能获取到实际大小, 但本质上是下载了一遍
        except Exception as e:
            file_size = 1
        down_size = 0  # 已下载大小
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):  # 每次请求数据不超过 chunk_size 的值, 防治大文件下载失败
                if chunk:
                    f.write(chunk)
                    down_size += len(chunk)
                    """
                    sys.stdout.write() 说明:
                    sys.stdout.write()为 输出一个字符串, print(obj)实际上是调用sys.stdout.write(obj+'\n')
                    sys.stdout.write(obj+'\n') \n 表示换行且回到下一行的最开始位置
                    sys.stdout.write(obj+'\r') \r 表示返回到当行的最开始位置
                    """
                    sys.stdout.write(
                        f'\r[{path}][下载进度]: {round((down_size / file_size) * 100, 2)}%  ({down_size} / {file_size})')  # 下载进度条
        if not os.stat(path).st_size >= file_size:
            print(
                f"  文件下载缺失 ({os.stat(path).st_size} / {down_size}) --> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return False  # 文件大小校验失败导致
        else:
            print(
                f"  文件下载完成 ({os.stat(path).st_size} / {down_size}) --> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True  # 下载成功
    except Exception as e:
        return False  # 异常导致下载失败


def recode_text(file_path: str, language: str = "ja"):
    """
    document: 本函数功能为将文本文件中的日语乱码再编译
    param file_path: 乱码文件(txt文本文件)
    param language: 乱码语言编码
    return: True
    example: recode_text(r"E:\example\readme.txt")
    """
    code_map = {
        "ja": {"encode": "GBK", "decode": "Shift_JIS"},
        "en": None,
        "ko": None,
    }
    encode = code_map[language]["encode"]
    decode = code_map[language]["decode"]
    with open(file_path, "r", ) as f:  # encoding="utf-8"
        text = f.read()
    with open(file_path, "w", encoding="utf-8") as f:
        text = text.encode(encoding=encode).decode(encoding=decode, errors="ignore")
        f.write(text)
    return True


def decimal_system_conversion(number: int, system: int) -> list[str]:
    """
    document: 本函数功能为将原数据为十进制的数值, 转换为指定进制, 输出其存放指定进制的单值列表
    param number: 原数值(十进制)
    param system: 需要转化至的进制
    return: 存放指定进制的单值列表
    example: decimal_system_conversion(999, 8)  # 将十进制 999 转换为 8 进制, 结果为 [1, 7, 4, 7]
    """
    import math
    import array
    def _decimal_system_conversion_recursion(_number: int, _result: list):
        """ 递归计算 """
        power = (int(math.log(_number, system)))  # 最大指数, 同时也是当前值指向result的下标
        _result[power] = int(_number / system ** power)  # 赋值
        _number -= system ** power * int(_number / system ** power)  # 自减
        if _number > 0:
            _number, _result = _decimal_system_conversion_recursion(_number, _result)
        return _number, _result

    def _get_c_type(_sys):
        """ 根据占用资源分配 C 类型 """
        type_mapping = [
            {"max": 255, "c_type": "B"},
            {"max": 65535, "c_type": "H"},
            {"max": 4294967295, "c_type": "I"},
        ]
        for type_dict in type_mapping:
            if _sys < type_dict["max"]:
                return type_dict["c_type"]
        else:
            raise Exception(f"system is out of range({type_mapping[-1]['max']})")

    c_type = _get_c_type(system)  # 获取C类型
    # 创建值为0且索引值足够的结果列表 由array代替list以提升执行效率
    result = array.array(c_type, (0 for _ in range(0, int(math.log(number, system)) + 1)))
    num, result = _decimal_system_conversion_recursion(number, result.tolist())  # 调用递归函数
    result = result[::-1]
    return result


def get_mode(element_list: list) -> list:
    """
    document: 本函数功能为返回元素列表中的众数对象列表(可能有多个众数)
    param element_list: 元素列表
    return: 返回众数
    example: get_mode([1,2,2,2,3,4,4,5,6])
    """
    element_dict = {}
    for element in element_list:
        element_dict[element] = element_dict[element] + 1 if element in element_dict else 1
    sort_list = sorted(element_dict.items(), key=lambda x: x[1], reverse=True)
    mode_count = sort_list[0][1]  # 最多对象的数量

    mode = []
    for element in sort_list:
        if element[1] == mode_count:
            mode.append(element[0])
        else:
            break
    return mode


def generate_pdf(root_dir: str, get_width_func="mode", quality=95):
    """
    document: 本函数功能为将目录和其子目录下的图片文件, 按照每个文件夹来导出为pdf文件
    param root_dir: 需要处理的根目录
    param get_width_func: 获取 pdf 中展示的宽度对其方式的函数模式, 默认为 mode 众数模式
    param quality: 清晰度, 95为高画质, 数值越低图片失真越严重, 图片质量越模糊, 文件大小越小
    return: True
    example: generate_pdf(r"D:\example")
    """
    import os
    from PIL import Image
    from natsort import natsorted
    import psutil
    import sys
    import gc

    def _generate_pdf_get_mode(element_list) -> object:
        """
        document: 本函数功能为返回元素列表中的众数对象
        param element_list: 元素列表
        return: 众数对象
        example: _generate_pdf_get_mode([1,2,2,2,3,4,4,5,6])
        """
        return get_mode(element_list)[0]

    def _generate_pdf_internal_func(_root, img_basename_list, _get_width_callback):
        """
        document: 本函数功能为返回元素列表中的众数对象
        param root: 图片文件所在路径
        param img_basename_list: 图片文件 basename 列表
        return: True
        example: _generate_pdf_internal_func(root, processing_file_list)
        """
        pdf_basename = f"{os.path.basename(_root)}.pdf"  # pdf文件名
        # 根据需要处理的图片的宽度, 用 get_width_callback 方法 取需要 pdf 中展示的宽度 -> output_width
        width_list = [Image.open(os.path.join(_root, file)).width for file in img_basename_list]
        output_width = _get_width_callback(width_list)

        img_list = []  # 存放img对象: Image.open返回值的列表
        pdf = None  # 创建一个值为None的pdf对象, 保存的时候需要判断该对象是否不为None

        memory_footprint = 0  # 占用内存量
        img_basename_dict = {}  # 用于最终展示的信息字典
        for img_file in natsorted(img_basename_list):  # natsorted 排序是符合windows文件名的排序
            memory_footprint = int(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024)  # 计算内存消耗
            sys.stdout.write(f"\r[ 正在处理 {pdf_basename} ]  [ 内存占用 {memory_footprint} MB ]  [ 正在处理图片 {img_file} ]")

            img_format = get_file_type(os.path.join(_root, img_file))[0]  # 获取图像文件的格式
            # channel = channel_mapping[img_format] if img_format in channel_mapping else "RGBA"  # 根据根式选择符合的RGBA通道
            channel = "RGB"
            img_basename_dict[img_file] = channel  # 记录信息到 img_basename_dict

            img_obj = Image.open(os.path.join(_root, img_file)).convert(channel)  # 创建单张图片的对象
            if img_obj.width != output_width:  # 根基width的对齐方式使图片的宽度向输出宽度对齐(高度同比适配)
                output_height = int(img_obj.height * (output_width / img_obj.width))
                img_obj = img_obj.resize((output_width, output_height), Image.LANCZOS)
            if not pdf:  # 如果当前单图对象是该pdf中的首个单图文件, 则将其设置为pdf的第一张图, 否则添加到img_list中
                pdf = img_obj
                continue
            img_list.append(img_obj)
        if pdf:
            # 将 img_list 添加到 pdf
            sys.stdout.write(f"\r[ 正在处理 {pdf_basename} ]  [ 内存占用 {memory_footprint} MB ]  [ 正在合成pdf文件 {pdf_basename} ]")
            pdf.save(os.path.join(_root, pdf_basename), 'pdf', save_all=True, append_images=img_list, quality=quality)
            sys.stdout.write(
                f"\r[ 处理完毕 {pdf_basename} ]  [ 消耗内存 {memory_footprint} MB ]  [ 根目录 {_root} ]  [ 图片列表 {img_basename_dict} ]\n")
            return True
        else:
            return False

    SUFFIX = [".jpg", ".JPG", ".png", ".PNG", ".jpeg", ".JPEG", ".webp", ".WEBP"]  # 需要处理的文件类型
    # pdf 创建宽度标准的方法映射
    get_width_callback_mapping = {
        "error": _generate_pdf_get_mode,  # 入参异常所调用的方法
        "mode": _generate_pdf_get_mode,  # 向最多相同宽度图片的宽度对齐(众数)
        "max": max,  # 向最宽图片的宽度对齐
    }
    # RGB(A)通道映射
    channel_mapping = {
        "JPE": "RGB",
        "JPEG": "RGB",
        "JPG": "RGB",
        "PNG": "RGBA",
    }
    # 根据map查询到需要调用的方法
    get_width_callback = get_width_callback_mapping[get_width_func] if get_width_func in get_width_callback_mapping else \
        get_width_callback_mapping["error"]

    # 开始处理文件
    for root, dirs, files in os.walk(root_dir):
        gc.collect()  # 清理内存
        processing_file_list = [file for file in files if os.path.splitext(file)[-1] in SUFFIX]
        if processing_file_list:  # 当前目录下有需要执行的文件
            # 调用_inner函数, 创建一个内部的作用域, 方便清理内存, 防止内存溢出
            _generate_pdf_internal_func(root, processing_file_list, get_width_callback)
    return True


def include_sort(string_list: list, reverse=True) -> list:
    """
    document: 本函数功能为将输入的字符串列表按照包含关系进行排序
    param string_list: 字符串列表
    return: 照包含关系进行排序的结果
    example: include_sort(["早", "早上好", "早上", "你好", "好"])
    """
    element_list = []  # 用于存储 element_dict 字典的列表

    for element in string_list:
        element_dict = {"value": element, "level": 1}  # value 为字符串内容, level为该字符串的包含等级: 1级为最低->不包含...
        for other in [_ele for _ele in string_list if _ele != element]:  # 遍历old_list 除了当前 element 的 对象
            if other in element:
                element_dict["level"] += 1  # 如果被包含, 则包含等级 level 自增
        element_list.append(element_dict)  # 将结果添加到 element_list

    # 对element_list 按照 element_dict的 level进行排序
    element_list.sort(key=lambda _element_dict: (_element_dict['level']), reverse=reverse)
    # 排序结果转换为列表
    res_list = [_element_dict["value"] for _element_dict in element_list]
    return res_list  # 返回列表结果

def dec_to_alphanumeric(number):
    """
    document: 本函数用于数字转字母, 实现效果如下:
    1 - A; 2 - B; 4 - C; 4 - D
    param number: 需要被转换的数字
    return: 转换后的字母
    example: dec_to_alphanumeric(1)  return A
    """
    base26 = []
    while number > 0:
        number, remainder = divmod(number, 26)
        if remainder == 0:
            base26.append('Z')
            number -= 1
        else:
            base26.append(chr(remainder - 1 + 65))
    base26 = base26[::-1]
    return ''.join(base26)


def get_file_type(file_path: str) -> list:
    """
    document: 本函数功能为从文件头标识判断获取指定文件的格式
    param file_path: 指定文件路径
    return: 可能符合文件类型的后缀列表
    example: get_file_type(r"E:\example.zip")
    """
    file_header_mapping = {
        '00 00 00 18 66 74 79 70 33 67 70 35': ['MP4'],
        '00 00 00 20 66 74 79 70 4D 34 41 20 00 00 00 00': ['M4A', 'M4A', 'M4V'],
        '00 00 00 nn 66 74 79 70 33 67 70': ['3GG', '3GP', '3G2'],
        '00 00 01': ['MPA'],
        '00 00 01 00': ['SPL'],
        '00 00 01 00 00': ['ICO'],
        '00 00 01 00 01 00 20 20': ['ICO'],
        '00 00 01 B3': ['mpg', 'mpeg'],
        '00 00 01 BA': ['mpg', 'vob'],
        '00 00 02': ['TAG', 'TGA'],
        '00 00 02 00': ['wb2'],
        '00 00 02 00 00': ['tga'],
        '00 00 02 00 01 00 20 20': ['CUR'],
        '00 00 02 00 06 04 06 00 08 00 00 00 00 00': ['wk1'],
        '00 00 07': ['PJT'],
        '00 00 0F': ['MOV'],
        '00 00 10 00 00': ['tga'],
        '00 00 1A 00 00 10 04 00': ['wk3'],
        '00 00 1A 00 02 10 04 00': ['wk4', 'wk5'],
        '00 00 1A 00 05 10 04': ['123'],
        '00 00 1A 00 07 80 01 00': ['fm3'],
        '00 00 49 49 58 50 52': ['qxd'],
        '00 00 4D 4D 58 50 52': ['qxd'],
        '00 00 77': ['MOV'],
        '00 01 00': ['DDB', 'TST', 'TTF'],
        '00 01 00 00 4D 53 49 53 41 4D 20 44 61 74 61 62 61 73 65': ['MNY'],
        '00 01 00 00 53 74 61 6E 64 61 72 64 20 41 43 45 20 44 42': ['ACCDB'],
        '00 01 00 00 53 74 61 6E 64 61 72 64 20 4A 65 74 20 44 42': ['MDB'],
        '00 01 00 08 00 01 00 01 01': ['IMG'],
        '00 01 01': ['FLT'],
        '00 01 42 41': ['ABA'],
        '00 01 42 44': ['DBA'],
        '00 06 15 61 00 00 00 02 00 00 04 D2 00 00 10 00': ['db'],
        '00 11 AF': ['fli'],
        '00 1E 84 90 00 00 00 00': ['snm'],
        '00 50 01': ['XMV'],
        '00 5C 41 B1 FF': ['enc'],
        '00 BF': ['sol'],
        '00 FF FF': ['IMG', 'MDF', 'SMD'],
        '00 FF FF FF FF FF FF FF FF FF FF 00 00 02 00 01': ['mdf'],
        '01 00 00 00 01': ['pic'],
        '01 00 00 00 58 00 00 00': ['emf'],
        '01 00 09 00': ['wmf'],
        '01 00 09 00 00 03': ['wmf'],
        '01 0F 00 00': ['mdf'],
        '01 10': ['tr1'],
        '01 DA 01 01 00 03': ['rgb'],
        '01 FF 02 04 03 02': ['drw'],
        '02 00 09 00': ['wmf'],
        '02 64 73 73': ['dss'],
        '03': ['dat', 'db3'],
        '03 00 00 00': ['qph'],
        '03 00 00 00 41 50 50 52': ['adx'],
        '03 00 00 00 C4 66 C4 56': ['evt'],
        '04': ['db4'],
        '06 05 00': ['RAW'],
        '07': ['drw'],
        '07 64 74 32 64 64 74 64': ['dtd'],
        '08': ['db'],
        '09 02 06 00 00 00 10 00 B9 04 5C 00': ['xls'],
        '09 04 06 00 00 00 10 00 F6 05 5C 00': ['xls'],
        '0A 05 01': ['PCS'],
        '0A 05 01 08': ['pcx'],
        '0A nn 01 01': ['pcx'],
        '0C ED': ['mp'],
        '0D 44 4F 43': ['doc'],
        '0E 4E 65 72 6F 49 53 4F': ['nri'],
        '0E 57 4B 53': ['wks'],
        '11 00 00 00 53 43 43 41': ['pf'],
        '12 34 56 78 90 FF': ['doc'],
        '17 A1 50': ['PCB'],
        '1A 00 00': ['ntf'],
        '1A 00 00 03 00 00': ['nsf', 'ntf'],
        '1A 00 00 03 00 00 11 00': ['nsf'],
        '1A 00 00 04 00 00': ['nsf'],
        '1A 0B': ['pak'],
        '1A 0x': ['arc'],
        '1A 35 01 00': ['eth'],
        '1A 45 DF A3 93 42 82 88 6D 61 74 72 6F 73 6B 61': ['mkv'],
        '1A 52 54 53 20 43 4F 4D 50 52 45 53 53 45 44 20 49 4D 41 47 45 20 56 31 2E 30 1A': ['dat'],
        '1D 7D': ['ws'],
        '1F 8B': ['gz', 'TAR', 'tgz'],
        '1F 8B 08': ['gz', 'tgz'],
        '1F 9D': ['Z'],
        '1F 9D 8C': ['Z'],
        '1F 9D 90': ['TAR.Z'],
        '20 00 60 40 60': ['wk1', 'wks'],
        '20 00 68 00 20 0': ['fmt'],
        '20 20 20': ['BAS'],
        '21 12': ['ain'],
        '21 3C 61 72 63 68 3E 0A': ['lib'],
        '21 42 44 4E': ['pst'],
        '23 20': ['msi'],
        '23 20 4D 69 63 72 6F 73 6F 66 74 20 44 65 76 6 56C 6F 70 65 72 20 53 74 75 64 69 6F': ['dsp'],
        '23 21 41 4D 52': ['amr'],
        '23 3F 52 41 44 49 41 4E 43 45 0A': ['hdr'],
        '23 44 45': ['PRG'],
        '23 45 58': ['m3u'],
        '24 46 4C 32 40 28 23 29 20 53 50 53 53 20 44 41 54 41 20 46 49 4C 45': ['sav'],
        '24 53 6F': ['PLL'],
        '25 21 50 53': ['eps'],
        '25 21 50 53 2D 41 64 6F 62 65': ['eps', 'ps'],
        '25 21 50 53 2D 41 64 6F 62 65 2D 33 2E 30 20 45 50 53 46 2D 33 20 30': ['eps'],
        '25 50 44': ['PDF'],
        '25 50 44 46': ['PDF', 'fdf'],
        '25 50 44 46 2D 31 2E': ['PDF'],
        '28 54 68 69 73 20 66 69 6C 65': ['hqx'],
        '28 54 68 69 73 20 66 69 6C 65 20 6D 75 73 74 20 62 65 20 63 6F 6E 76 65 72 74 65 64 20 77 69 74 68 20 42 69 6E 48 65 78 20': [
            'hqx'],
        '2A 24 20': ['LIB'],
        '2A 2A 2A 20 20 49 6E 73 74 61 6C 6C 61 74 69 6F 6E 20 53 74 61 72 74 65 64 20': ['log'],
        '2A 50 52': ['ECO'],
        '2A 76 65': ['SCH'],
        '2D 6C 68 35 2D': ['lha'],
        '2E 52 45 43': ['ivr'],
        '2E 52 4D': ['RM'],
        '2E 52 4D 46': ['rm', 'rmvb'],
        '2E 52 4D 46 00 00 00 12 00': ['ra'],
        '2E 72 61 FD': ['RA', 'RAM'],
        '2E 72 61 FD 00': ['RA'],
        '2E 73 6E 64': ['AU'],
        '30': ['CAT'],
        '30 00 00 00 4C 66 4C 65': ['evt'],
        '30 26 B2': ['WMA', 'WMV'],
        '30 26 B2 75 8E 66 CF 11': ['asf'],
        '30 26 B2 75 8E 66 CF 11 A6 D9 00 AA 00 62 CE 6C': ['asf', 'wma', 'wmv'],
        '30 31 4F 52 44 4E 41 4E 43 45 20 53 55 52 56 45 59 20 20 20 20 20 20 20': ['ntf'],
        '30 37 30 37 30 37': ['TAR', 'cpio'],
        '31 BE': ['wri'],
        '31 BE 00': ['WRI'],
        '31 BE 00 00 00 AB 00 00': ['doc'],
        '32 BE': ['wri'],
        '37 7A BC AF 27 1C': ['7z'],
        '38 42 50': ['PSD'],
        '38 42 50 53': ['psd'],
        '3A 42 61 73 65': ['cnt'],
        '3A 56 45 52 53 49 4F 4E': ['sle'],
        '3A DE 68 B1': ['dcx'],
        '3C': ['ASX', 'XDR'],
        '3C 21 44': ['HTM'],
        '3C 21 44 4F 43 54': ['htm', 'html'],
        '3C 21 45 4E 54 49 54 59': ['dtd'],
        '3C 21 64 6F 63 74 79 70': ['dci'],
        '3C 3F 78': ['MSC', 'XML'],
        '3C 3F 78 6D 6C': ['xml'],
        '3C 3F 78 6D 6C 20 76 65 72 73 69 6F 6E 3D': ['manifest'],
        '3C 3F 78 6D 6C 20 76 65 72 73 69 6F 6E 3D 22 31 2E 30 22 3F 3E 0D 0A 3C 4D 4D 43 5F 43 6F 6E 73 6F 6C 65 46 69 6C 65 20 43 6F 6E 73 6F 6C 65 56 65 72 73 69 6F 6E 3D 22': [
            'msc'],
        '3C 48 54 4D 4C 3E': ['htm', 'html'],
        '3C 4D 61 6B 65 72 46 69 6C 65 20': ['fm'],
        '3C 68 74 6D 6C 3E': ['htm', 'html'],
        '3F 5F 03': ['HLP', 'LHP'],
        '3F 5F 03 00': ['gid', 'hlp', 'lhp'],
        '41 43 31': ['dwg'],
        '41 43 31 30': ['dwg'],
        '41 43 76': ['SLE'],
        '41 4D 59 4F': ['SYW'],
        '41 4F 4C 20 46 65 65 64 62 61 67': ['BAG'],
        '41 4F 4C 44 42': ['ABY', 'IDX'],
        '41 4F 4C 49 44 58': ['IND'],
        '41 4F 4C 49 4E 44 45 58': ['ABI'],
        '41 4F 4C 56 4D 31 30 30': ['ORG', 'PFC'],
        '41 56 47 36 5F 49 6E 74 65 67 72 69 74 79 5F 44 61 74 61 62 61 73 65': ['DAT'],
        '41 56 49 20': ['AVI'],
        '41 72 43 01': ['ARC'],
        '42 45 47 49 4E 3A 56 43 41 52 44 0D 0A': ['vcf'],
        '42 49 4C': ['LDB'],
        '42 4C 49 32 32 33 51': ['bin'],
        '42 4D': ['bmp', 'dib'],
        '42 4D 3E': ['BMP'],
        '42 4F 4F 4B 4D 4F 42 49': ['prc'],
        '42 5A 68': ['BZ', 'BZ2', 'BZ2', 'TAR.BZ2', 'TBZ2', 'TB2'],
        '43 23 2B 44 A4 43 4D A5 48 64 72': ['RTD'],
        '43 42 46 49 4C 45': ['CBD'],
        '43 44 30 30 31': ['ISO'],
        '43 48 41': ['FNT'],
        '43 4D 58 31': ['CLB'],
        '43 4F 4D 2B': ['CLB'],
        '43 50 54 37 46 49 4C 45': ['CPT'],
        '43 50 54 46 49 4C 45': ['CPT'],
        '43 52 45 47': ['DAT'],
        '43 52 55 53 48': ['cru', 'crush'],
        '43 52 55 53 48 20 76': ['CRU'],
        '43 57 53': ['SWF'],
        '43 61 74 61 6C 6F 67 20 33 2E 30 30 00': ['CTF'],
        '43 6C 69 65 6E 74 20 55 72 6C 43 61 63 68 65 20 4D 4D 46 20 56 65 72 20': ['DAT'],
        '44 42 46 48': ['DB'],
        '44 4D 53 21': ['DMS'],
        '44 4F 53': ['ADF'],
        '44 56 44': ['DVR', 'IFO'],
        '44 65 6C 69 76 65 72 79 2D 64 61 74 65 3A': ['eml'],
        '45 4C 49 54 45 20 43 6F 6D 6D 61 6E 64 65 72 20': ['CDR'],
        '45 4E 54 52 59 56 43 44 02 00 00 01 02 00 18 58': ['VCD'],
        '45 50': ['MDI'],
        '45 52 46 53 53 41 56 45 44 41 54 41 46 49 4C 45': ['DAT'],
        '45 56 46': ['Enn (where nn are numbers)'],
        '45 6C 66 46 69 6C 65 00': ['EVTX'],
        '45 86 00 00 06 00': ['qbb'],
        '46 41 58 43 4F 56 45 52 2D 56 45 52': ['CPE'],
        '46 45 44 46': ['SBV'],
        '46 4C 56 01': ['FLV'],
        '46 4F 52 4D': ['IFF'],
        '46 4F 52 4D 00': ['AIFF'],
        '46 57 53': ['SWF'],
        '46 72 6F 6D 20 20 20': ['EML'],
        '46 72 6F 6D 20 3F 3F 3F': ['EML'],
        '46 72 6F 6D 3A 20': ['EML'],
        '47 46 31 50 41 54 43 48': ['PAT'],
        '47 49 46 38': ['GIF'],
        '47 49 46 38 37 61': ['gif'],
        '47 49 46 38 39 61': ['gif'],
        '47 50 41 54': ['PAT'],
        '47 58 32': ['GX2'],
        '48 48 02': ['PDG'],
        '48 48 47 42 31': ['SH3'],
        '49 20 49': ['TIF', 'TIFF'],
        '49 44 33': ['MP3'],
        '49 44 33 03 00 00 00': ['KOZ'],
        '49 49 1A 00 00 00 48 45 41 50 43 43 44 52 02 00': ['CRW'],
        '49 49 2A': ['TIF', 'TIFF'],
        '49 49 2A 00': ['TIF', 'TIFF'],
        '49 53 63': ['CAB'],
        '49 53 63 28': ['CAB', 'HDR'],
        '49 54 4F 4C 49 54 4C 53': ['LIT'],
        '49 54 53': ['CHM'],
        '49 54 53 46': ['CHI', 'CHM'],
        '49 6E 6E 6F 20 53 65 74 75 70 20 55 6E 69 6E 73 74 61 6C 6C 20 4C 6F 67 20 28 62 29': ['DAT'],
        '4A 41 52 43 53 00': ['JAR'],
        '4A 47 03 0E 00 00 00': ['ART'],
        '4A 47 04 0E 00 00 00': ['ART'],
        '4B 47 42 5F 61 72 63 68 20 2D': ['KGB'],
        '4B 49 00 00': ['SHD'],
        '4C 00 00': ['LNK'],
        '4C 00 00 00': ['LNK'],
        '4C 00 00 00 01 14 02': ['LNK'],
        '4C 00 00 00 01 14 02 00': ['LNK'],
        '4C 01': ['obj'],
        '4C 4E 02 00': ['GID', 'HLP'],
        '4D 41 52 31 00': ['MAR'],
        '4D 41 52 43': ['MAR'],
        '4D 41 72 30 00': ['MAR'],
        '4D 44 4D 50 93 A7': ['DMP', 'HDMP'],
        '4D 45 44': ['MDS'],
        '4D 47 58 20 69 74 70 64': ['ds4'],
        '4D 49 4C 45 53': ['MLS'],
        '4D 4C 53 57': ['MLS'],
        '4D 4D 00 2A': ['TIF', 'TIFF'],
        '4D 4D 00 2B': ['TIF', 'TIFF'],
        '4D 4D 2A': ['TIF', 'TIFF'],
        '4D 4D 4D 44 00 00': ['MMF'],
        '4D 53 43 46': ['CAB', 'PPZ', 'SNP'],
        '4D 53 46 54 02 00 01 00': ['TLB'],
        '4D 53 5F 56 4F 49 43 45': ['CDR, DVF', 'MSV'],
        '4D 54 68 64': ['MID', 'MIDI'],
        '4D 56': ['DSN'],
        '4D 56 32 31 34': ['MLS'],
        '4D 56 32 43': ['MLS'],
        '4D 5A': ['ACM', 'AX', 'COM', 'DLL', 'DRV', 'EXE', 'PIF', 'QTS', 'QTX', 'SYS', 'CPL', 'exe', 'dll', 'drv',
                  'vxd', 'sys', 'ocx', 'vbx', 'exe', 'dll', 'drv', 'vxd', 'sys', 'ocx', 'vbx', 'exe', 'com', '386',
                  'ax', 'acm', 'sys', 'dll', 'drv', 'flt', 'fon', 'ocx', 'scr', 'lrc', 'vxd', 'cpl', 'x32', 'FON',
                  'OCX', 'OLB', 'SCR', 'VBX', 'VXD, 386'],
        '4D 5A 16': ['DRV'],
        '4D 5A 50': ['DPL'],
        '4D 5A 90': ['DLL', 'EXE', 'DLL', 'OCX', 'OLB', 'IMM', 'IME', 'IME', 'IMM', 'OCX', 'OLB'],
        '4D 5A 90 00 03 00 00 00': ['API', 'AX', 'FLT'],
        '4D 5A EE': ['COM'],
        '4E 45 53': ['NES'],
        '50 4B 03': ['ZIP'],
        '50 4B 03 04': ['ZIP', 'JAR', 'ZIPX'],
        '50 4B 30 30': ['ZIP'],
        '50 4B 30 30 50 4B 03 04': ['ZIP'],
        '52 45 47 45 44 49 54 34': ['REG'],
        '52 49 46': ['WAV'],
        '52 49 46 46': ['ANI'],
        '52 61 72': ['RAR'],
        '52 61 72 21': ['RAR'],
        '52 65 63': ['EML', 'PPC'],
        '53 49 54 21': ['SIT'],
        '53 52 01 00': ['SLY', 'SRT', 'SLT'],
        '53 74 61 6E 64 61 72 64 20 4A': ['MDB', 'MDA', 'MDE', 'MDT'],
        '53 74 75 66 66 49 74': ['SIT'],
        '55 46 41': ['UFA'],
        '57 41 56 45': ['WAV'],
        '57 41 56 45 66 6D 74': ['WAV'],
        '57 6F 72 64 50 72 6F': ['LWP'],
        '58 42 45': ['XBE'],
        '5A 4F 4F 20': ['ZOO'],
        '5B 41 44': ['PBK'],
        '5B 43 6C': ['CCD'],
        '5B 57 69': ['CPX'],
        '5B 76 65 72 5D': ['AMI'],
        '5F 27 A8 89': ['JAR'],
        '60 EA': ['ARJ'],
        '60 EA 27': ['ARJ'],
        '68 74 6D 6C 3E': ['HTML'],
        '6D 64 61 74': ['MOV', 'QT'],
        '6D 6F 6F 76': ['MOV'],
        '72 73 69 6F 6E 3D 22 31 3C 3F 78 6D 6C 20 76 65 2E 30 22 3F 3E': ['XUL'],
        '7B 50 72': ['GTD'],
        '7B 5C 72': ['RTF'],
        '7B 5C 72 74 66': ['RTF'],
        '7E 42 4B 00': ['PSP'],
        '7F 45 4C 46 01 01 01 00': ['ELF'],
        '7F FE 34 0A': ['DOC'],
        '80 53 43': ['SCM'],
        '87 F5 3E': ['GBC'],
        '89 50 4E': ['PNG'],
        '89 50 4E 47': ['PNG'],
        '89 50 4E 47 0D 0A': ['PNG'],
        '89 50 4E 47 0D 0A 1A 0A': ['PNG'],
        '91 33 48 46': ['HAP'],
        'AC 9E BD 8F': ['QDF'],
        'C2 20 20': ['NLS'],
        'C5 D0 D3': ['EPS'],
        'CDR': ['CDR'],
        'CF AD 12 FE': ['DBX'],
        'CF AD 12 FE C5 FD 74 6F': ['DBX'],
        'D0 CF 11': ['MAX', 'PPT', 'XLS'],
        'D0 CF 11 E0': ['DOT', 'PPT', 'XLA', 'PPA', 'PPS', 'POT', 'MSI', 'SDW', 'DB', 'XLS'],
        'D0 CF 11 E0 A1 B1 1A E1': ['DOC', 'DOT', 'XLS', 'XLT', 'XLA', 'PPT', 'APR', 'PPA', 'PPS', 'POT', 'MSI', 'SDW',
                                    'DB'],
        'D7 CD C6 9A': ['WMF'],
        'E3 82 85 96': ['PWL'],
        'E9 3B 03': ['COM'],
        'ED AB EE DB': ['RPM'],
        'FF 57 50 43': ['WP', 'WPD'],
        'FF 57 50 47': ['WPG'],
        'FF D8 FF': ['JPG', 'JPEG'],
        'FF D8 FF E0 00': ['JPG', 'JPE', 'JPEG'],
        'FF D8 FF FE 00': ['JPG', 'JPE', 'JPEG'],
        'FF FB 50': ['MP3'],
        'FF FE 3C': ['XSL'],
        'FF FE 3C 00 52 00 4F 00 4F 00 54 00 53 00 54 00 55 00 42 00': ['XML'],
        'FF FF FF': ['SUB'],
        # '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00': ['pdb'],  # 11 byte offset
        # '2D 6C 68': ['lha', 'lzh'],  # 2 byte offset
        # '3E 00 03 00 FE FF 09 00 06': ['wb3'],  #24 byte offset
        # '40 40 40 20 00 00 40 40 40 40': ['enl'],  # 32 byte offset
        # '00 6E 1E F0': ['ppt'],  # 512 byte offset
        # '09 08 10 00 00 06 05 00': ['xls'],  # 512 byte offset
        # '0F 00 E8 03': ['ppt'],  # 512 byte offset
        # '00 00 FF FF FF FF': ['hlp'],  # 7 byte offset
        'calc': ['SXC'],
        'draw': ['SXD'],
        'impress': ['SXI'],
        'lh': ['LZH'],
        'math': ['SXM'],
        'writer': ['SXW'],
    }
    with open(file_path, 'rb') as f:
        bins = f.read(30)  # 读取文件头前20位
    hex_str = u""  # 十六进制
    for b in bins:
        hexadecimal = hex(b)[2:]  # 十进制转十六进制, 去掉前面的0x
        if len(hexadecimal) % 2:
            hexadecimal = u"0" + hexadecimal
        hex_str += " " + hexadecimal  # 拼接十六进制字符串
    bins = hex_str.upper().strip()  # 字母转为大写 如:"50 4B 03 04 14 00 00 00 00 00 29 5A FA 56 00 00 00 00 00 00"

    file_type = []
    for header_code in file_header_mapping.keys():
        lens = len(header_code)  # 需要的长度
        if bins[0:lens] == header_code:
            file_type += file_header_mapping[header_code]
            # break

    # file_type = get_mode(file_type) if file_type else ["unknown"]
    file_type = list(set(file_type)) if file_type else ["unknown"]
    return file_type


# def tet(input_image_path, output_image_path):
#     from PIL import Image
#     image = Image.open(input_image_path).convert("RGBA")  # 用 RGBA 通道格式打开图片，并将其转换为PIL图像对象
#     width, height = image.size  # 获取图像的宽度和高度
#
#     transparent_image = Image.new("RGBA", (width, height))  # 创建一个 RGBA 通道的新图片
#     # 遍历图像的每个像素
#     for x in range(width):
#         for y in range(height):
#             r, g, b, a = image.getpixel((x, y))  # 获取input图片的像素的 RGB 值
#
#             up_xy = (x, y - 1) if y-1 >= 0 else (x, y)
#             down_xy = (x, y + 1) if y+1 < height else (x, y)
#             left_xy = (x-1, y) if x-1 >= 0 else (x, y)
#             right_xy = (x+1, y) if x+1 < width else (x, y)
#
#             aa_xy = (x-1, y-1) if x-1 >= 0 and y-1 >= 0 else (x, y)
#             bb_xy = (x+1, y-1) if x+1 < width and y-1 >= 0 else (x, y)
#             cc_xy = (x-1, y+1) if x-1 >= 0 and y+1 < height else (x, y)
#             dd_xy = (x+1, y+1) if x+1 < width and y+1 < height else (x, y)
#
#             try:
#                 up = image.getpixel(up_xy)
#                 down = image.getpixel(down_xy)
#                 left = image.getpixel(left_xy)
#                 right = image.getpixel(right_xy)
#                 aa = image.getpixel(aa_xy)
#                 bb = image.getpixel(bb_xy)
#                 cc = image.getpixel(cc_xy)
#                 dd = image.getpixel(dd_xy)
#
#             except Exception as e:
#                 print(width, height, up_xy, down_xy, left_xy, right_xy)
#                 raise e
#
#             # print(up, down, left, right, r)
#             has = 0
#             new_c = [0,0,0,0]
#             if aa[3]!=0:
#                 has += 1
#                 for _ in range(4):
#                     new_c[_] += up[_]
#             if bb[3]!=0:
#                 has += 1
#                 for _ in range(4):
#                     new_c[_] += up[_]
#             if cc[3]!=0:
#                 has += 1
#                 for _ in range(4):
#                     new_c[_] += up[_]
#             if dd[3]!=0:
#                 has += 1
#                 for _ in range(4):
#                     new_c[_] += up[_]
#
#
#             # if not (up[0]==up[1] and up[1]==up[2] and up[2]==255):
#             if up[3]!=0:
#                 has += 1
#                 for _ in range(4):
#                     new_c[_] += up[_]
#             # if not (down[0] == down[1] and down[1] == down[2] and down[2] == 255):
#             if down[3]!=0:
#                 has += 1
#                 for _ in range(4):
#                     new_c[_] += up[_]
#             # if not (left[0] == left[1] and left[1] == left[2] and left[2] == 255):
#             if left[3]!=0:
#                 has += 1
#                 for _ in range(4):
#                     new_c[_] += up[_]
#             # if not (right[0] == right[1] and right[1] == right[2] and right[2] == 255):
#             if right[3]!=0:
#                 has += 1
#                 for _ in range(4):
#                     new_c[_] += up[_]
#             # print(has)
#             # print(has, a, x, y)
#             if has>=5 and a==0:
#
#                 for _ in range(4):
#                     new_c[_] = int(new_c[_] / has)
#                 new_c = tuple(new_c)
#                 print("同", has, a, new_c, x, y)
#                 transparent_image.putpixel((x, y), new_c)
#             elif has<=4 and a!=0:
#                 print("删", has, a, (0, 0, 0, 0), x, y)
#                 transparent_image.putpixel((x, y), (0, 0, 0, 0))
#             else:
#                 # print("")
#                 transparent_image.putpixel((x, y), (r, g, b, a))  # 将非目标颜色的像素保持不变
#
#     transparent_image.save(output_image_path)  # 保存处理后的图像到文件
#     return True


def image_replace_color(input_image_path, output_image_path, old_color=(228, 228, 228), new_color=(255, 255, 255),
                        new_alpha=255):
    """
    document: 本函数功能为将将图片的某种颜色像素替换为其他颜色(支持改变透明通道)
    param input_image_path: 原图片文件路径
    param output_image_path: 新创建图片文件路径
    param old_color: 需要被替换掉的像素的 RGB 值
    param new_color: 用于替换的 RGB 值
    param new_alpha: 用于替换的 Alpha通道值
    return: True
    example: image_replace_color(r"D:\example\example_1.png", r"D:\example\example_2.png")
    """
    from PIL import Image
    image = Image.open(input_image_path).convert("RGBA")  # 用 RGBA 通道格式打开图片，并将其转换为PIL图像对象
    width, height = image.size  # 获取图像的宽度和高度

    transparent_image = Image.new("RGBA", (width, height))  # 创建一个 RGBA 通道的新图片
    # 遍历图像的每个像素
    for x in range(width):
        for y in range(height):
            r, g, b, a = image.getpixel((x, y))  # 获取input图片的像素的 RGB 值
            if (r, g, b) == old_color:  # 需要替换的目标像素
                new_alpha = new_alpha  # 255 - g
                transparent_image.putpixel((x, y), (*new_color, new_alpha))  # 将目标颜色的像素变成 (*new_color, new_alpha)
            else:
                # r = int(r * (1 + (1.8*r + 20) / 255) - 0.2*r + 15)
                # g = int(g * (1 + (1.8*g + 20) / 255) - 0.2*r + 15)
                # b = int(b * (1 + (1.8*b + 20) / 255) - 0.2*r + 15)
                transparent_image.putpixel((x, y), (r, g, b, a))  # 将非目标颜色的像素保持不变

    transparent_image.save(output_image_path)  # 保存处理后的图像到文件
    return True


def set_signature(document_path: str, image_path: str, key_word: str, output_path: str, pos: tuple, size: tuple):
    """
    document: 本函数功能为将图片作为背景插入word文档的执行段落位置
    param document_path: 待处理word文件的路径
    param image_path: 签章图片的文件的路径
    param key_word: 签章段落中包含的关键字
    param output_path: 处理之后word文件的输出路径
    param pos: 签章在段落中的坐标
    param size:  签章大小
    return: True
    example: set_signature(r"D:\example\example.doc", r"D:\example\example.png", “此处盖章”, r"D:\example\example.doc", (-50, 200), (124, 124))
    """
    from spire.doc import TextWrappingStyle, Document, FileFormat
    # 加载Word文档
    document = Document()  # 创建一个Document对象
    document.LoadFromFile(document_path)
    # 查询段落
    selections = document.FindAllString(key_word, False, False)
    for selection in selections:
        selection = selection.GetAsRange()[0].OwnerParagraph  # 定位到每一段

        picture = selection.AppendPicture(image_path)  # 在段落中插入图片
        picture.TextWrappingStyle = TextWrappingStyle.Behind  # 设置图片在文字下方

        picture.HorizontalPosition = pos[0]  # 设置图片水平位置
        picture.VerticalPosition = pos[1]  # 设置图片垂直位置

        picture.Height = size[0]  # 改变印章尺寸, 高度
        picture.Width = size[1]  # 改变印章尺寸, 宽度

    # 保存document
    document.SaveToFile(output_path, FileFormat.Docx)
    document.Close()
    return True


def export_psd(psd_path, output_png_path):
    """
    将 psd 文件的可见图层导出为 png
    param psd_path: psd 文件路径
    param output_png_path: png 文件输出路径
    return: True/ False
    example: export_psd(psd_path, png_path)
    """
    import psd_tools  # install psd-tools
    import os
    try:
        psd = psd_tools.PSDImage.open(psd_path)  # 加载PSD文件
        composite = psd.composite()  # 合成所有图层
        composite.save(output_png_path)  # 保存合成图像
    except Exception:
        if os.path.exists(output_png_path):
            os.remove(output_png_path)
        return False
    return True


def calculate_image_similarity(image1_path, image2_path, similarity=0.85):
    """
    对比两张图片的相似度, 返回是否相似(True/ False)
    :param image1_path: 需要比对的图片 1
    :param image2_path: 需要比对的图片 1
    :param similarity: 相似度标准, 默认值为0.9, 当高于此默认值, 则返回 Ture, 否则返回 False
    :return: 是否相似, 当高于similarity, 则返回 Ture, 否则返回 False
    example: similarity = calculate_image_similarity(d_path, e_path)
    """
    from PIL import Image
    import imagehash
    is_similar = False
    result_similarity = 0
    try:
        # 打开图片, 转换为灰度图
        image1 = Image.open(image1_path).convert('L')
        image2 = Image.open(image2_path).convert('L')
        # 计算两张图的哈希值
        phash_1, phash_2 = imagehash.phash(image1), imagehash.phash(image2)  # 感知哈希 ,不同于aHash, 但首先它确实是离散余弦变换和频域
        whash_1, whash_2 = imagehash.whash(image1), imagehash.whash(image2)  # 小波散列, 几天前我把它添加到库里, 它的工作原理在频域中作为pHash但它使用DWT代替DCT变换
        dhash_1, dhash_2 = imagehash.dhash(image1), imagehash.dhash(image2)  # 梯度散列, 计算每个像素的差值, 并与平均差异的差异进行比较。
        ahash_1, ahash_2 = imagehash.average_hash(image1), imagehash.average_hash(image2)  # 平均散列, 对于每个像素输出1, 如果该像素是大于或等于平均值, 否则为0
        # 计算相似度
        p_similarity = 1 - (phash_1 - phash_2) / len(phash_1.hash) ** 2
        w_similarity = 1 - (whash_1 - whash_2) / len(whash_1.hash) ** 2
        d_similarity = 1 - (dhash_1 - dhash_2) / len(dhash_1.hash) ** 2
        a_similarity = 1 - (ahash_1 - ahash_2) / len(ahash_1.hash) ** 2
        result_similarity = (p_similarity + w_similarity + d_similarity + a_similarity) / 4  # 综合相似度
        # 判断是否相似
        if result_similarity > similarity:
            is_similar = True
    except Exception:
        pass
    return is_similar, result_similarity


# def is_mosaic(image_path, threshold=0.9):
#     from PIL import Image
#     image = Image.open(image_path)
#     pixels = image.load()
#     max_count = threshold * image.size[0] * image.size[1]
#     unique_colors = set()
#     for x in range(image.size[0]):
#         for y in range(image.size[1]):
#             color = pixels[x, y]
#             if len(unique_colors) < max_count:
#                 unique_colors.add(color)
#             else:
#                 if color not in unique_colors:
#                     return True
#     return False
#
# # 使用示例
# image_path = r'E:\@#\Entertainment - movie& readingMatter& music& game\Illustration - mine\[000] exquisite\[DAGASI]96e21e47-db66-4bda-b093-8358a0b78599.png'
# print(is_mosaic(image_path))


if __name__ == "__main__":
    # for i in range(10):
    #     tet(rf"C:\Users\Administrator\Desktop\11\{i}.png", rf"C:\Users\Administrator\Desktop\11\{i+1}.png")

    # old_color = (245, 243, 241)
    # new_color = (255, 255, 255)
    # new_alpha = 255
    # image_replace_color(r"C:\Users\Administrator\Desktop\10000号\WORREP_02.png", r"C:\Users\Administrator\Desktop\10000号\WORREP_03.png", old_color=old_color, new_color=new_color, new_alpha=new_alpha)
    exit()
    """
    this is running function
    
    For the convenience of understanding and searching, function names will be named in Chinese
    """

    def unzip_delete_package(_base_path, _display_suffix):
        """ 解压 base_path 下所有子目录的 zip压缩包 到子目录下, 并删除 zip 压缩包 """
        import os
        # 解压文件夹下的 zip 压缩包, 并删除该文件
        get_suffix(_base_path, display_suffix=_display_suffix)
        for root, dirs, files in os.walk(_base_path):
            for file in files:
                suffix = file.split(".")[-1]
                if suffix in ["zip", "ZIP"]:
                    print(f"{os.path.join(root, file)}  -  -  -  -  -  - > > >  {root}")
                    try:
                        unpack_zip(os.path.join(root, file), root)
                        os.remove(os.path.join(root, file))
                    except Exception as e:
                        print(e)

    base_path = r"E:\nsfw-processed\illustration\[200] [Tama]"
    display_suffix = ["7z", "7Z", "zip", "ZIP", "rar", "RAR"]
    # unzip_delete_package(base_path, display_suffix)
    # exit()

    def export_psd_delete_similar_image(_base_path, _display_suffix):
        """
        对 base_path 下的所有子目录, 如果有psd文件存在, 则导出该文件的png格式tmp.png
        使用 tmp.png 对比该子目录下的其他所有的 image, 如果相似度高于0.9, 则删除 image, 对比完所有 image 后删除 tmp.png
        """
        import os
        import time
        get_suffix(_base_path, display_suffix=_display_suffix)
        for root, dirs, files in os.walk(_base_path):
            for file_p in files:
                psd_suffix = file_p.split(".")[-1]
                if psd_suffix in ["psd", "PSD", "psb", "PSB"]:
                    psd_path = os.path.join(root, file_p)
                    png_path = psd_path + f".temp_{str(time.time()).replace('.', '')}.png"
                    is_export = export_psd(psd_path, png_path)
                    if not is_export:
                        continue
                    print(f"创建{png_path}")
                    for file_i in files:
                        image_suffix = file_i.split(".")[-1]
                        if image_suffix in ["png", "PNG", "jpg", "JPG", "jpeg", "JPEG"]:
                            is_similar = calculate_image_similarity(os.path.join(root, file_i), png_path)

                            if is_similar[0]:
                                os.remove(os.path.join(root, file_i))
                                print(f"> > > > > >删除{os.path.join(root, file_i)} ---------- {is_similar[1]}")
                    # os.remove(png_path)
                    # print(f"删除{png_path}")

    base_path = r"E:\nsfw-processed\illustration\[300] [Mitsu]\[2020-11-01] Term34\T034_t02_PSD"
    display_suffix = ["psd", "PSD", "psb", "PSB"]
    # export_psd_delete_similar_image(base_path, display_suffix)

    # generate_pdf(r"F:\#[09] download\整理")

    # print("栰奜業弌僗僀乕僷乕".encode(encoding="GBK").decode(encoding="Shift_JIS", errors="ignore"))
    # recode_text(r"G:\nsfw-processing\game-3.0\[MountBatten] ドリス姫と夜のオツトメ_zh_1.06\updete_history.txt")

    # old_color = (132, 175, 109)
    # new_color = (255, 255, 255)
    # new_alpha = 0
    # image_replace_color(r"F:\@#\Private\Devise\玛卡兰迪亚\处理2.png", r"F:\@#\Private\Devise\玛卡兰迪亚\处理3.png", old_color=old_color, new_color=new_color, new_alpha=new_alpha)
    pass

    # export_psd(r"E:\test\[artist] [1=2]\[2023-08-01]\20230816Bpsd.psd", r"E:\test\[artist] [1=2]\[2023-08-01]\20230816Bpsd.png")
    # print(calculate_image_similarity(r"E:\test\[artist] [1=2]\[2023-08-01]\20230816A1.png", r"E:\test\[artist] [1=2]\[2023-08-01]\20230816Bpsd.png"))

