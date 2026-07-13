# Compilation errors

This report is generated from per-sample `meta.json` records. API and
infrastructure failures are kept separate from model-generated Typst errors.

## Error classes

| Error class | Final failures |
|---|---:|
| `api_or_provider` | 1 |

## Failed samples

| Sample | Category | Attempts | Error class | Final error |
|---|---|---:|---|---|
| `01_prose_sections_001` | `01_prose_sections` | 1 | `api_or_provider` | OpenRouter HTTP 402: {"error":{"message":"Insufficient credits. This account never purchased credits. Make sure your key is on the correct account or org, and if so, purchase more at https://openrouter.ai/settings/credits","code":402}} |
