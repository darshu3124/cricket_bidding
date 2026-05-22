import fitz
doc = fitz.open(r"C:\Users\HP\Downloads\bbhc league.pdf")
links = []
for page in doc:
    for link in page.get_links():
        if 'uri' in link:
            links.append(link['uri'])
print(f"Found {len(links)} links")
if links:
    print(links[:5])
