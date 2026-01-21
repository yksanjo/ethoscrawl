"""
Privacy Layer for EthosCrawl

Privacy-preserving techniques for ethical data collection.
This module provides differential privacy, anonymization, and other
privacy-preserving transformations for scraped data.
"""

import hashlib
import random
import re
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class PrivacyLevel(Enum):
    """Privacy preservation levels"""
    MINIMAL = "minimal"      # Basic anonymization
    STANDARD = "standard"    # GDPR compliance
    STRICT = "strict"        # Differential privacy
    MAXIMUM = "maximum"      # Federated learning only


@dataclass
class PrivacyConfig:
    """Configuration for privacy preservation"""
    level: PrivacyLevel = PrivacyLevel.STANDARD
    epsilon: float = 1.0          # For differential privacy (lower = more private)
    add_noise: bool = True        # Whether to add noise to numerical data
    anonymize_text: bool = True   # Whether to anonymize text fields
    hash_sensitive: bool = True   # Whether to hash sensitive identifiers


class PrivacyEngine:
    """
    Privacy-preserving engine for ethical data collection.
    
    This engine applies various privacy-preserving transformations
    to scraped data to protect individual privacy while maintaining
    data utility for analysis.
    """
    
    # Common PII patterns
    PII_PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b(\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b',
    }
    
    # Common sensitive field names
    SENSITIVE_FIELDS = {
        'email', 'phone', 'telephone', 'mobile', 'cell',
        'ssn', 'social_security', 'national_id',
        'credit_card', 'card_number', 'payment',
        'address', 'street', 'city', 'zip', 'postal',
        'birth_date', 'dob', 'age',
        'ip', 'ip_address', 'user_id', 'username',
    }
    
    def __init__(self, config: Optional[PrivacyConfig] = None):
        """
        Initialize the privacy engine.
        
        Args:
            config: Privacy configuration settings
        """
        self.config = config or PrivacyConfig()
        self._sensitive_cache: Dict[str, str] = {}
        logger.info(f"PrivacyEngine initialized with level: {self.config.level.value}")
    
    def apply_privacy(self, data: Union[Dict, List], context: Optional[Dict] = None) -> Any:
        """
        Apply privacy-preserving transformations to data.
        
        Args:
            data: The data to transform (dict, list, or primitive)
            context: Additional context for privacy decisions
            
        Returns:
            Privacy-preserved data
        """
        if context is None:
            context = {}
        
        if self.config.level == PrivacyLevel.MINIMAL:
            return self._basic_anonymization(data, context)
        elif self.config.level == PrivacyLevel.STANDARD:
            return self._gdpr_compliant(data, context)
        elif self.config.level == PrivacyLevel.STRICT:
            return self._differential_privacy(data, context)
        elif self.config.level == PrivacyLevel.MAXIMUM:
            return self._maximum_privacy(data, context)
        else:
            return self._basic_anonymization(data, context)
    
    def _basic_anonymization(self, data: Any, context: Dict) -> Any:
        """Basic PII removal and anonymization"""
        if isinstance(data, dict):
            return self._anonymize_dict(data, context, basic=True)
        elif isinstance(data, list):
            return [self._basic_anonymization(item, context) for item in data]
        elif isinstance(data, str):
            return self._anonymize_string(data, basic=True)
        else:
            return data
    
    def _gdpr_compliant(self, data: Any, context: Dict) -> Any:
        """GDPR-compliant data processing"""
        if isinstance(data, dict):
            return self._anonymize_dict(data, context, gdpr=True)
        elif isinstance(data, list):
            return [self._gdpr_compliant(item, context) for item in data]
        elif isinstance(data, str):
            return self._anonymize_string(data, gdpr=True)
        else:
            # Apply noise to numerical values for GDPR
            if isinstance(data, (int, float)) and self.config.add_noise:
                return self._add_gaussian_noise(data, scale=0.1)
            return data
    
    def _differential_privacy(self, data: Any, context: Dict) -> Any:
        """Apply differential privacy techniques"""
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                # Check if this is a sensitive field
                if self._is_sensitive_field(key):
                    result[key] = self._apply_dp_to_value(value, key)
                else:
                    result[key] = self._differential_privacy(value, context)
            return result
        elif isinstance(data, list):
            # For lists, we need to be careful with differential privacy
            if all(isinstance(item, (int, float)) for item in data):
                # Numerical list - apply DP to the whole list
                return self._apply_dp_to_list(data)
            else:
                # Mixed list - process each item
                return [self._differential_privacy(item, context) for item in data]
        elif isinstance(data, (int, float)):
            return self._apply_dp_to_numeric(data)
        elif isinstance(data, str):
            return self._anonymize_string(data, differential=True)
        else:
            return data
    
    def _maximum_privacy(self, data: Any, context: Dict) -> Any:
        """Maximum privacy preservation (for federated learning)"""
        # For maximum privacy, we only return aggregated statistics
        # or heavily anonymized data
        
        if isinstance(data, dict):
            # Only keep non-sensitive fields with heavy anonymization
            result = {}
            for key, value in data.items():
                if not self._is_sensitive_field(key):
                    anonymized = self._maximum_privacy(value, context)
                    if anonymized is not None:
                        result[key] = anonymized
            return result if result else None
        elif isinstance(data, list):
            # For lists, return only count and basic stats
            if len(data) > 0:
                numeric_data = [item for item in data if isinstance(item, (int, float))]
                if numeric_data:
                    return {
                        'count': len(data),
                        'numeric_count': len(numeric_data),
                        'has_non_numeric': len(data) > len(numeric_data)
                    }
                else:
                    return {'count': len(data)}
            return {'count': 0}
        elif isinstance(data, (int, float)):
            # Return bucketed value
            return self._bucket_value(data)
        elif isinstance(data, str):
            # Return only string length and hash
            return {
                'length': len(data),
                'hash': self._hash_value(data),
                'is_pii': self._contains_pii(data)
            }
        else:
            return None
    
    def _anonymize_dict(self, data: Dict, context: Dict, **kwargs) -> Dict:
        """Anonymize a dictionary based on privacy level"""
        result = {}
        
        for key, value in data.items():
            # Check if this is a sensitive field
            if self._is_sensitive_field(key):
                # Apply appropriate anonymization
                if kwargs.get('basic', False):
                    result[key] = self._hash_value(str(value))
                elif kwargs.get('gdpr', False):
                    result[key] = self._gdpr_anonymize(key, value)
                elif kwargs.get('differential', False):
                    result[key] = self._apply_dp_to_value(value, key)
                else:
                    result[key] = '[REDACTED]'
            else:
                # Recursively process non-sensitive fields
                if isinstance(value, dict):
                    result[key] = self._anonymize_dict(value, context, **kwargs)
                elif isinstance(value, list):
                    result[key] = [self._anonymize_dict(item, context, **kwargs) 
                                  if isinstance(item, dict) else item 
                                  for item in value]
                elif isinstance(value, str):
                    result[key] = self._anonymize_string(value, **kwargs)
                else:
                    result[key] = value
        
        return result
    
    def _anonymize_string(self, text: str, **kwargs) -> str:
        """Anonymize a string based on privacy level"""
        if not text or not isinstance(text, str):
            return text
        
        # Check for PII patterns
        if self._contains_pii(text):
            if kwargs.get('basic', False):
                # Basic: replace with generic placeholder
                return '[ANONYMIZED]'
            elif kwargs.get('gdpr', False):
                # GDPR: hash the PII parts
                return self._redact_pii(text, hash=True)
            elif kwargs.get('differential', False):
                # Differential privacy: heavy redaction
                return self._redact_pii(text, hash=False, redact=True)
            else:
                return '[REDACTED]'
        
        # If no PII, return as-is or with light processing
        return text
    
    def _contains_pii(self, text: str) -> bool:
        """Check if text contains PII"""
        if not isinstance(text, str):
            return False
        
        text_lower = text.lower()
        
        # Check for sensitive field names in the text
        for field in self.SENSITIVE_FIELDS:
            if field in text_lower:
                return True
        
        # Check for PII patterns
        for pattern_name, pattern in self.PII_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _redact_pii(self, text: str, hash: bool = False, redact: bool = True) -> str:
        """Redact or hash PII in text"""
        result = text
        
        # Replace email addresses
        result = re.sub(
            self.PII_PATTERNS['email'],
            '[EMAIL]' if not hash else f'[EMAIL:{self._hash_value(text)}]',
            result
        )
        
        # Replace phone numbers
        result = re.sub(
            self.PII_PATTERNS['phone'],
            '[PHONE]' if not hash else f'[PHONE:{self._hash_value(text)}]',
            result
        )
        
        return result
    
    def _is_sensitive_field(self, field_name: str) -> bool:
        """Check if a field name indicates sensitive data"""
        field_lower = field_name.lower()
        
        # Check exact matches and partial matches
        for sensitive_field in self.SENSITIVE_FIELDS:
            if (sensitive_field == field_lower or 
                sensitive_field in field_lower or 
                field_lower in sensitive_field):
                return True
        
        return False
    
    def _hash_value(self, value: Any) -> str:
        """Create a deterministic hash of a value"""
        if value is None:
            return 'null'
        
        value_str = str(value)
        
        # Use cache to ensure same value always hashes to same result
        if value_str in self._sensitive_cache:
            return self._sensitive_cache[value_str]
        
        # Create hash with salt for additional security
        salt = "ethoscrawl_privacy_salt"
        hash_obj = hashlib.sha256(f"{salt}:{value_str}".encode())
        hash_result = hash_obj.hexdigest()[:16]  # Use first 16 chars
        
        self._sensitive_cache[value_str] = hash_result
        return hash_result
    
    def _gdpr_anonymize(self, field_name: str, value: Any) -> Any:
        """Apply GDPR-specific anonymization"""
        if isinstance(value, str):
            if self._contains_pii(value):
                return self._hash_value(value)
            return value
        elif isinstance(value, (int, float)):
            if self.config.add_noise:
                return self._add_gaussian_noise(value, scale=0.05)
            return value
        else:
            return '[GDPR_REDACTED]'
    
    def _apply_dp_to_value(self, value: Any, field_name: str) -> Any:
        """Apply differential privacy to a value"""
        if isinstance(value, (int, float)):
            return self._apply_dp_to_numeric(value)
        elif isinstance(value, str):
            # For strings, we can't easily apply DP, so we hash
            return self._hash_value(value)
        elif isinstance(value, bool):
            # For booleans, we can use randomized response
            return self._randomized_response(value)
        else:
            return '[DP_REDACTED]'
    
    def _apply_dp_to_numeric(self, value: Union[int, float]) -> float:
        """Apply differential privacy to a numeric value"""
        if not self.config.add_noise:
            return float(value)
        
        # Add Laplace noise for differential privacy
        scale = 1.0 / self.config.epsilon if self.config.epsilon > 0 else 1.0
        noise = self._laplace_noise(scale)
        
        return float(value) + noise
    
    def _apply_dp_to_list(self, values: List[Union[int, float]]) -> List[float]:
        """Apply differential privacy to a list of numeric values"""
        if not values:
            return []
        
        # Calculate sensitivity (max - min)
        if len(values) > 1:
            sensitivity = max(values) - min(values)
        else:
            sensitivity = 1.0
        
        # Add noise proportional to sensitivity
        scale = sensitivity / self.config.epsilon if self.config.epsilon > 0 else sensitivity
        noisy_values = [float(v) + self._laplace_noise(scale) for v in values]
        
        return noisy_values
    
    def _laplace_noise(self, scale: float) -> float:
        """Generate Laplace noise for differential privacy"""
        u = random.uniform(-0.5, 0.5)
        return -scale * (1 if u < 0 else -1) * (1 - 2 * abs(u))
    
    def _add_gaussian_noise(self, value: float, scale: float = 0.1) -> float:
        """Add Gaussian noise to a value"""
        noise = random.gauss(0, scale * abs(value) if value != 0 else scale)
        return float(value) + noise
    
    def _randomized_response(self, value: bool) -> bool:
        """Apply randomized response for boolean values"""
        if not value:
            return False
        
        # With probability p, tell the truth; with probability 1-p, lie
        p = 0.75  # Truth probability
        return random.random() < p
    
    def _bucket_value(self, value: float) -> str:
        """Bucket a numeric value for maximum privacy"""
        if value < 0:
            return "negative"
        elif value == 0:
            return "zero"
        elif value < 10:
            return "small"
        elif value < 100:
            return "medium"
        elif value < 1000:
            return "large"
        else:
            return "very_large"
    
    def get_privacy_report(self, data_before: Any, data_after: Any) -> Dict:
        """Generate a privacy transformation report"""
        return {
            "privacy_level": self.config.level.value,
            "epsilon": self.config.epsilon,
            "transformations_applied": self._count_transformations(data_before, data_after),
            "noise_added": self.config.add_noise,
        }
    
    def _count_transformations(self, before: Any, after: Any) -> int:
        """Count the number of transformations applied"""
        # Simplified implementation
        if before == after:
            return 0
        return 1


# Example usage
def example():
    """Example usage of PrivacyEngine"""
    # Sample data with PII
    sample_data = {
        "user": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-123-4567",
            "age": 35,
            "salary": 75000.50
        },
        "metadata": {
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0"
        }
    }
    
    print("Original data:")
    print(json.dumps(sample_data, indent=2))
    
    # Test different privacy levels
    for level in PrivacyLevel:
        print(f"\n--- {level.value.upper()} Privacy ---")
        config = PrivacyConfig(level=level)
        engine = PrivacyEngine(config)
        
        anonymized = engine.apply_privacy(sample_data)
        print(json.dumps(anonymized, indent=2))
        
        report = engine.get_privacy_report(sample_data, anonymized)
        print(f"Privacy report: {report}")


if __name__ == "__main__":
    import json
    example()