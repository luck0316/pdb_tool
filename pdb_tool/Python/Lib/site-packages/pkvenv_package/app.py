import os
from binascii import hexlify
import pdbparse
from mmgui import App, BrowserWindow

app = App(headless=False)
win = None


def open_file():
    path = win.show_file_dialog_for_file("打开文件", "*")
    return path[0]


def close_window():
    win.close()


def dump_pdb_info(pdb_file_path):
    try:
        pdb = pdbparse.parse(pdb_file_path, fast_load=True)  # pdb信息
        pdb_stream = pdb.streams[pdbparse.PDB_STREAM_PDB]
        pdb_stream.load()

        pdb_data = pdb_stream.data  # PDB_STREAM_PDB的二进制数据
        pdb_data_hex = pdb_data.hex()  # 转哈希值

        offset1, data, value = fomatted(pdb_data_hex, pdb_data)
        version, timeDateStamp, age, guidstr, names = pdb_msg(pdb_stream)
        offset2, g2_data, g2_value = other_guid(pdb_file_path, pdb_data_hex)

        return offset1, data, value, version, timeDateStamp, age, guidstr, names, offset2, g2_data, g2_value
    except Exception as e:
        return "该文件不是有效文件"
def other_guid(pdb_file_path, pdb_data_hex):
    with open(pdb_file_path, 'rb') as f:
        pdb_stream_data = f.read()  # pdb二进制数据
    pdb_stream_hex = pdb_stream_data.hex()
    guid = pdb_data_hex[24:56]

    if pdb_stream_hex.count(guid, 0, -1) > 1:
        if pdb_stream_hex.find(guid, 0, pdb_stream_hex.find(pdb_data_hex)) != -1:
            find_data = pdb_stream_hex.find(guid, 0, pdb_stream_hex.find(pdb_data_hex))
        else:
            find_data = pdb_stream_hex.find(guid, pdb_stream_hex.index(pdb_data_hex) + 32, -1)
        total_find = pdb_stream_hex[find_data - 24:find_data + 32 + 32 * 8 + 2]
        offset, total_find, guid2_value = fomatted(total_find, bytes.fromhex(total_find))
        return offset, total_find, guid2_value
    else:
        return "未发现第二个GUID"


def pdb_msg(pdb_stream):
    version = pdb_stream.Version
    timeDateStamp = pdb_stream.TimeDateStamp.strftime('%Y-%m-%d %H:%M:%S')
    age = pdb_stream.Age
    names = pdb_stream.names
    guidstr = (u'%08x%04x%04x%s' % (
        pdb_stream.GUID.Data1, pdb_stream.GUID.Data2,
        pdb_stream.GUID.Data3,
        "".join(
            [hexlify(pdb_stream.GUID.Data4[i:i + 2]).decode('ascii') for i in
             range(0, len(pdb_stream.GUID.Data4), 2)])
    )).upper()
    return version, timeDateStamp, age, guidstr, names


def fomatted(pdb_data_hex, pdb_data):
    formatted_data = ' '.join([pdb_data_hex[i:i + 2] for i in range(0, len(pdb_data_hex), 2)])  # data格式
    formatted_data = '\n'.join([formatted_data[i:i + 47] for i in range(0, len(formatted_data), 48)]).upper()

    value = ''.join([chr(byte) if 32 <= byte <= 126 else '.' for byte in pdb_data])
    formatted_value = ''
    offset = ""
    for i in range(0, len(value), 16):
        formatted_value += value[i:i + 16] + '\n'
        offset += f"{i:08X}" + '\n'

    return offset, formatted_data, formatted_value


def on_create(ctx):
    global win
    win = BrowserWindow({
        "title": "Demo",
        "width": 1140,
        "height": 800,
        "dev_mode": False,
    })
    win.webview.bind_function("dump_pdb_info", dump_pdb_info)
    win.webview.bind_function("open_file", open_file)
    win.webview.bind_function("close_window", close_window)
    win.webview.bind_function("other_guid", other_guid)
    win.webview.load_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html"))
    win.show()


def main():
    global app
    app = App(headless=False)
    app.on("create", on_create)
    app.run()


main()
