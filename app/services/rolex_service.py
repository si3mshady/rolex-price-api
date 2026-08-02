import statistics
from math import ceil
from typing import List, Optional, Dict, Any, Tuple

from app.config import settings
from app.models.watch import Watch
from app.schemas.watch import WatchSchema, PaginatedWatchResponse, WatchReferenceDetailResponse
from app.schemas.collection import CollectionSummary, CollectionListResponse
from app.schemas.statistics import StatisticsResponse, PriceStatistics, SizeStatistics
from app.schemas.health import HealthResponse
from app.utils.data_loader import load_rolex_data


class RolexNotFoundError(Exception):
    """Exception raised when a requested Rolex resource is not found."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class RolexService:
    """
    Business logic layer for Rolex watch catalog operations, search, analytics, and collection breakdown.
    """

    def __init__(self, watches: Optional[List[Watch]] = None):
        if watches is not None:
            self._watches = watches
        else:
            try:
                data_path = settings.resolve_data_path()
                self._watches = load_rolex_data(data_path)
            except Exception as err:
                self._watches = []

    def set_watches(self, watches: List[Watch]) -> None:
        """Explicitly set the in-memory watch collection."""
        self._watches = watches

    @property
    def watch_count(self) -> int:
        return len(self._watches)

    def get_health_status(self) -> HealthResponse:
        """
        Returns system health and catalog state.
        """
        from datetime import datetime, timezone
        return HealthResponse(
            status="healthy",
            app_name=settings.APP_NAME,
            version=settings.APP_VERSION,
            timestamp=datetime.now(timezone.utc),
            watches_loaded=len(self._watches),
        )

    def get_watches(
        self,
        collection: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_size: Optional[int] = None,
        max_size: Optional[int] = None,
        complication: Optional[str] = None,
        is_por: Optional[bool] = None,
        sort_by: str = "reference",
        sort_order: str = "asc",
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedWatchResponse:
        """
        Retrieves paginated watches matching the provided query filters.
        """
        filtered = self._apply_filters(
            watches=self._watches,
            collection=collection,
            min_price=min_price,
            max_price=max_price,
            min_size=min_size,
            max_size=max_size,
            complication=complication,
            is_por=is_por,
        )

        sorted_watches = self._sort_watches(filtered, sort_by=sort_by, sort_order=sort_order)
        return self._paginate(sorted_watches, page=page, limit=limit)

    def get_watch_by_reference(self, reference: str) -> WatchReferenceDetailResponse:
        """
        Retrieves all watch variants associated with a specific Rolex reference number.
        """
        ref_norm = reference.strip().upper()
        matching = [w for w in self._watches if w.reference.upper() == ref_norm]

        if not matching:
            raise RolexNotFoundError(f"Rolex reference '{reference}' was not found in the catalog.")

        canonical_ref = matching[0].reference
        canonical_collection = matching[0].collection
        priced_variants = [w.price for w in matching if w.price is not None]

        min_price = min(priced_variants) if priced_variants else None
        max_price = max(priced_variants) if priced_variants else None

        variants_schemas = [WatchSchema.model_validate(w) for w in matching]

        return WatchReferenceDetailResponse(
            reference=canonical_ref,
            collection=canonical_collection,
            variants_count=len(matching),
            min_price=min_price,
            max_price=max_price,
            variants=variants_schemas,
        )

    def get_collections(
        self,
        sort_by: str = "name",
        sort_order: str = "asc",
    ) -> CollectionListResponse:
        """
        Groups catalog watches by collection family and computes aggregate statistics.
        """
        collections_map: Dict[str, List[Watch]] = {}
        for w in self._watches:
            collections_map.setdefault(w.collection, []).append(w)

        summaries: List[CollectionSummary] = []
        for name, items in collections_map.items():
            priced = [w.price for w in items if w.price is not None]
            min_p = min(priced) if priced else None
            max_p = max(priced) if priced else None
            avg_p = round(statistics.mean(priced), 2) if priced else None

            sizes = sorted(list({w.size for w in items}))
            comps = sorted(list({comp for w in items for comp in w.complications}))

            summaries.append(
                CollectionSummary(
                    name=name,
                    watch_count=len(items),
                    min_price=min_p,
                    max_price=max_p,
                    avg_price=avg_p,
                    sizes=sizes,
                    complications=comps,
                )
            )

        # Sorting collections
        reverse = (sort_order.lower() == "desc")
        if sort_by == "watch_count":
            summaries.sort(key=lambda c: c.watch_count, reverse=reverse)
        elif sort_by == "avg_price":
            summaries.sort(key=lambda c: (c.avg_price if c.avg_price is not None else -1), reverse=reverse)
        else:  # default to name
            summaries.sort(key=lambda c: c.name.lower(), reverse=reverse)

        return CollectionListResponse(
            total_collections=len(summaries),
            collections=summaries,
        )

    def search_watches(
        self,
        q: str,
        page: int = 1,
        limit: int = 20,
        collection: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> PaginatedWatchResponse:
        """
        Performs full-text keyword search across reference, collection, description, and complications.
        """
        query_terms = [t.lower() for t in q.strip().split() if t.strip()]

        matched: List[Watch] = []
        for w in self._watches:
            searchable_text = f"{w.reference} {w.collection} {w.description} {' '.join(w.complications)}".lower()
            if all(term in searchable_text for term in query_terms):
                matched.append(w)

        filtered = self._apply_filters(
            watches=matched,
            collection=collection,
            min_price=min_price,
            max_price=max_price,
        )

        return self._paginate(filtered, page=page, limit=limit)

    def get_statistics(self) -> StatisticsResponse:
        """
        Calculates catalog-wide price distributions, size distributions, collection breakdowns, and highlights.
        """
        total_watches = len(self._watches)
        unique_refs = len({w.reference for w in self._watches})
        unique_collections = len({w.collection for w in self._watches})

        priced_watches = [w for w in self._watches if w.price is not None]
        prices = [w.price for w in priced_watches if w.price is not None]
        por_count = total_watches - len(priced_watches)

        if prices:
            min_price = min(prices)
            max_price = max(prices)
            avg_price = round(statistics.mean(prices), 2)
            median_price = round(statistics.median(prices), 2)
        else:
            min_price = max_price = avg_price = median_price = None

        price_stats = PriceStatistics(
            total_priced_watches=len(priced_watches),
            total_por_watches=por_count,
            min_price=min_price,
            max_price=max_price,
            avg_price=avg_price,
            median_price=median_price,
        )

        sizes = [w.size for w in self._watches if w.size > 0]
        size_dist: Dict[int, int] = {}
        for s in sizes:
            size_dist[s] = size_dist.get(s, 0) + 1

        if sizes:
            min_size = min(sizes)
            max_size = max(sizes)
            avg_size = round(statistics.mean(sizes), 2)
        else:
            min_size = max_size = 0
            avg_size = 0.0

        size_stats = SizeStatistics(
            min_size=min_size,
            max_size=max_size,
            avg_size=avg_size,
            size_distribution=dict(sorted(size_dist.items())),
        )

        collection_counts: Dict[str, int] = {}
        for w in self._watches:
            collection_counts[w.collection] = collection_counts.get(w.collection, 0) + 1

        complication_counts: Dict[str, int] = {}
        for w in self._watches:
            for comp in w.complications:
                complication_counts[comp] = complication_counts.get(comp, 0) + 1

        sorted_priced = sorted(priced_watches, key=lambda w: w.price if w.price is not None else 0, reverse=True)
        most_expensive = [WatchSchema.model_validate(w) for w in sorted_priced[:5]]
        least_expensive = [WatchSchema.model_validate(w) for w in sorted_priced[-5:][::-1]]

        return StatisticsResponse(
            total_watches=total_watches,
            total_unique_references=unique_refs,
            total_collections=unique_collections,
            price_stats=price_stats,
            size_stats=size_stats,
            collection_counts=dict(sorted(collection_counts.items(), key=lambda x: x[1], reverse=True)),
            complication_counts=dict(sorted(complication_counts.items(), key=lambda x: x[1], reverse=True)),
            most_expensive_watches=most_expensive,
            least_expensive_watches=least_expensive,
        )

    def _apply_filters(
        self,
        watches: List[Watch],
        collection: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_size: Optional[int] = None,
        max_size: Optional[int] = None,
        complication: Optional[str] = None,
        is_por: Optional[bool] = None,
    ) -> List[Watch]:
        filtered = watches

        if collection:
            coll_clean = collection.strip().lower()
            filtered = [w for w in filtered if coll_clean in w.collection.lower()]

        if min_price is not None:
            filtered = [w for w in filtered if w.price is not None and w.price >= min_price]

        if max_price is not None:
            filtered = [w for w in filtered if w.price is not None and w.price <= max_price]

        if min_size is not None:
            filtered = [w for w in filtered if w.size >= min_size]

        if max_size is not None:
            filtered = [w for w in filtered if w.size <= max_size]

        if complication:
            comp_clean = complication.strip().lower()
            filtered = [
                w for w in filtered
                if any(comp_clean in c.lower() for c in w.complications)
            ]

        if is_por is not None:
            filtered = [w for w in filtered if w.is_por == is_por]

        return filtered

    def _sort_watches(self, watches: List[Watch], sort_by: str, sort_order: str) -> List[Watch]:
        reverse = (sort_order.lower() == "desc")

        def sort_key(w: Watch):
            if sort_by == "price":
                # Put POR (None price) at the end regardless of sort direction if ascending, or beginning if descending
                if w.price is None:
                    return -1.0 if reverse else float("inf")
                return w.price
            elif sort_by == "collection":
                return w.collection.lower()
            elif sort_by == "size":
                return w.size
            else:  # reference
                return w.reference.lower()

        return sorted(watches, key=sort_key, reverse=reverse)

    def _paginate(self, watches: List[Watch], page: int, limit: int) -> PaginatedWatchResponse:
        total = len(watches)
        total_pages = ceil(total / limit) if limit > 0 else 1
        page = max(1, page)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit

        items = [WatchSchema.model_validate(w) for w in watches[start_idx:end_idx]]

        return PaginatedWatchResponse(
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
            items=items,
        )


# Global service instance singleton
rolex_service = RolexService()
