from typing import List
from langchain.docstore.document import Document
from langchain.document_loaders.markdown import UnstructuredMarkdownLoader

class CustomMarkdownLoader(UnstructuredMarkdownLoader):
    """
    Custom loader that loads Markdown and groups "child"
    content to their "parents".
    """
    def _get_elements(self):
        elements = super()._get_elements()
        for el in elements:
            setattr(el.metadata, "id", el.id)
        return elements

    def _group_docs(self, docs: List[Document]):
        result = []
        for doc in docs:
            parent = {}
            if doc.metadata["category"] == "Title":
                parent["id"] = doc.metadata["id"]
                parent["title"] = doc.page_content
                parent["children"] = [
                    {"content": child.page_content, "parent_id": child.metadata["parent_id"]}
                    for child in docs
                    if "parent_id" in child.metadata
                    and child.metadata["parent_id"] == doc.metadata["id"]
                ]
                result.append(parent)
        return result

    def load(self) -> List:
        docs =  super().load()
        return self._group_docs(docs)

def get_material(source: str, **kwargs):
    mock = kwargs.get("mock", None)
    if mock:
        source = "README.md"
    loader = CustomMarkdownLoader(source, mode="elements")
    data = loader.load()
    return data
