
from mtgtools.MtgDB import MtgDB
import traceback
import argparse
import os, sys
import shutil

import warnings

warnings.filterwarnings('ignore', message=r'Could not find any cards in this matching the line')

MAGIC_DB_FILE = os.path.join(
    os.environ['HOME'], 
    '.proxyprint',
    'magicdb.fs')

MAX_QUALITY = 95

def load_db():
    full_update = False
    if not os.path.exists(MAGIC_DB_FILE):
        if not os.path.exists(os.path.dirname(MAGIC_DB_FILE)):
            os.makedirs(os.path.dirname(MAGIC_DB_FILE))
        full_update = True
    mtg_db = MtgDB(MAGIC_DB_FILE)
    if full_update:
        try:
            mtg_db.full_update_from_scryfall()
        except:
            traceback.print_exc()
            print('Unable to load full db from scryfall')

    try:
        mtg_db.update_new_from_scryfall()
    except:
        traceback.print_exc()
        print('Unable to update db from scryfall')

    cards = mtg_db.root.scryfall_cards
    return cards

#def create_proxies(self, scaling_factor=1.0, margins=(130, 130), cut_space=True,quality=75, dir_path='', image_format='jpeg', file_names='proxies'):

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('decklist')
    parser.add_argument('-o', '--output-dir', default=None, help='directory to dump the proxies, defaults to current directory')
    parser.add_argument('-s', '--scaling-factor', default=1.0, help='overall scaling factor of the proxies. play with this to get sizes right on various printers')
    parser.add_argument('-x', '--xmargin', default=130, help='x axis margins')
    parser.add_argument('-y', '--ymargin', default=130, help='y axis margins')
    parser.add_argument('-c', '--include-cut-space', default=False, action='store_true', help='Include 1 pixel of cut space between images')
    parser.add_argument('-q', '--quality', default=75, help='Image quality value. increases size of files. max is %d' % MAX_QUALITY)
    parser.add_argument('-i', '--image-format', default='jpeg', help='Image format for output, supports whatever pillow does')
    args = parser.parse_args()

    base_name = os.path.splitext(os.path.basename(args.decklist))[0]

    print('Loading cards database...')
    cards = load_db()
    print('Loading decklist file from %s...' % args.decklist)
    
    with open(args.decklist) as decklist_file:
        decklist_str = decklist_file.read()
    print('Building decklist...')
    decklist = cards.from_str(decklist_str)

    if not args.output_dir:
        output_dir = os.path.join(os.getcwd(), base_name)
    else:
        output_dir = args.output_dir

    if not os.path.exists(os.path.dirname(output_dir)):
        os.makedirs(os.path.dirname(output_dir))
    elif os.path.exists(output_dir):
        print('Found existing directory at %s, deleting it...' % args.output_dir)
        shutil.rmtree(output_dir)

    print('Creating proxies in directory %s...' % output_dir)
    decklist.create_proxies(
        scaling_factor=args.scaling_factor, margins=(args.xmargin, args.ymargin), 
        cut_space=args.include_cut_space, quality=min(args.quality, MAX_QUALITY), 
        dir_path=output_dir, 
        image_format='jpeg', file_names=base_name)
    print('All done!')
    return 0

if __name__ == '__main__':
    main()