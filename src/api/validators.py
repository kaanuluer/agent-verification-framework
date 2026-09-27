"""
Agent Verification Framework - Input Validation Module
"""

from typing import Dict, Any, List, Optional
from .config import ValidationConfig


class ValidationError(Exception):
    """Custom validation error"""
    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


def validate_string_length(
    value: Optional[str],
    field_name: str,
    max_length: int,
    required: bool = True
) -> None:
    """Validate string length"""
    if value is None:
        if required:
            raise ValidationError(f"{field_name} is required", field_name)
        return
    
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string", field_name)
    
    if len(value) > max_length:
        raise ValidationError(
            f"{field_name} exceeds maximum length of {max_length}",
            field_name
        )


def validate_dict_size(
    value: Optional[Dict[str, Any]],
    field_name: str,
    max_keys: int,
    max_value_length: int
) -> None:
    """Validate dictionary size"""
    if value is None:
        return
    
    if not isinstance(value, dict):
        raise ValidationError(f"{field_name} must be a dictionary", field_name)
    
    if len(value) > max_keys:
        raise ValidationError(
            f"{field_name} exceeds maximum of {max_keys} keys",
            field_name
        )
    
    for key, val in value.items():
        if not isinstance(key, str):
            raise ValidationError(
                f"{field_name} keys must be strings",
                field_name
            )
        
        if isinstance(val, str) and len(val) > max_value_length:
            raise ValidationError(
                f"{field_name}[{key}] value exceeds maximum length of {max_value_length}",
                field_name
            )


def validate_list_size(
    value: Optional[List],
    field_name: str,
    max_items: int
) -> None:
    """Validate list size"""
    if value is None:
        return
    
    if not isinstance(value, list):
        raise ValidationError(f"{field_name} must be a list", field_name)
    
    if len(value) > max_items:
        raise ValidationError(
            f"{field_name} exceeds maximum of {max_items} items",
            field_name
        )


def validate_enum(
    value: Optional[str],
    field_name: str,
    allowed_values: set,
    required: bool = True
) -> None:
    """Validate enum value"""
    if value is None:
        if required:
            raise ValidationError(f"{field_name} is required", field_name)
        return
    
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string", field_name)
    
    value_upper = value.upper()
    if value_upper not in allowed_values:
        raise ValidationError(
            f"{field_name} must be one of: {', '.join(sorted(allowed_values))}",
            field_name
        )


def sanitize_string(value: str) -> str:
    """Sanitize string input"""
    if not isinstance(value, str):
        return value
    
    # Remove null bytes
    value = value.replace('\x00', '')
    
    # Strip leading/trailing whitespace
    value = value.strip()
    
    return value


def validate_intent_request(data: Dict[str, Any]) -> List[str]:
    """
    Validate intent verification request
    Returns list of validation errors
    """
    errors = []
    
    try:
        # Validate type
        validate_enum(
            data.get('type'),
            'type',
            ValidationConfig.ALLOWED_INTENT_TYPES,
            required=True
        )
    except ValidationError as e:
        errors.append(e.message)
    
    try:
        # Validate description
        validate_string_length(
            data.get('description'),
            'description',
            ValidationConfig.MAX_DESCRIPTION_LENGTH,
            required=True
        )
    except ValidationError as e:
        errors.append(e.message)
    
    try:
        # Validate target (optional)
        validate_string_length(
            data.get('target'),
            'target',
            ValidationConfig.MAX_TARGET_LENGTH,
            required=False
        )
    except ValidationError as e:
        errors.append(e.message)
    
    try:
        # Validate expected_outcome (optional)
        validate_string_length(
            data.get('expected_outcome'),
            'expected_outcome',
            ValidationConfig.MAX_DESCRIPTION_LENGTH,
            required=False
        )
    except ValidationError as e:
        errors.append(e.message)
    
    try:
        # Validate risk_level
        validate_enum(
            data.get('risk_level', 'MEDIUM'),
            'risk_level',
            ValidationConfig.ALLOWED_RISK_LEVELS,
            required=False
        )
    except ValidationError as e:
        errors.append(e.message)
    
    try:
        # Validate context (optional)
        validate_dict_size(
            data.get('context'),
            'context',
            ValidationConfig.MAX_CONTEXT_SIZE,
            ValidationConfig.MAX_CONTEXT_VALUE_LENGTH
        )
    except ValidationError as e:
        errors.append(e.message)
    
    try:
        # Validate level (optional)
        validate_enum(
            data.get('level', 'STANDARD'),
            'level',
            ValidationConfig.ALLOWED_VERIFICATION_LEVELS,
            required=False
        )
    except ValidationError as e:
        errors.append(e.message)
    
    return errors


def validate_action_request(data: Dict[str, Any]) -> List[str]:
    """
    Validate action verification request
    Returns list of validation errors
    """
    errors = []
    
    # Validate session_id
    if not data.get('session_id'):
        errors.append("session_id is required")
    
    # Validate intent
    intent_data = data.get('intent')
    if not intent_data:
        errors.append("intent is required")
    elif not isinstance(intent_data, dict):
        errors.append("intent must be a dictionary")
    else:
        intent_errors = validate_intent_request(intent_data)
        errors.extend([f"intent.{e}" for e in intent_errors])
    
    # Validate action
    action_data = data.get('action')
    if not action_data:
        errors.append("action is required")
    elif not isinstance(action_data, dict):
        errors.append("action must be a dictionary")
    else:
        try:
            # Validate action type
            validate_string_length(
                action_data.get('type'),
                'action.type',
                100,
                required=True
            )
        except ValidationError as e:
            errors.append(e.message)
        
        try:
            # Validate action description
            validate_string_length(
                action_data.get('description'),
                'action.description',
                ValidationConfig.MAX_DESCRIPTION_LENGTH,
                required=True
            )
        except ValidationError as e:
            errors.append(e.message)
        
        try:
            # Validate parameters (optional)
            validate_dict_size(
                action_data.get('parameters'),
                'action.parameters',
                ValidationConfig.MAX_PARAMETERS_SIZE,
                ValidationConfig.MAX_CONTEXT_VALUE_LENGTH
            )
        except ValidationError as e:
            errors.append(e.message)
        
        try:
            # Validate side_effects (optional)
            validate_list_size(
                action_data.get('side_effects'),
                'action.side_effects',
                ValidationConfig.MAX_SIDE_EFFECTS
            )
        except ValidationError as e:
            errors.append(e.message)
        
        # Validate success (optional, must be boolean)
        success = action_data.get('success', True)
        if not isinstance(success, bool):
            errors.append("action.success must be a boolean")
        
        # Validate duration_ms (optional, must be number)
        duration = action_data.get('duration_ms')
        if duration is not None and not isinstance(duration, (int, float)):
            errors.append("action.duration_ms must be a number")
    
    return errors
