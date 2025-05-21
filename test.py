from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("pdfs/Cours_5_Polymere_autonomie.pdf")
pages = loader.load()
print(pages[0].page_content)
