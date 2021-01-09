import os

PROJECT_NAME = "eks-cicd-template"
REPOSITORY_PATH = os.path.realpath(__file__)[:os.path.realpath(__file__).find(PROJECT_NAME)]
PROJECT_PATH = os.path.join(REPOSITORY_PATH, PROJECT_NAME)

JWT_SECRET = os.environ.get('JWT_SECRET')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
