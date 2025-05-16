from typing import Self
from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    """
    Base class for all Data Transfer Objects (DTOs), providing convenient helpers
    for validation, merging, and data dumping.

    Features:
    ---------
    - Enables merging multiple DTO instances into one via `.v(...)`
    - Provides `.d(recursive=True)` for flexible serialization
    - Uses `from_attributes=True` to support ORM integration

    Usage Example:
    --------------
        class A(BaseDTO):
            foo: str
        
        class B(BaseDTO):
            bar: int
        
        a = A(foo="hello")
        b = B(bar=123)

        class AB(BaseDTO):
            foo: str
            bar: int

        ab = AB.v(a, b)
        print(ab)  # -> AB(foo='hello', bar=123)
    """

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def v(cls, *data_transfer_objects: "BaseDTO", recursive: bool = True) -> Self:
        """
        Merge multiple DTO instances into one and validate as the current class.

        This method is useful when you have multiple partial DTOs and want to
        construct a single validated DTO instance from them.

        Parameters:
        -----------
        *data_transfer_objects : BaseDTO
            One or more DTO instances whose fields will be merged together.
        recursive : bool, default=True
            Whether to recursively serialize nested DTOs via `.d()` or keep them as-is.

        Returns:
        --------
        Self
            A new validated instance of the current DTO class.

        Example:
        --------
            class A(BaseDTO): foo: str
            class B(BaseDTO): bar: int
            class AB(BaseDTO): foo: str; bar: int

            ab = AB.v(A(foo="x"), B(bar=1))
            # -> AB(foo='x', bar=1)
        """
        overall_dump = {}
        for dto in data_transfer_objects:
            overall_dump |= dto.d(recursive=recursive)
        return cls.model_validate(overall_dump)

    def d(self, recursive: bool = True) -> dict:
        """
        Dump the DTO as a dictionary.

        Parameters:
        -----------
        recursive : bool, default=True
            If True, will apply `.d()` recursively on nested DTOs.
            If False, nested DTOs are returned as-is without serializing.

        Returns:
        --------
        dict
            A dictionary representation of the DTO suitable for validation,
            logging, or sending to other services.

        Example:
        --------
            class Child(BaseDTO): x: int
            class Parent(BaseDTO): child: Child

            p = Parent(child=Child(x=1))
            p.d()  # -> {'child': {'x': 1}} if recursive=True
                   # -> {'child': Child(x=1)} if recursive=False
        """
        data = self.model_dump()

        if recursive:
            for key, val in data.items():
                if isinstance(val, BaseDTO):
                    data[key] = val.d(recursive=True)

        return data
