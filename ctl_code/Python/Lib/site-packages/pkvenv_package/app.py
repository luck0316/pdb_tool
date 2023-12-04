import os
import re

from mmgui import App, BrowserWindow

app = App(headless=False)
win = None

device_dict = {
    0x00000001: "FILE_DEVICE_BEEP",
    0x00000002: "FILE_DEVICE_CD_ROM",
    0x00000003: "FILE_DEVICE_CD_ROM_FILE_SYSTEM",
    0x00000004: "FILE_DEVICE_CONTROLLER",
    0x00000005: "FILE_DEVICE_DATALINK",
    0x00000006: "FILE_DEVICE_DFS",
    0x00000007: "FILE_DEVICE_DISK",
    0x00000008: "FILE_DEVICE_DISK_FILE_SYSTEM",
    0x00000009: "FILE_DEVICE_FILE_SYSTEM",
    0x0000000a: "FILE_DEVICE_INPORT_PORT",
    0x0000000b: "FILE_DEVICE_KEYBOARD",
    0x0000000c: "FILE_DEVICE_MAILSLOT",
    0x0000000d: "FILE_DEVICE_MIDI_IN",
    0x0000000e: "FILE_DEVICE_MIDI_OUT",
    0x0000000f: "FILE_DEVICE_MOUSE",
    0x00000010: "FILE_DEVICE_MULTI_UNC_PROVIDER",
    0x00000011: "FILE_DEVICE_NAMED_PIPE",
    0x00000012: "FILE_DEVICE_NETWORK",
    0x00000013: "FILE_DEVICE_NETWORK_BROWSER",
    0x00000014: "FILE_DEVICE_NETWORK_FILE_SYSTEM",
    0x00000015: "FILE_DEVICE_NULL",
    0x00000016: "FILE_DEVICE_PARALLEL_PORT",
    0x00000017: "FILE_DEVICE_PHYSICAL_NETCARD",
    0x00000018: "FILE_DEVICE_PRINTER",
    0x00000019: "FILE_DEVICE_SCANNER",
    0x0000001a: "FILE_DEVICE_SERIAL_MOUSE_PORT",
    0x0000001b: "FILE_DEVICE_SERIAL_PORT",
    0x0000001c: "FILE_DEVICE_SCREEN",
    0x0000001d: "FILE_DEVICE_SOUND",
    0x0000001e: "FILE_DEVICE_STREAMS",
    0x0000001f: "FILE_DEVICE_TAPE",
    0x00000020: "FILE_DEVICE_TAPE_FILE_SYSTEM",
    0x00000021: "FILE_DEVICE_TRANSPORT",
    0x00000022: "FILE_DEVICE_UNKNOWN",
    0x00000023: "FILE_DEVICE_VIDEO",
    0x00000024: "FILE_DEVICE_VIRTUAL_DISK",
    0x00000025: "FILE_DEVICE_WAVE_IN",
    0x00000026: "FILE_DEVICE_WAVE_OUT",
    0x00000027: "FILE_DEVICE_8042_PORT",
    0x00000028: "FILE_DEVICE_NETWORK_REDIRECTOR",
    0x00000029: "FILE_DEVICE_BATTERY",
    0x0000002a: "FILE_DEVICE_BUS_EXTENDER",
    0x0000002b: "FILE_DEVICE_MODEM",
    0x0000002c: "FILE_DEVICE_VDM",
    0x0000002d: "FILE_DEVICE_MASS_STORAGE",
    0x0000002e: "FILE_DEVICE_SMB",
    0x0000002f: "FILE_DEVICE_KS",
    0x00000030: "FILE_DEVICE_CHANGER",
    0x00000031: "FILE_DEVICE_SMARTCARD",
    0x00000032: "FILE_DEVICE_ACPI",
    0x00000033: "FILE_DEVICE_DVD",
    0x00000034: "FILE_DEVICE_FULLSCREEN_VIDEO",
    0x00000035: "FILE_DEVICE_DFS_FILE_SYSTEM",
    0x00000036: "FILE_DEVICE_DFS_VOLUME",
    0x00000037: "FILE_DEVICE_SERENUM",
    0x00000038: "FILE_DEVICE_TERMSRV",
    0x00000039: "FILE_DEVICE_KSEC",
    0x0000003A: "FILE_DEVICE_FIPS",
    0x0000003B: "FILE_DEVICE_INFINIBAND",
    0x0000003E: "FILE_DEVICE_VMBUS",
    0x0000003F: "FILE_DEVICE_CRYPT_PROVIDER",
    0x00000040: "FILE_DEVICE_WPD",
    0x00000041: "FILE_DEVICE_BLUETOOTH",
    0x00000042: "FILE_DEVICE_MT_COMPOSITE",
    0x00000043: "FILE_DEVICE_MT_TRANSPORT",
    0x00000044: "FILE_DEVICE_BIOMETRIC",
    0x00000045: "FILE_DEVICE_PMI",
    0x00000046: "FILE_DEVICE_EHSTOR",
    0x00000047: "FILE_DEVICE_DEVAPI",
    0x00000048: "FILE_DEVICE_GPIO",
    0x00000049: "FILE_DEVICE_USBEX",
    0x00000050: "FILE_DEVICE_CONSOLE",
    0x00000051: "FILE_DEVICE_NFP",
    0x00000052: "FILE_DEVICE_SYSENV",
    0x00000053: "FILE_DEVICE_VIRTUAL_BLOCK",
    0x00000054: "FILE_DEVICE_POINT_OF_SERVICE",
    0x00000055: "FILE_DEVICE_STORAGE_REPLICATION",
    0x00000056: "FILE_DEVICE_TRUST_ENV",
    0x00000057: "FILE_DEVICE_UCM",
    0x00000058: "FILE_DEVICE_UCMTCPCI",
    0x00000059: "FILE_DEVICE_PERSISTENT_MEMORY",
    0x0000005a: "FILE_DEVICE_NVDIMM",
    0x0000005b: "FILE_DEVICE_HOLOGRAPHIC",
    0x0000005c: "FILE_DEVICE_SDFXHCI",
    0x0000005d: "FILE_DEVICE_UCMUCSI"
}

access_dict = {
    0: "FILE_ANY_ACCESS",
    1: "FILE_READ_ACCESS",
    2: "FILE_WRITE_ACCESS",
    3: "FILE_READ_ACCESS | FILE_WRITE_ACCESS"
}

method_dict = {
    0: "METHOD_BUFFERED",
    1: "METHOD_IN_DIRECT",
    2: "METHOD_OUT_DIRECT",
    3: "METHOD_NEITHER"
}


def parse_control_code(control_code):
    if control_code.lower().startswith('0x'):
        ctl_code = int(control_code, 16)

        device_type = (ctl_code & 0xffff0000) >> 16
        function_code = (ctl_code >> 2) & 0x00000FFF
        access = (ctl_code >> 14) & 0x3
        method = ctl_code & 3
        device_type_str = hex(device_type)
        function_code_str = hex(function_code)

        device_str = device_dict.get(device_type, None)
        access_str = access_dict.get(access, None)
        method_str = method_dict.get(method, None)
        if device_str and access_str and method_str:
            define_statement = f"#define IO_CTL_DIY CTL_CODE({device_str}, {function_code_str}, {method_str}, {access_str})"
            return device_type_str, device_str, function_code_str, access_str, method_str, define_statement
        else:
            return "解析失败，请重新检查control_code"

    else:
        return None, None, None, None, None, "control_code输入格式错误，请输入0x开头16进制字符串"

def micro_to_code(device_type_hex, function_code_hex, access, method):
    print(device_type_hex)
    if device_type_hex.lower().startswith('0x'):
        device_type = int(device_type_hex, 16)
        device_str = device_dict.get(device_type, None)
    else:
        device_type = next((k for k, v in device_dict.items() if v == device_type_hex), None)
        if device_type:
            device_str = device_type_hex
        else:
            device_str = None

    access_int = next((k for k, v in access_dict.items() if v == access), None)
    if access_int in [0, 1, 2, 3]:
        access_str = access
    else:
        access_str = None

    method_int = next((k for k, v in method_dict.items() if v == method), None)
    if method_int in [0, 1, 2, 3]:
        method_str = method
    else:
        method_str = None

    print(access_str)
    if function_code_hex.lower().startswith('0x') and device_str and access_str and method_str:
        function_code_int = int(function_code_hex, 16)
        control_code = ((device_type << 16) | (access_int << 14) | (function_code_int << 2) | method_int)
        define_statement = f"#define IO_CTL_DIY CTL_CODE({device_str}, {hex(function_code_int)}, {method_str}, {access_str})"
        print(control_code)
        return hex(control_code), define_statement
    else:
        return "请检查相关数据是否填写正确"

def parse_define_statement(define_statement):
    match = re.search(r"#define\s+(\w+)\s+(\w+)\s*\(([^,]+),([^,]+),([^,]+),([^)]+)\)", define_statement)
    if match:
        io_ctl_diy, ctl_code, device_str, function_code_str, method_str, access_str = match.groups()

        device_type = next((k for k, v in device_dict.items() if v.strip() == device_str.strip()), None)
        function_code = int(function_code_str.strip(), 16)
        access = next((k for k, v in access_dict.items() if v.strip() == access_str.strip()), None)
        method = next((k for k, v in method_dict.items() if v.strip() == method_str.strip()), None)
        if device_type and access in [0, 1, 2, 3] and method in [0, 1, 2, 3]:
            control_code = ((device_type << 16) | (access << 14) | (function_code << 2) | method)
            return hex(control_code), device_str.strip(), hex(function_code), access_str.strip(), method_str.strip()
        else:
            return "请重新检查数据"
    else:
        return "请重新检查代码格式是否正确"


def on_create(ctx):
    global win
    win = BrowserWindow({
        "title": "Demo",
        "width": 1200,
        "height": 1200,
        "dev_mode": False,
    })
    win.webview.bind_function("parse_control_code", parse_control_code)
    win.webview.bind_function("micro_to_code", micro_to_code)
    win.webview.bind_function("parse_define_statement", parse_define_statement)
    win.webview.load_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html"))
    win.show()


def main():
    global app
    app = App(headless=False)
    app.on("create", on_create)
    app.run()


main()
