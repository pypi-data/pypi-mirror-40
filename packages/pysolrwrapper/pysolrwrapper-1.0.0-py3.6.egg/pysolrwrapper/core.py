import logging
from pysolr import (ZooKeeper, SolrCloud)
from pysolrwrapper import utils
from pysolrwrapper.filter import Filter


class SolrQuery():

    def __init__(self, zookeeper: str, collection: str):
        ZooKeeper.CLUSTER_STATE = f'/collections/{collection}/state.json'
        self.solr_cloud = SolrCloud(ZooKeeper(
            zookeeper), collection, results_cls=dict)
        self._t = []
        self._query = None
        self._sort = []
        self._conf = {
            'defType': 'edismax',
            'fl': '*',
            'qf':  'concept_synonym_name^1 concept_name^2 concept_mapped_name^1',
            'pf3': 'concept_synonym_name^3 concept_name^6 concept_mapped_name^3',
            'ps3': '2',
            'sort': 'score desc',
            'hl': 'false',
            'hl.method': 'unified',
            'termVectors': 'true',
            'hl.fragsize': 10,
            'hl.snippets': 10,
            'hl.requireFieldMatch': 'true',
            'hl.fl': 'concept_name,concept_synonym_name,concept_mapped_name',
            'sow': 'false',
            'rows': 15,
            'wt': 'python',
            'facet': 'false',
            'facet.field': ['domain_id', 'standard_concept'],
            'facet.limit': 5,
            'hl.tag.pre': "<b style='background-color:#fffbb8;'>",
            'hl.tag.post': "</b>",
        }

#    def boost(self, attr: str, order: str):
#        self._conf['sort'] = f"{attr} {order}"
#        return(self)

    def select(self, columns: [str]):
        self._conf['fl'] = ",".join(columns)
        return(self)

    def sort(self, attr: str, order: str):
        self._sort.append(f"{attr} {order}")
        return(self)

    def limit(self, num: int):
        self._conf['rows'] = num
        return(self)

    def facet(self, limit: int, columns: [str]):
        self._conf['facet'] = 'true'
        self._conf["facet.field"] = columns
        self._conf["facet.limit"] = limit
        if limit == -1:
            self._conf.pop("facet.limit", None)
        return(self)

    def highlight(self, columns: [str]):
        self._conf['hl'] = 'true'
        self._conf['hl.fl'] = ",".join(columns)
        return(self)

    def set_type_simple(self):
        self._conf['defType'] = 'simple'
        return(self)

    def set_type_edismax(self):
        self._conf['defType'] = 'edismax'
        return(self)

    def add_filter(self, value: [Filter]):
        self._t.append(str(value))
        return(self)

    def run(self) -> dict:
        self._query = " AND ".join(self._t)
        if len(self._sort) > 0:
            self._conf['sort'] = ", ".join(self._sort)
        results = self.solr_cloud.search(
            q=self._query,  **self._conf)
        logging.warning(str(self._conf))
        logging.warning(str(self._query))
        return(utils.convert_result(results))

