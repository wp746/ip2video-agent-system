# Contributing

Keep the system modular:

- Put orchestration logic in `src/core/`.
- Put production-stage logic in `src/pipelines/`.
- Put final document formatting in `src/output/`.
- Put style and universe assumptions in `templates/` and `universe/`.
- Add examples whenever a pipeline behavior changes.

Before committing:

```bash
python -m src.main --input examples/sprout_guardian_input.yaml
python scripts/validate_production_package.py output/小芽守护者_30s_prompt_pack
```
