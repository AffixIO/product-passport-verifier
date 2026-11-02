import pytest
from passport import EvidenceEvent, ProductPassport, Verifier

def make_passport():
    pid = "northstar-001"
    first = EvidenceEvent.create("manufactured", "northstar-brand", pid, "2026-01-01", {"model": "Runner"})
    second = EvidenceEvent.create("distributed", "northstar-logistics", pid, "2026-01-02", {"destination": "retailer"}, first.event_digest)
    return ProductPassport.create(pid, "Runner", "Northstar", "northstar-brand", [first, second])

def test_verified_with_matching_receipt_and_identifier():
    p = make_passport(); r = Verifier({"northstar-brand", "northstar-logistics"}).verify(p, presented_id=p.product_id, receipt={"product_id": p.product_id})
    assert r.status == "VERIFIED"

def test_tampered_event_is_rejected():
    p = make_passport(); p.events[1].details["destination"] = "unknown"
    assert Verifier({"northstar-brand", "northstar-logistics"}).verify(p).status == "TAMPERED"

def test_unknown_issuer_is_partial_not_verified():
    p = make_passport(); assert Verifier(set()).verify(p).status == "PARTIAL"

def test_revoke_mismatch_and_missing_receipt():
    p = make_passport()
    assert Verifier({"northstar-brand"}, {p.product_id}).verify(p).status == "REVOKED"
    assert Verifier({"northstar-brand"}).verify(p, presented_id="other").status == "MISMATCH"
    assert Verifier({"northstar-brand", "northstar-logistics"}).verify(p).status == "PARTIAL"

def test_passport_must_start_with_manufacture():
    event = EvidenceEvent.create("distributed", "issuer", "x", "2026-01-01", {})
    with pytest.raises(ValueError): ProductPassport.create("x", "m", "b", "issuer", [event])
