from radicale.storage import (
    BaseCollection, Collection as FSCollection, sanitize_path, Item, ComponentNotFoundError, get_etag, UnsafePathError, groupby, get_uid
)
import collections
import requests
import vobject
from hashlib import md5
import time
from .LockCollection import LockCollection


def _get_attributes_from_path(path):
    '''Parse path to separate attributes 

    :param path: Path
    :type path: string
    :return: Parts of path
    :rtype: list<str>
    '''

    sane_path = sanitize_path(path).strip("/")
    attributes = sane_path.split("/")
    if not attributes[0]:
        attributes.pop()

    return attributes


class SiriusCachedApi:
    def __init__(self, logger, configuration):
        self.cache = {}
        self.logger = logger
        self.lock_collection = LockCollection()
        self.expiration = 300
        self.load_configuration(configuration)

    def load_configuration(self, configuration):
        '''Load configuration

        :raises ValueError: Raise if configuration file is not valid
        '''
        if configuration.has_option("storage", "cache_expire"):
            try:
                value_new = int(configuration.get("storage", "cache_expire"))
            except:
                raise ValueError("'cache_expire' is not number")
            self.expiration = max(value_new, self.expiration)
        self.logger.info(
            "Configuration storage 'cache_expire' is %r", self.expiration)

    def update_sirus_events(self, auth):
        '''Get updated events from sirius

        :param auth: Auth string "{school_username}:{sirius_local_token}"
        :type auth: str
        :raises ValueError: auth string is not valid
        :raises ConnectionError: Connection failed
        '''

        data = auth.split('|', 1)
        if len(data) != 2:
            raise ValueError(
                "Auth doesn't contains auth in format username|token")
        with self.lock_collection.get_lock(auth):
            self.logger.info("Downloading Sirius Data for %r", data[0])
            resp = requests.get(url='https://sirius.fit.cvut.cz/api/v1/people/' +
                                data[0]+'/events.ical', params=dict(access_token=data[1]))
            if resp.status_code != 200:
                raise ConnectionError("Cannot download data from Sirius")

            self.logger.info(
                "Downloading Sirius Data for %r complete", data[0])
            result = {}
            vcal = vobject.readOne(resp.text)
            for vevent in vcal.vevent_list:
                cal = vobject.iCalendar()
                cal.add(vevent)
                result[vevent.uid.value] = cal

            expired = int(time.time()) + self.expiration
            last_modified = time.strftime(
                "%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
            self.cache[auth] = {"events": result,
                                "expired": expired, "last_modified": last_modified}

    def is_valid(self, auth):
        '''Check if cache for known auth is not expired

        :param auth: Auth string "{school_username}:{sirius_local_token}"
        :type auth: str
        :return: True if valid
        :rtype: bool
        '''

        with self.lock_collection.get_lock(auth):
            return auth in self.cache and int(time.time()) < self.cache[auth]['expired']

    def get_sirius_event(self, auth, uid):
        '''Get Sirius Event for know auth

        :param auth: Auth string "{school_username}:{sirius_local_token}"
        :type auth: str
        :param uid: Unique ID for event
        :type uid: string
        :return: Event
        :rtype: VCALENDAR
        '''

        with self.lock_collection.get_lock(auth):
            if not self.is_valid(auth):
                self.update_sirus_events(auth)

            if uid in self.cache[auth]["events"]:
                return self.cache[auth]["events"][uid]

            return None

    def get_sirius_uids(self, auth):
        '''Get all UIDS for know auth

        :param auth: Auth string "{school_username}:{sirius_local_token}"
        :type auth: str
        :return: List of uids
        :rtype: list<str>
        '''

        with self.lock_collection.get_lock(auth):
            if not self.is_valid(auth):
                self.update_sirus_events(auth)

            return self.cache[auth]["events"].keys()

    def get_sirius_last_update(self, auth):
        '''Get Update of known Auth

        :param auth: Auth string "{school_username}:{sirius_local_token}"
        :type auth: str
        :return: last modified date in "%a, %d %b %Y %H:%M:%S GMT" format, if Auth is unknown date 1.1.1970 is returned
        :rtype: str
        '''

        with self.lock_collection.get_lock(auth):
            if auth in self.cache:
                return self.cache[auth]["last_modified"]
            else:
                return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(0))


class Collection(BaseCollection):
    OVERLAY_FIELD = "x-overlay"
    '''Name of field with information of changed values. Used for overwriting VEVENT.
    '''

    REMOVE_FIELD = "x-remove"
    '''Name of field with information if event was removed.
    '''

    @classmethod
    def static_init(self):
        '''Init Storage module
        '''
        FSCollection.configuration = self.configuration
        FSCollection.logger = self.logger
        FSCollection.static_init()
        self.sirius_cache = SiriusCachedApi(self.logger, self.configuration)

    @classmethod
    def verify(cls):
        '''Verify if storage is consistent
        '''
        FSCollection.verify()

    @classmethod
    def acquire_lock(self, mode, user=None):
        """Set a context manager to lock the whole storage.
        ``mode`` must either be "r" for shared access or "w" for exclusive
        access.
        ``user`` is the name of the logged in user or empty.
        """
        return FSCollection.acquire_lock(mode, user)

    @classmethod
    def discover(self, path, depth="0"):
        """Discover a list of collections under the given ``path``.
        If ``depth`` is "0", only the actual object under ``path`` is
        returned.
        If ``depth`` is anything but "0", it is considered as "1" and direct
        children are included in the result.
        The ``path`` is relative.
        The root collection "/" must always exist.
        """
        attributes = _get_attributes_from_path(path)
        if len(attributes) == 3 and attributes[1] == "sirius":
            for collection in FSCollection.discover("/%s/%s/" % (attributes[0], attributes[1]), "0"):
                yield self(collection).get(attributes[2])
            return

        for collection in FSCollection.discover(path, depth):
            if isinstance(collection, BaseCollection):
                yield self(collection)
            elif isinstance(collection, Item):
                collection.collection = self(collection.collection)
                yield collection
            else:
                yield collection

    @classmethod
    def create_collection(self, href, items=None, props=None):
        '''Create collection if not exits, sirius collection is created with user collection.

        :param href: Collection hiearchy
        :type href: str
        :param items: Predefined events
        :param items: list<VCALENDAR>
        :param props: Meta information of collection
        :param props: dict
        :raises NotImplementedError: Creating of custom collection is not allowed
        :return: Created or Existed collection
        '''

        attributes = _get_attributes_from_path(href)
        if len(attributes) == 0 or len(attributes) == 3:
            return FSCollection.create_collection(href, items, props)

        if len(attributes) == 1:
            col = FSCollection.create_collection(href, items, props)
            siriusPath = href+"/sirius/"
            self.logger.info("Creating sirius collection %r", siriusPath)
            props = collections.OrderedDict([('C:calendar-description', 'Sirius Bridge'), ('C:supported-calendar-component-set',
                                                                                           'VEVENT'), ('D:displayname', 'Sirius'), ('ICAL:calendar-color', '#c62349ff'), ('tag', 'VCALENDAR')])
            sirius = FSCollection.create_collection(siriusPath, items, props)
            return col

        self.logger.info("Own collection is not allowed %r", href)
        raise NotImplementedError

    def __init__(self, collection):
        '''Init overlay collection

        :param collection: Radicale multifilesystem collection
        '''

        self.collection = collection

    def __getattr__(self, attr):
        '''Pass attributes call to underlaying collection
        '''

        return getattr(self.collection, attr)

    def get_sirius_auth(self):
        '''Get Auth String

        :raises ValueError: Collection path doesn't contains Auth
        :return: Auth string "{school_username}:{sirius_local_token}"
        :rtype: string
        '''

        attributes = _get_attributes_from_path(self.path)
        if len(attributes) < 2:
            raise ValueError("Path is not sirius collection")
        return attributes[0]

    def is_sirius_collection(self):
        '''Check if actial collection can be used as sirius collection

        :return: True if collection is sirius
        :rtype: bool
        '''

        try:
            self.get_sirius_auth()
            return True
        except:
            return False

    def list(self):
        '''Return list of valid events' uids. Removed events are filtred.

        :return: UIDS
        :rtype: list<str>
        '''

        if self.is_sirius_collection():
            uids = []
            for uid in self.sirius_cache.get_sirius_uids(self.get_sirius_auth()):
                event = self.collection.get(uid)
                if event is None or self.REMOVE_FIELD not in event.vevent.contents:
                    uids.append(uid)
            return uids
        else:
            return self.collection.list()

    def merge_event_load(self, event_sirius, event_local):
        '''Merge event from Sirius and local source based on "X-OVERLAY" fields.

        If field is overlayed local field is used.

        :param event_sirius: Event from sirius
        :type event_sirius: VCALENDAR
        :param event_local: Event from local storage
        :type event_local: VCALENDAR
        :return: Merged event,If event is removed (field 'X-REMOVE') function return None
        :rtype: VCALENDAR
        '''

        if event_sirius is None:
            return None
        if event_local is None:
            return event_sirius

        # Remove if not exist
        if self.REMOVE_FIELD in event_local.vevent.contents:
            return None

        # Overlay changed fields
        if self.OVERLAY_FIELD not in event_local.vevent.contents:
            return event_sirius

        for field in event_local.vevent.contents[self.OVERLAY_FIELD]:
            field = field.value.lower()
            if field in event_local.vevent.contents:
                event_sirius.vevent.contents[field] = event_local.vevent.contents[field]

        return event_sirius

    def get(self, href):
        '''Get single merged event by UID

        :param href: Event UID
        :type href: str
        :return: Merged event, None if not exist
        :rtype: VCALENDAR
        '''

        if not self.is_sirius_collection():
            return self.collection.get(href)

        auth = self.get_sirius_auth()
        event_sirius = self.sirius_cache.get_sirius_event(auth, href)
        event_local = self.collection.get(href)
        event_final = self.merge_event_load(event_sirius, event_local)
        if event_final is None:
            return
        return Item(self, event_final, href, self.sirius_cache.get_sirius_last_update(auth))

    def track_event_changes(self, href, event_sirius, vobject_item):
        '''Tracked changed fields in uploaded event

        Following fileds are followed: 'dtstart', 'dtend', 'description', 'location','summary', 'url', 'last-modified', 'transp'

        :param href: Event UID
        :type href: str
        :param event_sirius: sirius event
        :type event_sirius: VCALENDAR
        :param vobject_item: uploaded event
        :type vobject_item: VCALENDAR
        :return: VCALENDAR with overlay fields
        :rtype: VCALENDAR
        '''

        fields = ['dtstart', 'dtend', 'description', 'location',
                  'summary', 'url', 'last-modified', 'transp']
        event_sirius = event_sirius.vevent.contents
        event_new = vobject_item.vevent.contents

        fields_updated = []

        for field in fields:
            if field not in event_sirius:
                if field in event_new:
                    fields_updated.append(field)
                continue
            if field not in event_new:
                continue

            sirius = event_sirius[field][0].value
            new = event_new[field][0].value
            if isinstance(sirius, str):
                sirius = sirius.rstrip()

            if isinstance(new, str):
                new = new.rstrip()

            if sirius != new:
                fields_updated.append(field)

        vobject_item.vevent.contents[self.OVERLAY_FIELD] = []
        for field in fields_updated:
            vobject_item.vevent.add(self.OVERLAY_FIELD).value = field
        return vobject_item

    def upload(self, href, vobject_item):
        '''Save changes in local storage, creating new event is not allowed

        :param href: Event UID
        :type href: VCALENDAR
        :param vobject_item: Uploaded Event
        :type vobject_item: VCALENDAR
        :return: Uploaded Event with overlay fields
        :rtype: VCALENDAR
        '''

        event_sirius = self.sirius_cache.get_sirius_event(
            self.get_sirius_auth(), href)

        # If object does not exist on sirius don't save it
        if event_sirius is None:
            raise NotImplementedError("Creating own event is not allowed")

        merged_vobject = self.track_event_changes(
            href, event_sirius, vobject_item)
        return self.collection.upload(href, merged_vobject)

    def delete(self, href=None):
        '''Delete Event in collection

        :param href: Event UID (if None delete collection), defaults to None
        :param href: str, optional
        :raises ValueError: Collection remove is not allowed
        '''
        if not self.is_sirius_collection():
            return self.collection.delete(href)
        if href == None:
            raise ValueError("Cannot remove sirius collection")

        event_sirius = self.sirius_cache.get_sirius_event(
            self.get_sirius_auth(), href)

        event_sirius.vevent.contents[self.REMOVE_FIELD] = []
        event_sirius.vevent.add(self.REMOVE_FIELD).value = "1"
        self.collection.upload(href, event_sirius)

    def get_multi2(self, hrefs):
        """Fetch multiple items.

        Functionally similar to ``get``, but might bring performance benefits
        on some storages when used cleverly. It's not required to return the
        requested items in the correct order. Duplicated hrefs can be ignored.

        Returns tuples with the href and the item or None if the item doesn't
        exist.

        """
        return ((href, self.get(href)) for href in hrefs)

    def get_all(self):
        """Fetch all items.

        Functionally similar to ``get``, but might bring performance benefits
        on some storages when used cleverly.

        """
        return map(self.get, self.list())

    def get_meta(self, key=None):
        """Get metadata value for collection.
        Return the value of the property ``key``. If ``key`` is ``None`` return
        a dict with all properties
        """
        return self.collection.get_meta(key)

    def set_meta_all(self, props):
        """Set metadata values for collection.
        ``props`` a dict with values for properties.
        """
        return self.collection.set_meta_all(props)

    @property
    def last_modified(self):
        """Get the HTTP-datetime of when the collection was modified."""
        return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

    @property
    def etag(self):
        """Encoded as quoted-string (see RFC 2616)."""
        m = md5()
        m.update(self.last_modified.encode('utf-8'))
        return '"%s"' % m.hexdigest()

    @property
    def is_principal(self):
        """Collection is a principal."""
        return self.collection.is_principal

    @property
    def owner(self):
        """The owner of the collection."""
        return self.collection.owner

    @property
    def path(self):
        """Get the collection path."""
        return self.collection.path
