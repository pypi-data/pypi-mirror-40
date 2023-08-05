import click
from IPython.display import display
from docx import Document


# Directory Listings

def directory_listing():
    import glob
    vals = []
    for filename in glob.glob("*." + 'docx'):
        vals.append(filename)
    return sorted(set(vals))

def display_directory_listing():
    display('\n'.join(directory_listing()))

# View the Doc
def doc_displayer(filename, p_num):
    my_text = Document(filename)
    alist = []
    for paragraph in my_text.paragraphs:
        if paragraph.text == "":
            pass
        else:
            alist.append(paragraph.text)
    display('\n'.join(alist[0:p_num]))
