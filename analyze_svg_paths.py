import xml.etree.ElementTree as ET

tree = ET.parse('F:/talentflow-ai/Main CV.svg')
root = tree.getroot()

for i, p in enumerate(root.findall('.//{http://www.w3.org/2000/svg}path')):
    fill = p.attrib.get('fill', '')
    stroke = p.attrib.get('stroke', '')
    if fill in ['#e2e8f0', '#06b6d4', '#0097a7', '#0f172a'] or stroke:
        d = p.attrib.get('d', '')
        print(f"Path {i}: fill={fill} stroke={stroke} len_d={len(d)} d={repr(d[:80])}")
