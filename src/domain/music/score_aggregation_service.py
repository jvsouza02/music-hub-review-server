from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import NamedTuple

class TrackScoreData(NamedTuple):
    average: Decimal
    review_count: int

class AlbumScoreData(NamedTuple):
    average: Decimal
    reviewed_tracks: int

@dataclass(frozen=True)
class AggregationResult:
    average: Decimal | None
    reviewed_count: int
    total_count: int
    coverage: Decimal
    is_visible: bool

class ScoreAggregationService:
    @staticmethod
    def calculate_album_average(
        tracks: list[TrackScoreData],
        total_tracks: int,
        min_coverage: Decimal = Decimal("0.5"),
        min_abs_tracks: int = 3,
    ) -> AggregationResult:
        reviewed_count = len(tracks)
        coverage = Decimal(reviewed_count) / Decimal(total_tracks)
        is_visible = coverage>=min_coverage or reviewed_count>=min_abs_tracks

        average = None
        if is_visible and tracks:
            weighted_sum = sum(
                track.average * track.review_count
                for track in tracks
            )
            
            total_reviews = sum(track.review_count for track in tracks)
            
            average = (weighted_sum / total_reviews).quantize(
                Decimal("0.1"), rounding=ROUND_HALF_UP
            )

        return AggregationResult(
            average=average,
            reviewed_count=reviewed_count,
            total_count=total_tracks,
            coverage=coverage,
            is_visible=is_visible
        )

    @staticmethod
    def calculate_artist_average(
        albums: list[AlbumScoreData],
        total_albums: int,
        min_coverage: Decimal = Decimal("0.5"),
        min_abs_albums: int = 2,
    ) -> AggregationResult:
        reviewed_count = len(albums)
        coverage = Decimal(reviewed_count) / Decimal(total_albums)
        is_visible = coverage>=min_coverage or reviewed_count>=min_abs_albums

        average = None
        if is_visible and albums:
            weighted_sum = sum(
                album.average * album.review_count
                for album in albums
            )
            
            total_reviews = sum(album.review_count for album in albums)
            
            average = (weighted_sum / total_reviews).quantize(
                Decimal("0.1"), rounding=ROUND_HALF_UP
            )

        return AggregationResult(
            average=average,
            reviewed_count=reviewed_count,
            total_count=total_albums,
            coverage=coverage,
            is_visible=is_visible
        )