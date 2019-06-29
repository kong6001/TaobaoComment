import requests

headers = {
    "Host": 'rate.tmall.com',
"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
"Accept": '*/*',
"Accept-Language": 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
"Accept-Encoding": 'gzip, deflate, br',
"Referer": 'https://detail.tmall.com/item.htm?spm=a230r.1.14.224.47ba156bKdnWi1&id=566421673470&ns=1&abbucket=12',
"Connection": 'keep-alive',
"Cookie": 'cna=VSwoEy9S4joCAXAKVA0fo5Yn; isg=BHh4m9uRUCBQNrr-XGRBw3FySibKSd11kAJpLLLpnrNpzRq3W_M3-yQrhQVYhpRD; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; lid=myrgood; enc=spaD6yoVBxkDdwyPf1aSIWLsVbdHGiQS1yzhJsKqOjE4Ibnzo0JGDAltEqD%2FDcfeo0Mak%2BT7WKHhO4jpImKdDg%3D%3D; um=2BA477700510A7DF4B6C155E52F9BD26552C31997FB56304A2BC4871DC27CA70900658A7ACFF8F8FCD43AD3E795C914CFEC440E461D6DB38BBCD29DF5BA4390C; OZ_1U_2061=vid=vb9deefda248b1.0&ctime=1537076988&ltime=0; l=bBjEIVcnv6CGVOf6KOCwCuI8Lq_TLIO4YuPRwCXwi_5C1_KLWZ7OlFV5TEp6Vs5POfTp4KXJ7LpT2FFLJyaf.; _m_h5_tk=55604bccc00ed2c1a12cea8404316df8_1560009535831; _m_h5_tk_enc=d01bcfabfb2006ab6eb9869e143ccab4; x=__ll%3D-1%26_ato%3D0; t=2150bc9b756be7147858039a105889c7; _tb_token_=53551b66841ae; cookie2=55eceab93c2609c03121e01205debb04; dnk=myrgood; csg=5b526091; whl=-1%260%260%260; skt=87d3f6803b149d09; hng=CN%7Czh-CN%7CCNY%7C156'
}

url = "https://rate.tmall.com/list_detail_rate.htm?itemId=566421673470&spuId=946472412&sellerId=2943953365&order=3&currentPage=1&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098"
byte = requests.get(url, headers=headers,
                    timeout=10)
string = byte._content.decode('UTF-8')


