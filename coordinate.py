"Geocode practices offline"
import time
import sqlite3
import ffs

con =  sqlite3.connect('zip_and_post_codes.sqlite')
c = con.cursor()

# from geopy import geocoders

# g = geocoders.Google(domain="maps.google.co.uk")

data = ffs.Path('/home/david/src/ohc/nhs-prescriptions/data/prescriptions')

statins = data / 'practice_statin_totals.csv'
coded = data / 'practice_statin_totals_geocoded.csv'

with statins.csv() as csv:
    headers = csv.next()
    with coded.csv() as out:
        out.writerow(headers)

        for line in csv:
            # time.sleep(0.5)
            pc = line[4].replace(' ', '')
            c.execute("select * from codes where code='{0}';".format(pc))
            try:

                pc, lat, lng, reg = c.fetchone()
                print pc, lat, lng
            except TypeError:
                print pc
                lat = ''
                lng = ''
            # print addr
            # try:
            #     place, (lat, lng) = g.geocode(addr)
            # except geocoders.google.GQueryError:
            #     place, (lat, lng) = None, ("", "")
            # except ValueError:
            #     place, (lat, lng) = None, ("", "")

            # print place, (lat, lng)

            line.append(lat)
            line.append(lng)
            out.writerow(line)
