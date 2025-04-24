class PromptTemplate:
    """
    A class to represent a prompt template for generating text.
    """

    def __init__(self, template: str):
        """
        Initialize the PromptTemplate with a given template string.

        Args:
            template (str): The template string for the prompt.
        """
        self.template = template

    def format(self, **kwargs) -> str:
        """
        Generate a prompt by filling in the template with provided keyword arguments.

        Args:
            **kwargs: Keyword arguments to fill in the template.

        Returns:
            str: The generated prompt.
        """
        return self.template.format(**kwargs)