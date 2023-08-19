import os
import shutil
from datetime import date
from typing import List
from unittest.mock import Mock, patch

import pytest

from webapps.diagram import PlotGenerator


# Mock residence data for testing
class MockResidence:
    def __init__(self, country, country_code, start_date, end_date):
        self.country = country
        self.country_code = country_code
        self.start_date = start_date
        self.end_date = end_date


class TestPlotGenerator:
    @pytest.fixture
    def mock_residences(self) -> List[MockResidence]:
        return [
            MockResidence("Iran", "IR", date(2020, 1, 1), "2023-03-03"),
            MockResidence("Iraq", "IQ", date(2020, 3, 1), "present"),
        ]

    @pytest.fixture
    def mock_db(self) -> Mock:
        return Mock()

    def test_generate_plots(self, mock_residences, mock_db):
        with patch("repositories.residence_repo.get_residences") as mock_get_residences:
            mock_get_residences.return_value = mock_residences
            user_id = 0
            plot_generator = PlotGenerator(user_id, mock_db)

            assert plot_generator.user_id == user_id
            assert plot_generator.residences == mock_residences
            assert plot_generator.db == mock_db
            assert plot_generator.user_directory == f"dynamic/{user_id}"

            plot_generator.generate_plots()
            png_file_count = sum(
                1
                for file in os.listdir(plot_generator.user_directory)
                if file.endswith(".png")
            )
            assert png_file_count > 1
            shutil.rmtree(plot_generator.user_directory)
            assert not os.path.exists(
                plot_generator.user_directory
            ), "Directory still exist."
