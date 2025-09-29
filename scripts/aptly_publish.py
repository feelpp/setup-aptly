#!/usr/bin/env python3
"""
Mock aptly_publish.py script for testing the setup-aptly action.
This simulates the real aptly_publish.py behavior for CI testing.
"""

import argparse
import logging
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Mock aptly publish script for testing")
    parser.add_argument("--component", required=True)
    parser.add_argument("--distro", default="noble")
    parser.add_argument("--channel", default="stable")
    parser.add_argument("--debs", required=True)
    parser.add_argument("--pages-repo", required=True)
    parser.add_argument("--branch", default="gh-pages")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--sign", action="store_true")
    parser.add_argument("--keyid", default=None)
    parser.add_argument("--passphrase", default=None)
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    
    logging.info("Mock aptly_publish.py started")
    logging.info("Component: %s", args.component)
    logging.info("Distribution: %s", args.distro)
    logging.info("Channel: %s", args.channel)
    logging.info("Debs path: %s", args.debs)
    logging.info("Pages repo: %s", args.pages_repo)
    logging.info("Signing: %s", "yes" if args.sign else "no")
    
    # Verify .deb files exist
    debs_path = Path(args.debs)
    if not debs_path.exists():
        logging.error("Debs path does not exist: %s", debs_path)
        sys.exit(1)
    
    deb_files = list(debs_path.glob("*.deb"))
    if not deb_files:
        logging.error("No .deb files found in: %s", debs_path)
        sys.exit(1)
    
    logging.info("Found %d .deb files", len(deb_files))
    for deb in deb_files:
        logging.info("  - %s", deb.name)
    
    # Simulate aptly operations
    logging.info("Mock: Creating aptly repository...")
    logging.info("Mock: Adding packages to repository...")
    logging.info("Mock: Creating snapshot...")
    logging.info("Mock: Publishing snapshot...")
    
    if args.sign:
        if not args.keyid:
            logging.error("GPG key ID required for signing")
            sys.exit(1)
        logging.info("Mock: Signing repository with key %s", args.keyid)
    
    logging.info("Mock: Syncing to pages repository...")
    logging.info("Mock: Publishing completed successfully")
    
    print(f"Mock publish completed for {args.component} ({args.distro}/{args.channel})")

if __name__ == "__main__":
    main()