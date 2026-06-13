import os
import re
from pathlib import Path

FRONTEND_SRC = Path(__file__).resolve().parent.parent.parent / "frontend" / "src"

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    original_content = content

    # 1. Colors
    # Mostly replace dark bg with white, and light text with dark text
    content = content.replace('bg-slate-900', 'bg-white')
    content = content.replace('bg-slate-800', 'bg-gray-50')
    content = content.replace('bg-slate-700', 'bg-gray-100')
    content = content.replace('bg-gray-900', 'bg-white')
    content = content.replace('bg-gray-800', 'bg-gray-50')
    
    # Text colors
    content = content.replace('text-white', 'text-black')
    content = content.replace('text-slate-300', 'text-gray-800')
    content = content.replace('text-slate-400', 'text-gray-600')
    content = content.replace('text-gray-300', 'text-gray-800')
    content = content.replace('text-gray-400', 'text-gray-600')
    
    # Border colors
    content = content.replace('border-slate-800', 'border-gray-200')
    content = content.replace('border-slate-700', 'border-gray-300')
    
    # Accent buttons (keep some blue or just make them black? User said "very fewer rest colours")
    content = content.replace('bg-blue-600', 'bg-black text-white')
    content = content.replace('hover:bg-blue-700', 'hover:bg-gray-800')
    content = content.replace('text-blue-400', 'text-black font-bold')

    # 2. Section heights
    # Add min-h-screen to main sections (we can look for <section className=" and add min-h-screen if not there)
    # Actually, it's safer to just replace 'py-20' with 'min-h-screen py-20 flex flex-col justify-center'
    content = content.replace('py-20', 'min-h-screen py-20 flex flex-col justify-center')
    content = content.replace('py-16', 'min-h-screen py-16 flex flex-col justify-center')
    content = content.replace('py-24', 'min-h-screen py-24 flex flex-col justify-center')

    # 3. Navbar hover
    # User wanted "on hovering navbar option it has smooth change in backgroud color to black and text to white and some fraction of time for smooth ness"
    if 'Navbar.jsx' in filepath.name or 'MobileNav.jsx' in filepath.name:
        content = content.replace('hover:text-blue-400', 'transition-colors duration-300 hover:bg-black hover:text-white px-3 py-2')
        # fix duplicate px-3 py-2 if already there
        content = content.replace('px-3 py-2 px-3 py-2', 'px-3 py-2')

    # 4. Hero section headings
    if 'HeroSection.jsx' in filepath.name:
        content = content.replace('text-4xl sm:text-5xl md:text-6xl', 'text-6xl sm:text-7xl md:text-8xl lg:text-9xl')
        content = content.replace('text-5xl', 'text-7xl')
    
    # 5. Make Footer black
    if 'Footer.jsx' in filepath.name:
        # Revert the white background back to black for the footer
        content = content.replace('bg-white', 'bg-black')
        content = content.replace('text-black', 'text-white')
        content = content.replace('border-gray-200', 'border-gray-800')
        content = content.replace('text-gray-800', 'text-gray-300')

    # Fix button text being black on black if we changed bg-blue-600 to bg-black text-white
    content = content.replace('text-black text-white', 'text-white')

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)

def main():
    for root, _, files in os.walk(FRONTEND_SRC):
        for file in files:
            if file.endswith('.jsx'):
                process_file(Path(root) / file)

if __name__ == "__main__":
    main()
