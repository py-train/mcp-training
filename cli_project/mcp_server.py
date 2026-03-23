from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(
    "read_doc",
    description="Reads the content of a document given its ID.",
)
def read_doc(
    doc_id: str = Field(description="The ID of the document to read.")
) -> str:
    return docs.get(doc_id, "Not found!")


# TODO: Write a tool to edit a doc
@mcp.tool(
    "edit_doc",
    description="Edits the content of a document given its ID.",
)
def edit_doc(
    doc_id: str = Field(description="The ID of the document to edit."),
    original_content: str = Field(description="The original content of the document."),
    changed_content: str = Field(description="The new content for the document.")
) -> str:
    docs[doc_id] = docs.get(doc_id, "Not found!").replace(original_content, changed_content)
    return "Document updated successfully."


# TODO: Write a resource to return all doc id's
@mcp.resource(
    "docs://documents",
    mime_type="application/json",
    description="Lists all document IDs."
)
def list_docs() -> list[str]:
    return list(docs.keys())


# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",
    description="Returns the contents of a particular document."
)
def get_doc(doc_id: str) -> str:
    return docs.get(doc_id, "Not found!")


# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name='format',
    description="Rewrites the contents of a document formatted as markdown."
)
def format_document(
    doc_id: str = Field(description="The ID of the document to format.")
) -> list[base.Message]:
    prompt = f'''
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary.
    Use the 'edit_document' tool to save changes to the document.
    '''

    return [base.UserMessage(content=prompt)]

# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
