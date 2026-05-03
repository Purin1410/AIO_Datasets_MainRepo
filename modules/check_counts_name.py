import re
from google.colab import auth
from googleapiclient.discovery import build
from collections import defaultdict

  # ─── AUTHENTICATE & BUILD DRIVE CLIENT ───────────────────────────────────────
auth.authenticate_user()
service = build('drive', 'v3', cache_discovery=False)

  # ─── CONFIGURATION ───────────────────────────────────────────────────────────
FOLDER_ID        = "1mSHOCx47KRQtKCDaI2JgOllkGvJM3HmI"
MAX_NUMBER       = 30   # xx  : 01–30
MAX_NUM_PER_GROUP = 4   # max images per (index, type) group → e.g. 01_c01_01…01_c01_04

PATTERN = re.compile(r'^(\d{3})_c(\d{2})_(\d{2})\.jpg$', re.IGNORECASE)

  # ─── FETCH ALL FILES IN FOLDER ────────────────────────────────────────────────
def list_files_in_folder(folder_id: str) -> list[str]:
    """Return all filenames inside the given Drive folder (handles pagination)."""
    filenames = []
    page_token = None
    query = f"'{folder_id}' in parents and trashed = false and mimeType != 'application/vnd.google-apps.folder'"

    while True:
        resp = service.files().list(
            q=query,
            fields="nextPageToken, files(name)",
            pageSize=1000,
            pageToken=page_token
        ).execute()

        filenames.extend(f['name'] for f in resp.get('files', []))
        page_token = resp.get('nextPageToken')
        if not page_token:
            break

    return sorted(filenames)

  # ─── VALIDATE ─────────────────────────────────────────────────────────────────
def validate_files(filenames: list[str]):
    errors          = []                    # (filename, reason)
    valid           = []                    # correctly named files
    groups          = defaultdict(list)     # (idx, typ) → [num, ...]

    for fname in filenames:

        # 1. Must be .jpg
        if not fname.lower().endswith('.jpg'):
            errors.append((fname, "Not a .jpg file"))
            continue

          # 2. Must match XX_cXX_xx.jpg
        m = PATTERN.match(fname)
        if not m:
            errors.append((fname, "Format mismatch – expected  XX_cXX_xx.jpg  (each part = 2 digits)"))
            continue

        idx, typ, num = int(m.group(1)), int(m.group(2)), int(m.group(3))

          # 3. Range checks
        if not (1 <= num <= MAX_NUMBER):
            errors.append((fname, f"Number {num:02d} out of range (01–{MAX_NUMBER:02d})"))
            continue

        groups[(idx, typ)].append(num)
        valid.append(fname)

      # 4. Sequence checks per (index, type) group
    sequence_errors = []
    for (idx, typ), nums in sorted(groups.items()):
        nums_sorted = sorted(nums)
        label = f"{idx:02d}_c{typ:02d}_*"

          # Duplicates
        if len(nums_sorted) != len(set(nums_sorted)):
            dupes = sorted({n for n in nums_sorted if nums_sorted.count(n) > 1})
            sequence_errors.append(f"  {label}  →  duplicate numbers: {[f'{n:02d}' for n in dupes]}")

          # Per-group max
        if len(nums_sorted) > MAX_NUM_PER_GROUP:
            extras = nums_sorted[MAX_NUM_PER_GROUP:]
            sequence_errors.append(
                f"  {label}  →  {len(nums_sorted)} files exceeds max {MAX_NUM_PER_GROUP} per group "
                f"(extra: {[f'{n:02d}' for n in extras]})"
            )

      # ─── PRINT REPORT ────────────────────────────────────────────────────────
    W = 62
    print(f"\n{'═'*W}")
    print(f"  📁  Folder ID : {FOLDER_ID}")
    print(f"  📄  Total files checked : {len(filenames)}")
    print(f"{'═'*W}\n")

    print("✅  VALID FILES")
    print("─" * W)
    if valid:
        for f in valid:
            print(f"   {f}")
    else:
        print("   (none)")

    print(f"\n❌  FORMAT / RANGE ERRORS  ({len(errors)})")
    print("─" * W)
    if errors:
        for fname, reason in errors:
            print(f"   {fname}")
            print(f"      ↳  {reason}")
    else:
        print("   ✔  none")

    print(f"\n⚠️   SEQUENCE ERRORS  ({len(sequence_errors)})")
    print("─" * W)
    if sequence_errors:
        for e in sequence_errors:
            print(e)
    else:
        print("   ✔  none – all groups are consecutive starting from _01")

    print(f"\n{'═'*W}")
    total = len(errors) + len(sequence_errors)
    if total == 0:
        print("  🎉  ALL FILES PASS – naming is fully correct.")
    else:
        print(f"  ❌  {total} issue(s) found. Please review above.")
    print(f"{'═'*W}\n")

  # ─── RUN ──────────────────────────────────────────────────────────────────────
filenames = list_files_in_folder(FOLDER_ID)
validate_files(filenames)