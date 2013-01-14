"Geocode practices offline"
import ffs
from ffs.contrib import mold

data = ffs.Path('/home/david/src/ohc/nhs-prescription-analytics/data')

coded = data / 'practice_statin_totals_geocoded.csv'

with coded.csv() as csv:
    csv.next()
    markers = [r for r in csv if r[-1] and r[-2]]

tpl = ffs.Path('presentation/practicejs.jinja2')

outfile = data / 'practice.js'
if outfile:
    outfile.truncate()
outfile << mold.cast(tpl, markers=markers)
