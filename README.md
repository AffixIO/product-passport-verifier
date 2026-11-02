# Product passport verifier

Can an AI agent or a resale platform verify the evidence around a product without treating a photograph or a seller's claim as proof of authenticity?

This repository is a small, reviewable reference implementation for product passports. It models manufacturer attestation, distribution events, receipt matching, trusted issuers, revocation and tamper-evident provenance. It uses fictional Northstar products so the example does not impersonate or claim integration with Adidas, Nike, Jordan or any other brand.

## Five-minute quickstart

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install pytest
pytest -q
python demo.py
```

The demo should report `VERIFIED` for a fictional product whose identifier, provenance chain and simulated receipt all match.

## Verification states

- `VERIFIED`: trusted issuer, intact event chain, matching identifier and receipt.
- `PARTIAL`: evidence is intact but an issuer is unknown or receipt evidence is missing.
- `TAMPERED`: an event or its chain link no longer matches its digest.
- `MISMATCH`: the presented identifier or receipt belongs to another product.
- `REVOKED`: the product has been withdrawn by the configured revocation registry.

## What this can and cannot prove

This example verifies evidence supplied by an issuer. It does not prove physical authenticity from an image, establish legal ownership, replace brand security systems, or guarantee that a product is safe. In a real deployment, the brand or an authorised supply-chain participant must issue the underlying credentials and publish revocation information.

## AffixIO integration boundary

The core example is local and dependency-light. A production adapter could replace the local digest envelope with documented AffixIO SDK proof-generation and verification interfaces, pin approved issuers, and retain a minimal audit record. This repository intentionally does not invent SDK calls, handle private keys, call a live brand API, or process payments.

## Real-world integration path

1. A brand or authorised distributor issues a product passport.
2. Manufacture, transfer and recall events are appended to the passport chain.
3. A wallet, retailer or agent presents the product identifier and optional receipt evidence.
4. The verifier checks issuer trust, chain integrity, revocation and identifier binding.
5. The result is shown with its limitations, not reduced to an overconfident yes/no claim.

## Safety and privacy

Use pseudonymous product identifiers where possible. Do not put customer names, addresses, purchase histories, private keys or secret issuer material in a public passport. Fixture data in this repository is fictional.

## Status

Research example. Simulated only. Not affiliated with or endorsed by any footwear, apparel or retail brand.

## Contributing

Small tested improvements are welcome. Keep fixtures fictional, avoid trademark impersonation, and explain what each evidence source actually proves.

## License

MIT
