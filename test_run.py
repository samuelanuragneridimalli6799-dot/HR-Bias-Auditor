from auditor import audit_job_posting

# A realistic job post packed with common bias markers:
sample_text = """
We are looking for a rockstar digital native who can aggressively dominate our competitors. 
The ideal candidate graduated with an elite degree within the last 3 years, has native English fluency, 
and exhibits relentless energy and stamina to thrive in a high-pressure 60+ hour work week.
"""

print("Running compliance & bias audit with Gemini...")
result = audit_job_posting(job_title="Senior Growth Marketer", text=sample_text)

print("\n" + "=" * 50)
print(f"FAIRNESS SCORE : {result['overall_fairness_score']} / 100")
print(f"RISK LEVEL     : {result['risk_level']}")
print("=" * 50)
print(f"\nEXECUTIVE SUMMARY:\n{result['summary']}")

print("\nIDENTIFIED FLAGS & PROXIES:")
for i, flag in enumerate(result['flags'], start=1):
    print(f"\n{i}. [{flag['category']}] \"{flag['flagged_phrase']}\"")
    print(f"   Reason: {flag['explanation']}")
    print(f"   Neutral Alternative: {flag['suggested_replacement']}")

print("\n" + "=" * 50)
print("INCLUSIVE REWRITE SUGGESTION:")
print("=" * 50)
print(result['inclusive_rewrite'])