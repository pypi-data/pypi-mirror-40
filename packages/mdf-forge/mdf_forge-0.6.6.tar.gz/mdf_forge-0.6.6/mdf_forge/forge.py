import os
from urllib.parse import urlparse

import globus_sdk
import mdf_toolbox
import requests
from tqdm import tqdm


# Maximum recommended number of HTTP file transfers
# Large transfers are much better suited to Globus Transfer use
HTTP_NUM_LIMIT = 50
# Maximum number of results per search allowed by Globus Search
SEARCH_LIMIT = 10000
# Maximum number of results to return when advanced=False
NONADVANCED_LIMIT = 10


class Forge:
    """Forge fetches metadata and files from the Materials Data Facility.
    Forge is intended to be the best way to access MDF data for all users.
    An internal Query object is used to make queries. From the user's perspective,
    an instantiation of Forge will black-box searching.
    """
    __default_index = "mdf"
    __auth_services = ["data_mdf", "transfer", "search", "petrel"]
    __anon_services = ["search"]
    __app_name = "MDF_Forge"
    __transfer_interval = 60  # 1 minute, in seconds
    __inactivity_time = 1 * 60 * 60  # 1 hour, in seconds

    def __init__(self, index=__default_index, local_ep=None, anonymous=False,
                 clear_old_tokens=False, **kwargs):
        """Create an MDF Forge Client.

        Arguments:
            index (str): The Search index to search on. **Default:** ``"mdf"``.
            local_ep (str): The endpoint ID of the local Globus Connect Personal endpoint.
                    If needed but not provided, the local endpoint will be autodetected
                    if possible.
            anonymous (bool): If ``True``, will not authenticate with Globus Auth.
                    If ``False``, will require authentication.
                    **Default:** ``False``.

                    Caution:
                        Authentication is required for some Forge functionality,
                        including viewing private datasets and using Globus Transfer.

            clear_old_tokens (bool): If ``True``, will force reauthentication.
                    If ``False``, will use existing tokens if possible.
                    Has no effect if ``anonymous`` is ``True``.
                    **Default:** ``False``.

        Keyword Arguments:
            services (list of str): *Advanced users only.* The services to authenticate with,
                    using Toolbox. An empty list will disable authenticating with Toolbox.
            clients (dict): *Advanced users only.* Clients or authorizers to use instead
                    of the defaults.

                    Overwritable clients:

                    * ``search`` (*globus_sdk.SearchClient*)
                    * ``transfer`` (*globus_sdk.TransferClient*)
                    * ``data_mdf`` (*GlobusAuthorizer* for MDF NCSA endpoint)
                    * ``petrel`` (*GlobusAuthorizer* for MDF Petrel endpoint)

                    The clients/authorizers must be properly authenticated.
                    Forge will still attempt to authenticate with Toolbox
                    in accordance with the services keyword argument.
        """
        self.__anonymous = anonymous
        self.index = index
        self.local_ep = local_ep

        if self.__anonymous:
            services = kwargs.get('services', self.__anon_services)
            clients = (mdf_toolbox.anonymous_login(services) if services else {})
        else:
            services = kwargs.get('services', self.__auth_services)
            clients = (mdf_toolbox.login(
                                        credentials={
                                            "app_name": self.__app_name,
                                            "services": services,
                                            "index": self.index},
                                        clear_old_tokens=clear_old_tokens) if services else {})
        user_clients = kwargs.get("clients", {})
        self.__search_client = user_clients.get("search", clients.get("search", None))
        self.__transfer_client = user_clients.get("transfer", clients.get("transfer", None))
        self.__data_mdf_authorizer = user_clients.get("data_mdf",
                                                      clients.get("data_mdf",
                                                                  globus_sdk.NullAuthorizer()))
        self.__petrel_authorizer = user_clients.get("petrel",
                                                    clients.get("petrel",
                                                                globus_sdk.NullAuthorizer()))

        self.__query = Query(self.__search_client)

    # ***********************************************
    # * Core functions
    # ***********************************************

    def match_field(self, field, value, required=True, new_group=False):
        """Add a ``field:value`` term to the query.
        Matches will have the ``value`` in the ``field``.

        Arguments:
            field (str): The field to check for the value.
                    The field must be namespaced according to Elasticsearch rules
                    using the dot syntax.
                    For example, ``"mdf.source_name"`` is the ``source_name`` field
                    of the ``mdf`` dictionary.
            value (str): The value to match.
            required (bool): If ``True``, will add term with ``AND``.
                    If ``False``, will use ``OR``. **Default:** ``True``.
            new_group (bool): If ``True``, will separate the term into a new parenthetical group.
                    If ``False``, will not.
                    **Default:** ``False``.

        Returns:
            Forge: Self
        """
        # No-op on missing arguments
        if not field and not value:
            return self
        # If not the start of the query string, add an AND or OR
        if self.__query.initialized:
            if required:
                self.__query.and_join(new_group)
            else:
                self.__query.or_join(new_group)
        self.__query.field(str(field), str(value))
        return self

    def exclude_field(self, field, value, new_group=False):
        """Exclude a ``field:value`` term from the query.
        Matches will NOT have the ``value`` in the ``field``.

        Arguments:
            field (str): The field to check for the value.
                    The field must be namespaced according to Elasticsearch rules
                    using the dot syntax.
                    For example, ``"mdf.source_name"`` is the ``source_name`` field
                    of the ``mdf`` dictionary.
            value (str): The value to exclude.
            new_group (bool): If ``True``, will separate term the into a new parenthetical group.
                    If ``False``, will not.
                    **Default:** ``False``.

        Returns:
            Forge: Self
        """
        # No-op on missing arguments
        if not field and not value:
            return self
        # If not the start of the query string, add an AND
        # OR would not make much sense for excluding
        if self.__query.initialized:
            self.__query.and_join(new_group)
        self.__query.negate().field(str(field), str(value))
        return self

    def search(self, q=None, index=None, advanced=False, limit=SEARCH_LIMIT, info=False,
               reset_query=True):
        """Execute a search and return the results, up to the ``SEARCH_LIMIT``.

        Arguments:
            q (str): The query to execute. **Default:** The current helper-formed query, if any.
                    There must be some query to execute.
            index (str): The Search index to search on. **Default:** The current index.
            advanced (bool): If ``True``, will submit query in "advanced" mode
                    to enable field matches and other advanced features.
                    If ``False``, only basic fulltext term matches will be supported.
                    **Default:** ``False`` if no helpers have been used to build the query, or
                    ``True`` if helpers have been used.
            limit (int): The maximum number of results to return.
                    The max for this argument is the ``SEARCH_LIMIT`` imposed by Globus Search.
                    **Default:** ``SEARCH_LIMIT``.
            info (bool): If ``False``, search will return a list of the results.
                    If ``True``, search will return a tuple containing the results list
                    and other information about the query.
                    **Default:** ``False``.
            reset_query (bool): If ``True``, will destroy the current query after execution
                    and start a fresh one.
                    If ``False``, will keep the current query set.
                    **Default:** ``True``.

        Returns:
            If ``info`` is ``False``, *list*: The search results.
            If ``info`` is ``True``, *tuple*: The search results,
            and a dictionary of query information.
        """
        if not index:
            index = self.index
        res = self.__query.search(q=q, index=index, advanced=advanced, limit=limit, info=info)
        if reset_query:
            self.reset_query()
        return res

    def aggregate(self, q=None, index=None, scroll_size=SEARCH_LIMIT, reset_query=True):
        """Perform an advanced query, and return *all* matching results.
        Will automatically perform multiple queries in order to retrieve all results.

        Note:
            All ``aggregate`` queries run in advanced mode, and ``info`` is not available.

        Arguments:
            q (str): The query to execute. **Default:** The current helper-formed query, if any.
                    There must be some query to execute.
            index (str): The Search index to search on. **Default:** The current index.
            scroll_size (int): Maximum number of records returned per query. Must be
                    between one and the ``SEARCH_LIMIT`` (inclusive).
                    **Default:** ``SEARCH_LIMIT``.
            reset_query (bool): If ``True``, will destroy the current query after execution
                    and start a fresh one.
                    If ``False``, will keep the current query set.
                    **Default:** ``True``.

        Returns:
            list of dict: All matching records.
        """
        if not index:
            index = self.index
        res = self.__query.aggregate(q=q, index=index, scroll_size=scroll_size)
        if reset_query:
            self.reset_query()
        return res

    def show_fields(self, block=None, index=None):
        """Retrieve and return the mapping for the given metadata block.

        Arguments:
            block (str): The top-level field to fetch the mapping for (for example, ``"mdf"``),
                    or the special values ``"all"`` for everything or `None` for just the
                    top-level fields.
                    **Default:** ``None``.
            index (str): The Search index to map. **Default:** The current index.

        Returns:
            dict: ``field:datatype`` pairs.
        """
        if not index:
            index = self.index
        mapping = self.__query.mapping(index=index)
        if block == "all":
            return mapping
        elif not block:
            blocks = set()
            for key in mapping.keys():
                blocks.add(key.split(".")[0])
            block_map = {}
            for b in blocks:
                block_map[b] = "object"
        else:
            block_map = {}
            for key, value in mapping.items():
                if key.startswith(block):
                    block_map[key] = value
        return block_map

    def current_query(self):
        """Return the current query string.

        Returns:
            str: The current query.
        """
        return self.__query.clean_query()

    def reset_query(self):
        """Destroy the current query and create a fresh one.
        This method should not be chained.

        Returns:
            None
        """
        del self.__query
        self.__query = Query(self.__search_client)
        return

    # ***********************************************
    # * Expanded functions
    # ***********************************************

    def match_exists(self, field, required=True, new_group=False):
        """Require a field to exist in the results.
        Matches will have some value in ``field``.

        Arguments:
            field (str): The field to check.
                    The field must be namespaced according to Elasticsearch rules
                    using the dot syntax.
                    For example, ``"mdf.source_name"`` is the ``source_name`` field
                    of the ``mdf`` dictionary.
            required (bool): If ``True``, will add term with ``AND``.
                    If ``False``, will use ``OR``. **Default:** ``True``.
            new_group (bool): If ``True``, will separate the term into a new parenthetical group.
                    If ``False``, will not.
                    **Default:** ``False``.

        Returns:
            Forge: Self
        """
        return self.match_field(field, "*", required=required, new_group=new_group)

    def match_not_exists(self, field, new_group=False):
        """Require a field to not exist in the results.
        Matches will not have ``field`` present.

        Arguments:
            field (str): The field to check.
                    The field must be namespaced according to Elasticsearch rules
                    using the dot syntax.
                    For example, ``"mdf.source_name"`` is the ``source_name`` field
                    of the ``mdf`` dictionary.
            new_group (bool): If ``True``, will separate the term into a new parenthetical group.
                    If ``False``, will not.
                    **Default:** ``False``.

        Returns:
            Forge: Self
        """
        return self.exclude_field(field, "*", new_group=new_group)

    def match_range(self, field, start=None, stop=None, inclusive=True,
                    required=True, new_group=False):
        """Add a ``field:[some range]`` term to the query.
        Matches will have a ``value`` in the range in the ``field``.

        Arguments:
            field (str): The field to check for the value.
                    The field must be namespaced according to Elasticsearch rules
                    using the dot syntax.
                    For example, ``"mdf.source_name"`` is the ``source_name`` field
                    of the ``mdf`` dictionary.
            start (str or int): The starting value, or ``None`` for no lower bound.
                    **Default:** ``None``.
            stop (str or int): The ending value, or ``None`` for no upper bound.
                    **Default:** ``None``.
            inclusive (bool): If ``True``, the ``start`` and ``stop`` values will be included
                    in the search.
                    If ``False``, the start and stop values will not be included
                    in the search.
                    **Default:** ``True``.
            required (bool): If ``True``, will add term with ``AND``.
                    If ``False``, will use ``OR``. **Default:** ``True``.
            new_group (bool): If ``True``, will separate the term into a new parenthetical group.
                    If ``False``, will not.
                    **Default:** ``False``.

        Returns:
            Forge: Self
        """
        # Accept None as *
        if start is None:
            start = "*"
        if stop is None:
            stop = "*"
        # *-* is the same as field exists
        if start == "*" and stop == "*":
            return self.match_exists(field, required=required, new_group=new_group)

        if inclusive:
            value = "[" + str(start) + " TO " + str(stop) + "]"
        else:
            value = "{" + str(start) + " TO " + str(stop) + "}"
        return self.match_field(field, value, required=required, new_group=new_group)

    def exclude_range(self, field, start="*", stop="*", inclusive=True, new_group=False):
        """Exclude a ``field:[some range]`` term from the query.
        Matches will not have any ``value`` in the range in the ``field``.

        Arguments:
            field (str): The field to check for the value.
                    The field must be namespaced according to Elasticsearch rules
                    using the dot syntax.
                    For example, ``"mdf.source_name"`` is the ``source_name`` field
                    of the ``mdf`` dictionary.
            start (str or int): The starting value, or ``None`` for no lower bound.
                    **Default:** ``None``.
            stop (str or int): The ending value, or ``None`` for no upper bound.
                    **Default:** ``None``.
            inclusive (bool): If ``True``, the ``start`` and ``stop`` values will be excluded
                    from the search.
                    If ``False``, the ``start`` and ``stop`` values will not be excluded
                    from the search.
                    **Default:** ``True``.
            new_group (bool): If ``True``, will separate the term into a new parenthetical group.
                    If ``False``, will not.
                    **Default:** ``False``.

        Returns:
            Forge: Self
        """
        # Accept None as *
        if start is None:
            start = "*"
        if stop is None:
            stop = "*"
        # *-* is the same as field doesn't exist
        if start == "*" and stop == "*":
            return self.match_not_exists(field, new_group=new_group)

        if inclusive:
            value = "[" + str(start) + " TO " + str(stop) + "]"
        else:
            value = "{" + str(start) + " TO " + str(stop) + "}"
        return self.exclude_field(field, value, new_group=new_group)

    # ***********************************************
    # * Specific functions
    # ***********************************************

    def exclusive_match(self, field, value):
        """Match exactly the given value(s), with no other data in the field.

        Arguments:
            field (str): The field to check for the value.
                    The field must be namespaced according to Elasticsearch rules
                    using the dot syntax.
                    For example, ``"mdf.source_name"`` is the ``source_name`` field
                    of the ``mdf`` dictionary.
            value (str or list of str): The value(s) to match exactly.

        Returns:
            Forge: Self
        """
        if isinstance(value, str):
            value = [value]

        # Hacky way to get ES to do exclusive search
        # Essentially have a big range search that matches NOT anything
        # Except for the actual values
        # Example: [foo, bar, baz] =>
        #   (NOT {* TO foo} AND [foo TO foo] AND NOT {foo to bar} AND [bar TO bar]
        #    AND NOT {bar TO baz} AND [baz TO baz] AND NOT {baz TO *})
        # Except it must be sorted to not overlap
        value.sort()

        # Start with removing everything before first value
        self.exclude_range(field, "*", value[0], inclusive=False, new_group=True)
        # Select first value
        self.match_range(field, value[0], value[0])
        # Do the rest of the values
        for index, val in enumerate(value[1:]):
            self.exclude_range(field, value[index-1], val, inclusive=False)
            self.match_range(field, val, val)
        # Add end
        self.exclude_range(field, value[-1], "*", inclusive=False)
        # Done
        return self

    def match_source_names(self, source_names):
        """Add sources to match to the query.

        Arguments:
            source_names (str or list of str): The ``source_name`` values to match.

        Returns:
            Forge: Self
        """
        # If no source_names are supplied, nothing to match
        if not source_names:
            return self
        if isinstance(source_names, str):
            source_names = [source_names]
        # First source should be in new group and required
        self.match_field(field="mdf.source_name", value=source_names[0],
                         required=True, new_group=True)
        # Other sources should stay in that group, and not be required
        for src in source_names[1:]:
            self.match_field(field="mdf.source_name", value=src, required=False, new_group=False)
        return self

    def match_ids(self, mdf_ids):
        """Match all the IDs in the given ``mdf_id`` list.

        Arguments:
            mdf_ids (str or list of str): The IDs to match.

        Returns:
            Forge: Self
        """
        # If no IDs are supplied, nothing to match
        if not mdf_ids:
            return self
        if isinstance(mdf_ids, str):
            mdf_ids = [mdf_ids]
        # First ID should be in new group and required
        self.match_field(field="mdf.mdf_id", value=mdf_ids[0], required=True, new_group=True)
        # Other IDs should stay in that group, and not be required
        for mid in mdf_ids[1:]:
            self.match_field(field="mdf.mdf_id", value=mid, required=False, new_group=False)
        return self

    def match_elements(self, elements, match_all=True):
        """Add elemental abbreviations to the query.

        Arguments:
            elements (str or list of str): The elements to match. For example, `"Fe"` for iron.
            match_all (bool): If ``True``, will add with ``AND``.
                    If ``False``, will use ``OR``.
                    Default ``True``.

        Returns:
            Forge: Self
        """
        # If no elements are supplied, nothing to match
        if not elements:
            return self
        if isinstance(elements, str):
            elements = [elements]
        # First element should be in new group and required
        self.match_field(field="material.elements", value=elements[0],
                         required=True, new_group=True)
        # Other elements should stay in that group
        for element in elements[1:]:
            self.match_field(field="material.elements", value=element, required=match_all,
                             new_group=False)
        return self

    def match_titles(self, titles):
        """Add titles to the query.

        Arguments:
            titles (str or list of str): The titles to match.

        Returns:
            Forge: Self
        """
        if not titles:
            return self
        if not isinstance(titles, list):
            titles = [titles]

        self.match_field(field="dc.titles.title", value=titles[0], required=True, new_group=True)
        for title in titles[1:]:
            self.match_field(field="dc.titles.title", value=title, required=False, new_group=False)
        return self

    def match_years(self, years=None, start=None, stop=None, inclusive=True):
        """Add years and limits to the query.

        Arguments:
            years (int or string, or list of int or strings): The years to match.
                    Note that this argument overrides the start, stop, and inclusive arguments.
            start (int or string): The lower range of years to match.
            stop (int or string): The upper range of years to match.
            inclusive (bool): If ``True``, the start and stop values will be included
                    in the search. If ``False``, they will be excluded.
                    **Default:** ``True``.
        Returns:
            Forge: Self
        """
        # If nothing supplied, nothing to match
        if years is None and start is None and stop is None:
            return self

        if years is not None and years != []:
            if not isinstance(years, list):
                years = [years]
            years_int = []
            for year in years:
                try:
                    y_int = int(year)
                    years_int.append(y_int)
                except ValueError:
                    print("Invalid year: '", year, "'", sep="")

            # Only match years if valid years were supplied
            if len(years_int) > 0:
                self.match_field(field="dc.publicationYear", value=years_int[0], required=True,
                                 new_group=True)
                for year in years_int[1:]:
                    self.match_field(field="dc.publicationYear",
                                     value=year, required=False, new_group=False)
        else:
            if start is not None:
                try:
                    start = int(start)
                except ValueError:
                    print("Invalid start year: '", start, "'", sep="")
                    start = None
            if stop is not None:
                try:
                    stop = int(stop)
                except ValueError:
                    print("Invalid stop year: '", stop, "'", sep="")
                    stop = None

            self.match_range(field="dc.publicationYear", start=start, stop=stop,
                             inclusive=inclusive, required=True, new_group=True)
        return self

    def match_resource_types(self, types):
        """Match the given resource types.

        Arguments:
            types (str or list of str): The ``resource_type`` values to match.

        Returns:
            Forge: Self
        """
        # If no types, nothing to match
        if not types:
            return self
        if isinstance(types, str):
            types = [types]
        # First type should be in new group and required
        self.match_field(field="mdf.resource_type", value=types[0], required=True, new_group=True)
        # Other IDs should stay in that group, and not be required
        for rt in types[1:]:
            self.match_field(field="mdf.resource_type", value=rt, required=False, new_group=False)
        return self

    def match_repositories(self, repositories, match_all=True):
        """Match the given repositories.
        Repositories are MDF-identified collections of datasets from a group
        or organization.

        Arguments:
            repositories (str or list of str): The repositories to match.
            match_all (bool): If ``True``, will add with ``AND``.
                    If ``False``, will use ``OR``.
                    **Default:** ``True``.

        Returns:
            Forge: Self
        """
        # If no repos, nothing to match
        if not repositories:
            return self
        if isinstance(repositories, str):
            repositories = [repositories]
        # First repo should be in new group and required
        self.match_field(field="mdf.repositories", value=repositories[0],
                         required=True, new_group=True)
        # Other elements should stay in that group
        for repo in repositories[1:]:
            self.match_field(field="mdf.repositories", value=repo, required=match_all,
                             new_group=False)

    # ***********************************************
    # * Premade searches
    # ***********************************************

    def search_by_elements(self, elements, source_names=[], index=None, limit=None,
                           match_all=True, info=False):
        """Execute a search for the given elements in the given sources.
        ``search_by_elements([x], [y])`` is equivalent to
        ``match_elements([x]).match_source_names([y]).search()``.

        Note:
            This method will use terms from the current query, and resets the current query.

        Arguments:
            elements (list of str): The elements to match. For example, `"Fe"` for iron.
            source_names (list of str): The ``source_name``s to match.
                    **Default:** ``[]``.
            index (str): The Search index to search on. **Default:** The current index.
            limit (int): The maximum number of results to return.
                    The max for this argument is the ``SEARCH_LIMIT`` imposed by Globus Search.
                    **Default:** ``SEARCH_LIMIT``.
            match_all (bool): If ``True``, will add elements with ``AND``.
                    If ``False``, will use ``OR``.
                    **Default:** ``True``.
            info (bool): If ``False``, search will return a list of the results.
                    If ``True``, search will return a tuple containing the results list
                    and other information about the query.
                    **Default:** ``False``.

        Returns:
            If ``info`` is ``False``, *list*: The search results.
            If ``info`` is ``True``, *tuple*: The search results,
            and a dictionary of query information.
        """
        return (self.match_elements(elements, match_all=match_all)
                    .match_source_names(source_names)
                    .search(index=index, limit=limit, info=info))

    def search_by_titles(self, titles, index=None, limit=None, info=False):
        """Execute a search for the given titles.
        ``search_by_titles([x])`` is equivalent to ``match_titles([x]).search()``

        Note:
            This method will use terms from the current query, and resets the current query.

        Arguments:
            titles (list of str): The titles to match.
            index (str): The Search index to search on. **Default:** The current index.
            limit (int): The maximum number of results to return.
                    The max for this argument is the ``SEARCH_LIMIT`` imposed by Globus Search.
                    **Default:** ``SEARCH_LIMIT``.
            info (bool): If ``False``, search will return a list of the results.
                    If ``True``, search will return a tuple containing the results list
                    and other information about the query.
                    **Default:** ``False``.

        Returns:
            If ``info`` is ``False``, *list*: The search results.
            If ``info`` is ``True``, *tuple*: The search results,
            and a dictionary of query information.
        """
        return self.match_titles(titles).search(index=index, limit=limit, info=info)

    def aggregate_sources(self, source_names, index=None):
        """Aggregate all records with the given ``source_name`` values.
        There is no limit to the number of results returned.
        Please beware of aggregating very large datasets.

        Caution:
            It is recommended that you check how many entries will be returned from your chosen
            datasets by running ``match_source_names(source_names).search(limit=0, info=True)``
            before using ``aggregate_sources()``.

        Note:
            This method will use terms from the current query, and resets the current query.

        Arguments:
            source_names (str or list of str): The ``source_name`` values to aggregate.
            index (str): The Search index to search on. **Default:** The current index.

        Returns:
            list of dict: All of the entries from the ``source_name`` matches.
        """
        return self.match_source_names(source_names).aggregate(index=index)

    def fetch_datasets_from_results(self, entries=None, query=None, reset_query=True):
        """Retrieve the dataset entries for given records.
        Note that this method may use the current query.

        Note:
            This method will use terms from the current query, and resets the current query.

        Arguments:
            entries (dict, list of dict, or tuple of dict): The records to parse
                    to find the datasets. This argument can be a single entry,
                    a list of entries, or a tuple with a list of entries.
                    The latter two options support both return values of the ``search()`` method.
                    If entries is ``None``, the current query is executed and those
                    results are used instead. **Default:** ``None``.
            query (str): If not ``None``, search for entries using this query
                    instead of the current query. Has no effect if ``entries`` is not ``None``.
                    **Default:** ``None``.
            reset_query (bool): Has no effect unless ``entries`` and ``query`` are both ``None``.
                    If ``True``, will reset the current query after searching for entries.
                    If ``False``, will not reset the current query.
                    **Default:** ``True``.

        Returns:
            list: The dataset entries.
        """
        if entries is None:
            entries = self.search(q=query, reset_query=(query is None or reset_query))
        # If entries is not a list of dict, make it one
        if isinstance(entries, dict):
            entries = [entries]
        elif isinstance(entries, tuple):
            entries = entries[0]
        ds_ids = set()
        # For every entry, extract the appropriate ID
        for entry in entries:
            # For records, extract the parent_id
            # Most entries should be records here
            if entry["mdf"]["resource_type"] == "record":
                ds_ids.add(entry["mdf"]["parent_id"])
            # For datasets, extract the mdf_id
            elif entry["mdf"]["resource_type"] == "dataset":
                ds_ids.add(entry["mdf"]["mdf_id"])
            # For anything else (collection), do nothing
            else:
                pass
        return self.match_ids(list(ds_ids)).search()

    def get_dataset_version(self, source_name):
        """Get the version of a certain dataset.

        Arguments:
            source_name (string): The ``source_name`` of the dataset.

        Returns:
            int: Version of the dataset in question.
        """

        hits = self.search("mdf.source_name:{} AND"
                           " mdf.resource_type:dataset".format(source_name),
                           advanced=True, limit=2)

        # Some error checking
        if len(hits) == 0:
            raise ValueError("No such dataset found: " + source_name)
        elif len(hits) > 1:
            raise ValueError("Unexpectedly matched multiple datasets with source_name '{}'. "
                             "Please contact MDF support.".format(source_name))
        else:
            return hits[0]['mdf']['version']

    # ***********************************************
    # * Data retrieval functions
    # ***********************************************

    def http_download(self, results, dest=".", preserve_dir=False, verbose=True):
        """Download data files from the provided results using HTTPS.
        For a large number of files, you should use ``globus_download()`` instead,
        which uses Globus Transfer.

        Arguments:
            results (dict): The records from which files should be fetched.
                    This should be the return value of a search method.
            dest (str): The destination path for the data files on the local machine.
                    **Default:** The current directory.
            preserve_dir (bool): If ``True``, the directory structure for the data files will be
                    recreated at the destination.
                    If ``False``, only the data files themselves will be saved.
                    **Default:** ``False``.
            verbose (bool): If ``True``, status and progress messages will be printed.
                    If ``False``, only error messages will be printed.
                    **Default:** ``True``.

        Returns:
            *dict*: The status information for the download:
                    * **success** (*bool*): ``True`` if the download succeeded. ``False``
                        if it failed.
                    * **message** (*str*): The error message, if the download failed.
        """
        if self.__anonymous:
            print("Error: Anonymous HTTP download not yet supported.")
            return {
                "success": False,
                "message": "Anonymous HTTP download not yet supported."
                }
        # If user submitted single result, make into list
        if isinstance(results, dict):
            results = [results]
        # If results have info attached, remove it
        elif isinstance(results, tuple):
            results = results[0]
        if len(results) > HTTP_NUM_LIMIT:
            print("Error: Too many results supplied. Use globus_download()"
                  + " for fetching more than "
                  + str(HTTP_NUM_LIMIT)
                  + " entries.")
            return {
                "success": False,
                "message": ("Too many results supplied. Use globus_download()"
                            + " for fetching more than "
                            + str(HTTP_NUM_LIMIT)
                            + " entries.")
                }
        for res in tqdm(results, desc="Fetching files", disable=(not verbose)):
            if res["mdf"]["resource_type"] == "dataset":
                print("Skipping datset entry for '{}': Cannot download dataset over HTTPS. "
                      "Use globus_download() for datasets.".format(res["mdf"]["source_id"]))
            elif res["mdf"]["resource_type"] == "record":
                for dl in res.get("files", []):
                    url = dl.get("url", None)
                    if url:
                        parsed_url = urlparse(url)
                        remote_path = parsed_url.path
                        # local_path should be either dest + whole path or dest + filename
                        if preserve_dir:
                            local_path = os.path.normpath(dest + "/" + remote_path)
                        else:
                            local_path = os.path.normpath(dest + "/"
                                                          + os.path.basename(remote_path))
                        # Make dirs for storing the file if they don't exist
                        # preserve_dir doesn't matter; local_path has accounted for it already
                        try:
                            os.makedirs(os.path.dirname(local_path))
                        # If dest is current dir and preserve_dir=False, there are no dirs to make.
                        # os.makedirs() will raise FileNotFoundError (Python3 subclass of IOError).
                        # Since it means all dirs required exist, it can be swallowed.
                        except (IOError, OSError):
                            pass
                        # Check if file already exists, change filename if necessary
                        collisions = 0
                        while os.path.exists(local_path):
                            # Save and remove extension
                            local_path, ext = os.path.splitext(local_path)
                            # Check if already added number to end
                            old_add = "("+str(collisions)+")"
                            collisions += 1
                            new_add = "("+str(collisions)+")"
                            # Remove old number if exists
                            if local_path.endswith(old_add):
                                local_path = local_path[:-len(old_add)]
                            # Add new number
                            local_path = local_path + new_add + ext

                        headers = {}
                        # Check for Petrel vs. NCSA url for authorizer
                        # Petrel
                        if parsed_url.netloc == "e38ee745-6d04-11e5-ba46-22000b92c6ec.e.globus.org":
                            authorizer = self.__petrel_authorizer
                        elif parsed_url.netloc == "data.materialsdatafacility.org":
                            authorizer = self.__data_mdf_authorizer
                        else:
                            authorizer = globus_sdk.NullAuthorizer()
                        authorizer.set_authorization_header(headers)
                        response = requests.get(url, headers=headers)
                        # Handle first 401 by regenerating auth headers
                        if response.status_code == 401:
                            authorizer.handle_missing_authorization()
                            authorizer.set_authorization_header(headers)
                            response = requests.get(url, headers=headers)
                        # Handle other errors by passing the buck to the user
                        if response.status_code != 200:
                            print("Error {} when attempting to access "
                                  "'{}'".format(response.status_code, url))
                        else:
                            # Write out the binary response content
                            with open(local_path, 'wb') as output:
                                output.write(response.content)
            else:
                print("Error: Found unknown resource_type '{}'. "
                      "Skipping entry.".format(res["mdf"]["resource_type"]))
        return {
            "success": True
            }

    def globus_download(self, results, dest=".", dest_ep=None, preserve_dir=False,
                        inactivity_time=None, download_datasets=False, verbose=True):
        """Download data files from the provided results using Globus Transfer.
        This method requires Globus Connect to be installed on the destination endpoint.

        Arguments:
            results (dict): The records from which files should be fetched.
                    This should be the return value of a search method.
            dest (str): The destination path for the data files on the local machine.
                    **Default:** The current directory.
            dest_ep (str): The destination endpoint ID. **Default:** The autodetected local GCP.
            preserve_dir (bool): If ``True``, the directory structure for the data files will be
                    recreated at the destination. The path to the new files
                    will be relative to the ``dest`` path
                    If ``False``, only the data files themselves will be saved.
                    **Default:** ``False``.
            inactivity_time (int): Number of seconds the Transfer is allowed to go without progress
                    before being cancelled.
                    **Default:** ``self.__inactivity_time``.
            download_datasets (bool): If ``True``, will download the full dataset for any dataset
                    entries given.
                    If ``False``, will skip dataset entries with a notification.
                    **Default:** ``False``.

                    Caution:
                        Datasets can be large. Additionally, if you do not
                        filter out records from a dataset you provide, you may end
                        up with duplicate files. Use with care.

            verbose (bool): If ``True``, status and progress messages will be printed,
                    and errors will prompt for continuation confirmation.
                    If ``False``, only error messages will be printed,
                    and the Transfer will always continue.
                    **Default:** ``True``.

        Returns:
            list of str: The task IDs of the Globus transfers.
        """
        if self.__anonymous:
            print("Error: Anonymous Globus Transfer not supported.")
            return {
                "success": False,
                "message": "Anonymous Globus Transfer not supported."
                }
        dest = os.path.abspath(dest)
        # If results have info attached, remove it
        if type(results) is tuple:
            results = results[0]
        if not dest_ep:
            if not self.local_ep:
                self.local_ep = mdf_toolbox.get_local_ep(self.__transfer_client)
            dest_ep = self.local_ep
        if not inactivity_time:
            inactivity_time = self.__inactivity_time

        # Assemble the transfer data
        tasks = {}
        filenames = set()
        links_processed = set()
        for res in tqdm(results, desc="Processing records", disable=(not verbose)):
            file_list = []
            if res["mdf"]["resource_type"] == "dataset":
                if download_datasets:
                    g_link = res.get("data", {}).get("endpoint_path", None)
                    if g_link:
                        file_list.append(g_link)
                elif verbose:
                    print("Skipping dataset '{}' because argument 'download_datasets' is "
                          "False. Use caution if enabling.".format(res["mdf"]["source_id"]))
            elif res["mdf"]["resource_type"] == "record":
                for dl in res.get("files", []):
                    g_link = dl.get("globus", None)
                    if g_link:
                        file_list.append(g_link)
            else:
                print("Error: Found unknown resource_type '{}'. "
                      "Skipping entry.".format(res["mdf"]["resource_type"]))
            for globus_link in file_list:
                # If the data is on a Globus Endpoint
                if globus_link not in links_processed:
                    links_processed.add(globus_link)
                    ep_id = urlparse(globus_link).netloc
                    ep_path = urlparse(globus_link).path
                    # local_path should be either dest + whole path or dest + filename
                    if preserve_dir:
                        # ep_path is absolute, so os.path.join does not work
                        local_path = os.path.abspath(dest + ep_path)
                    else:
                        # If ep_path is to dir, basename is ''
                        # basename(dirname(ep_path)) gives just first dir's name
                        base_name = os.path.basename(ep_path)
                        if not base_name:
                            base_name = os.path.basename(os.path.dirname(ep_path))
                        local_path = os.path.abspath(os.path.join(dest, base_name))

                    # Make dirs for storing the file if they don't exist
                    # preserve_dir doesn't matter; local_path has accounted for it already
                    try:
                        os.makedirs(os.path.dirname(local_path))
                    # If dest is current dir and preserve_dir=False, there are no dirs to make.
                    # os.makedirs() will raise FileNotFoundError (Python3 subclass of IOError).
                    # Since it means all dirs required exist, it can be swallowed.
                    except (IOError, OSError):
                        pass

                    if not preserve_dir:
                        # Check if file already exists, change filename if necessary
                        # The pattern is to add a number just before the extension
                        # (e.g., myfile(1).ext)
                        collisions = 0
                        while os.path.exists(local_path) or local_path in filenames:
                            # Get extension, if exists
                            base_file, ext = os.path.splitext(local_path)
                            # Check if already added number to end
                            old_add = "("+str(collisions)+")"
                            collisions += 1
                            new_add = "("+str(collisions)+")"
                            if base_file.endswith(old_add):
                                local_path = base_file[:-len(old_add)] + new_add + ext
                            else:
                                local_path = base_file + new_add + ext

                    # If ep_path points to a dir, the trailing slash has been removed
                    if ep_path.endswith("/"):
                        local_path += "/"
                    # Add data to list of transfer files
                    if ep_id not in tasks.keys():
                        tasks[ep_id] = []
                    tasks[ep_id].append((ep_path, local_path))
                    filenames.add(local_path)

        # Submit the jobs
        success = 0
        failed = 0
        for task_ep, task_paths in tqdm(tasks.items(), desc="Transferring data",
                                        disable=(not verbose)):
            transfer = mdf_toolbox.custom_transfer(self.__transfer_client, task_ep, dest_ep,
                                                   task_paths, interval=self.__transfer_interval,
                                                   inactivity_time=inactivity_time)
            cont = True
            # Prime loop
            event = next(transfer)
            try:
                # Loop ends on StopIteration from generator exhaustion
                while True:
                    if not event["success"] and cont:
                        print("Error: {} - {}".format(event["code"], event["description"]))
                        if verbose:
                            # Allow user to abort transfer if verbose, else cont is always True
                            user_cont = input("Continue Transfer (y/n)?\n")
                            cont = (user_cont.strip().lower() == "y"
                                    or user_cont.strip().lower() == "yes")
                    event = transfer.send(cont)
            except StopIteration:
                pass
            if not event["success"]:
                print("Error transferring with endpoint '{}': {} - "
                      "{}".format(task_ep, event["status"],
                                  event["nice_status_short_description"]))
                failed += 1
                # Allow cancellation of remaining Transfers if Transfer are remaining
                if verbose and list(tasks.keys())[-1] != task_ep:
                    user_cont = input("Continue Transfer (y/n)?\n")
                    if not (user_cont.strip().lower() == "y"
                            or user_cont.strip().lower() == "yes"):
                        break
            else:
                success += 1

        if verbose:
            print("All transfers processed\n{} transfers succeeded\n"
                  "{} transfers failed".format(success, failed))
        return

    def http_stream(self, results, verbose=True):
        """Yield data files from the provided results using HTTPS, through a generator.
        For a large number of files, you should use ``globus_download()`` instead,
        which uses Globus Transfer.

        Arguments:
            results (dict): The records from which files should be fetched.
                    This should be the return value of a search method.
            verbose (bool): If ``True``, status and progress messages will be printed.
                    If ``False``, only error messages will be printed.
                    **Default:** ``True``.

        Yields:
            str: Text of each data file.
        """
        if self.__anonymous:
            print("Error: Anonymous HTTP download not yet supported.")
            yield {
                "success": False,
                "message": "Anonymous HTTP download not yet supported."
                }
            return
        # If results have info attached, remove it
        if type(results) is tuple:
            results = results[0]
        if type(results) is not list:
            results = [results]
        if len(results) > HTTP_NUM_LIMIT:
            print("Too many results supplied. Use globus_download()"
                  + " for fetching more than "
                  + str(HTTP_NUM_LIMIT)
                  + " entries.")
            yield {
                "success": False,
                "message": ("Too many results supplied. Use globus_download()"
                            + " for fetching more than "
                            + str(HTTP_NUM_LIMIT)
                            + " entries.")
                }
            return
        for res in results:
            for dl in res.get("files", []):
                url = dl.get("url", None)
                if url:
                    parsed_url = urlparse(url)
                    headers = {}
                    # Check for Petrel vs. NCSA url for authorizer
                    # Petrel
                    if parsed_url.netloc == "e38ee745-6d04-11e5-ba46-22000b92c6ec.e.globus.org":
                        authorizer = self.__petrel_authorizer
                    elif parsed_url.netloc == "data.materialsdatafacility.org":
                        authorizer = self.__data_mdf_authorizer
                    else:
                        authorizer = globus_sdk.NullAuthorizer()
                    authorizer.set_authorization_header(headers)
                    response = requests.get(url, headers=headers)
                    # Handle first 401 by regenerating auth headers
                    if response.status_code == 401:
                        authorizer.handle_missing_authorization()
                        authorizer.set_authorization_header(headers)
                        response = requests.get(url, headers=headers)
                    # Handle other errors by passing the buck to the user
                    if response.status_code != 200:
                        print("Error ", response.status_code, " when attempting to access '",
                              url, "'", sep="")
                        yield None
                    else:
                        yield response.text


class Query:
    """
    Danger:
        The ``Query`` class is meant for internal ``Forge`` use. General users should not
        instantiate a ``Query`` object directly, but advanced users may do so at their own risk.

        Using a ``Query`` directly is an officially unsupported behavior
        and may be subject to breaking, unlisted changes in the future.

    Notes:
        Query strings may end up wrapped in parentheses, which has no direct effect on the search.
        Adding terms must be chained with ``and()`` or ``or()``.
        Terms will not have spaces in between otherwise, and it is desirable to be explicit about
        which terms are required.
    """
    def __init__(self, search_client, q=None, limit=None, advanced=False):
        """Create a Query object.

        Arguments:
            search_client (globus_sdk.SearchClient): The Globus Search client to use for searching.
            q (str): The query string to start with. **Default:** Not set.
            limit (int): The maximum number of results to return. **Default:** Not set.
            advanced (bool): If ``True``, will submit query in "advanced" mode to
                enable field matches.
                If ``False``, only basic fulltext term matches will be supported (unless
                ``advanced`` is set after instantiation).
                **Default:** ``False``.
        """
        self.__search_client = search_client
        self.query = q or "("
        self.limit = limit
        self.advanced = advanced
        # initialized is True if something has been added to the query
        # __init__(), term(), and field() can change this value to True
        self.initialized = not self.query == "("

    def __clean_query_string(self, q):
        """Clean up a query string for searching.
        This method does not access self, so that a search will not change state.

        Returns:
            str: The clean query string.
        """
        q = q.replace("()", "").strip()
        if q.endswith("("):
            q = q[:-1].strip()
        # Remove misplaced AND/OR/NOT at end
        if q[-3:] == "AND" or q[-3:] == "NOT":
            q = q[:-3]
        elif q[-2:] == "OR":
            q = q[:-2]

        # Balance parentheses
        while q.count("(") > q.count(")"):
            q += ")"
        while q.count(")") > q.count("("):
            q = "(" + q

        return q.strip()

    def clean_query(self):
        """Returns the current query, cleaned for user consumption.

        Returns:
            str: The clean current query.
        """
        return self.__clean_query_string(self.query)

    def term(self, term):
        """Add a term to the query.

        Arguments:
            term (str): The term to add.

        Returns:
            Query: Self
        """
        self.query += term
        self.initialized = True
        return self

    def field(self, field, value):
        """Add a ``field:value`` term to the query.
        Matches will have the ``value`` in the ``field``.

        Note:
            This method triggers advanced mode.

        Arguments:
            field (str): The field to check for the value, in Elasticsearch dot syntax.
            value (str): The value to match.

        Returns:
            Query: Self
        """
        # Cannot add field:value if one is blank
        if field and value:
            self.query += field + ":" + value
            # Field matches are advanced queries
            self.advanced = True
            self.initialized = True
        return self

    def operator(self, op, close_group=False):
        """Add an operator between terms.
        There must be a term added before using this method.
        All operators have helpers, so this method is usually not necessary to directly invoke.

        Arguments:
            op (str): The operator to add. Must be in the OP_LIST.
                close_group (bool): If ``True``, will end the current parenthetical
                group and start a new one.
                If ``False``, will continue current group.

                Example::
                    "(foo AND bar)" is one group.
                    "(foo) AND (bar)" is two groups.

        Returns:
            Query: Self
        """
        # List of allowed operators
        OP_LIST = ["AND", "OR", "NOT"]
        op = op.upper().strip()
        if op not in OP_LIST:
            print("Error: '", op, "' is not a valid operator.", sep='')
        else:
            if close_group:
                op = ") " + op + " ("
            else:
                op = " " + op + " "
            self.query += op
        return self

    def and_join(self, close_group=False):
        """Combine terms with AND.
        There must be a term added before using this method.

        Arguments:
            close_group (bool): If ``True``, will end the current group and start a new one.
                    If ``False``, will continue current group.

                    Example::

                        If the current query is "(term1"
                        .and(close_group=True) => "(term1) AND ("
                        .and(close_group=False) => "(term1 AND "

        Returns:
            Query: Self
        """
        if not self.initialized:
            print("Error: You must add a term before adding an operator.",
                  "The current query has not been changed.")
        else:
            self.operator("AND", close_group=close_group)
        return self

    def or_join(self, close_group=False):
        """Combine terms with OR.
        There must be a term added before using this method.

        Arguments:
            close_group (bool): If ``True``, will end the current group and start a new one.
                    If ``False``, will continue current group.

                    Example:

                        If the current query is "(term1"
                        .or(close_group=True) => "(term1) OR("
                        .or(close_group=False) => "(term1 OR "

        Returns:
            Query: Self
        """
        if not self.initialized:
            print("Error: You must add a term before adding an operator.",
                  "The current query has not been changed.")
        else:
            self.operator("OR", close_group=close_group)
        return self

    def negate(self):
        """Negates the next added term with NOT.

        Returns:
            Query: Self
        """
        self.operator("NOT")
        return self

    def search(self, q=None, index=None, advanced=None, limit=None, info=False, retries=3):
        """Execute a search and return the results, up to the ``SEARCH_LIMIT``.

        Arguments:
            q (str): The query to execute. **Default:** The current helper-formed query, if any.
                    There must be some query to execute.
            index (str): The Search index to search on. **Required**.
            advanced (bool): If ``True``, will submit query in "advanced" mode
                to enable field matches and other advanced features.
                If ``False``, only basic fulltext term matches will be supported.
                **Default:** ``False`` if no helpers have been used to build the query, or
                ``True`` if helpers have been used.
            limit (int): The maximum number of results to return.
                    The max for this argument is the ``SEARCH_LIMIT`` imposed by Globus Search.
                    **Default:** ``SEARCH_LIMIT`` for advanced-mode queries,
                    ``NONADVANCED_LIMIT`` for limited-mode queries.
            info (bool): If ``False``, search will return a list of the results.
                    If ``True``, search will return a tuple containing the results list
                    and other information about the query.
                    **Default:** ``False``.
            retries (int): The number of times to retry a Search query if it fails.
                           **Default:** 3.

        Returns:
            If ``info`` is ``False``, *list*: The search results.
            If ``info`` is ``True``, *tuple*: The search results,
            and a dictionary of query information.
        """

        if q is None:
            q = self.query
        if not q.strip("()"):
            print("Error: No query")
            return ([], {"error": "No query"}) if info else []
        if index is None:
            print("Error: No index specified")
            return ([], {"error": "No index"}) if info else []
        else:
            uuid_index = mdf_toolbox.translate_index(index)
        if advanced is None or self.advanced:
            advanced = self.advanced
        if limit is None:
            limit = self.limit or (SEARCH_LIMIT if advanced else NONADVANCED_LIMIT)
        if limit > SEARCH_LIMIT:
            limit = SEARCH_LIMIT

        q = self.__clean_query_string(q)

        # Simple query (max 10k results)
        qu = {
            "q": q,
            "advanced": advanced,
            "limit": limit,
            "offset": 0
            }
        tries = 0
        errors = []
        while True:
            try:
                search_res = self.__search_client.post_search(uuid_index, qu)
            except globus_sdk.SearchAPIError as e:
                if tries >= retries:
                    raise
                else:
                    errors.append(repr(e))
            except Exception as e:
                if tries >= retries:
                    raise
                else:
                    errors.append(repr(e))
            else:
                break
            tries += 1
        res = mdf_toolbox.gmeta_pop(search_res, info=info)
        # Add additional info
        if info:
            res[1]["query"] = qu
            res[1]["index"] = index
            res[1]["index_uuid"] = uuid_index
            res[1]["retries"] = tries
            res[1]["errors"] = errors
        return res

    def aggregate(self, q=None, index=None, retries=1, scroll_size=SEARCH_LIMIT):
        """Perform an advanced query, and return *all* matching results.
        Will automatically perform multiple queries in order to retrieve all results.

        Note:
            All ``aggregate`` queries run in advanced mode, and ``info`` is not available.

        Arguments:
            q (str): The query to execute. The current helper-formed query, if any.
                    There must be some query to execute.
            index (str): The Search index to search on. Required.
            retries (int): The number of times to retry a Search query if it fails.
                           **Default:** 1.
            scroll_size (int): Maximum number of records returned per query. Must be
                    between one and the ``SEARCH_LIMIT`` (inclusive).
                    **Default:** ``SEARCH_LIMIT``.

        Returns:
            list of dict: All matching entries.
        """
        if q is None:
            q = self.query
        if not q.strip("()"):
            print("Error: No query")
            return []
        if index is None:
            print("Error: No index specified")
            return []
        if scroll_size <= 0:
            scroll_size = 1

        q = self.__clean_query_string(q)

        # Get the total number of records
        total = self.search(q, index=index, limit=0, advanced=True,
                            info=True)[1]["total_query_matches"]

        # If aggregate is unnecessary, use Search automatically instead
        if total <= SEARCH_LIMIT:
            return self.search(q, index=index, limit=SEARCH_LIMIT, advanced=True)

        # Scroll until all results are found
        output = []

        scroll_pos = 0
        with tqdm(total=total) as pbar:
            while len(output) < total:

                # Scroll until the width is small enough to get all records
                #   `scroll_id`s are unique to each dataset. If multiple datasets
                #   match a certain query, the total number of matching records
                #   may exceed the maximum that search will return - even if the
                #   scroll width is much smaller than that maximum
                scroll_width = scroll_size
                while True:
                    query = "(" + q + ') AND (mdf.scroll_id:>=%d AND mdf.scroll_id:<%d)' % (
                                            scroll_pos, scroll_pos+scroll_width)
                    results, info = self.search(query, index=index, advanced=True,
                                                info=True, retries=retries)

                    # Check to make sure that all the matching records were returned
                    if info["total_query_matches"] <= len(results):
                        break

                    # If not, reduce the scroll width
                    # new_width is proportional with the proportion of results returned
                    new_width = scroll_width * (len(results) // info["total_query_matches"])
                    # scroll_width should never be 0, and should only be 1 in rare circumstances
                    scroll_width = new_width if new_width > 1 else max(scroll_width//2, 1)

                # Append the results to the output
                output.extend(results)
                pbar.update(len(results))
                scroll_pos += scroll_width

        return output

    def mapping(self, index):
        """Fetch the entire mapping for the specified index.

        Arguments:
            index (str): The index to map.

        Returns:
            dict: The full mapping for the index.
        """
        return (self.__search_client.get(
                    "/unstable/index/{}/mapping".format(mdf_toolbox.translate_index(index)))
                ["mappings"])
