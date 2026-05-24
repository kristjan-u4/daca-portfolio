# Python Code Style Rules

When creating or modifying Python scripts, always follow these Clean Code structure principles:

## Step-Down Rule (The Newspaper Metaphor):
   - Public/main functions and high-level logic must be defined at the top of the file.
   - Private helper functions (methods starting with an underscore `_`) must always be placed below the main functions that call them.
   - Readability order: A reader should be able to read the source code from top to bottom, following the high-level flow before getting into implementation details.

### Function Ordering Example
```python
   def main_function():
       # High-level logic
       _helper_one()
       _helper_two()

   def _helper_one():
       # Implementation detail

   def _helper_two():
       # Implementation detail
```

## Code Style & Documentation Rules

- **Mandatory Docstrings:** Every function, class, and public method MUST include a clear, professional docstring that explains its purpose, arguments (`Args`), and return values (`Returns`).
- **Language Constraint:** All code documentation—including docstrings and architectural comments—must be written exclusively in **English**. 
- **Strictly Ban Inline Explanations:** Do NOT add inline comments to modified or added lines to explain the git diff or the change itself (e.g., ban comments like `# Use the newly created week_label for x-axis`). The logic inside the function must remain clean and uncluttered.
- **String Literal Quoting:** Use double quotes (`"strings"`) as the default for all string literals. Single quotes (`'strings'`) are strictly reserved for situations where you need to nest a string within another string (e.g., `"f-string with 'nested' quotes"` or HTML attributes).
