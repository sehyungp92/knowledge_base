# Global Model Routing

This command is handled directly by the Python gateway.

- `/model` shows the current global default model tier.
- `/model fast`, `/model balanced`, and `/model deep` switch the global tier.
- `/model haiku`, `/model sonnet`, and `/model opus` are supported aliases for the same tiers.

Do not call external tools for this command.
