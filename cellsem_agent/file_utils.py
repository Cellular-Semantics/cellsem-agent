import csv


def tsv_to_string(tsv):
    """Convert a TSV file to a string representation."""
    with open(tsv, newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        rows = list(reader)
        if not rows:
            return ""
        header = "\t".join(rows[0])
        body = "\n".join("\t".join(row) for row in rows[1:])
        return header + "\n" + body


def tsv_to_md_table(tsv):
    """Convert a TSV file to a Markdown table."""
    md_table = ""
    with open(tsv, newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        rows = list(reader)
        if rows:
            header = "| " + " | ".join(rows[0]) + " |"
            separator = "| " + " | ".join(['---'] * len(rows[0])) + " |"
            body = "\n".join("| " + " | ".join(row) + " |" for row in rows[1:])
            md_table = "\n".join([header, separator, body])
    print("TSV as Markdown table:\n" + md_table)
    return md_table
