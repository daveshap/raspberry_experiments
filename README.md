# Raspberry Experiments

Mission: Create an open source finetuning dataset that allows anyone to train AI models to engage in "Test Time Comput" or chain of thought reasoning. 

## Process

For starters, OpenAI GPT-4o only needs 50 to 100 samples to get started. We can demonstrate success by simply improving what the base model does. For instance, if the base GPT-4o scores 25% on a given benchmark, but we can boost that to 32% with a simple finetuning job, that is a solid proof of concept. So our goal is simply to create a statistically significant lift in performance. 

1. We need some high quality queries that would be realistic from a user perspective. These can be synthesized easily enough. 
2. We need some high quality chains of thought (reasoning) as the answer. Ideally they would be correct answers, but most importantly we just need to train the model to use reasoning. 