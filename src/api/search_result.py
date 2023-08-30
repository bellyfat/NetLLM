import json
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional


@dataclass
class SearchParameters:
    query: str
    location: str
    language: str
    num_results: int
    autocorrect: bool
    page: int
    search_engine: str


@dataclass
class KnowledgeGraph:
    title: str
    type: str
    website: str
    description: str
    description_source: str
    description_link: str
    attributes: Dict[str, str]


@dataclass
class OrganicResult:
    title: str
    link: str
    snippet: str
    position: int
    date: str


@dataclass
class PeopleAlsoAsk:
    question: str
    snippet: str
    title: str
    link: str


@dataclass
class TopStory:
    title: str
    link: str
    source: str
    date: str


@dataclass
class RelateSearch:
    query: str


@dataclass
class UsefulInfo:
    knowledge_graph: Optional[KnowledgeGraph]
    organic_results: List[OrganicResult]
    people_also_ask: Optional[PeopleAlsoAsk]
    top_stories: Optional[TopStory]

    def __str__(self) -> str:
        return json.dumps(asdict(self), indent=None, ensure_ascii=False)


@dataclass
class SearchResult:
    search_parameters: SearchParameters
    knowledge_graph: Optional[KnowledgeGraph]
    organic_results: List[OrganicResult]
    top_stories: Optional[TopStory]
    people_also_ask: Optional[PeopleAlsoAsk]
    related_searches: Optional[RelateSearch]

    def __init__(self, search_result_json: Dict):
        # Map SearchParameters
        self.search_parameters = SearchParameters(
            query=search_result_json["searchParameters"]["q"],
            location=search_result_json["searchParameters"].get("gl", ""),
            language=search_result_json["searchParameters"].get("hl", ""),
            num_results=search_result_json["searchParameters"].get("num", 0),
            autocorrect=search_result_json["searchParameters"].get(
                "autocorrect", False
            ),
            page=search_result_json["searchParameters"].get("page", 1),
            search_engine=search_result_json["searchParameters"].get("engine", ""),
        )

        # Map KnowledgeGraph
        knowledge_graph_data = search_result_json.get("knowledgeGraph", {})
        self.knowledge_graph = (
            KnowledgeGraph(
                title=knowledge_graph_data.get("title", ""),
                type=knowledge_graph_data.get("type", ""),
                website=knowledge_graph_data.get("website", ""),
                description=knowledge_graph_data.get("description", ""),
                description_source=knowledge_graph_data.get("descriptionSource", ""),
                description_link=knowledge_graph_data.get("descriptionLink", ""),
                attributes=knowledge_graph_data.get("attributes", {}),
            )
            if knowledge_graph_data
            else None
        )

        # Map OrganicResults
        organic_results_data = search_result_json.get("organic", [])
        self.organic_results = [
            OrganicResult(
                title=result.get("title", ""),
                link=result.get("link", ""),
                snippet=result.get("snippet", ""),
                date=result.get("date", ""),
                position=result.get("position", ""),
            )
            for result in organic_results_data
        ]

        # Additional Fields
        self.top_stories = search_result_json.get("topStories", None)
        self.people_also_ask = search_result_json.get("peopleAlsoAsk", None)
        self.related_searches = search_result_json.get("relatedSearches", None)

        self.useful_info = self.get_useful_info()

    def get_useful_info(self) -> UsefulInfo:
        return UsefulInfo(
            knowledge_graph=self.knowledge_graph,
            organic_results=self.organic_results[:3],
            people_also_ask=self.people_also_ask[:1],
            top_stories=self.top_stories[:1],
        )
