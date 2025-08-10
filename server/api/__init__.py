from api.structure import APIStructure
from api.endpoint import APIEndpoint
from api.endpoint import APIPath

basic_structure = APIStructure("api")
basic_structure.endpoints = [
    APIEndpoint(
        name="read",
        method="POST",
        body_structure={"path": str}        
    ),
    APIEndpoint(
        name="write",
        method="PUT",
        body_structure={
            "path": str,
            "data": str,
            "hash": str
        }
    ),
    APIEndpoint(
        name="copy",
        method="PUT",
        body_structure={
            "path": {
                "source": str,
                "dest": str
            }
        }
    ),
    APIEndpoint(
        name="move",
        method="PUT",
        body_structure={
            "path": {
                "source": str,
                "dest": str
            }
        }
    ),
    APIEndpoint(
        name="file",
        method="POST",
        body_structure={
            "path": str,
        },
        parent=APIPath("create")
    ),
    APIEndpoint(
        name="dir",
        method="POST",
        body_structure={
            "path": str,
        },
        parent=APIPath("create")
    )
]