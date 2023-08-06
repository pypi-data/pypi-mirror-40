from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "SpiderControl_commoms",      #这里是pip项目发布的名称
    version = "1.0.0",  #版本号，数值大的会优先被pip
    keywords = ["pip", "SpiderControl_commoms","featureextraction"],
    description = "suitang python spiders control",
    long_description = "",
    license = "",

    url = "https://github.com/KokoXin/SpiderControl_commoms.git",     #项目相关文件地址，一般是github
    author = "KokoXin",
    author_email = "541883569@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["pymysql"]          #这个项目需要的第三方库
)