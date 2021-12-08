#!/usr/bin/env python3

import json
import os
import sqlite3 as sql


def load_clips(cursor):
    cursor.execute("""
        SELECT * FROM clip
    """)
    return [dict(r) for r in cursor.fetchall()]


def load_clip_tags(cursor, clip_id):
    cursor.execute("""
        SELECT * FROM
            taggedclip
                INNER JOIN
            cliptag ON taggedclip.tag_id = cliptag.id
        WHERE object_id = ?
    """, (clip_id,))
    return [dict(r) for r in cursor.fetchall()]


def load_clip_segments(cursor, clip_id):
    cursor.execute("""
        SELECT * FROM
            clip_segments
                INNER JOIN
            clipsegment ON clip_segments.clipsegment_id = clipsegment.id
        WHERE clip_id = ?
    """, (clip_id,))
    return [dict(r) for r in cursor.fetchall()]


def load_clip_source(cursor, source_id):
    cursor.execute("""
        SELECT * FROM
            clipsource
        WHERE id = ?
    """, (source_id,))
    return dict(cursor.fetchall()[0])


def load_clip_contributor(cursor, credit_id):
    cursor.execute("""
        SELECT * FROM
            contributor
        WHERE id = ?
    """, (credit_id,))
    rows = cursor.fetchall()
    if rows:
        return dict(rows[0])
    else:
        return {}


def generate_clip_listing(clip, write):
    write('<div class="clip-listing">')
    write(f"<img src=\"{clip['icon']}\" alt=\"{clip['name']} icon\">")
    write("")
    write(f"### [{clip['name']}](/clip/{clip['id']}/)\n")
    
    tag_data = []
    for tag in clip["tags"]:
        tag_data.append(f"[{tag['name']}](/concept/{tag['slug']}/)")
    if tag_data:
        write(" | ".join(tag_data))
    write('</div>')
    write("")


def generate_clip_page(clip):
    clip_id = clip["id"]

    if not os.path.isdir(f"clip/{clip_id}"):
        os.mkdir(f"clip/{clip_id}")
    
    md_file = open(f"clip/{clip_id}/index.md", "w")
    def write(content):
        md_file.write(f"{content}\n")
    
    write(f"## {clip['name']}\n")
    write(f"{clip['description']}\n")

    write(f"*Concepts:*")
    for tag in clip["tags"]:
        write(f"[{tag['name']}](/concept/{tag['slug']}/)")
    write("")

    write(f"*Source:* {clip['source']['title']}\n")

    write(f"*Season:* {clip['season_number']}\n")

    write(f"*Disc:* {clip['disc_number']}\n")

    write(f"*Segments:*\n")
    for segment in clip["segments"]:
        sh = int(segment["start_hours"])
        sm = int(segment["start_minutes"])
        ss = int(segment["start_seconds"])

        eh = int(segment["end_hours"])
        em = int(segment["end_minutes"])
        es = int(segment["end_seconds"])

        write(f" * {sh:02d}:{sm:02d}:{ss:02d} - {eh:02d}:{em:02d}:{es:02d}")

    write("")

    write("*Clip:*\n")
    write(f"{clip['embed_id']}")

    md_file.close()


def generate_concept_page(concept):
    concept_slug = concept["slug"]

    dir_path = f"concept/{concept_slug}"
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    
    md_file = open(f"{dir_path}/index.md", "w")
    def write(content):
        md_file.write(f"{content}\n")
    
    write(f"## Concept: {concept['name']}\n")
    write(f"{concept['description']}\n")

    write("<hr>")

    for clip in concept["clips"]:
        generate_clip_listing(clip, write)
    
    md_file.close()


def generate_main_page(clips):
    md_file = open("index.md", "w")
    def write(content):
        md_file.write(f"{content}\n")
    
    with open("index.md_", "r") as in_file:
        write(in_file.read())
    
    for clip in clips:
        generate_clip_listing(clip, write)
    
    md_file.close()


def generate_index_page(concepts):
    md_file = open("index/index.md", "w")
    def write(content):
        md_file.write(f"{content}\n")
    
    sorted_concepts = sorted(concepts, key=lambda v: v["name"])
    links = []
    for concept in sorted_concepts:
        name = concept["name"]
        slug = concept["slug"]
        links.append(f'<a href="/concept/{slug}">{name}</a>')
    write('<div id="concept-index">')
    write(" | ".join(links))
    write('</div>')

    md_file.close()


def download_icon(clip):
    from urllib.request import urlopen

    file_name = clip["icon"].split("/")[-1]
    icon_path = f"media/icons/{file_name}"

    if not os.path.isfile(icon_path):
        # We don't have the icon, so download it
        print(f"downloading {file_name}")
        base_url = "http://server.yadayadayadaecon.com/media"
        full_url = f"{base_url}/{clip['icon']}"
        response = urlopen(full_url)
        with open(icon_path, "wb") as icon_file:
            icon_file.write(response.read())
    
    clip["icon"] = icon_path


def main():
    # Load the data

    conn = sql.connect("data/all.db")
    conn.row_factory = sql.Row
    cursor = conn.cursor()

    clips = []
    for clip in load_clips(cursor):
        clip_id = clip["id"]
        source_id = clip["source_id"]
        credit_id = clip["credit_id"]

        clip["tags"] = load_clip_tags(cursor, clip_id)
        clip["segments"] = load_clip_segments(cursor, clip_id)
        clip["source"] = load_clip_source(cursor, source_id)
        clip["contributor"] = load_clip_contributor(cursor, credit_id)

        download_icon(clip)

        clips.append(dict(clip))

    conn.close()

    # Generate clip data

    for clip in clips:
        clip_id = clip["id"]
        with open(f"data/clips/{clip_id}.json", "w") as clip_file:
            json.dump(clip, clip_file)
    
    with open("data/clips.json", "w") as clips_file:
        json.dump(clips, clips_file)

    # Generate concept / tag data

    concepts = {}
    for clip in clips:
        for tag in clip["tags"]:
            slug = tag["slug"]
            if slug not in concepts:
                concepts[slug] = dict(tag)
                concepts[slug]["clips"] = []
            concepts[slug]["clips"].append(clip)
    
    for slug, tag in concepts.items():
        with open(f"data/concepts/{slug}.json", "w") as tag_file:
            json.dump(tag, tag_file)
    
    with open("data/concepts.json", "w") as concepts_file:
        json.dump(concepts, concepts_file)
    
    # Write clip Markdown files

    for clip in clips:
        generate_clip_page(clip)
    
    for concept in concepts.values():
        generate_concept_page(concept)
    
    generate_main_page(clips)
    generate_index_page(concepts.values())

if __name__ == "__main__":
    main()

