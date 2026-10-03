from uuid import UUID
from decimal import Decimal, ROUND_HALF_UP
import logging

from src.infrastructure.database.connection import AsyncSessionLocal
from src.infrastructure.database.track.repository import TrackRepository
from src.infrastructure.database.album.repository import AlbumRepository
from src.infrastructure.database.artist.repository import ArtistRepository
from src.application.review.score_aggregation_service import ScoreAggregationService, TrackScoreData, AlbumScoreData

logger = logging.getLogger(__name__)

class AggregationOrchestrator:
    @staticmethod
    async def run_aggregation_for_new_review(track_id: UUID, new_score_value: float) -> None:
        async with AsyncSessionLocal() as session:
            try:
                track_repo = TrackRepository(session)
                album_repo = AlbumRepository(session)
                artist_repo = ArtistRepository(session)

                track = await track_repo.get_by_id(track_id)
                if not track:
                    return

                old_count = track.review_count or 0
                old_avg = track.average_score or Decimal("0.0")
                new_score = Decimal(str(new_score_value))

                new_count = old_count + 1
                new_avg = ((old_avg * Decimal(old_count)) + new_score) / Decimal(new_count)
                
                track_average = new_avg.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

                await track_repo.update(track.id, {
                    "average_score": track_average,
                    "review_count": new_count
                })

                album = await album_repo.get_by_id(track.album_id)
                if album:
                    album_tracks = await track_repo.get_by_album(album.id)
                    
                    track_data_list = [
                        TrackScoreData(average=t.average_score, review_count=t.review_count)
                        for t in album_tracks 
                        if t.review_count > 0 and t.average_score is not None
                    ]

                    if track_data_list:
                        album_agg = ScoreAggregationService.calculate_album_average(
                            tracks=track_data_list,
                            total_tracks=album.total_tracks or len(album_tracks)
                        )
                        
                        await album_repo.update(album.id, {
                            "average_score": album_agg.average,
                            "review_count": album_agg.reviewed_count
                        })

                    artist = await artist_repo.get_by_id(album.artist_id)
                    if artist:
                        artist_albums = await album_repo.get_by_artist(artist.id)
                        
                        album_data_list = [
                            AlbumScoreData(average=a.average_score, reviewed_tracks=a.review_count)
                            for a in artist_albums 
                            if a.review_count > 0 and a.average_score is not None
                        ]

                        if album_data_list:
                            artist_agg = ScoreAggregationService.calculate_artist_average(
                                albums=album_data_list,
                                total_albums=len(artist_albums)
                            )
                            
                            await artist_repo.update(artist.id, {
                                "average_score": artist_agg.average,
                                "review_count": artist_agg.reviewed_count
                            })

                await session.commit()
                logger.info(f"Notas agregadas em cascata com sucesso para a track {track_id}")

            except Exception as e:
                await session.rollback()
                logger.error(f"Erro ao agregar notas da track {track_id}: {str(e)}")