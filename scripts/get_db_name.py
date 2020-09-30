from urllib.parse import urlsplit

from dynaconf import settings


def get_db_name():
    url = urlsplit(settings.DATABASE_URL)
    name = url.path.replace("/", "")
    return name


def main():
    name = get_db_name()
    print(name)


if __name__ == "__main__":
    main()
