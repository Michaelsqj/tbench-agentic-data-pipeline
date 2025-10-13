You are preparing compliance evidence for an infrastructure audit. Create an executable Bash script at `tools/generate_package_inventory.sh` that inspects the current container and writes a CSV report to `artifacts/package_inventory.csv`.

Requirements:
- The CSV must contain the header `package,version,installation_state,recorded_at`.
- Include every package reported by `dpkg-query` with its version.
- Mark `installation_state` as `manual` when `apt-mark showmanual` lists the package, otherwise `auto`.
- Use a single ISO-8601 UTC timestamp for `recorded_at`, apply it to every row, and echo the same value to stdout.
- Sort rows alphabetically by package name and overwrite the CSV on each run.
- Fail fast with a clear error message if required commands are unavailable.
