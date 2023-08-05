# -*- coding: utf-8 -*-
import argparse
import io
import os

from wowlint.wowfile import Resource, BlockType


def song_to_text(song):
    result = u''
    verse_counter = 1
    bridge_counter = 1
    chorus_counter = 1

    for block in song.content.block:
        if block.type == BlockType.VERSE:
            result += "Verse {}\n".format(verse_counter)
            verse_counter += 1
        elif block.type == BlockType.CHORUS:
            result += "Chorus {}\n".format(chorus_counter)
            chorus_counter += 1
        elif block.type == BlockType.BRIDGE:
            result += "Bridge {}\n".format(bridge_counter)
            bridge_counter += 1

        for line in block.line:
            result += line.text
            result += '\n'

        result += '\n'

    if song.content.author or song.content.copyright:
        result += 'CCLI Song # 0 FOR PP IMPORT\n'

        if song.content.author:
            result += song.content.author
            result += '\n'
        if song.content.copyright:
            result += u'© {}\n'.format(song.content.copyright)
            result += '\n'

    return result


def liturgy_to_text(liturgy):
    result = u''
    for line in liturgy.content.line:
        result += line.text
        result += '\n'
    return result


_RESOURCE_MAPPING = {
    'Song Words': song_to_text,
    'Liturgy': liturgy_to_text
}


def _create_arg_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--encoding', default='utf-8',
                        help='''Character encoding to use in output (default utf-8, may require windows-1252 for Windows).
If characters are encountered in the source file that cannot be encoded in the chosen character set, an error will be
raised (e.g. you try to encode Chinese characters into us-ascii).'''
                        )
    parser.add_argument('files', help='Words of Worship file (song or liturgy) to process', metavar='wowfile', nargs='+')

    return parser


def main():
    args = _create_arg_parser().parse_args()
    for wowfile in args.files:
        with open(wowfile, 'rb') as f:
            resource = Resource.parse(f.read())
            outfile = '{}.txt'.format(os.path.splitext(wowfile)[0])
            print '{} ({}) => {}'.format(wowfile, resource.filetype, outfile)

            if resource.filetype in _RESOURCE_MAPPING:
                as_text = _RESOURCE_MAPPING[resource.filetype](resource)
                with io.open(outfile, 'w', encoding=args.encoding) as of:
                    of.write(as_text)
            else:
                print "Unknown file type {}".format(resource.filetype)


if __name__ == '__main__':
    main()
