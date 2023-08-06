# -*- coding: utf-8 -*-

from . import fmconcert


def main():
    url = fmconcert.parse_cl_args()
    fmconcert.main(url)


if __name__ == "__main__":
    main()
