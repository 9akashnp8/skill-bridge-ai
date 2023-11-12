from typing import List
from langchain.docstore.document import Document
from langchain.document_loaders.markdown import UnstructuredMarkdownLoader

from .models import TopicInfo


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


def group_topic_info(docs: List[Document]) -> List[TopicInfo]:
    result = []
    title_docs = [doc for doc in docs if doc.metadata["category"] == "Title"]
    child_docs = [doc for doc in docs if "parent_id" in doc.metadata]
    for doc in title_docs:
        topic_info = TopicInfo(
            id=doc.metadata["id"],
            title=doc.page_content,
            info="".join(
                child.page_content
                for child in child_docs
                if child.metadata["parent_id"] == doc.metadata["id"]
            ),
        )
        result.append(topic_info)
    return result


def get_topic_infos(source: str, **kwargs) -> List[TopicInfo]:
    mock = kwargs.get("mock", None)
    if mock:
        source = "README.md"
    loader = CustomMarkdownLoader(source, mode="elements")
    data = loader.load()
    material = group_topic_info(data)
    return material
