# itemid = '540622763937'  # 184
# itemid = '547752478009'  # 1922
# itemid = '545828211529'  # 10567,只能爬到5000条,原因不明
# itemid='558760911386'#手机
# itemid = '564439093146'#女装
# itemid='532558514838'#洗衣机
# itemid = '531815202400'  # 鞋
# itemid='43355921321'#辣条
# itemid = '569368595929'  #洗发水
# itemid = '574357375991'  #萨克斯 21页
# itemid = '551237284670'#保温杯 25页

# itemid = '567423250312'
#itemid = '558509313522'
#itemid = '558964631148'

#itemid = '570133905140'
itemid = '558509313522'
file_path = 'D:/taobao_comments/'

itemid_list = {
    '575984231019',
    '578318605036',
    '578153420589',
    '569705565098',
    '562099309982',
    '579794586729',
    '579484379629',
    '570133905140',
    '578409039288',
    '577383278492',
    '570277442121',
    '566603286049',
    '567332753408',
    '570279488000',
    '570097969072',
    '560616381158',
    '578963996425',
    '569648771868',
    '579842255434',
    '578963825369'}

len_avg = 35.7
len_variance = 769835

#稍、欠
level1words=['半点','不大','不丁点儿','不甚','不怎么','聊','没怎么','轻度','弱','丝毫','微','相对','点点滴滴','多多少少','怪','好生','还','或多或少','略','略加','略略','略微','略为','蛮','稍','稍稍','稍微','稍为','稍许','挺','未免','相当','些','些微','些小','一点','一点儿','一些','有点','有点儿','有些']
#较
level2words = ['大不了', '多', '更', '更加', '更进一步', '更为', '还', '还要', '较', '较比', '较为', '进一步', '那般', '那么', '那样', '强', '如斯', '益', '益发', '尤甚', '逾', '愈', '愈...愈', '愈发', '愈加', '愈来愈', '愈益', '远远', '越...越', '越发', '越加', '越来越', '越是', '这般', '这样', '足', '足足']
#很、超
level3words = ['不过', '不少', '不胜', '惨', '沉', '沉沉', '出奇', '大为', '多', '多多', '多加', '多么', '分外', '格外', '够瞧的', '够戗', '好', '好不', '何等', '很', '很是', '坏', '可', '老', '老大', '良', '颇', '颇为', '甚', '实在', '太', '太甚', '特', '特别', '尤', '尤其', '尤为', '尤以', '远', '着实', '曷', '碜', '不为过', '超', '超额', '超外差', '超微结构', '超物质', '出头', '多', '浮', '过', '过度', '过分', '过火', '过劲', '过了头', '过猛', '过热', '过甚', '过头', '过于', '过逾', '何止', '何啻', '开外', '苦', '老', '偏', '强', '溢', '忒']
#极其
level4words = ['百分之百', '倍加', '备至', '不得了', '不堪', '不可开交', '不亦乐乎', '不折不扣', '彻头彻尾', '充分', '到头', '地地道道', '非常', '极', '极度', '极端', '极其', '极为', '截然', '尽', '惊人地', '绝', '绝顶', '绝对', '绝对化', '刻骨', '酷', '满', '满贯', '满心', '莫大', '奇', '入骨', '甚为', '十二分', '十分', '十足', '死', '滔天', '痛', '透', '完全', '完完全全', '万', '万般', '万分', '万万', '无比', '无度', '无可估量', '无以复加', '无以伦比', '要命', '要死', '已极', '已甚', '异常', '逾常', '贼', '之极', '之至', '至极', '卓绝', '最为', '佼佼', '郅', '綦', '齁', '最']

# wo1 = ['手机', '外观', '质量', '功能', '价格', '屏幕', '信号', '颜色', '电池', '音乐', '拍照', '内存']
# wo2 = ['售前','售后','客服','赠品','保修','服务']
# wo3 = ['包装','快递','态度','速度','发货']
wo1 = ['手机','外观','质量','功能','价格','屏幕','信号','颜色','很漂亮','舒服','手机袋','操作','亲民','清晰度','差','好看','惊艳','外观设计','全给','电池','美丽','全屏','满格','漂亮','机王','漂亮','位','音质','面','拍照','接收','超','六寸','渐变色','卖家','清晰','实惠','灵敏','差差','轻薄','顺手','机身','产品','电池容量','好用','背部','拔','外观','好久','轻薄','完会','灯光','家里','尺寸','网络','手里','超薄','很漂亮','够买','够','吸引','屏','不好','刚刚','第七个','刚刚','描述','设计','关键','个人感觉','很差','渐变','挺快','握持','这家','简洁','信得过','人脸识别','塑料玩具','紫色','好滴','薄','款式','实用功能','第一个','顺畅','使劲','手感','感觉','握','品牌机','靓丽','价格比','轻薄','打不出','高大','期待','好看','报号','外放','七百多','指纹识别','单薄','棒','完完全全','清晰度','称心如意','灵活','老公','色彩','2G','很漂亮','七夕节','高大','可以信赖','造型','划算','相机','听不清','靓丽','太棒了','完美','店家','屏幕','买','机身','格','红色','用过','超','需要的话','人性化','外表','细腻','翻盖机','翡冷翠','更好','水滴','外公','启动','值','解锁','怀疑','大气','刚刚','外表','相符','机身','全','总体','会断','渐变色','点订','强大','五分','设置','价钱','ai','手机信号','机身','闪亮','颜色','光顾','顺畅','般','屏幕显示','电信','大屏幕','国产品牌','惊艳','托','不玩大','网购','画面','WiFi','舒适','因人而异','靓丽','作个','很大','同型号','摄像头','情况','傲雪','流线型','手里','经营','轻','新品','单手操作','讲话','外表','存储量','屏幕','红火','内存','我家','背面','弹出来','舒服','意外','炫酷','商品质量','视频','无敌','照片','失灵','水滴','犀利','质感','意','轻巧','小华','界面','上班时间','女孩子','下功夫','时尚','价优','屏幕显示','平民','艳丽','两分钟','美观','安好','款','好而价','灵敏','品质','亮点','录音','超薄','大屏','爱不释手','发言权','智能','拥有','占','同一个','智能化','炫酷','蓝紫色','发得','小点','下手','宽度','一月','紫','战','大屏','低廉','语音','一款','舒适','莫名','强大','外观','高','从始至终','音量','早用','靓丽','地方','尺寸','薄','反应速度快','动静','拍照','推存','分屏','4G','一眼','饱和','女生','好使','厚重感','弟弟','自带','没见','触感','漂亮','窄','懒癌','拿在手上','买下来','像素','三四天','屏幕','p20pro','拥有','刷单','舒适','浮夸','手里','电到','洋气','温润','拿在手上','多方','够用','块','分辨率','解决办法','线条','前摄','手感','物美价廉','用途','暮光金','光感','充满','清晰度','六月份','一款','还来','轻薄','看来看去','留海','一两','女生','四台','顺手','模版','款','这回','女生','长短','高','手机','不错','非常','喜欢','满意','可以','收到','很快','好评','华为','物流','速度','小米','就是','没有','感觉','还是','声音','这个','流畅','快递','老人','性价比','真的','客服','使用','好看','问题','质量','支持','宝贝','屏幕','特别','苏宁','一直','一个','发货','手感','值得','购买','妈妈','东西','评价','荣耀','拍照','价格','好用','几天','运行','正品']
wo2 = []
wo3=[]