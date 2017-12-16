SELECT Country.Name, Country.Population, Country.SurfaceArea
FROM Country 
JOIN City AS Cities ON Cities.CountryCode = Country.Code
JOIN City AS Cap ON Cap.CountryCode = Country.Code
JOIN Capital ON Capital.CityId = Cap.Id
GROUP BY Country.Name HAVING MAX(Cities.Population) > Cap.Population
ORDER BY (Country.Population / Country.SurfaceArea) DESC, Country.Name

