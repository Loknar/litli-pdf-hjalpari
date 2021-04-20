#!/usr/bin/python
import argparse
import os
import sys

import pdf2image
# from PIL import Image
import PyPDF2
import pytesseract

import logman


Args = None


def print_help_and_exit():
    if Args is not None:
        Args.print_help(sys.stderr)
    else:
        logman.error('Args was None, exiting ..')
    sys.exit(1)


def main():
    in_filename = 'Eisner-The_Three_Curricula_That_Schools_Teach'
    print('loading pdf to pillow images ..')
    images_in = pdf2image.convert_from_path('pdf/%s.pdf' % (in_filename, ))

    cut_pages_horizontally = True
    rotate_counter_clockwise = True

    images = []
    if cut_pages_horizontally:
        print('cutting each page horizontally to two pages ..')
        if rotate_counter_clockwise:
            print('rotating pages 90° counter clockwise ..')
        for image_in in images_in:
            upper_half = image_in.crop(
                (0, 0, image_in.width, int(image_in.height / 2))
            )
            lower_half = image_in.crop(
                (0, int(image_in.height / 2) + 1, image_in.width, image_in.height)
            )
            if rotate_counter_clockwise:
                upper_half = upper_half.rotate(90, expand=True)
                lower_half = lower_half.rotate(90, expand=True)
            images.append(upper_half)
            images.append(lower_half)
    else:
        if rotate_counter_clockwise:
            print('rotating pages 90° counter clockwise ..')
            for image_in in images_in:
                images.append(image_in.rotate(90, expand=True))
        else:
            images = images_in

    output_dir = 'pdf/%s' % (in_filename, )
    if not os.path.exists(output_dir):
        # create log output directory
        os.makedirs(os.path.join(output_dir, 'pages'))

    pdfs_filepaths = []
    filenumber = 1
    for image in images:
        filename = 'page_{:03d}.pdf'.format(filenumber)
        filepath = os.path.join(output_dir, 'pages', filename)
        print('making page %s searchable ..' % (filenumber, ))
        pdf = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
        with open(filepath, 'w+b') as f:
            f.write(pdf)  # pdf type is bytes by default
        pdfs_filepaths.append(filepath)
        filenumber += 1

    print('merging pages to single file ..')
    merger = PyPDF2.PdfFileMerger()
    for pdf_filepath in pdfs_filepaths:
        merger.append(pdf_filepath)
    merged_filepath = os.path.join(output_dir, '%s.pdf' % (in_filename, ))
    merger.write(merged_filepath)
    merger.close()

    print('done.')

    # import pdb; pdb.set_trace()


if __name__ == '__main__':
    Args = argparse.ArgumentParser(
        description='Litli PDF Hjálpari', formatter_class=argparse.RawTextHelpFormatter
    )
    Args.add_argument('-ln', '--logger-name', default='hjalpari', help=(
        'Define logger name (Default: "hjalpari").'
    ))
    if len(sys.argv) == 1:
        print_help_and_exit()
    pargs = Args.parse_args()
    # main()
