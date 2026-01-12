"""
Submit a BigQuery job to run a query.

This script parses a Markdown file to extract metadata and body content, generates a BigQuery INSERT statement, and submits it to BigQuery.
It uses the BigQueryClient class to handle the submission and execution of the query.

"""

import argparse
import ast
import uuid
from pathlib import Path
import os
from typing import Sequence, Mapping, Any
from google.cloud import bigquery


def upload_to_bq(data: Sequence[Mapping[str, Any]], full_table_id: str) -> None:
    """
    Upload a list of rows to BigQuery.
    """
    rows = [dict(row) for row in data]

    client = bigquery.Client.from_service_account_json(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    # Check bigquery if `id` is already present
    query = f"""
    SELECT id FROM `{full_table_id}` WHERE id IN ({",".join([f"'{row['id']}'" for row in rows])})
    """
    query_job = client.query(query)
    existing_ids = {row["id"] for row in query_job.result()}
    # Filter out rows with existing IDs
    rows = [row for row in rows if row["id"] not in existing_ids]
    if not rows:
        print("No new rows to insert.")
        return

    errors = client.insert_rows_json(full_table_id, rows)
    if errors:
        raise RuntimeError(f"Errors inserting rows: {errors}")


def parse_markdown_file(filepath: str, bucket: str = "gn-portfolio") -> dict:
    """
    Parse a Markdown file whose first lines define a metadata dictionary in the format:
    @{key = "value"
      key2 = ["list", "of", "tags"]
      ...
    }
    The rest of the file is treated as the body. Returns a dict of metadata with an added
    "body" key containing the Markdown body text. If the metadata lacks an "id" key,
    a new UUID is generated, inserted into the metadata, and the file is rewritten
    with the updated frontmatter (metadata only) followed by the original body.

    :param filepath: Path to the Markdown file.
    :return: Dictionary of metadata including "body" (and "id", if newly added).
    """
    path = Path(filepath)
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if not lines or not lines[0].startswith("@{"):
        raise ValueError("File does not start with a frontmatter dictionary.")

    # Locate end of frontmatter
    end_idx = next((i for i, ln in enumerate(lines) if ln.strip() == "}"), None)
    if end_idx is None:
        raise ValueError("Closing '}' for frontmatter not found.")

    fm_lines = lines[: end_idx + 1]
    body_lines = lines[end_idx + 1 :]

    # Extract inner lines (between @{ and })
    inner = []
    for i, ln in enumerate(fm_lines):
        if i == 0:
            # Strip '@{' prefix
            rest = ln[len("@{") :].rstrip("\n")
            if rest.strip():
                inner.append(rest)
        elif i < end_idx:
            inner.append(ln.rstrip("\n"))
    metadata = {}
    for ln in inner:
        ln_strip = ln.strip()
        if not ln_strip or "=" not in ln_strip:
            continue
        key, val = ln_strip.split("=", 1)
        key = key.strip()
        val = val.strip()
        # Safely evaluate the value (string or list)
        try:
            metadata[key] = ast.literal_eval(val)
        except Exception:
            metadata[key] = val.strip()

    # Combine body
    body = "".join(body_lines)
    metadata["body"] = body

    # If 'id' is present, ensure it's a string
    if "id" in metadata:
        print(f"Found 'id': {metadata['id']}")
        if isinstance(metadata["id"], str):
            metadata["id"] = metadata["id"].strip('"')
        else:
            raise ValueError("'id' must be a string.")

    # If missing 'id', generate and rewrite file
    if "id" not in metadata:
        new_id = str(uuid.uuid4())
        metadata["id"] = new_id

        def fmt_val(v):
            if isinstance(v, str):
                return f'"{v}"'
            if isinstance(v, list):
                return "[" + ", ".join(f'"{item}"' for item in v) + "]"
            return str(v)

        # Order keys: id first, then other metadata (excluding 'body')
        ordered = ["id"] + [k for k in metadata if k not in ("id", "body")]

        # Build new frontmatter
        fm_out = []
        # First line
        first_key = ordered[0]
        fm_out.append(f"@{{{first_key} = {fmt_val(metadata[first_key])}\n")
        # Remaining lines
        for key in ordered[1:]:
            if key == "tags":
                fm_out.append(f"  {key} = {metadata[key]}\n")
            else:
                fm_out.append(f"  {key} = {fmt_val(metadata[key])}\n")
        fm_out.append("}\n")

        # Write back updated file (metadata frontmatter + original body)
        with path.open("w", encoding="utf-8") as f:
            f.writelines(fm_out)
            f.writelines(body_lines)

    # Assert all keys are now in metadata
    required_keys = [
        "id",
        "title",
        "tags",
        "date",
        "body",
        "views",
        "likes",
        "image",
        "description",
        "type",
        "disabled",
    ]
    for key in required_keys:
        if key not in metadata:
            raise ValueError(f"Missing required metadata key: {key}")

    # Report to console all keys found
    print("Metadata keys found:", ", ".join(metadata.keys()))
    return metadata


def main(
    path: str,
    table: str = "noble-office-299208.portfolio.gn-blog",
) -> None:
    """
    Submit a BigQuery job to run a query.

    Args:
        project_id (str): The GCP project ID.
        dataset_id (str): The BigQuery dataset ID.
        table_id (str): The BigQuery table ID.
        job_id (str): The job ID for the BigQuery job.
        query (str): The SQL query to run.
        location (str, optional): The location for the BigQuery job. Defaults to "US".
    """
    # Parse the Markdown file to extract metadata
    data = [parse_markdown_file(path)]
    upload_to_bq(data=data, full_table_id=table)


parser = argparse.ArgumentParser(description="Submit a BigQuery job.")
parser.add_argument(
    "--markdown_file", type=str, required=True, help="Path to the Markdown file."
)
parser.add_argument(
    "--table",
    type=str,
    default="noble-office-299208.portfolio.gn-blog",
    help="BigQuery table to write results.",
)

if __name__ == "__main__":
    args = parser.parse_args()
    main(args.markdown_file, args.table)
