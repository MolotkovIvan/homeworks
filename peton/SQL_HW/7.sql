SELECT Country.Name
FROM Country
LEFT JOIN City ON City.CountryCode = Country.Code 
WHERE Country.Population <> 0
GROUP BY Country.Name
HAVING COALESCE(SUM(City.Population) * 2, 0) < Country.Population
ORDER BY Country.Name