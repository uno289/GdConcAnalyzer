import hid

path = b'\\\\?\\HID#VID_1774&PID_1001#6&2f5aa21&0&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}'
h = hid.device()
h.open_path(path)

print("Opened USBRH")

for i in range(256):
    try:
        data = h.get_feature_report(i, 64)
        if any(data):
            print(i, data)
    except Exception:
        pass