from components.base_component import BaseComponent
from components.shaft_component import ShaftComponent
from components.flange_component import FlangeComponent
from components.plate_component import PlateComponent
from components.lbracket_component import LBracketComponent
from components.ubracket_component import UBracketComponent
from components.housing_component import HousingComponent

from schemas.shaft_schema import ShaftParams
from schemas.flange_schema import FlangeParams
from schemas.plate_schema import PlateParams
from schemas.Lbracket_schema import LbracketParams
from schemas.ubracket_schema import UbracketParams
from schemas.housing_schema import HousingParams

class ComponentFactory:
    """
    Factory for creating and registering CAD components dynamically.
    Provides zero-code addition of future parts by allowing runtime registration.
    """
    REGISTRY = {
        "shaft": ShaftComponent,
        "flange": FlangeComponent,
        "plate": PlateComponent,
        "lbracket": LBracketComponent,
        "ubracket": UBracketComponent,
        "housing": HousingComponent,
    }

    SCHEMA_REGISTRY = {
        "shaft": ShaftParams,
        "flange": FlangeParams,
        "plate": PlateParams,
        "lbracket": LbracketParams,
        "ubracket": UbracketParams,
        "housing": HousingParams,
    }

    @classmethod
    def create(cls, type_str: str, **params) -> BaseComponent:
        """
        Instantiate a component by type string.
        Raises ValueError with clear message for unknown types.
        Before instantiation, validate params using the matching existing
        Pydantic schema (ShaftSchema, FlangeSchema, etc.) — same rules as
        the existing /api/{model}/generate endpoints.
        """
        if type_str not in cls.REGISTRY:
            raise ValueError(f"Unknown component type: '{type_str}'. Available types: {list(cls.REGISTRY.keys())}")
        
        # 1. Validate params against the existing Pydantic schema for this component.
        # This guarantees that the validation logic remains DRY and relies on a single source of truth.
        schema_class = cls.SCHEMA_REGISTRY.get(type_str)
        if schema_class:
            schema_class(**params)
            
        # 2. Instantiate the component using the validated params.
        component_class = cls.REGISTRY[type_str]
        return component_class(**params)

    @classmethod
    def register(cls, type_str: str, component_class, schema_class=None):
        """
        Register a new component type at runtime. One line to add future parts.
        This enables zero-code addition of new components to the factory without modifying existing code.
        """
        cls.REGISTRY[type_str] = component_class
        if schema_class:
            cls.SCHEMA_REGISTRY[type_str] = schema_class
