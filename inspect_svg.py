import xml.etree.ElementTree as ET
import base64
import os

tree = ET.parse('F:/talentflow-ai/Main CV.svg')
root = tree.getroot()

print("SVG Tag:", root.tag)
print("SVG Attributes:", root.attrib)

ns = {'svg': 'http://www.w3.org/2000/svg', 'xlink': 'http://www.w3.org/1999/xlink'}

# Check images
images = root.findall('.//{http://www.w3.org/2000/svg}image')
print(f"Total embedded images: {len(images)}")
for i, img in enumerate(images):
    href = img.attrib.get('{http://www.w3.org/1999/xlink}href') or img.attrib.get('href', '')
    x = img.attrib.get('x')
    y = img.attrib.get('y')
    w = img.attrib.get('width')
    h = img.attrib.get('height')
    print(f"Image {i}: pos=({x}, {y}) size=({w}x{h}) data_len={len(href)}")
    if href.startswith('data:image'):
        header, b64data = href.split(',', 1)
        ext = 'png' if 'png' in header else 'jpg' if 'jpeg' in header or 'jpg' in header else 'bin'
        img_bytes = base64.b64decode(b64data)
        out_path = f"F:/talentflow-ai/data/extracted_image_{i}.{ext}"
        with open(out_path, 'wb') as f:
            f.write(img_bytes)
        print(f"  Saved image {i} to {out_path} ({len(img_bytes)} bytes)")

# Check text elements
texts = root.findall('.//{http://www.w3.org/2000/svg}text')
print(f"\nTotal text elements: {len(texts)}")
sample_texts = []
for t in texts:
    txt = "".join(t.itertext()).strip()
    if txt:
        sample_texts.append(txt)

print("First 20 text snippets:")
for st in sample_texts[:20]:
    print(" -", repr(st))
