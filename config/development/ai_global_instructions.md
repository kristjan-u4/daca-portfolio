# AI Development Framework & Project Constraints

You are acting as an expert Python developer in this repository. To ensure maintainability, consistency, and alignment with the local environment, you must strictly follow the rules and constraints described in this file.

## Code Structure & The Step-Down Rule

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

- **Mandatory Docstrings:** Every function, class, and public method MUST include a clear, professional docstring that explains its purpose, arguments (`Args`), and return values (`Returns`). Whenever you perform changes in existing code, always ensure that docstrings remain relevant and update them if necessary.
- **Language Constraint:** All code documentation — including docstrings and architectural comments and all string literals — must be written exclusively in **English**. 
- **Strictly Ban Inline Explanations:** Do NOT add inline comments to modified or added lines to explain the git diff or the change itself (e.g., ban comments like `# Use the newly created week_label for x-axis`). The logic inside the function must remain clean and uncluttered.
- **String Literal Quoting:** Use double quotes (`"strings"`) as the default for all string literals. Single quotes (`'strings'`) are strictly reserved for situations where you need to nest a string within another string (e.g., `"f-string with 'nested' quotes"` or HTML attributes).

## Environment and Dependencies

- Check the `.python-version` file in the root directory to ensure code generation is strictly compatible with the specified Python version.
- Always check the `requirements.out` file in the root directory to verify installed Python package versions before writing imports or using specific library APIs.
- Do not assume newer or older API syntaxes than what is strictly installed in the environment.

## File Operations & Git Safety
- **Strictly Prohibit Raw Move/Delete Commands:** Do NOT generate or execute raw shell commands (like `mv`, `rm`, `cp`) to move, rename, or delete files that are tracked by Git.
- **Mandatory Git Operations:** You MUST use official Git operations (`git mv` for moving/renaming and `git rm` for deleting) to preserve file history and ensure changes are properly staged.
- **Safety First:** If you cannot perform the move using Git commands directly, ask the user for clarification instead of falling back to raw OS-level commands.

## Coding Philosophy: Fail-Fast over Defensive Programming

* **No Masking of Internal Logic:** For internal system states, calculated variables, or configuration lookups (e.g., dictionaries), do not provide generic fallbacks or default values to prevent crashes.
* **Let it Crash:** If a value or key is missing due to a developer error, the application must fail immediately and loudly (e.g., raise `KeyError`, `ValueError`, etc.). 
* **Avoid Duplication:** Avoid duplicating structures inside fallback mechanisms (like `dict.get(key, default_structure)`). Prefer direct lookups like `dict[key]` to ensure strict compliance with defined configurations.
