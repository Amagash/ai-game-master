from setuptools import setup, find_packages

setup(
    name="ai_game_master",
    version="0.1",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        'streamlit',
        'boto3',
        'python-dotenv',
        'reportlab',
        'Pillow',
    ]
) 