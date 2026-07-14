# Hermes FCOS RPM

Private, purpose-built release pipeline for native Hermes Agent on Fedora CoreOS.

The workflow resolves only the latest upstream GitHub Release tag, builds a noarch Fedora RPM in a Fedora container, verifies the RPM payload, publishes it as a GitHub release asset, and records the upstream source revision. It never builds from the moving upstream `main` branch.

The RPM is intended to be layered into a derived FCOS image. It installs Hermes under `/usr/lib/hermes-agent`, a launcher at `/usr/bin/hermes`, and a dedicated native systemd service is supplied by the consuming host repository. Mutable state and secrets are deliberately outside the RPM.
