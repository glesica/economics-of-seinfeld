-- Build the SQLite3 database from the CSV data dump from the original site.

drop table if exists clip;
drop table if exists clipsegment;
drop table if exists cliptag;
drop table if exists taggedclip;
drop table if exists clip_segments;
drop table if exists clipsource;
drop table if exists contributor;

.mode csv

.import clips_clip.csv clip
.import clips_clipsegment.csv clipsegment
.import clips_cliptag.csv cliptag
.import clips_taggedclip.csv taggedclip
.import clips_clip_segments.csv clip_segments
.import clips_clipsource.csv clipsource
.import clips_contributor.csv contributor

.schema clip
.schema clipsegment
.schema cliptag
.schema taggedclip
.schema clip_segments
.schema clipsource
.schema contributor

