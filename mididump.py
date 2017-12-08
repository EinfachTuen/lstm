#!/usr/bin/env python3

import json
import struct
import sys

def ReadUntil(f, buf):
    buf=bytes(buf)
    if not len(buf):
        return
    while True:
        t=f.read(1)
        if not t:
            raise EOFError
        if buf.startswith(t):
            pos=f.tell()
            if f.read(len(buf)-1)==buf[1:]:
                return
            f.seek(pos, 0)

def ReadOrEOF(f, size):
    b=f.read(size)
    if len(b)==size:
        return b
    else:
        raise EOFError

def ScanBigInt(f, prefix=b''):
    res=0
    count=-len(prefix)
    while True:
        if prefix:
            t=struct.unpack('>B', prefix[0:1])[0]
            prefix=prefix[1:]
        else:
            t=struct.unpack('>B', ReadOrEOF(f, 1))[0]
        count+=1
        if t&0x80:
            res=(res<<7)|(t&0x7f)
        else:
            return ((res<<7)|t, count)

def main(fn):
    resultString = ""
    resultString += '<!--\n  Output of midid, a simple MIDI dump tool.\n  vim: ft=xml\n-->\n'
    f=open(fn, "rb")
    ReadUntil(f, b'MThd')
    mthd_len=struct.unpack('>L', ReadOrEOF(f, 4))[0]
    mthd=struct.unpack('>HHH', ReadOrEOF(f, 6))
    resultString +='%08x <mthd size="%d" type="%d" tracks="%d" division="%d">\n' % ((f.tell()-14, mthd_len)+mthd)
    for trkno in range(mthd[1]):
        resultString +='%08x  ' % f.tell()
        mtrk=ReadOrEOF(f, 4)
        assert mtrk==b'MTrk'
        mtrk_len=struct.unpack('>L', ReadOrEOF(f, 4))[0]
        resultString +='<mtrk size="%d">\n' % mtrk_len
        mtrk_len_read=0
        last_time=0
        last_meta=0x80
        while mtrk_len_read<mtrk_len:
            resultString +='%08x   ' % f.tell()
            timestamp=ScanBigInt(f)
            mtrk_len_read+=timestamp[1]
            if mtrk_len_read>=mtrk_len: raise EOFError
            last_time+=timestamp[0]
            meta=ReadOrEOF(f, 1)
            mtrk_len_read+=1
            meta_int=struct.unpack('>B', meta)[0]
            if mtrk_len_read>=mtrk_len: raise EOFError
            if meta_int&0x80:
                last_meta, param=meta, ReadOrEOF(f, 1)
                mtrk_len_read+=1
                meta_int=struct.unpack('>B', meta)[0]
            else:
                meta, param=last_meta, meta
                meta_int=struct.unpack('>B', meta)[0]
            if meta_int==0xff:
                meta_len=ScanBigInt(f)
                mtrk_len_read+=meta_len[1]
                if mtrk_len_read>mtrk_len: raise EOFError
                meta_data=ReadOrEOF(f, meta_len[0])
                mtrk_len_read+=meta_len[0]
                if mtrk_len_read>mtrk_len: raise EOFError
                resultString +='  <meta  time="%d/%d" event="0x%02x" type="0x%02x" len="%d" data=' % (last_time, mthd[2], meta_int, param[0], meta_len[0])
                if param[0]==0x51:
                    tempo=0
                    for tempoi in meta_data:
                        tempo=(tempo<<8)|tempoi
                    resultString +='"%.2f" />\n' % (60000000.0/tempo)
                elif param[0] in (0x54, 0x58):
                    resultString +='"%s" />\n' % ' '.join([str(meta_datai) for meta_datai in meta_data])
                elif param[0]==0x59 and meta_len[0]==2:
                    resultString +='"%s %s" />\n' % ((('C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#')[meta_data[0]] if meta_data[0] in range(0, 8) else ('B', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F')[meta_data[0]-249] if meta_data[0] in range(249, 256) else meta_data[0]), (('Maj', 'min')[meta_data[1]] if meta_data[1] in (0, 1) else meta_data[1]))
                else:
                    resultString +='%s />\n' % json.dumps(meta_data.decode('utf-8', 'replace'), ensure_ascii=False)
            elif meta_int&0xf0==0xf0:
                meta_len=ScanBigInt(f, param)
                mtrk_len_read+=meta_len_tuple[1]
                if mtrk_len_read>mtrk_len: raise EOFError
                meta_data=ReadOrEOF(f, meta_len[0])
                mtrk_len_read+=meta_len[0]
                if mtrk_len_read>mtr-k_len: raise EOFError
                resultString +='  <sysex time="%d/%d" event="0x%02x" len="%d" param=%s />\n' % (last_time, mthd[2], meta_int, meta_len[0], json.dumps(meta_data.decode('utf-8', 'replace'), ensure_ascii=False))
            else:
                resultString +='  <event time="%d/%d" event="0x%x" channel="%2d" param="' % (last_time, mthd[2], meta_int>>4, (meta_int&0xf)+1)
                if mtrk_len_read>mtrk_len: raise EOFError
                if meta_int>>4 not in (0xc, 0xd):
                    param+=ReadOrEOF(f, 1)
                    mtrk_len_read+=1
                if meta_int>>4 in (0x8, 0x9, 0xa):
                    resultString +='%-3s %d" />\n' % ( '%s%d' % (('C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B')[param[0]%12], param[0]/12-1), param[1])
                elif len(param)==2:
                    resultString +='0x%02x %d" />\n' % (param[0], param[1])
                else:
                    resultString +='%d" />\n' % param[0]
        resultString +='%08x  </mtrk>\n' % f.tell()
    resultString +='%08x </mthd>\n' % f.tell()
    f.close()
    return resultString

if __name__=='__main__':
   print(main("fp-1all.mid"))

