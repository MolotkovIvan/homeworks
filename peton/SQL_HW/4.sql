SELECT Country.Name, COUNT(City.Population) AS NumberOfMetropolises
FROM Country
LEFT JOIN City ON City.CountryCode = Country.Code AND City.Population >= 1e6
GROUP BY Country.Name
ORDER BY NumberOfMetropolises DESC