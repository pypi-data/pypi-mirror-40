import json
from xml.dom import minidom
from danmu_utils.common.IConverter import IConverter


class DiyidanToBilibiliConverter(IConverter):
    @property
    def DANMU_TYPE_SRC(self):
        return 'diyidan'

    @property
    def DANMU_TYPE_DST(self):
        return 'bilibili'

    @property
    def DANMU_EXTNAME_SRC(self):
        return 'dydjson'

    @property
    def DANMU_EXTNAME_DST(self):
        return 'xml'

    def _convert_entry(self, entry):
        try:
            if 'text' in entry:
                dst_text = entry['text']
                dst_time = entry['time'] / 10
                dst_color = int(entry['color'].split('#')[1], 16)
                dst_sender = entry['danmakuId']
            elif 'danmakuContent' in entry:
                dst_text = entry['danmakuContent']
                dst_time = entry['danmakuTime'] / 1000
                dst_color = entry['danmakuTextColor']
                dst_sender = entry['danmakuId']
        except Exception as e:
            print(e)
            return None
        xml = minidom.Document()
        dst_entry = xml.createElement('d')
        p = '%f,%d,%d,%d,%d,%d,%d,%d' % (
            dst_time,  # 1. 弹幕发送相对视频的时间（以前是以秒为单位的整数，现在用浮点记了，更精准）
            1,  # 2. 弹幕类型：1~3（但貌似只见过1）滚动弹幕、4底端弹幕、5顶端弹幕、6逆向弹幕、7精准定位、8高级弹幕【默认是1，基本以1、4、5多见】
            25,  # 3. 字号：12非常小,16特小,18小,25中,36大,45很大,64特别大【默认是25】
            dst_color,  # 4. 字体颜色：不是RGB而是十进制
            0,  # 5. 弹幕发送时的UNIX时间戳，基准时间1970-1-1 08:00:00
            0,  # 6. 弹幕池类型：0普通 1字幕 2特殊
            dst_sender,  # 7. 发送者ID【注意不是uid，具体怎么关联的还不清楚，屏蔽用】
            0  # 8. 弹幕在数据库的ID
        )
        dst_entry.setAttribute('p', p)
        dst_entry.appendChild(xml.createTextNode(dst_text))
        return dst_entry

    def convert(self, data):
        try:
            item_src = json.loads(data)
        except Exception as e:
            print(e)
            return None
        xml = minidom.Document()
        list = xml.createElement('i')
        xml.appendChild(list)
        for entry_src in item_src['data']['danmakuList']:
            entry_dst = self._convert_entry(entry_src)
            if (entry_dst == None):
                continue
            list.appendChild(entry_dst)
        item_dst = xml.toprettyxml(encoding='UTF-8')
        return item_dst


from danmu_utils.common.plugin_collection import add_convert_tool

add_convert_tool(DiyidanToBilibiliConverter().DANMU_TYPE_SRC, DiyidanToBilibiliConverter().DANMU_TYPE_DST, DiyidanToBilibiliConverter)
