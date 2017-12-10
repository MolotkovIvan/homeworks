SELECT Country.Name FROM Country
LEFT JOIN City ON City.CountryCode = Country.Code 
WHERE Country.Population <> 0
GROUP BY Country.Name HAVING (SUM(City.Population) * 2 < Country.Population) OR SUM(City.Population) IS NULL
ORDER BY Country.Name