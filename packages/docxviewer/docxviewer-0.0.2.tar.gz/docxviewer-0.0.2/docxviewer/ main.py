import click
from IPython.display import display
from docx import Document
from docxviewer.doc_viewer import directory_listing, display_directory_listing, doc_displayer

@click.command()
@click.option('--select', '-select', default=3, help="Number of documents to display.")
@click.option('--p_num', '-p_num', default=3, help="Number of paragraphs to display.")
@click.option('--all', is_flag=True, help = "Raise flag to display preview of all doc files in the folder")
@click.option('--see', is_flag=True, help = "Raise flag to display all .docx files in the directory")
def output(select, p_num, all, see):
    if see:
        display_directory_listing()
    else:
        if all:
            filenames = directory_listing()
            for filename in filenames:
                print('\n',filename), doc_displayer(filename,p_num), print('\n')
        else:
            filenames = directory_listing()[0:select]
            for filename in filenames:
                print('\n',filename), doc_displayer(filename,p_num), print('\n')

def main():
    output(select,p_num,all,see)
