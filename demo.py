from passport import EvidenceEvent, ProductPassport, Verifier

product_id = "northstar-runner-001"
events = [
    EvidenceEvent.create("manufactured", "northstar-brand", product_id, "2026-01-10T09:00:00Z", {"model": "Runner 01", "size": "9"}),
    EvidenceEvent.create("distributed", "northstar-logistics", product_id, "2026-01-15T09:00:00Z", {"destination": "northstar-retailer-01"}, None),
]
# Link the second event to the first, as a real issuer workflow would.
events[1] = EvidenceEvent.create("distributed", "northstar-logistics", product_id, "2026-01-15T09:00:00Z", {"destination": "northstar-retailer-01"}, events[0].event_digest)
passport = ProductPassport.create(product_id, "Runner 01", "Northstar", "northstar-brand", events)
report = Verifier({"northstar-brand", "northstar-logistics"}).verify(passport, presented_id=product_id, receipt={"product_id": product_id})
print({"mode": "simulation", "product": passport.model, "status": report.status, "checks": report.checks})
