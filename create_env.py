#!/usr/bin/env python3

# Create .env file with OpenAI API key
api_key = "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"

with open('.env', 'w', encoding='utf-8') as f:
    f.write(f'OPENAI_API_KEY={api_key}')

print("✅ .env file created successfully!")
print(f"API key length: {len(api_key)}") 