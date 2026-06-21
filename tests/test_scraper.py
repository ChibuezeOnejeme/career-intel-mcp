import pytest

from tests.conftest import MockScraper


@pytest.fixture
def scraper() -> MockScraper:
    return MockScraper()


@pytest.mark.asyncio
async def test_scrape_linkedin(scraper: MockScraper):
    result = await scraper.scrape_job_listing("https://www.linkedin.com/jobs/view/12345")
    assert result.title == "Senior Backend Engineer"
    assert result.company == "Tech Corp"
    assert result.source == "linkedin"
    assert "Python" in result.description


@pytest.mark.asyncio
async def test_scrape_indeed(scraper: MockScraper):
    result = await scraper.scrape_job_listing("https://www.indeed.com/jobs/view/12345")
    assert result.title == "Backend Engineer"
    assert result.company == "Indeed Inc"
    assert result.source == "indeed"


@pytest.mark.asyncio
async def test_scrape_unknown_url_defaults_to_generic(scraper: MockScraper):
    result = await scraper.scrape_job_listing("https://www.randomjobsite.com/job/123")
    assert result.source == "generic"
    assert result.title == "Software Engineer"


@pytest.mark.asyncio
async def test_scrape_close_does_not_raise(scraper: MockScraper):
    await scraper.close()
