"Utils for fpsql"

import ast


def safe_literal_eval(data: str):
    """# Function: safe_literal_eval
      Attempts to safely eval something through ast
    # Inputs:
      data: str - The data to eval

    # Returns:
      any - The evaluated data

    # Raises:
      None"""
    if data:
        try:
            return ast.literal_eval(data[0])
        except ValueError:
            return data[0]
    return None
