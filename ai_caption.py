from openai import OpenAI

client = OpenAI()

prompt = input("Enter your content topic (e.g. fitness, real estate, AI): ")

response = client.responses.create(
    model="gpt-4.1-mini",
    input=f"Write 20 engaging social media captions about: {prompt}. Number each caption and keep them short, punchy, and viral."
)

print("\nCaptions:\n")
print(response.output_text)

with open("captions.txt", "w", encoding="utf-8") as f:
    f.write(response.output_text)

print("\nSaved to captions.txt ✅")