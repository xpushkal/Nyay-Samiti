# Legal Data Package
# Contains Constitution of India, IPC, CrPC and other legal datasets

from .constitution import ConstitutionService, CONSTITUTION_ARTICLES, WRITS, FUNDAMENTAL_DUTIES, SCHEDULES
from .legal_terms import LEGAL_GLOSSARY

__all__ = [
    "ConstitutionService",
    "CONSTITUTION_ARTICLES", 
    "WRITS",
    "FUNDAMENTAL_DUTIES",
    "SCHEDULES",
    "LEGAL_GLOSSARY"
]
