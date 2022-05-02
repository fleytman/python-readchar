# -*- coding: utf-8 -*-
# This file is based on this gist:
# http://code.activestate.com/recipes/134892/
# So real authors are DannyYoo and company.
import sys

if sys.platform.startswith("linux"):
    from .readchar_linux import readchar
elif sys.platform == "darwin":
    from .readchar_linux import readchar
elif sys.platform in ("win32", "cygwin"):
    import msvcrt

    from . import key
    from .readchar_windows import readchar
else:
    raise NotImplementedError("The platform %s is not supported yet" % sys.platform)


if sys.platform in ("win32", "cygwin"):
    #
    # Windows uses scan codes for extended characters. The ordinal returned is
    # 256 * the scan code.  This dictionary translates scan codes to the
    # unicode sequences expected by readkey.
    #
    # for windows scan codes see:
    #   https://msdn.microsoft.com/en-us/library/aa299374
    #      or
    #   http://www.quadibloc.com/comp/scan.htm
    xlate_dict = {
        13: key.ENTER,
        27: key.ESC,
        15104: key.F1,
        15328: key.F1,
        15360: key.F2,
        15584: key.F2,
        15616: key.F3,
        15840: key.F3,
        15872: key.F4,
        16096: key.F4,
        16128: key.F5,
        16352: key.F5,
        16384: key.F6,
        16608: key.F6,
        16640: key.F7,
        16864: key.F7,
        16896: key.F8,
        17120: key.F8,
        17152: key.F9,
        17376: key.F9,
        17408: key.F10,
        17632: key.F10,
        34048: key.F11,
        34272: key.F11,
        34304: key.F12,
        34528: key.F12,
        # don't have table entries for...
        # CTR_A, ..
        # ALT_A, ..
        # CTRL-F1, ..
        # CTRL_ALT_SUPR,
        # CTRL_ALT_A, .., etc.
        20992: key.INSERT,
        21216: key.INSERT,
        21248: key.SUPR,  # key.py uses SUPR, not DELETE
        21472: key.SUPR,  # key.py uses SUPR, not DELETE
        18688: key.PAGE_UP,
        18912: key.PAGE_UP,
        20736: key.PAGE_DOWN,
        20960: key.PAGE_DOWN,
        18176: key.HOME,
        18400: key.HOME,
        20224: key.END,
        20448: key.END,
        18432: key.UP,
        18656: key.UP,
        20480: key.DOWN,
        20704: key.DOWN,
        19200: key.LEFT,
        19424: key.LEFT,
        19712: key.RIGHT,
        19936: key.RIGHT,
    }

    def readkey(getchar_fn=None):
        # Get a single character on Windows. if an extended key is pressed, the
        # Windows scan code is translated into a the unicode sequences readchar
        # expects (see key.py).
        while True:
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                a = ord(ch)
                if a == 0 or a == 224:
                    b = ord(msvcrt.getch())
                    x = a + (b * 256)

                    try:
                        return xlate_dict[x]
                    except KeyError:
                        return None
                    return x
                elif a == 8:
                    return key.BACKSPACE
                elif a == 13:
                    return key.ENTER
                else:
                    return ch.decode()

else:

    def readkey(getchar_fn=None):
        getchar = getchar_fn or readchar
        c1 = getchar()
        if ord(c1) != 0x1B:
            return c1
        c2 = getchar()
        if ord(c2) != 0x5B:
            return c1 + c2
        c3 = getchar()
        if ord(c3) != 0x33:
            return c1 + c2 + c3
        c4 = getchar()
        return c1 + c2 + c3 + c4
