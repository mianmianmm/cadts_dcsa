from cadts_dcsa.block.utils import calc_sha1


file1 = 'E:\\Users\\LiRui\\Downloads\\VanDyke.SecureCRT.and.SecureFX.8.3.0.Build.1514.rar'
file2 = 'E:\\tmp\\VanDyke.SecureCRT.and.SecureFX.8.3.0.Build.1514.rar'


def print_hex(s):
    for c in s:
        print '%02X' % ord(c),
    print


with open(file1, 'rb') as f1:
    print_hex(f1.read(32))

with open(file2, 'rb') as f2:
    print_hex(f2.read(32))

