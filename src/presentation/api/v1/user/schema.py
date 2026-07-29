from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Annotated
from uuid import UUID

class UserCreateSchema(BaseModel):
    username: Annotated[
        str,
        Field(
            min_length=2,
            max_length=50,
            title="Username",
            description="Username to be displayed in the application.",
            examples=["João Victor", "John Valverde Brix"]
        )
    ]
    email: Annotated[
        EmailStr,
        Field(
            title="User Email",
            description="Email used to register and log in the application.",
            examples=["joao.victor@email.com", "noah.gravens123@email.com"]
        )
    ]
    password: Annotated[
        str,
        Field(
            min_length=8,
            title="User Password",
            description="Password to register and log in the application. It must have at least 8 caracters.",
            examples=["mypassword123", "@passeye"]
        )
    ]

class UserResponseSchema(BaseModel):
    id: Annotated[
        UUID,
        Field(
            title="User ID",
            description="User identifier in the application.", 
        )
    ]
    username: Annotated[
        str,
        Field(
            title="Username",
            description="Username to be displayed in the application.",
        )
    ]
    email: Annotated[
        EmailStr,
        Field(
            title="User Email",
            description="Email used to register and log in the application.",
        )
    ]
    is_active: Annotated[
        bool,
        Field(
            title="User Status",
            description="This shows if the User is active or deleted in the application."
        )
    ]

    model_config = ConfigDict(from_attributes=True)

class UserUpdateSchema(BaseModel):
    username: Annotated[
        str | None,
        Field(
            min_length=2,
            max_length=50,
            title="Username",
            description="Username to be displayed in the application.",
            examples=["João Victor", "John Valverde Brix"]
        )
    ] = None
    email: Annotated[
        EmailStr | None,
        Field(
            title="User Email",
            description="Email used to register and log in the application.",
            examples=["joao.victor@email.com", "noah.gravens123@email.com"]
        )
    ] = None
    password: Annotated[
        str | None,
        Field(
            min_length=8,
            title="User Password",
            description="Password to register and log in the application. It must have at least 8 caracters.",
            examples=["mypassword123", "@passeye"]
        )
    ] = None