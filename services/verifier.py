from services.web_search import search_web

def verify_claims(claims):
    results = []

    for claim in claims:
        search_results = search_web(claim)

        if not search_results:
            results.append({
                "claim": claim,
                "status": "False",
                "evidence": "No credible sources found."
            })
            continue

        snippets = " ".join([r["content"] for r in search_results])

        if any(word in snippets.lower() for word in claim.lower().split()):
            status = "Verified"
        else:
            status = "Inaccurate"

        results.append({
            "claim": claim,
            "status": status,
            "evidence": snippets[:500] + "..."
        })

    return results
