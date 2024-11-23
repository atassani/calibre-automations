# calibre-automations

## Goodread automations

After exporting my whole book library from Goodreads into `goodreads_library_export.csv`, this script updated my personal Calibre library with its reviews.

Export is done from "My Books" and in "Tools", in the menu at the bottom left, "Import and export".

The matching of books from both databases is done by title, ussing `difflib` and a substring of the title. For some titles I had to update titles in the CSV file.

To access Calibre I used Python and `calibre-debug` but also experimented with `calibredb`. The only line that updates the Calibre Library is:

```python
db.set_field('#comments', book_to_comment)
```

As the script concatenated the existing custom `comments` field with the comments from Goodreads, running the script again will duplicate the comment.

* `comments.py`
* `calibre_cc_to_tags.py`
* `config.py`
* `calibre-comments`

## Synchronization of readorder custom field and tag

I use a custom field `readorder` to identify when I want to read the books but CalibreWeb cannot use that field. However, CalibreWeb can use tags, so I replicate the contents of the custom field as a tag in the form `readorder:<value>`.

I created two scripts to report discrepancies and to updated values.

* `calibre_readorder_sync_report.py`
* `calibre_sync_readorder.py`

