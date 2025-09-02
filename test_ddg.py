from langchain_community.tools import DuckDuckGoSearchResults

# Create search tool (structured results)
search = DuckDuckGoSearchResults()

# Example: search for AI trends 2025
results = search.run("latest trends in Artificial Intelligence 2025")

print("Structured Results:\n")
print(results)
