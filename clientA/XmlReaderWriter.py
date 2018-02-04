import xml.etree.ElementTree as ET
from xml.dom import minidom

file_name='CCTV_INFO.xml'
def create_xml(cctv_sources, cctv_descriptions):
    root=ET.Element('CCTV_INFO')
    i=0
    for source in cctv_sources:

        a=ET.SubElement(root,'CCTV')
        b=ET.SubElement(a,'CCTV_SOURCE').text=str(source)
        c=ET.SubElement(a,'CCTV_DESCRIPTION').text=cctv_descriptions[i]
        i=i+1
    tree=ET.ElementTree(root)
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open(file_name, "w") as f:
        f.write(xmlstr)
    print('CCTV INFO STORED')
def read_xml():
    cctv_sources=[]
    cctv_descriptions=[]
    tree = ET.parse(file_name)
    root=tree.getroot()

    for child in root:
        cctv_sources.append(child[0].text)
        cctv_descriptions.append(child[1].text)

    return cctv_sources,cctv_descriptions