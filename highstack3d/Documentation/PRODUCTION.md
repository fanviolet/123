# Production handoff

The native 3D gameplay, procedural 3D asset pipeline and Android build are self-contained. The following cannot be truthfully finalized without publisher-owned accounts/secrets:

1. Final Android package ownership and Play App Signing key.
2. AdMob app/ad-unit IDs and consent configuration.
3. Google Play Billing product creation, prices and backend purchase validation.
4. Google Play Games Services OAuth and leaderboard ID.
5. Privacy policy URL and Play Console Data safety declarations.
6. Optional server authority / Play Integrity checks for top Ranked scores.

The test APK deliberately simulates ads/purchases and marks synthetic leaderboard users as `Rival` rather than pretending they are human users. Ranked mode ignores purchased gameplay boosts and ad revive so leaderboard play is not pay-to-win.
