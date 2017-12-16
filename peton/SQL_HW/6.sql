SELECT City.Name, City.Population, Country.Population
FROM City
JOIN Country ON City.CountryCode = Country.Code
ORDER BY (CAST (City.Population AS Double) / CAST (Country.Population AS Double)) DESC, City.Name
LIMIT 20 