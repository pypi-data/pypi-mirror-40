from pathlib import Path
import sys
from dltpy.gen.stored_message import StoredMessage
from dltpy.gen.payload_item import PayloadItem
from IPython.lib.pretty import pprint
from dltpy import dltfile
from binascii import hexlify
import kaitaistruct
import io
import logging

def do_print(fn: Path):
    f = dltfile.DltFile(fn)
    for dm in f:
        assert isinstance(dm, dltfile.DltMessage)

        print('[%9.4f] %4s:%4s %r' % (dm.ts, dm.app, dm.ctx, dm.payload))
    return
    fd = fn.open('rb')
    f_len = fn.stat().st_size
    # dltpy.gen.dlt_file.DltFile.from_file(fn)
    # 100 - single string
    skip = 2000
    while fd.tell() < f_len:
        msg: StoredMessage = StoredMessage.from_io(fd)
        if msg.msg.hdr.use_ext:
            hdr: StoredMessage.BasicHeader = msg.msg.hdr
            ext: StoredMessage.ExtendedHeader = msg.msg.ext_hdr
            if not ext.verbose:
                continue

            print('[%8.4f] %4s:%4s %r', msg.msg.hdr.tmsp * 1e-4, )
            if True or not skip:
                pl = msg.msg.payload
                # pprint(hdr.__dict__)
                # pprint(ext.__dict__)
                # if pl[:4] == b'\x03\0\0\0':
                #     pl = pl[4:]
                b = io.BytesIO(pl)
                print('%8.4f [%4s:%4s] %s' % (hdr.tmsp / 1e4, ext.app, ext.ctx, pl))
                print(hex(pl))
                print(hex(pl))
                while b.tell() < len(pl):
                    item = PayloadItem.from_io(b)
                    pprint(item.plt.__dict__)
                    value = get_value(item)
                    if value is None:
                        print("FAAAAILLL")
                        return
                    if isinstance(value, kaitaistruct.KaitaiStruct):
                        pprint(value.__dict__)
                    else:
                        pprint(value)

            skip-=1
            if skip < 0:
                break




def main():
    # do_print(sys.argv[1])
    do_print(Path('/Users/equi/PycharmProjects/dltpy/data/park_crash_1.dlt'))
    pass
if __name__ == '__main__':
    main()