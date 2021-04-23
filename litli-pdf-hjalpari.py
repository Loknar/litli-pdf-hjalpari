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


def print_help_and_exit(code=1):
    if Args is not None:
        Args.print_help(sys.stderr)
    else:
        logman.error('Args was None, exiting ..')
    sys.exit(code)


def formatSize(sizeInBytes, decimalNum=1, isUnitWithI=False, sizeUnitSeperator=' '):
    '''look who's lazy: https://stackoverflow.com/a/53567149/2401628'''
    sizeUnitList = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']
    largestUnit = 'Y'
    if isUnitWithI:
        sizeUnitListWithI = []
        for curIdx, eachUnit in enumerate(sizeUnitList):
            unitWithI = eachUnit
            if curIdx >= 1:
                unitWithI += 'i'
            sizeUnitListWithI.append(unitWithI)
        sizeUnitList = sizeUnitListWithI
        largestUnit += 'i'
    suffix = 'B'
    decimalFormat = '.' + str(decimalNum) + 'f'  # '.1f'
    finalFormat = '%' + decimalFormat + sizeUnitSeperator + '%s%s'  # '%.1f%s%s'
    sizeNum = sizeInBytes
    for sizeUnit in sizeUnitList:
        if abs(sizeNum) < 1024.0:
            return finalFormat % (sizeNum, sizeUnit, suffix)
        sizeNum /= 1024.0
    return finalFormat % (sizeNum, largestUnit, suffix)


def main(arguments):
    if 'init_logger' in arguments and arguments['init_logger'] is True:
        logman.init(
            arguments['logger_name'], role=arguments['role'], output_dir=arguments['log_directory']
        )
    # input_file, handle relative path location if being run through bash/powershell script
    if os.path.isabs(arguments['input_file']):
        input_file = arguments['input_file']
    elif 'LITLI_HJALPARI_CURRENT_DIR' in os.environ:
        input_file = os.path.join(
            os.environ['LITLI_HJALPARI_CURRENT_DIR'], arguments['input_file']
        )
    else:
        input_file = arguments['input_file']
    # output_file, handle relative path location if being run through bash/powershell script
    if os.path.isabs(arguments['output_file']):
        output_file = arguments['output_file']
    elif 'LITLI_HJALPARI_CURRENT_DIR' in os.environ:
        output_file = os.path.join(
            os.environ['LITLI_HJALPARI_CURRENT_DIR'], arguments['output_file']
        )
    else:
        output_file = arguments['output_file']
    if arguments['overwrite'] is False and os.path.exists(output_file):
        logman.error('Output file already exists, use flag --overwrite to overwrite.')
        sys.exit(1)
    tesseract_lang = None
    if arguments['language'] in pytesseract.get_languages():
        tesseract_lang = arguments['language']
    elif arguments['language'] is not None:
        logman.warning((
            'Provided language identifier "%s" not available according to tesseract CLI, language '
            'options available are: %s. Check your Tesseract setup if you think a language is '
            'missing that should be available. Using default language setting ("osd").' % (
                arguments['language'],
                ', '.join(['"%s"' % (lang, ) for lang in pytesseract.get_languages()])
            )
        ))
    file_size = None
    try:
        file_size = os.path.getsize(input_file)
    except FileNotFoundError:
        logman.error('File "%s" not found.' % (arguments['input_file'], ))
        sys.exit(1)
    file_size_h = formatSize(file_size)
    input_filename = os.path.basename(input_file)
    logman.info('Filename: "%s".' % (input_filename, ))
    logman.info('File size: %s.' % (file_size_h, ))
    if input_filename[-4:].lower() != '.pdf':
        logman.warning('Filename does not seem to have a PDF file extension.')
        input_filename_only = input_filename
    else:
        input_filename_only = input_filename[:-4]
    try:
        in_file_pdf_info = pdf2image.pdfinfo_from_path(input_file)
    except pdf2image.exceptions.PDFPageCountError:
        logman.error(
            'Unable to read page count from "%s", are you sure it\'s a valid pdf file?' % (
                input_filename,
            )
        )
        sys.exit(1)
    page_count = in_file_pdf_info['Pages']
    logman.info('Page count: %s.' % (page_count, ))

    out_pdfs_filepaths = []
    out_pagenumber = 1
    for page_number in range(1, page_count + 1):
        images = []
        logman.info('Converting original page %s to image object ..' % (page_number, ))
        page_image = pdf2image.convert_from_path(
            input_file, first_page=page_number, last_page=page_number
        )[0]
        if arguments['cut_pages_horizontally'] is True:
            logman.info('Splitting page horizontally to two pages ..')
            upper_half = page_image.crop(
                (0, 0, page_image.width, int(page_image.height / 2))
            )
            lower_half = page_image.crop(
                (0, int(page_image.height / 2) + 1, page_image.width, page_image.height)
            )
            if arguments['rotate_counter_clockwise'] is True:
                logman.info('Rotating pages counter clockwise ..')
                upper_half = upper_half.rotate(90, expand=True)
                lower_half = lower_half.rotate(90, expand=True)
            elif arguments['rotate_clockwise'] is True:
                logman.info('Rotating pages clockwise ..')
                upper_half = upper_half.rotate(-90, expand=True)
                lower_half = lower_half.rotate(-90, expand=True)
            elif arguments['rotate_flip'] is True:
                logman.info('Flipping pages 180 degrees ..')
                upper_half = upper_half.rotate(180, expand=True)
                lower_half = lower_half.rotate(180, expand=True)
            if arguments['cut_pages_horizontally_reverse'] is True:
                logman.info('Lower part of splitted page comes first ..')
                images.append(lower_half)
                images.append(upper_half)
            else:
                images.append(upper_half)
                images.append(lower_half)
        else:
            if arguments['rotate_counter_clockwise'] is True:
                logman.info('Rotating page counter clockwise ..')
                images.append(page_image.rotate(90, expand=True))
            elif arguments['rotate_clockwise'] is True:
                logman.info('Rotating page clockwise ..')
                images.append(page_image.rotate(-90, expand=True))
            elif arguments['rotate_flip'] is True:
                logman.info('Flipping page 180 degrees ..')
                images.append(page_image.rotate(180, expand=True))
            else:
                images.append(page_image)
        output_dir = os.path.join('temp', input_filename_only, 'pages')
        if not os.path.exists(output_dir):
            logman.info('Creating temporary files folder "%s" ..' % (output_dir, ))
            os.makedirs(output_dir)
        for image in images:
            filename = 'page_{:03d}.pdf'.format(out_pagenumber)
            filepath = os.path.join(output_dir, filename)
            logman.info('Making page %s searchable ..' % (out_pagenumber, ))
            pdf = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang=tesseract_lang)
            with open(filepath, 'w+b') as outfile:
                outfile.write(pdf)  # pdf type is bytes by default
            out_pdfs_filepaths.append(filepath)
            logman.info('Searchable page %s written to file "%s".' % (out_pagenumber, filepath))
            out_pagenumber += 1

    logman.info('Merging all %s pages to single file ..' % (out_pagenumber - 1, ))
    merger = PyPDF2.PdfFileMerger()
    for pdf_filepath in out_pdfs_filepaths:
        merger.append(pdf_filepath)
    merged_filepath = os.path.join(output_file)
    merger.write(merged_filepath)
    merger.close()
    logman.info('Output written to file "%s".' % (output_file, ))

    logman.info('Done.')


if __name__ == '__main__':
    Args = argparse.ArgumentParser(
        description='Litli PDF Hjálpari', formatter_class=argparse.RawTextHelpFormatter,
        prog='litli-pdf-hjalpari'
    )
    Args.add_argument('-i', '--input-file', metavar=('INPUT_FILE', ), required=True, help=(
        'Input PDF file.'
    ))
    Args.add_argument('-o', '--output-file', metavar=('OUTPUT_FILE', ), required=True, help=(
        'Output PDF file.'
    ))
    Args.add_argument('-ow', '--overwrite', action='store_true', help=(
        'Overwrite output file if exists.'
    ))
    Args.add_argument('-del', '--delete-page-files', action='store_true', help=(
        'Delete individual page files which are generated when textifying PDF files.'
    ))
    Args.add_argument('-lang', '--language', default=None, help=(
        'Language code for Tesseract to use.'
    ))
    Args.add_argument('-cph', '--cut-pages-horizontally', action='store_true', help=(
        'Separate each page horizontally into two pages, top half first.'
    ))
    Args.add_argument('-cphr', '--cut-pages-horizontally-reverse', action='store_true', help=(
        'Separate each page horizontally into two pages, bottom half first.'
    ))
    Args.add_argument('-rc', '--rotate-clockwise', action='store_true', help=(
        'Rotate each page clockwise.'
    ))
    Args.add_argument('-rcc', '--rotate-counter-clockwise', action='store_true', help=(
        'Rotate each page counterclockwise.'
    ))
    Args.add_argument('-flip', '--rotate-flip', action='store_true', help=(
        'Rotate each page 180 degrees.'
    ))
    Args.add_argument('-ln', '--logger-name', default='hjalpari', help=(
        'Define logger name (Default: "hjalpari").'
    ))
    Args.add_argument('-ldir', '--log-directory', default='./logs/', help=(
        'Directory to write logs in. Default: "./logs/".'
    ))
    Args.add_argument('-r', '--role', default='cli', help=(
        'Define runner role. (Default: "cli")\n'
        'Available options: "cli", "api", "cron", "hook".'
    ))
    #
    if len(sys.argv) == 1:
        print_help_and_exit(code=0)
    pargs = Args.parse_args()
    arguments = {
        'init_logger': False,
        'logger_name': pargs.logger_name,
        'log_directory': pargs.log_directory,
        'role': pargs.role,
        'input_file': pargs.input_file,
        'output_file': pargs.output_file,
        'overwrite': pargs.overwrite,
        'delete_page_files': pargs.delete_page_files,
        'language': pargs.language,
        'cut_pages_horizontally': (
            pargs.cut_pages_horizontally or pargs.cut_pages_horizontally_reverse
        ),
        'cut_pages_horizontally_reverse': pargs.cut_pages_horizontally_reverse,
        'rotate_clockwise': pargs.rotate_clockwise,
        'rotate_counter_clockwise': pargs.rotate_counter_clockwise,
        'rotate_flip': pargs.rotate_flip
    }
    logman.init(
        arguments['logger_name'], role=arguments['role'], output_dir=arguments['log_directory']
    )
    main(arguments)
