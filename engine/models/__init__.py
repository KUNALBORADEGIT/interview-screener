# engine/models/__init__.py

# Add future models here 👇
from .candidate import Candidate
from .recommendation import Recommendation
from .interview import Interview
from .question import Question
from .jobdescription import JobDescription
from .jdtoqs import JDToQS

# dynamic import using `importlib`👇
import os
import importlib

models_dir = os.path.dirname(__file__)
for file in os.listdir(models_dir):
    if file.endswith(".py") and file not in ["__init__.py", "base_class.py"]:
        module_name = f"engine.models.{file[:-3]}"
        importlib.import_module(module_name)
