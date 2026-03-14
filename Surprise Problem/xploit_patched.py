import pygame
import sys
import math
import random
import time
import os

(_W, _H, _F, _T) = (960, 600, 60, 40)
(c0, c1, c2, c3) = ((0, 0, 0), (255, 255, 255), (80, 80, 80), (40, 40, 40))
(c4, c5, c6, c7) = ((220, 50, 50), (50, 200, 80), (50, 100, 220), (255, 210, 0))
(c8, c9, c10, c11) = ((255, 140, 0), (0, 220, 220), (160, 60, 200), (140, 20, 20))
(_GI, _GN) = (-0.5, 0.5)
_SEED = int.from_bytes(b'\xde\xad\xbe\xef', 'big')
_XK = 85
_MAGIC = _SEED ^ 0xCAFEBABE


def _xb(d, k=_XK):
    return bytes(b ^ k for b in d)


def _qh(x, y):
    return math.hypot(x, y)


def _qt():
    return pygame.time.get_ticks()

_fc = {}


def _gf(n):
    if n not in _fc:
        _fc[n] = pygame.font.SysFont('monospace', n, bold=True)
    return _fc[n]


def _sf():
    return _gf(17)


def _ht(s, t, x, y, c, ctr=False, sz=20):
    f = _gf(sz)
    img = f.render(t, True, c)
    if ctr:
        s.blit(img, (x - img.get_width() // 2, y))
    else:
        s.blit(img, (x, y))


class _Zv:
    _LK = 0

    def __init__(self):
        self._tk = _qt()
        self._ac = False

    def _ck(self):
        return (_qt() - self._tk) % 256

    def _ev(self, x):
        return x & 255 == 66

    @staticmethod
    def _rs(v):
        return v ^ _XK & 255


class _Eq:
    (_SW, _SH) = (30, 36)

    def __init__(self, x, y):
        self.r = pygame.Rect(x, y, self._SW, self._SH)
        self.vx = 0
        self.vy = 0
        self.og = False
        self.cn = 0
        self.hp = 3
        self.al = True
        self.gv = _GN
        self.jp = 12.7
        self.sp = 5
        self.bl = []
        self.sc = 0

    def _mi(self, k):
        self.vx = 0
        if k[pygame.K_LEFT]:
            self.vx = -(self.sp)
        if k[pygame.K_RIGHT]:
            self.vx = self.sp
        if k[pygame.K_UP] and self.og:
            self.vy = -(self.jp)
            self.og = False

    def _mj(self, k):
        self.vx = 0
        if k[pygame.K_LEFT]:
            self.vx = self.sp
        if k[pygame.K_RIGHT]:
            self.vx = -(self.sp)
        if k[pygame.K_DOWN] and self.og:
            self.vy = self.jp
            self.og = False

    def _fs(self, k):
        self.sc = max(0, self.sc - 1)
        if k[pygame.K_SPACE] and self.sc == 0:
            self.bl.append(_Fx(self.r.centerx, self.r.centery, 1))
            self.sc = 20

    def _ap(self, pf):
        self.vy += self.gv
        self.r.x += int(self.vx)
        self._cx(pf)
        self.r.y += int(self.vy)
        self._cy(pf)

    def _cx(self, pf):
        for p in pf:
            if self.r.colliderect(p):
                if self.vx > 0:
                    self.r.right = p.left
                else:
                    self.r.left = p.right
                self.vx = 0

    def _cy(self, pf):
        self.og = False
        for p in pf:
            if self.r.colliderect(p):
                if self.vy > 0:
                    self.r.bottom = p.top
                    self.vy = 0
                    if self.gv >= 0:
                        self.og = True
                elif self.vy < 0:
                    self.r.top = p.bottom
                    self.vy = 0
                    if self.gv < 0:
                        self.og = True

    def _ck(self):
        self.r.x = max(0, min(self.r.x, _W - self._SW))
        self.r.y = max(-200, min(self.r.y, _H + 200))

    def _v(self, s):
        pygame.draw.rect(s, c6, self.r)
        pygame.draw.rect(s, c9, self.r, 2)
        ex = self.r.x + 7
        ey = self.r.y + 8
        pygame.draw.circle(s, c1, (ex, ey), 5)
        pygame.draw.circle(s, c1, (ex + 14, ey), 5)
        pygame.draw.circle(s, c0, (ex + 2, ey), 2)
        pygame.draw.circle(s, c0, (ex + 16, ey), 2)


class _Fx:
    def __init__(self, x, y, d=1):
        self.r = pygame.Rect(x, y, 10, 6)
        self.vx = 12 * d
        self.ac = True

    def _u(self):
        self.r.x += self.vx
        if self.r.right < 0 or self.r.left > _W:
            self.ac = False

    def _v(self, s):
        pygame.draw.rect(s, c7, self.r)
        pygame.draw.rect(s, c8, self.r, 1)


class _Rx:
    _R = 10

    def __init__(self, x, y):
        self.r = pygame.Rect(x - self._R, y - self._R, self._R * 2, self._R * 2)
        self.cd = False

    def _v(self, s):
        if not self.cd:
            pygame.draw.circle(s, c7, self.r.center, self._R)
            pygame.draw.circle(s, c8, self.r.center, self._R, 2)


class _Ox:
    def __init__(self, x, y):
        self.r = pygame.Rect(x, y, _T, _T * 2)
        self.op = False
        self._pc = 0

    def _c(self, p):
        self._pc = p.cn
        # PATCH: was p.cn >= 9999, but only 3 coins exist
        if p.cn >= 3:
            self.op = True

    def _v(self, s):
        pygame.draw.rect(s, c5 if self.op else c4, self.r)
        pygame.draw.rect(s, c1, self.r, 2)
        if not self.op:
            pygame.draw.circle(s, c7, (self.r.right - 8, self.r.centery), 5)
        lbl = _sf().render(''.join(chr(o) for o in ([79, 80, 69, 78] if self.op else [76, 79, 67, 75, 69, 68])), True, c1)
        s.blit(lbl, (self.r.x, self.r.y - 20))


class _Tx:
    def __init__(self, x, y):
        self.r = pygame.Rect(x, y, _T, _T)

    def _v(self, s):
        pygame.draw.rect(s, c5, self.r)
        pygame.draw.rect(s, c1, self.r, 2)
        s.blit(_sf().render(''.join(chr(o) for o in (69, 88, 73, 84)), True, c0), (self.r.x + 4, self.r.y + 12))


class _Ux:
    def __init__(self, x, y):
        self.r = pygame.Rect(x, y, _T, _T)
        self._tm = 0

    def _u(self, p):
        # PATCH: reduced flee distance from 50 to 20 so player can actually collide
        if math.hypot(p.r.centerx - self.r.centerx, p.r.centery - self.r.centery) < 20:
            self.r.x = random.randint(60, _W - 100)
            self.r.y = random.randint(60, _H - 160)

    def _v(self, s):
        self._tm += 1
        g = abs(math.sin(self._tm * 0.05)) * 80
        pygame.draw.rect(s, (50, int(150 + g), 80), self.r)
        pygame.draw.rect(s, c1, self.r, 2)
        s.blit(_sf().render(''.join(chr(o) for o in (69, 88, 73, 84)), True, c0), (self.r.x + 4, self.r.y + 12))


class _Gx:
    (_SW, _SH) = (60, 60)
    _MX = 10

    def __init__(self, x, y):
        self.r = pygame.Rect(x, y, self._SW, self._SH)
        self.mh = self._MX
        self.hp = self._MX
        self.vx = 3
        self.dd = False

    def _td(self, n):
        self.hp -= n
        # PATCH: removed "self.hp = self.mh" which reset HP to max after every hit

    def _u(self, pf):
        self.r.x += self.vx
        if self.r.right >= _W or self.r.left <= 0:
            self.vx *= -1
        self.r.y += 4
        for p in pf:
            if self.r.colliderect(p):
                self.r.bottom = p.top
        if self.hp <= 0:
            self.dd = True

    def _v(self, s):
        if self.dd:
            return
        pygame.draw.rect(s, c11, self.r)
        pygame.draw.rect(s, c4, self.r, 3)
        bw = self._SW
        hw = int(bw * self.hp / self.mh)
        pygame.draw.rect(s, c3, (self.r.x, self.r.y - 14, bw, 10))
        pygame.draw.rect(s, c4, (self.r.x, self.r.y - 14, hw, 10))
        pygame.draw.rect(s, c1, (self.r.x, self.r.y - 14, bw, 10), 1)
        s.blit(_sf().render(''.join(chr(o) for o in (66, 79, 83, 83)), True, c1), (self.r.x + 6, self.r.y + 20))


class _Mx:
    def __init__(self):
        self.pf = []
        self.cp = False

    def _bg(self):
        self.pf.append(pygame.Rect(0, _H - _T, _W, _T))

    def _dp(self, s):
        for p in self.pf:
            pygame.draw.rect(s, c2, p)
            pygame.draw.rect(s, c3, p, 2)

    def _db(self, s, col=c3):
        s.fill(col)


class _S1(_Mx):
    _NM = ''.join(chr(c) for c in (83, 116, 97, 103, 101, 32, 49))

    def __init__(self, p):
        super().__init__()
        p.r.topleft = (60, _H - _T - p._SH)
        p.cn = 0
        self._bg()
        for x, y in ((200, 420), (360, 350), (520, 280), (680, 350)):
            self.pf.append(pygame.Rect(x, y, 120, _T))
        self.cv = [
            _Rx(240, 400),
            _Rx(400, 330),
            _Rx(560, 260)]
        self.dv = _Ox(820, _H - _T - _T * 2)

    def _u(self, p, ev):
        k = pygame.key.get_pressed()
        p._mi(k)
        p._ap(self.pf)
        p._ck()
        for c in self.cv:
            if not c.cd and p.r.colliderect(c.r):
                c.cd = True
                p.cn += 1
        self.dv._c(p)
        if self.dv.op and p.r.colliderect(self.dv.r):
            self.cp = True
        if p.r.top > _H + 100:
            p.r.topleft = (60, _H - _T - p._SH)
            p.vy = 0

    def _v(self, s):
        self._db(s, (20, 20, 35))
        self._dp(s)
        for c in self.cv:
            c._v(s)
        self.dv._v(s)

    def _n(self, s, p):
        _ht(s, f'{p.cn}', 10, 10, c7, sz=20)
        _ht(s, self._NM, _W // 2, 10, c1, ctr=True)


class _S2(_Mx):
    _NM = ''.join(chr(c) for c in (83, 116, 97, 103, 101, 32, 50))
    _SP = 2
    _OBS = [
        (115, 26, 120),
        (190, 26, 148),
        (265, 26, 108),
        (340, 26, 155),
        (415, 26, 132),
        (490, 26, 146),
        (565, 26, 112),
        (640, 26, 150),
        (715, 26, 125),
        (790, 26, 153),
        (855, 26, 118)]

    def __init__(self, p):
        super().__init__()
        p.r.topleft = (40, _H - _T - p._SH)
        p.cn = 0
        p.sp = self._SP
        self._bg()
        for ox, ow, oh in self._OBS:
            self.pf.append(pygame.Rect(ox, _H - _T - oh, ow, oh))
        self.xb = _Tx(905, _H - _T - _T)
        self.st = _qt()
        # PATCH: was 5 seconds, far too short at speed 2. Increased to 30.
        self.ts = 30
        self.go = False

    def _tl(self):
        return self.ts - (_qt() - self.st) / 1000

    def _u(self, p, ev):
        p.sp = self._SP
        if self.go:
            return
        if self._tl() <= 0:
            self._tgo()
        k = pygame.key.get_pressed()
        p._mi(k)
        p._ap(self.pf)
        p._ck()
        if p.r.top > _H + 100:
            p.r.topleft = (40, _H - _T - p._SH)
            p.vy = 0
        if p.r.colliderect(self.xb.r):
            self.cp = True

    def _tgo(self):
        self.go = True

    def _v(self, s):
        self._db(s, (20, 30, 20))
        for q in self.pf:
            pygame.draw.rect(s, c2, q)
            pygame.draw.rect(s, c3, q, 2)
        self.xb._v(s)
        if self.go:
            ov = pygame.Surface((_W, _H), pygame.SRCALPHA)
            ov.fill((180, 0, 0, 160))
            s.blit(ov, (0, 0))
            _ht(s, 'TERMINATED', _W // 2, _H // 2, c1, ctr=True, sz=42)
            _ht(s, 'PATCH AND RETRY', _W // 2, _H // 2 + 50, c7, ctr=True, sz=22)

    def _n(self, s, p):
        t = max(0, self._tl())
        if t < 2:
            cl = c4
        elif t < 4:
            cl = c7
        else:
            cl = c5
        _ht(s, f'{t:.2f}', _W // 2, 10, cl, ctr=True, sz=32)
        prog = min(1, max(0, (p.r.x - 40) / 865))
        pygame.draw.rect(s, c3, (10, _H - 22, 200, 8))
        pygame.draw.rect(s, c5, (10, _H - 22, int(200 * prog), 8))
        pygame.draw.rect(s, c1, (10, _H - 22, 200, 8), 1)
        _ht(s, self._NM, _W // 2, _H - 28, c1, ctr=True)


class _S3(_Mx):
    _NM = ''.join(chr(c) for c in (83, 116, 97, 103, 101, 32, 51))
    _SCY = _H - 239
    (_PL, _PR) = (150, 820)

    def __init__(self, p):
        super().__init__()
        p.r.topleft = (40, _H - _T - p._SH)
        p.cn = 0
        self.pf.append(pygame.Rect(0, _H - _T, self._PL, _T))
        self.pf.append(pygame.Rect(self._PR, _H - _T, _W - self._PR, _T))
        self.pf.append(pygame.Rect(self._PR + 30, _H - _T * 4, 120, _T))
        self.bp = []
        self.xb = _Tx(self._PR + 60, _H - _T * 5)
        # PATCH: _rdb() was never called, so bridge platforms were missing
        self._rdb()

    def _rdb(self):
        by = _H - _T
        for bx in range(self._PL, self._PR, 40):
            self.bp.append(pygame.Rect(bx, by - _T, 42, _T))
        self.pf.extend(self.bp)

    def _u(self, p, ev):
        k = pygame.key.get_pressed()
        p._mi(k)
        p._ap(self.pf)
        p._ck()
        if p.r.top <= self._SCY:
            p.r.topleft = (40, _H - _T - p._SH)
            p.vy = 0
        if p.r.top > _H + 100:
            p.r.topleft = (40, _H - _T - p._SH)
            p.vy = 0
        if p.r.colliderect(self.xb.r):
            self.cp = True

    def _v(self, s):
        self._db(s, (10, 10, 25))
        ceil_rect = pygame.Rect(0, 0, _W, self._SCY)
        pygame.draw.rect(s, c3, ceil_rect)
        sw = 24
        for sx in range(0, _W, sw):
            pts = [
                (sx, self._SCY),
                (sx + sw // 2, self._SCY + 18),
                (sx + sw, self._SCY)]
            pygame.draw.polygon(s, c4, pts)
            pygame.draw.polygon(s, c11, pts, 1)
        self._dp(s)
        for b in self.bp:
            pygame.draw.rect(s, (139, 90, 43), b)
            pygame.draw.rect(s, (200, 140, 60), b, 2)
        pygame.draw.rect(s, c0, pygame.Rect(self._PL, _H - _T, self._PR - self._PL, _T))
        vl = _sf().render(''.join(chr(o) for o in (86, 79, 73, 68)), True, (50, 50, 50))
        s.blit(vl, ((self._PL + self._PR) // 2 - vl.get_width() // 2, (_H - _T) + 8))
        self.xb._v(s)

    def _n(self, s, p):
        _ht(s, self._NM, _W // 2, 10, c1, ctr=True)


class _S4(_Mx):
    _NM = ''.join(chr(c) for c in (83, 116, 97, 103, 101, 32, 52))

    def __init__(self, p):
        super().__init__()
        p.r.topleft = (60, _H - _T - p._SH)
        p.cn = 0
        p.bl.clear()
        self._bg()
        self.pf.append(pygame.Rect(100, _H - _T * 4, 200, _T))
        self.pf.append(pygame.Rect(400, _H - _T * 6, 200, _T))
        self.bx = _Gx(700, _H - _T - _Gx._SH)
        self.xb = _Tx(870, _H - _T - _T)

    def _u(self, p, ev):
        k = pygame.key.get_pressed()
        p._mi(k)
        p._fs(k)
        p._ap(self.pf)
        p._ck()
        for b in p.bl:
            b._u()
        p.bl = [b for b in p.bl if b.ac]
        if not self.bx.dd:
            self.bx._u(self.pf)
            for b in p.bl:
                if b.ac and b.r.colliderect(self.bx.r):
                    self.bx._td(1)
                    b.ac = False
            if self.bx.r.colliderect(p.r):
                p.r.topleft = (60, _H - _T - p._SH)
                p.vy = 0
        if p.r.top > _H + 100:
            p.r.topleft = (60, _H - _T - p._SH)
            p.vy = 0
        if self.bx.dd and p.r.colliderect(self.xb.r):
            self.cp = True

    def _v(self, s):
        self._db(s, (30, 10, 10))
        self._dp(s)
        self.bx._v(s)
        self.xb._v(s)

    def _n(self, s, p):
        _ht(s, '[SPC]', 10, 10, c9, sz=16)
        _ht(s, self._NM, _W // 2, 10, c1, ctr=True)
        if self.bx.dd:
            _ht(s, 'PROCEED', _W // 2, _H // 2 - 40, c5, ctr=True, sz=26)


class _S5(_Mx):
    _NM = ''.join(chr(c) for c in (83, 116, 97, 103, 101, 32, 53))

    def __init__(self, p):
        super().__init__()
        p.gv = _GI
        p.r.topleft = (60, _T + 4)
        self.pf.append(pygame.Rect(0, 0, _W, _T))
        self.pf.append(pygame.Rect(0, _H - _T, _W, _T))
        for x, y in ((200, _T + 10), (380, _T + 60), (560, _T + 20), (740, _T + 80)):
            self.pf.append(pygame.Rect(x, y, 120, _T))
        self.wx = _Ux(700, _T + 4)

    def _u(self, p, ev):
        p.gv = _GI
        k = pygame.key.get_pressed()
        p._mj(k)
        p._ap(self.pf)
        p._ck()
        # PATCH: check collision BEFORE the exit runs away
        if p.r.colliderect(self.wx.r):
            self.cp = True
            return
        self.wx._u(p)
        if p.r.bottom > _H - _T:
            p.r.topleft = (60, _T + 4)
            p.vy = 0

    def _v(self, s):
        s.fill((15, 5, 30))
        for i in range(0, _W, 80):
            pygame.draw.line(s, (30, 10, 60), (i, 0), (i, _H))
        for j in range(0, _H, 60):
            pygame.draw.line(s, (30, 10, 60), (0, j), (_W, j))
        self._dp(s)
        self.wx._v(s)
        for ax in range(80, _W, 160):
            pygame.draw.polygon(s, (80, 0, 80), [
                (ax, _H - 80),
                (ax - 15, _H - 50),
                (ax + 15, _H - 50)])

    def _n(self, s, p):
        _ht(s, self._NM, _W // 2, _H - 28, c1, ctr=True)


class _S6(_Mx):
    _NM = ''.join(chr(c) for c in (83, 116, 97, 103, 101, 32, 54))
    (_BX, _BY, _BW, _BH) = (330, 140, 300, 270)
    _WT = 40

    def __init__(self, p):
        super().__init__()
        p.r.topleft = (60, _H - _T - p._SH)
        self._bg()
        self.pf.append(pygame.Rect(80, _H - _T * 4, 160, _T))
        self.pf.append(pygame.Rect(720, _H - _T * 4, 160, _T))
        self._bw = []
        # PATCH: original box was fully sealed. Open the bottom wall by omitting it.
        for rx, ry, rw, rh in (
            (self._BX, self._BY, self._BW, self._WT),                         # top
            # bottom wall removed to create opening
            (self._BX, self._BY, self._WT, self._BH),                         # left
            (self._BX + self._BW - self._WT, self._BY, self._WT, self._BH),   # right
        ):
            q = pygame.Rect(rx, ry, rw, rh)
            self._bw.append(q)
            self.pf.append(q)
        self.xb = _Tx(460, 255)

    def _u(self, p, ev):
        k = pygame.key.get_pressed()
        p._mi(k)
        p._ap(self.pf)
        p._ck()
        if p.r.top > _H + 100:
            p.r.topleft = (60, _H - _T - p._SH)
            p.vy = 0
        if p.r.colliderect(self.xb.r):
            self.cp = True

    def _v(self, s):
        self._db(s, (8, 8, 18))
        for i in range(0, _W, 120):
            pygame.draw.line(s, (18, 18, 35), (i, 0), (i, _H))
        for j in range(0, _H, 90):
            pygame.draw.line(s, (18, 18, 35), (0, j), (_W, j))
        for p in self.pf:
            if p not in self._bw:
                pygame.draw.rect(s, c2, p)
                pygame.draw.rect(s, c3, p, 2)
        for w in self._bw:
            pygame.draw.rect(s, c2, w)
            pygame.draw.rect(s, c3, w, 2)
        self.xb._v(s)

    def _n(self, s, p):
        _ht(s, self._NM, _W // 2, _H - 28, c1, ctr=True)
        _ht(s, '???', _W // 2, _H // 2 - 20, c2, ctr=True, sz=48)


_PV = _Zv()
_UNLK = 12648430
_CKSUM = sum(_UNLK.to_bytes(3, 'big'))


def _validate_env():
    return (_CKSUM ^ (_MAGIC & 255)) != 0


def _encode_flag(n):
    return bytes(b ^ (_XK + i) % 256 for i, b in enumerate(n.encode()))


def _decode_str(r):
    return ''.join(chr(c) for c in r)


_HDR = _encode_flag('xploit_dungeon_v1')
_LBL_T = _decode_str([84, 69, 82, 77, 73, 78, 65, 84, 69, 68])
_LBL_P = _decode_str([80, 65, 84, 67, 72, 32, 65, 78, 68, 32, 82, 69, 84, 82, 89])
_LBL_W = _decode_str([65, 67, 67, 69, 83, 83, 32, 71, 82, 65, 78, 84, 69, 68])
_LBL_E = _decode_str([69, 78, 84, 69, 82])
_LBL_G = _decode_str([88, 80, 76, 79, 73, 84, 32, 68, 85, 78, 71, 69, 79, 78])
_LBL_C = _decode_str([83, 84, 65, 71, 69, 32, 67, 76, 69, 65, 82])
_LBL_S = _decode_str([83, 85, 66, 77, 73, 84, 32, 80, 65, 84, 67, 72, 32, 43, 32, 82, 69, 80, 79, 82, 84])


def _scr_t(s, cl):
    s.fill((10, 10, 20))
    for t, sz, c, y in (
        (_LBL_G, 42, c9, _H // 2 - 120),
        (_decode_str([82, 69, 86, 69, 82, 83, 69, 32, 69, 78, 71, 73, 78, 69, 69, 82, 73, 78, 71, 32, 67, 72, 65, 76, 76, 69, 78, 71, 69]), 22, c2, _H // 2 - 60),
        (_decode_str([53, 32, 83, 84, 65, 71, 69, 83, 46, 32, 69, 65, 67, 72, 32, 79, 78, 69, 32, 73, 83, 32, 83, 69, 65, 76, 69, 68, 46]), 20, c8, _H // 2 - 20),
        (_decode_str([66, 82, 69, 65, 67, 72, 32, 84, 72, 69, 32, 66, 73, 78, 65, 82, 89, 32, 84, 79, 32, 80, 82, 79, 67, 69, 69, 68, 46]), 20, c1, _H // 2 + 10),
        (_decode_str([65, 82, 82, 79, 87, 83, 32, 124, 32, 83, 80, 65, 67, 69]), 18, c2, _H // 2 + 70),
        (_LBL_E, 24, c5, _H // 2 + 120),
    ):
        _ht(s, t, _W // 2, y, c, ctr=True, sz=sz)
    for i in range(0, _W, 40):
        pygame.draw.rect(s, c10, (i, 0, 36, 6))
        pygame.draw.rect(s, c10, (i, _H - 6, 36, 6))
    pygame.display.flip()
    while True:
        cl.tick(_F)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return


def _scr_w(s, cl):
    while True:
        s.fill((5, 20, 5))
        for t, sz, c, y in (
            (_LBL_W, 36, c5, _H // 2 - 80),
            (_decode_str([65, 76, 76, 32, 83, 84, 65, 71, 69, 83, 32, 67, 76, 69, 65, 82, 69, 68, 46]), 22, c1, _H // 2 - 20),
            (_LBL_S, 20, c9, _H // 2 + 20),
            (_LBL_E, 20, c2, _H // 2 + 80),
        ):
            _ht(s, t, _W // 2, y, c, ctr=True, sz=sz)
        pygame.display.flip()
        cl.tick(_F)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                pygame.quit()
                sys.exit()


def _scr_r(s, cl, nm):
    while True:
        s.fill((5, 5, 15))
        _ht(s, _LBL_C, _W // 2, _H // 2 - 50, c5, ctr=True, sz=40)
        _ht(s, nm, _W // 2, _H // 2 + 10, c1, ctr=True, sz=22)
        _ht(s, _LBL_E, _W // 2, _H // 2 + 60, c2, ctr=True, sz=18)
        pygame.display.flip()
        cl.tick(_F)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return


def _run():
    pygame.init()
    pygame.display.set_caption(_LBL_G)
    s = pygame.display.set_mode((_W, _H))
    cl = pygame.time.Clock()

    if not _validate_env():
        sys.exit(1)

    _scr_t(s, cl)

    p = _Eq(60, 400)
    _lv = [_S1, _S2, _S3, _S4, _S5, _S6]
    idx = 0

    def _mk(i):
        p.vx = 0
        p.vy = 0
        p.gv = _GN
        p.sp = 5
        p.bl.clear()
        return _lv[i](p)

    lv = _mk(0)

    while True:
        cl.tick(_F)
        ev = pygame.event.get()
        for e in ev:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        lv._u(p, ev)
        lv._v(s)
        p._v(s)
        for b in p.bl:
            b._v(s)
        lv._n(s, p)
        _ht(s, f'[{idx + 1}/6]', _W - 70, _H - 26, c2, sz=16)
        pygame.display.flip()

        if lv.cp:
            idx += 1
            if idx >= len(_lv):
                _scr_w(s, cl)
            else:
                _scr_r(s, cl, _lv[idx]._NM)
                lv = _mk(idx)

    pygame.quit()


if __name__ == '__main__':
    _run()
