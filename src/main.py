#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textnode as tnd


def main():
    tn = tnd.TextNode(
        "This is some anchor text", tnd.TextType.image, "https://example.com"
    )
    print(tn)


if __name__ == "__main__":
    main()
