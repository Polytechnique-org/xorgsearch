import MySQLdb
import argparse
import configparser
import json
import os.path
import sys


def connect():
    cfg = configparser.ConfigParser()
    cfg.read(os.path.expanduser('~/.my.cnf'))
    return MySQLdb.connect(
        host=cfg.get('client', 'host', fallback='localhost'),
        user=cfg.get('client', 'user', fallback=None),
        passwd=cfg.get('client', 'password', fallback=None),
        db=cfg.get('client', 'database', fallback='x5dat'),
    )


def load(db, limit):
    cursor = db.cursor()
    query = """
        SELECT      profiles.pid AS pid,
                    profiles.hrpid AS hrpid,
                    profiles.sex AS sex,
                    sections.text AS section,
                    profiles.cv AS resume,
                    profiles.freetext AS freetext,
                    display.public_name AS fullname,
                    display.promo AS promo
        FROM        profiles
        LEFT JOIN   profile_section_enum AS sections ON (profiles.section = sections.id)
        LEFT JOIN   profile_display AS display ON (profiles.pid = display.pid)
    """

    if limit:
        query += "LIMIT %d" % limit
    
    cursor.execute(query)

    for line in cursor:
        pid, hrpid, sex, section, resume, freetext, fullname, promo = line
        yield {
            'pid': pid,
            'hrpid': hrpid,
            'sex': sex,
            'section': section,
            'resume': resume,
            'freetext': freetext,
            'fullname': fullname,
            'promo': promo,
        }

    # Extra: pseudo
    # Extra: addresses
    # Extra: jobs


def dump(items, outfile):
    json.dump(list(items), outfile, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('outfile', default='-', type=argparse.FileType('w', encoding='utf-8'))
    parser.add_argument('--limit', '-l', default=0, type=int, help="Limit the number of lines")

    args = parser.parse_args()
    print("Dumping %s lines to %s..." % (args.limit if args.limit else "all", args.outfile.name), file=sys.stderr)
    db = connect()
    lines = load(db, args.limit)
    dump(lines, args.outfile)
    print("Done", file=sys.stderr)


if __name__ == '__main__':
    main()
