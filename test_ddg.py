from langchain_community.tools import DuckDuckGoSearchResults

search = DuckDuckGoSearchResults()

results = search.run("latest trends in Artificial Intelligence 2025")

print("Structured Results:\n")
print(results)
