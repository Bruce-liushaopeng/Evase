import openai


import openai
openai.api_key = "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"
print(openai.Completion.create(
  model="text-davinci-003",
  prompt="Why is SHA-2 a bad algorithm for hashing passwords?",
  max_tokens=250,
  temperature=0.1
))

