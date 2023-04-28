select *
from CovidVaccinations
order by date 

-- Select Data that we are going to be using

select location, date, total_cases, new_cases, total_deaths, population
from CovidDeaths
where continent !=''
order by 1,2

-- Looking at Total Cases vs Total Deaths
-- Shows likelihood od dying if you contract covid in your country

select location, date, total_cases, total_deaths,(total_deaths/total_cases)*100 as DeathPercentage
from CovidDeaths
where location like '%Algeria%' and  continent !=''
order by 1,2


-- Looking At Total Cases vs Population
-- shows what percentage of population got covid

select location, date, population, total_cases,(total_cases/population)*100 as PercentPoupulationInfected
from CovidDeaths
--where location like '%Algeria%'
order by 1,2


-- Looking at countries with Highest infection Rate compared to Population

select location, population, MAX(total_cases) as HighestInfectionCount ,MAX((total_cases/population)*100) as PercentPoupulationInfected
from CovidDeaths
--where location like '%Algeria%'
group by location, population
order by PercentPoupulationInfected desc


-- Showing the Countries with Highest Death Count per Population

Select Location, MAX(Total_deaths) as TotalDeathCount
From CovidDeaths
--Where location like '%Algeria%'
Where continent !=''
Group by Location
order by TotalDeathCount desc


-- BREAKING THINGS DOWN BY CONTINENT

-- Showing the continent with the highest death count per population

Select continent, MAX(Total_deaths) as TotalDeathCount
From CovidDeaths
--Where location like '%Algeria%'
Where continent !=''
Group by continent
order by TotalDeathCount desc


-- GLOBAL NUMBERS

select date, SUM(new_cases) as total_cases, SUM(new_deaths) as total_deaths, SUM(new_deaths)/(CASE WHEN SUM(new_cases) = 0 THEN NULL ELSE SUM(new_cases) END) as DeathPercentage
from CovidDeaths
--Where location like '%Algeria%'
where continent !='' 
group by date
order by 1,2


-- Total Population vs Vaccinations
-- Shows Percentage of Population that has recieved at least one Covid Vaccine

with PopvsVac (Continent, Location, Date, Population, New_vaccination, RollingPeopelVaccinated)
as 
(
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(vac.new_vaccinations) OVER (Partition by dea.Location order by dea.location, dea.date) as RollingPeopelVaccinated
from CovidDeaths dea
join CovidVaccinations vac
	on dea.location = vac.location
	and dea.date=vac.date
Where dea.continent !=''
--order by 2,3
)

select *,(RollingPeopelVaccinated/Population)*100
from PopvsVac
where Location like '%Algeria%'
order by 3


-- TEMP TABLE
DROP Table if exists #PercentPopulationVaccinated

Create Table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
RollingPeopleVaccinated numeric
)

Insert into #PercentPopulationVaccinated
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(vac.new_vaccinations) OVER (Partition by dea.Location order by dea.location, dea.date) as RollingPeopelVaccinated
from CovidDeaths dea
join CovidVaccinations vac
	on dea.location = vac.location
	and dea.date=vac.date
Where dea.continent !=''
--order by 2,3

Select *, (RollingPeopleVaccinated/Population)*100
From #PercentPopulationVaccinated


-- Creating View to store data for later visualizations

DROP View if exists PercentPopulationVaccinated

create View PercentPopulationVaccinated  as
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(vac.new_vaccinations) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null

select * 
from PercentPopulationVaccinated