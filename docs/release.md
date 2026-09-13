# Public release contents

AoS-2024 is a fresh repository containing the previously prepared release and the public
intermediate research archive. It does not import the research workspace's Git history.

It includes the three reusable skills, complete 113-paper report, final
scientific data, per-paper intermediate records, grouping and audit stages, review histories,
library evidence, historical scripts and the current blog draft with its dashboard image.

PDFs, PDF page images, raw paper text/TeX copies, private execution files, local source
registries, environments and duplicate HTML generations are excluded. Source URLs and
PDF hashes remain. [Intermediate export details](intermediate-artifacts.md).

The final census/audit files retain their original bytes. The intermediate manifest records
source and export hashes for each file and identifies local-path substitutions. Historical
hashes embedded in those records are not rewritten to make redacted copies appear identical.

Run `python3 scripts/check_release.py` to check the file manifest, preserved scientific
hashes, intermediate export hashes, local HTML links and common private-data patterns.
The scan is not a guarantee of detecting every secret or mathematical error.

The [Zulip post](zulip-post.md) remains a draft. It has not been sent.
