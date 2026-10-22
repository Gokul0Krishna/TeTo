import os
from pathlib import Path
import fpdf as pdf

#___________________________General Tools___________________________


def _list_all_folders(base_dir: str) -> list[str]:
    """List all available folder paths under the specified base directory."""
    folder_paths = []
    for root, dirs, _ in os.walk(base_dir):
        for d in dirs:
            folder_paths.append(os.path.join(root, d))
    return folder_paths

#____________________________Essay Tools___________________________

def list_college_folders() -> list[str]:
    """List all available folder paths under ~/Desktop/temp/College."""
    base_dir = os.path.expanduser("~/Desktop/temp/College")
    
    # Ensure the base directory exists so os.walk doesn't fail
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
        return [base_dir]
    
    return _list_all_folders(base_dir)



def Create_pdf(content: str, filename: str) -> None:
    """Creates a PDF file with the given content and saves it to the specified filename.
    """
    pdf_doc = pdf.FPDF()
    pdf_doc.add_page()
    pdf_doc.set_font("Arial", size=12)
    pdf_doc.multi_cell(0, 10, content)
    pdf_doc.output(filename)



#___________________________Music Tools___________________________

def list_music_folders() -> list[str]:
    """List all available folder paths under /home/gokul/Music."""
    base_dir = os.path.expanduser("/home/gokul/Music")
    
    # Ensure the base directory exists so os.walk doesn't fail
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
        return [base_dir]
    
    return _list_all_folders(base_dir)

import yt_dlp

def music_download(url, output_folder):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_folder}/%(playlist_title|album|title)s/%(playlist_index)02d - %(title)s.%(ext)s',
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
            {'key': 'FFmpegMetadata'},
        ],
        'ignoreerrors': True,
        'download_archive': f'{output_folder}/archive.txt',  
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    findandcreatefolder("Test")