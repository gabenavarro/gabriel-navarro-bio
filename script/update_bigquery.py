'''
Submit a BigQuery job to run a query.

This script parses a Markdown file to extract metadata and body content, generates a BigQuery INSERT statement, and submits it to BigQuery.
It uses the BigQueryClient class to handle the submission and execution of the query.

'''
import argparse
import ast
import uuid
from pathlib import Path
import uuid
import os
from typing import List, Dict, Any
from google.cloud import bigquery



def update_bq_row(
    data: List[Dict[str, Any]],
    full_table_id: str
) -> None:
    """
    Update existing BigQuery rows in `full_table_id` by matching on 'id'.
    All other fields in each dict will be overwritten where id == dict['id'].
    """
    client = bigquery.Client.from_service_account_json(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )

    # sanity check
    if not all("id" in row for row in data):
        raise ValueError("All rows must have an 'id' key.")

    # pull only the existing IDs
    ids = [row["id"] for row in data]
    id_list = ",".join(f"'{i}'" for i in ids)
    check_sql = f"""
    SELECT id
    FROM `{full_table_id}`
    WHERE id IN ({id_list})
    """
    existing = {r.id for r in client.query(check_sql).result()}
    if not existing:
        raise ValueError("No existing rows found for the provided IDs.")

    # now update each one
    for row in data:
        if row["id"] not in existing:
            continue

        sql = f"""
        UPDATE `{full_table_id}` 
        SET
          title       = @title,
          date        = @date,
          tags        = @tags,
          body        = @body,
          views       = @views,
          likes       = @likes,
          image       = @image,
          description = @description,
          `type`      = @type
        WHERE id = @id
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("title",       "STRING", row["title"]),
                bigquery.ScalarQueryParameter("date",        "TIMESTAMP",   row["date"]),
                bigquery.ArrayQueryParameter( "tags",        "STRING", row["tags"]),
                bigquery.ScalarQueryParameter("body",        "STRING", row["body"]),
                bigquery.ScalarQueryParameter("views",       "INT64",  row["views"]),
                bigquery.ScalarQueryParameter("likes",       "INT64",  row["likes"]),
                bigquery.ScalarQueryParameter("image",       "STRING", row["image"]),
                bigquery.ScalarQueryParameter("description", "STRING", row["description"]),
                bigquery.ScalarQueryParameter("type",        "STRING", row["type"]),
                bigquery.ScalarQueryParameter("id",          "STRING", row["id"]),
            ]
        )

        client.query(sql, job_config=job_config).result()


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
    lines = path.read_text(encoding='utf-8').splitlines(keepends=True)
    if not lines or not lines[0].startswith('@{'):
        raise ValueError("File does not start with a frontmatter dictionary.")
    
    # Locate end of frontmatter
    end_idx = next((i for i, ln in enumerate(lines) if ln.strip() == '}'), None)
    if end_idx is None:
        raise ValueError("Closing '}' for frontmatter not found.")
    
    fm_lines = lines[:end_idx+1]
    body_lines = lines[end_idx+1:]
    
    # Extract inner lines (between @{ and })
    inner = []
    for i, ln in enumerate(fm_lines):
        if i == 0:
            # Strip '@{' prefix
            rest = ln[len('@{'):].rstrip('\n')
            if rest.strip():
                inner.append(rest)
        elif i < end_idx:
            inner.append(ln.rstrip('\n'))
    metadata = {}
    for ln in inner:
        ln_strip = ln.strip()
        if not ln_strip or '=' not in ln_strip:
            continue
        key, val = ln_strip.split('=', 1)
        key = key.strip()
        val = val.strip()
        # Safely evaluate the value (string or list)
        try:
            metadata[key] = ast.literal_eval(val)
        except Exception:
            metadata[key] = val.strip()
    
    # Combine body
    body = ''.join(body_lines)
    metadata['body'] = body
    
    # If 'id' is present, ensure it's a string
    if 'id' in metadata:
        print(f"Found 'id': {metadata['id']}")
        if isinstance(metadata['id'], str):
            metadata['id'] = metadata['id'].strip('"')
        else:
            raise ValueError("'id' must be a string.")

    # If missing 'id', generate and rewrite file
    if 'id' not in metadata:
        new_id = str(uuid.uuid4())
        metadata['id'] = new_id

        metadata["image"] = f"https://storage.googleapis.com/{bucket}/images/{new_id}.svg"
        
        def fmt_val(v):
            if isinstance(v, str):
                return f'"{v}"'
            if isinstance(v, list):
                return '[' + ', '.join(f'"{item}"' for item in v) + ']'
            return str(v)
        
        # Order keys: id first, then other metadata (excluding 'body')
        ordered = ['id'] + [k for k in metadata if k not in ('id', 'body')]
        
        # Build new frontmatter
        fm_out = []
        # First line
        first_key = ordered[0]
        fm_out.append(f'@{{{first_key} = {fmt_val(metadata[first_key])}\n')
        # Remaining lines
        for key in ordered[1:]:
            if key == "tags":
                fm_out.append(f'  {key} = {metadata[key]}\n')
            else:
                fm_out.append(f'  {key} = {fmt_val(metadata[key])}\n')
        fm_out.append('}\n')
        
        # Write back updated file (metadata frontmatter + original body)
        with path.open('w', encoding='utf-8') as f:
            f.writelines(fm_out)
            f.writelines(body_lines)

    # Assert all keys are now in metadata
    required_keys = ['id', 'title', 'tags', 'date', 'body', 'views', 'likes', 'image', 'description', 'type']
    for key in required_keys:
        if key not in metadata:
            raise ValueError(f"Missing required metadata key: {key}")

    # Report to console all keys found
    print("Metadata keys found:", ', '.join(metadata.keys()))    
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
    update_bq_row(data=data,full_table_id=table)
   

parser = argparse.ArgumentParser(description="Submit a BigQuery job.")
parser.add_argument("--markdown_file", type=str, required=True, help="Path to the Markdown file.")
parser.add_argument("--table", type=str, default="noble-office-299208.portfolio.gn-blog", help="BigQuery table to write results.")

if __name__ == "__main__":
    args = parser.parse_args()
    main(args.markdown_file, args.table)