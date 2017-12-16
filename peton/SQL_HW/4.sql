SELECT Country.Name, COUNT(City.Population) AS NumberOfMetropolises
FROM Country
LEFT JOIN City ON City.CountryCode = Country.Code
WHERE City.Population >= 1e6
GROUP BY Country.Name
ORDER BY NumberOfMetropolises DESC