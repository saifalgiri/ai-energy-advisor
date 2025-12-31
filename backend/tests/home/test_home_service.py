
import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.home_service import HomeService
from app.schemas.home_schema import HomeCreate


class TestHomeService:    
    @pytest.mark.asyncio
    async def test_create_home_success(self, db_session: AsyncSession):
        # Arrange
        service = HomeService(db_session)
        home_data = HomeCreate(
            size_sqft=1500,
            year_built=1990,
            heating_type="gas",
            insulation_level="moderate",
            windows_type="double",
            roof_type="pitched",
            num_occupants=3,
            monthly_energy_bill=150.50,
            location="Berlin, Germany"
        )
        
        # Act
        home = await service.create_home(home_data)
        
        # Assert
        assert home is not None
        assert home.id is not None
        assert home.size_sqft == 1500
        assert home.year_built == 1990
        assert home.heating_type.value == "gas"
        assert home.insulation_level.value == "moderate"
        assert home.windows_type.value == "double"
        assert home.roof_type.value == "pitched"
        assert home.num_occupants == 3
        assert home.monthly_energy_bill == 150.50
        assert home.location == "Berlin, Germany"
        assert home.created_at is not None
    
    @pytest.mark.asyncio
    async def test_create_home_validates_data(self, db_session: AsyncSession):
        # Arrange
        service = HomeService(db_session)
        
        # Act & Assert - Invalid size (negative)
        with pytest.raises(Exception):  # Pydantic ValidationError
            home_data = HomeCreate(
                size_sqft=-100,  # Invalid!
                year_built=1990,
                heating_type="gas",
                insulation_level="moderate",
                windows_type="double",
                num_occupants=3,
                monthly_energy_bill=150.50,
                location="Berlin, Germany"
            )
        
        # Act & Assert - Invalid year (future)
        with pytest.raises(Exception):
            home_data = HomeCreate(
                size_sqft=1500,
                year_built=3000,  # Invalid!
                heating_type="gas",
                insulation_level="moderate",
                windows_type="double",
                num_occupants=3,
                monthly_energy_bill=150.50,
                location="Berlin, Germany"
            )
        
        # Act & Assert - Invalid heating type
        with pytest.raises(Exception):
            home_data = HomeCreate(
                size_sqft=1500,
                year_built=1990,
                heating_type="invalid",  # Invalid!
                insulation_level="moderate",
                windows_type="double",
                num_occupants=3,
                monthly_energy_bill=150.50,
                location="Berlin, Germany"
            )
    
    @pytest.mark.asyncio
    async def test_create_home_validates_bill_limit(self, db_session: AsyncSession):
        """Test that monthly bill validation works"""
        # Arrange
        service = HomeService(db_session)
        
        # Act & Assert - Bill too high
        with pytest.raises(Exception):  
            home_data = HomeCreate(
                size_sqft=1500,
                year_built=1990,
                heating_type="gas",
                insulation_level="moderate",
                windows_type="double",
                num_occupants=3,
                monthly_energy_bill=15000.00,  # Too high!
                location="Berlin, Germany"
            )
    
    @pytest.mark.asyncio
    async def test_get_home_success(self, db_session: AsyncSession):
        # Arrange
        service = HomeService(db_session)
        home_data = HomeCreate(
            size_sqft=1500,
            year_built=1990,
            heating_type="gas",
            insulation_level="moderate",
            windows_type="double",
            roof_type="pitched",
            num_occupants=3,
            monthly_energy_bill=150.50,
            location="Berlin, Germany"
        )
        created_home = await service.create_home(home_data)
        
        # Act
        retrieved_home = await service.get_home(created_home.id)
        
        # Assert
        assert retrieved_home is not None
        assert retrieved_home.id == created_home.id
        assert retrieved_home.size_sqft == created_home.size_sqft
        assert retrieved_home.location == created_home.location
    
    @pytest.mark.asyncio
    async def test_get_home_not_found(self, db_session: AsyncSession):
        # Arrange
        service = HomeService(db_session)
        fake_id = uuid4()
        
        # Act & Assert
        home = await service.get_home(fake_id)
        
        assert home is None
    


