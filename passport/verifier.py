from __future__ import annotations
from dataclasses import dataclass, asdict
from hashlib import sha256
import json

def digest(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

@dataclass(frozen=True)
class EvidenceEvent:
    kind: str
    issuer: str
    subject: str
    timestamp: str
    details: dict
    event_digest: str
    previous_digest: str | None = None

    @classmethod
    def create(cls, kind: str, issuer: str, subject: str, timestamp: str, details: dict, previous_digest: str | None = None):
        body = {"kind": kind, "issuer": issuer, "subject": subject, "timestamp": timestamp, "details": details, "previous_digest": previous_digest}
        return cls(kind, issuer, subject, timestamp, details, digest(body), previous_digest)

@dataclass(frozen=True)
class ProductPassport:
    product_id: str
    model: str
    brand: str
    issued_by: str
    events: tuple[EvidenceEvent, ...]
    passport_digest: str

    @classmethod
    def create(cls, product_id: str, model: str, brand: str, issued_by: str, events: list[EvidenceEvent]):
        if not events or events[0].kind != "manufactured":
            raise ValueError("a passport must begin with a manufacture event")
        if any(event.subject != product_id for event in events):
            raise ValueError("every event must identify the same product")
        body = {"product_id": product_id, "model": model, "brand": brand, "issued_by": issued_by,
                "events": [asdict(event) for event in events]}
        return cls(product_id, model, brand, issued_by, tuple(events), digest(body))

@dataclass(frozen=True)
class VerificationReport:
    status: str
    checks: tuple[str, ...]
    warnings: tuple[str, ...]

class Verifier:
    def __init__(self, trusted_issuers: set[str], revoked_products: set[str] | None = None):
        self.trusted_issuers = trusted_issuers
        self.revoked_products = revoked_products or set()

    def verify(self, passport: ProductPassport, *, presented_id: str | None = None, receipt: dict | None = None) -> VerificationReport:
        checks, warnings = [], []
        if passport.product_id in self.revoked_products:
            return VerificationReport("REVOKED", ("product-revocation",), ())
        if presented_id is not None and presented_id != passport.product_id:
            return VerificationReport("MISMATCH", ("presented-identifier",), ("The scanned identifier does not match the passport.",))
        if passport.issued_by not in self.trusted_issuers:
            warnings.append("passport issuer is not in the configured trust list")
        previous = None
        for event in passport.events:
            expected = EvidenceEvent.create(event.kind, event.issuer, event.subject, event.timestamp, event.details, previous).event_digest
            if event.previous_digest != previous or event.event_digest != expected:
                return VerificationReport("TAMPERED", tuple(checks), ("The evidence chain has been altered.",))
            previous = event.event_digest
            checks.append(event.kind)
        if receipt:
            if receipt.get("product_id") != passport.product_id:
                return VerificationReport("MISMATCH", tuple(checks), ("Receipt product does not match the passport.",))
            checks.append("receipt-match")
        else:
            warnings.append("no receipt evidence was supplied")
        if warnings:
            return VerificationReport("PARTIAL", tuple(checks), tuple(warnings))
        return VerificationReport("VERIFIED", tuple(checks), ())
