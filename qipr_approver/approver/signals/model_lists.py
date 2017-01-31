"""
This file just contains lists of different models so that
one can connect signals to them.
"""
from django.contrib.auth.models import User
from approver.models import *

AllNormalModels =[
    Address,
    BigAim,
    Category,
    Choice,
    ClinicalArea,
    ClinicalDepartment,
    ClinicalSetting,
    Contact,
    Expertise,
    Keyword,
    Organization,
    Person,
    Position,
    Project,
    QI_Interest,
    Question,
    Response,
    Section,
    Speciality,
    Suffix,
    Training,
    User,
]

# Nothing related to responses
AllRegistryModels = [
    # Address,
    # BigAim,
    # Category,
    # ClinicalArea,
    # ClinicalDepartment,
    # ClinicalSetting,
    # Contact,
    # Descriptor,
    # Expertise,
    # Keyword,
    # Organization,
    # Person,
    # Position,
    Project,
    # QI_Interest,
    # Self_Classification,
    # Speciality,
    # Suffix,
    # Training,
]
