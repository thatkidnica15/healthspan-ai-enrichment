from enrichment.tavily_researcher import TavilyResearcher

print("Starting test...")

researcher = TavilyResearcher()

result = researcher.research_contact(
    "Diogo Barardo",
    "NOVOS Labs",
    "Director of R&D"
)

print("RESULT:")
print(repr(result))