import re

import httpx
from bs4 import BeautifulSoup

from app.logging import get_logger
from app.schemas import JobListing

logger = get_logger(__name__)


class JobScraperService:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self) -> None:
        await self.client.aclose()

    async def scrape_job_listing(self, url: str) -> JobListing:
        if "linkedin.com" in url:
            return await self._scrape_linkedin(url)
        elif "indeed.com" in url:
            return await self._scrape_indeed(url)
        elif "glassdoor.com" in url:
            return await self._scrape_glassdoor(url)
        elif "weworkremotely.com" in url:
            return await self._scrape_weworkremotely(url)
        elif "remoteok.com" in url:
            return await self._scrape_remoteok(url)
        else:
            return await self._scrape_generic(url)

    async def _scrape_linkedin(self, url: str) -> JobListing:
        try:
            response = await self.client.get(url, headers=_stealth_headers())
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")

            title = (
                soup.find("h1", class_=re.compile("top-card-layout__title"))
                or soup.find("h1", class_=re.compile("headline"))
                or soup.find("h1")
            )
            title = title.get_text(strip=True) if title else ""

            company = (
                soup.find("a", class_=re.compile("top-card-layout__cta"))
                or soup.find("span", class_=re.compile("company-name"))
                or soup.find("div", class_=re.compile("top-card-sub-line"))
            )
            company = company.get_text(strip=True) if company else ""

            location = (
                soup.find("span", class_=re.compile("top-card__bullet-flares"))
                or soup.find("span", class_=re.compile("location"))
            )
            location = location.get_text(strip=True) if location else None

            description = (
                soup.find("div", class_=re.compile("show-more-less-html"))
                or soup.find("div", class_=re.compile("description"))
                or soup.find("article")
            )
            description = description.get_text(strip=True)[:3000] if description else ""

            salary = (
                soup.find("span", class_=re.compile("salary"))
                or soup.find("div", class_=re.compile("compensation"))
            )
            salary = salary.get_text(strip=True) if salary else None

            return JobListing(
                title=title,
                company=company,
                location=location,
                description=description,
                url=url,
                salary_min=self._parse_salary_min(salary),
                salary_max=self._parse_salary_max(salary),
                currency="USD",
                posted_days_ago=None,
                source="linkedin",
            )
        except Exception as e:
            logger.warning(f"LinkedIn scrape failed for {url}: {e}")
            return JobListing(title=url, company="", description="", url=url, source="linkedin")

    async def _scrape_indeed(self, url: str) -> JobListing:
        try:
            response = await self.client.get(url, headers=_stealth_headers())
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")

            title = (
                soup.find("h1", class_="jobsearch-JobInfoHeader-title")
                or soup.find("h1")
            )
            title = title.get_text(strip=True) if title else ""

            company = (
                soup.find("div", class_="jobsearch-CompanyInfoWithoutHeaderImage")
                or soup.find("a", class_="jobsearch-CompanyInfoAnchor")
                or soup.find("span", class_="company")
            )
            company = company.get_text(strip=True) if company else ""

            location = soup.find("div", class_="jobsearch-JobInfoHeader-location")
            location = location.get_text(strip=True) if location else None

            description = (
                soup.find("div", id="jobDescriptionText")
                or soup.find("div", class_="jobsearch-JobComponent")
            )
            description = description.get_text(strip=True)[:3000] if description else ""

            salary = soup.find("span", class_="estimated-salary")
            salary = salary.get_text(strip=True) if salary else None

            return JobListing(
                title=title,
                company=company,
                location=location,
                description=description,
                url=url,
                salary_min=self._parse_salary_min(salary),
                salary_max=self._parse_salary_max(salary),
                currency="USD",
                posted_days_ago=None,
                source="indeed",
            )
        except Exception as e:
            logger.warning(f"Indeed scrape failed for {url}: {e}")
            return JobListing(title=url, company="", description="", url=url, source="indeed")

    async def _scrape_glassdoor(self, url: str) -> JobListing:
        try:
            response = await self.client.get(url, headers=_stealth_headers())
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")

            title = soup.find("h1") or soup.find("h2", class_=re.compile("title"))
            title = title.get_text(strip=True) if title else ""

            company = (
                soup.find("div", class_=re.compile("company-name"))
                or soup.find("a", class_=re.compile("employer-name"))
            )
            company = company.get_text(strip=True) if company else ""

            location = soup.find("span", class_=re.compile("location"))
            location = location.get_text(strip=True) if location else None

            description = (
                soup.find("div", id="JobDescription")
                or soup.find("div", class_=re.compile("description"))
            )
            description = description.get_text(strip=True)[:3000] if description else ""

            salary = soup.find("span", class_=re.compile("salary"))
            salary = salary.get_text(strip=True) if salary else None

            return JobListing(
                title=title,
                company=company,
                location=location,
                description=description,
                url=url,
                salary_min=self._parse_salary_min(salary),
                salary_max=self._parse_salary_max(salary),
                currency="USD",
                posted_days_ago=None,
                source="glassdoor",
            )
        except Exception as e:
            logger.warning(f"Glassdoor scrape failed for {url}: {e}")
            return JobListing(title=url, company="", description="", url=url, source="glassdoor")

    async def _scrape_weworkremotely(self, url: str) -> JobListing:
        try:
            response = await self.client.get(url, headers=_stealth_headers())
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")

            title = soup.find("h1") or soup.find("h2", class_=re.compile("title"))
            title = title.get_text(strip=True) if title else ""

            company = (
                soup.find("a", class_=re.compile("company-link"))
                or soup.find("span", class_=re.compile("company"))
            )
            company = company.get_text(strip=True) if company else ""

            location_tag = soup.find("p", class_=re.compile("location"))
            location = location_tag.get_text(strip=True) if location_tag else None

            description = (
                soup.find("div", class_=re.compile("description"))
                or soup.find("article")
            )
            description = description.get_text(strip=True)[:3000] if description else ""

            return JobListing(
                title=title,
                company=company,
                location=location or "Remote",
                description=description,
                url=url,
                salary_min=None,
                salary_max=None,
                currency="USD",
                posted_days_ago=None,
                source="weworkremotely",
            )
        except Exception as e:
            logger.warning(f"WeWorkRemotely scrape failed for {url}: {e}")
            return JobListing(title=url, company="", description="", url=url, source="weworkremotely")

    async def _scrape_remoteok(self, url: str) -> JobListing:
        try:
            response = await self.client.get(url, headers=_stealth_headers())
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")

            title = soup.find("h1") or soup.find("h2", class_=re.compile("title"))
            title = title.get_text(strip=True) if title else ""

            company = (
                soup.find("a", class_=re.compile("company"))
                or soup.find("span", class_=re.compile("company-name"))
            )
            company = company.get_text(strip=True) if company else ""

            description = (
                soup.find("div", class_=re.compile("description"))
                or soup.find("article")
            )
            description = description.get_text(strip=True)[:3000] if description else ""

            return JobListing(
                title=title,
                company=company,
                location="Remote",
                description=description,
                url=url,
                salary_min=None,
                salary_max=None,
                currency="USD",
                posted_days_ago=None,
                source="remoteok",
            )
        except Exception as e:
            logger.warning(f"RemoteOK scrape failed for {url}: {e}")
            return JobListing(title=url, company="", description="", url=url, source="remoteok")

    async def _scrape_generic(self, url: str) -> JobListing:
        try:
            response = await self.client.get(url, headers=_stealth_headers())
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type:
                return JobListing(
                    title="Unable to parse",
                    company="",
                    description=f"URL returned non-HTML content: {content_type}",
                    url=url,
                    source="generic",
                )

            soup = BeautifulSoup(response.text, "lxml")

            for tag in soup.find_all(["script", "style", "nav", "header", "footer", "aside"]):
                tag.decompose()

            title = (
                soup.find("h1")
                or soup.find("meta", property="og:title")
                or soup.find("meta", attrs={"name": "title"})
            )
            if hasattr(title, "get"):
                title = title.get("content", "") or str(title)
            else:
                title = title.get_text(strip=True) if title else ""

            og_desc = soup.find("meta", property="og:description")
            meta_desc = soup.find("meta", attrs={"name": "description"})
            description = (og_desc or meta_desc)
            if description:
                description = description.get("content", "") or description.get_text(strip=True)
            else:
                body = soup.find("body")
                description = body.get_text(strip=True)[:3000] if body else ""

            h2_candidates = soup.find_all("h2")
            company = ""
            for h2 in h2_candidates[:3]:
                text = h2.get_text(strip=True)
                if text and len(text) < 100:
                    company = text
                    break

            return JobListing(
                title=title or url,
                company=company,
                location=None,
                description=description[:3000],
                url=url,
                salary_min=None,
                salary_max=None,
                currency="USD",
                posted_days_ago=None,
                source="generic",
            )
        except Exception as e:
            logger.warning(f"Generic scrape failed for {url}: {e}")
            return JobListing(
                title=url,
                company="",
                description=f"Failed to scrape: {str(e)}",
                url=url,
                source="generic",
            )

    def _parse_salary_min(self, salary_str: str | None) -> float | None:
        if not salary_str:
            return None
        matches = re.findall(r"[\d,]+(?:\.\d+)?", salary_str.replace(",", ""))
        if len(matches) >= 1:
            try:
                return float(matches[0])
            except ValueError:
                pass
        return None

    def _parse_salary_max(self, salary_str: str | None) -> float | None:
        if not salary_str:
            return None
        matches = re.findall(r"[\d,]+(?:\.\d+)?", salary_str.replace(",", ""))
        if len(matches) >= 2:
            try:
                return float(matches[1])
            except ValueError:
                pass
        return None


def _stealth_headers() -> dict[str, str]:
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
