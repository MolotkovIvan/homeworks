SELECT Country.Name, Country.Population, Country.SurfaceArea
FROM Country 
JOIN City AS C1 ON C1.CountryCode = Country.Code
JOIN City AS C2 ON C2.CountryCode = Country.Code
JOIN Capital ON Capital.CityId = C2.Id
GROUP BY Country.Name HAVING MAX(C1.Population) > C2.Population
ORDER BY (Country.Population / Country.SurfaceArea) DESC, Country.Name

