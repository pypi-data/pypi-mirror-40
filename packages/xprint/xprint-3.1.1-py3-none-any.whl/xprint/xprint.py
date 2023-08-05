# coding:utf-8
import sys
import colorama
from colorama import Fore, Back, Style

wr = sys.stdout.write


def init(autoreset: bool = False, convert=None, strip=None, wrap=True):
    colorama.init(autoreset=autoreset, convert=convert, strip=strip, wrap=wrap)


def lx(n: int = 2):
    for i in range(0, n):
        print()


def ex(n: int = 2):
    lx(n=n)
    exit()


def fi(inline: bool = True):
    if inline:
        wr(Style.RESET_ALL)
    else:
        print(Style.RESET_ALL)
    sys.stdout.flush()


def fx():  # same to fi(inline=False)
    print(Style.RESET_ALL)
    sys.stdout.flush()


def blank():
    wr(' ')
    fi()


def blanks(n: int = 1):
    for i in range(0, n):
        wr(' ')
    fi()


def step(with_blanks: int = 0):
    wr(Fore.LIGHTBLUE_EX + '>')
    fi()
    if blanks:
        blanks(with_blanks)


def steps(n: int = 1, with_blanks: int = 0):
    for i in range(0, n):
        wr(Fore.LIGHTBLUE_EX + '>')
    fi()
    if blanks:
        blanks(with_blanks)


def plain_text(plain_text: str):
    wr(Fore.BLUE + plain_text)
    fx()


def success(s: str = 'success.', inline: bool = False):
    wr(Fore.GREEN + '{}'.format(s))
    fi(inline=inline)


def error(s, inline: bool = False):
    wr(Back.RED + Fore.LIGHTWHITE_EX + ' {} '.format(s))
    fi(inline=inline)


def value(s, inline: bool = False):
    wr(Fore.LIGHTCYAN_EX + str(s))
    fi(inline=inline)


def job(s):
    print()
    wr(Back.BLUE + Fore.LIGHTWHITE_EX + ' - {} - '.format(s))
    fx()
    print()


def about_to(left, value=None, right=None, inline: bool = False):
    wr(Fore.LIGHTBLUE_EX + '> ')
    wr(Fore.LIGHTYELLOW_EX + left)
    if value: wr(Fore.LIGHTCYAN_EX + ' {}'.format(value))
    if right: wr(Fore.LIGHTYELLOW_EX + ' {}'.format(right))
    if inline: wr(Fore.LIGHTBLUE_EX + ' ... ')
    fi(inline=inline)


def about_t(left, value=None, right=None):
    about_to(left=left, value=value, right=right, inline=True)


def getting(s, inline: bool = True):
    wr(Fore.LIGHTBLUE_EX + '> ')
    wr(Fore.LIGHTYELLOW_EX + str(s))
    wr(Fore.LIGHTBLUE_EX + ' > ')
    fi(inline=inline)


def watching(s, inline: bool = True):
    wr(Fore.LIGHTBLUE_EX + '> ')
    wr(Fore.LIGHTYELLOW_EX + str(s))
    wr(Fore.LIGHTBLUE_EX + ' >')
    fi(inline=inline)
